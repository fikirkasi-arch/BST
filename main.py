"""JinniBell Pro okul zil ve tören programı yöneticisi."""
from __future__ import annotations

import os
import subprocess
import tempfile
import threading
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Dict, List, Optional

from mutagen import File as MutagenFile
from pydub import AudioSegment

from bell_app.audio import AudioController
from bell_app.config import BellConfig, BellEvent, WEEKDAYS
from bell_app.scheduler import ScheduleRunner

try:  # pragma: no cover - opsiyonel
    import yt_dlp  # type: ignore
except Exception:  # pragma: no cover - opsiyonel
    yt_dlp = None

MANUAL_BUTTONS = {
    "İstiklal Marşı": "istiklal",
    "Siren + İstiklal": "siren_istiklal",
    "1 dk Saygı": "silence_60",
    "2 dk Saygı": "silence_120",
    "1 dk Saygı + İstiklal": "silence60_istiklal",
    "2 dk Saygı + İstiklal": "silence120_istiklal",
}


class BellApplication:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("JinniBell Pro")
        self.config = BellConfig.load()
        self.audio = AudioController()
        self.audio.set_state_callback(self._update_status)
        self.manual_override = False
        self.bells_paused = False
        self.status_var = tk.StringVar(value="Hazır")
        self.recess_thread: Optional[threading.Thread] = None
        self._youtube_cache: Dict[str, str] = {}
        self._ceremony_index = 0

        self.scheduler = ScheduleRunner(
            self.config,
            self._handle_event,
            lambda: self.manual_override or self.bells_paused,
        )
        self.scheduler.start()

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._minimize_to_tray)

    # region UI
    def _build_ui(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(notebook)
        schedule_frame = ttk.Frame(notebook)
        sound_frame = ttk.Frame(notebook)
        ceremony_frame = ttk.Frame(notebook)

        notebook.add(control_frame, text="Kontrol")
        notebook.add(schedule_frame, text="Ders Programı")
        notebook.add(sound_frame, text="Ses Ayarları")
        notebook.add(ceremony_frame, text="Tören")

        self._build_control_tab(control_frame)
        self._build_schedule_tab(schedule_frame)
        self._build_sound_tab(sound_frame)
        self._build_ceremony_tab(ceremony_frame)
        self._refresh_holidays()

    def _build_control_tab(self, frame: ttk.Frame) -> None:
        button_frame = ttk.LabelFrame(frame, text="Manuel Butonlar")
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        for label, key in MANUAL_BUTTONS.items():
            ttk.Button(button_frame, text=label, command=lambda k=key: self._trigger_manual(k)).pack(
                fill=tk.X, padx=5, pady=2
            )

        status_frame = ttk.Frame(frame)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(status_frame, text="Durum:").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)

        volume_frame = ttk.LabelFrame(frame, text="Ses")
        volume_frame.pack(fill=tk.X, padx=10, pady=5)
        self.volume_var = tk.DoubleVar(value=self.config.volume)
        ttk.Scale(
            volume_frame,
            from_=0,
            to=1,
            orient=tk.HORIZONTAL,
            variable=self.volume_var,
            command=lambda _: self._change_volume(),
        ).pack(fill=tk.X, padx=5, pady=5)

        toggle_frame = ttk.Frame(frame)
        toggle_frame.pack(fill=tk.X, padx=10, pady=5)
        self.mute_var = tk.BooleanVar(value=self.config.muted)
        ttk.Checkbutton(toggle_frame, text="Zilleri Sustur", variable=self.mute_var, command=self._toggle_mute).pack(
            side=tk.LEFT, padx=5
        )
        self.pause_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            toggle_frame,
            text="Tören Modu (otomatik zil kapalı)",
            variable=self.pause_var,
            command=self._toggle_pause,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame, text="Arka Plana Al", command=self._minimize_to_tray).pack(pady=5)

        shutdown_frame = ttk.LabelFrame(frame, text="Otomatik Kapatma")
        shutdown_frame.pack(fill=tk.X, padx=10, pady=5)
        self.shutdown_var = tk.BooleanVar(value=self.config.auto_shutdown_enabled)
        ttk.Checkbutton(
            shutdown_frame,
            text="Bilgisayarı belirtilen saatte kapat",
            variable=self.shutdown_var,
            command=self._toggle_shutdown,
        ).pack(side=tk.LEFT, padx=5)
        self.shutdown_entry = ttk.Entry(shutdown_frame, width=8)
        self.shutdown_entry.insert(0, self.config.auto_shutdown_time or "20:00")
        self.shutdown_entry.pack(side=tk.LEFT, padx=5)

        today_frame = ttk.LabelFrame(frame, text="Bugünkü Ziller")
        today_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.today_list = tk.Listbox(today_frame)
        self.today_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._refresh_today()

        ttk.Label(
            frame,
            text="© 2026 Emre Esen tarafından kodlandı",
            font=("Segoe UI", 9, "italic"),
        ).pack(anchor=tk.W, padx=12, pady=(0, 10))

    def _build_schedule_tab(self, frame: ttk.Frame) -> None:
        top = ttk.Frame(frame)
        top.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(top, text="Gün").pack(side=tk.LEFT)
        self.day_var = tk.StringVar(value=WEEKDAYS[0])
        day_combo = ttk.Combobox(top, values=WEEKDAYS, textvariable=self.day_var, state="readonly")
        day_combo.pack(side=tk.LEFT, padx=5)
        day_combo.bind("<<ComboboxSelected>>", lambda _: self._refresh_event_list())

        self.event_list = tk.Listbox(frame)
        self.event_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        form = ttk.Frame(frame)
        form.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(form, text="Saat (HH:MM)").grid(row=0, column=0)
        ttk.Label(form, text="Başlık").grid(row=0, column=1)
        ttk.Label(form, text="Ses Tipi").grid(row=0, column=2)
        self.clock_entry = ttk.Entry(form)
        self.clock_entry.grid(row=1, column=0, padx=5)
        self.label_entry = ttk.Entry(form)
        self.label_entry.grid(row=1, column=1, padx=5)
        self.sound_var = tk.StringVar(value="student_entry")
        ttk.Combobox(
            form,
            textvariable=self.sound_var,
            values=list(self.config.sound_files.keys()),
            state="readonly",
        ).grid(row=1, column=2, padx=5)
        ttk.Button(form, text="Ekle", command=self._add_event).grid(row=1, column=3, padx=5)
        ttk.Button(form, text="Sil", command=self._delete_event).grid(row=1, column=4, padx=5)

        copy_frame = ttk.LabelFrame(frame, text="Program Kopyala")
        copy_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(copy_frame, text="Hedef Gün").pack(side=tk.LEFT, padx=5)
        self.copy_target_var = tk.StringVar(value=WEEKDAYS[1])
        ttk.Combobox(
            copy_frame,
            textvariable=self.copy_target_var,
            values=WEEKDAYS,
            state="readonly",
            width=12,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(copy_frame, text="Aktar", command=self._copy_schedule_to_day).pack(side=tk.LEFT, padx=5)

        holiday_frame = ttk.LabelFrame(frame, text="Tatil Günleri")
        holiday_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.holiday_list = tk.Listbox(holiday_frame, height=5)
        self.holiday_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        holiday_btns = ttk.Frame(holiday_frame)
        holiday_btns.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(holiday_btns, text="Ekle", command=self._add_holiday).pack(side=tk.LEFT, padx=5)
        ttk.Button(holiday_btns, text="Sil", command=self._remove_holiday).pack(side=tk.LEFT, padx=5)

        self._refresh_event_list()

    def _build_sound_tab(self, frame: ttk.Frame) -> None:
        ttk.Label(frame, text="Her ses için dosya seçin").pack(anchor=tk.W, padx=10, pady=5)
        self.recess_var = tk.BooleanVar(value=self.config.recess_music_enabled)
        for key, label in [
            ("student_entry", "Öğrenci Girişi"),
            ("teacher_entry", "Öğretmen Girişi"),
            ("lesson_exit", "Ders Çıkışı"),
            ("recess_music", "Teneffüs Müziği"),
            ("istiklal", "İstiklal Marşı"),
            ("siren", "Siren"),
            ("moment_of_silence", "Saygı Duruşu Sesi (opsiyonel)"),
        ]:
            self._build_sound_row(frame, key, label)

        ttk.Checkbutton(
            frame,
            text="Teneffüslerde müzik çal",
            variable=self.recess_var,
            command=self._toggle_recess_music,
        ).pack(anchor=tk.W, padx=10, pady=5)

    def _build_sound_row(self, frame: ttk.Frame, key: str, label: str) -> None:
        row = ttk.Frame(frame)
        row.pack(fill=tk.X, padx=10, pady=2)
        ttk.Label(row, text=label, width=28).pack(side=tk.LEFT)
        path_var = tk.StringVar(value=self.config.sound_files.get(key, ""))
        entry = ttk.Entry(row, textvariable=path_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        def choose() -> None:
            file_path = filedialog.askopenfilename(title=label)
            if file_path:
                path_var.set(file_path)
                self.config.sound_files[key] = file_path
                self.config.save()

        ttk.Button(row, text="Seç", command=choose).pack(side=tk.LEFT)

    def _build_ceremony_tab(self, frame: ttk.Frame) -> None:
        top = ttk.Frame(frame)
        top.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(top, text="Bilgisayardan Müzik Ekle", command=self._add_local_music).pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="YouTube'dan Ekle", command=self._add_youtube_music).pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="Sil", command=self._delete_ceremony_item).pack(side=tk.LEFT, padx=5)

        self.ceremony_list = tk.Listbox(frame)
        self.ceremony_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        play_frame = ttk.Frame(frame)
        play_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(play_frame, text="Seçileni Çal", command=self._play_selected_ceremony).pack(side=tk.LEFT, padx=5)
        ttk.Button(play_frame, text="Sıradaki", command=self._play_next_ceremony).pack(side=tk.LEFT, padx=5)

        self._refresh_ceremony_list()

    # endregion

    # region EVENT HANDLERS
    def _change_volume(self) -> None:
        value = self.volume_var.get()
        self.config.volume = value
        self.config.save()
        self.audio.set_volume(value)

    def _toggle_mute(self) -> None:
        state = self.mute_var.get()
        self.config.muted = state
        self.config.save()
        self.audio.set_muted(state)

    def _toggle_pause(self) -> None:
        self.bells_paused = self.pause_var.get()
        if self.bells_paused:
            self._update_status("Tören modu: Otomatik zil kapalı")
        else:
            self._update_status("Hazır")

    def _toggle_shutdown(self) -> None:
        self.config.auto_shutdown_enabled = self.shutdown_var.get()
        self.config.auto_shutdown_time = self.shutdown_entry.get()
        self.config.save()

    def _toggle_recess_music(self) -> None:
        self.config.recess_music_enabled = self.recess_var.get()
        self.config.save()

    def _add_event(self) -> None:
        clock = self.clock_entry.get().strip()
        label = self.label_entry.get().strip()
        if not clock or not label:
            messagebox.showwarning("Eksik bilgi", "Saat ve başlık doldurulmalı")
            return
        if ":" not in clock:
            messagebox.showwarning("Saat hatası", "HH:MM formatı kullanın")
            return
        self.config.add_event(self.day_var.get(), label, clock, self.sound_var.get())
        self._refresh_event_list()
        self._refresh_today()

    def _delete_event(self) -> None:
        idx = self.event_list.curselection()
        if not idx:
            messagebox.showinfo("Uyarı", "Silinecek zil seçin")
            return
        self.config.delete_event(self.day_var.get(), idx[0])
        self._refresh_event_list()
        self._refresh_today()

    def _copy_schedule_to_day(self) -> None:
        source = self.day_var.get()
        target = self.copy_target_var.get()
        if source == target:
            messagebox.showinfo("Bilgi", "Kaynak ve hedef gün aynı olamaz.")
            return
        self.config.copy_day_schedule(source, target)
        if self.day_var.get() == target:
            self._refresh_event_list()
        messagebox.showinfo("Kopyalandı", f"{source} programı {target} gününe aktarıldı.")

    def _refresh_holidays(self) -> None:
        if not hasattr(self, "holiday_list"):
            return
        self.holiday_list.delete(0, tk.END)
        for date_str, desc in sorted(self.config.holidays.items()):
            self.holiday_list.insert(tk.END, f"{date_str} - {desc}")

    def _add_holiday(self) -> None:
        date_str = simpledialog.askstring("Tatil Tarihi", "YYYY-AA-GG formatında girin")
        if not date_str:
            return
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Hata", "Tarih formatı geçersiz")
            return
        description = simpledialog.askstring("Açıklama", "Tatil açıklaması", initialvalue="Resmi Tatil")
        if not description:
            description = "Tatil"
        self.config.add_holiday(date_str, description)
        self._refresh_holidays()
        self._refresh_today()

    def _remove_holiday(self) -> None:
        selection = self.holiday_list.curselection()
        if not selection:
            messagebox.showinfo("Uyarı", "Silmek için tatil seçin")
            return
        value = self.holiday_list.get(selection[0])
        date_str = value.split(" - ", 1)[0]
        self.config.remove_holiday(date_str)
        self._refresh_holidays()
        self._refresh_today()

    def _refresh_event_list(self) -> None:
        self.event_list.delete(0, tk.END)
        for event in self.config.daily_schedule.get(self.day_var.get(), []):
            self.event_list.insert(tk.END, f"{event.clock} - {event.label} ({event.sound_type})")

    def _refresh_today(self) -> None:
        now = datetime.now()
        today = WEEKDAYS[now.weekday()]
        self.today_list.delete(0, tk.END)
        holiday_desc = self.config.holiday_for(now.date())
        if holiday_desc:
            self.today_list.insert(tk.END, f"Bugün tatil: {holiday_desc}")
            return
        events = self.config.daily_schedule.get(today, [])
        for event in events:
            self.today_list.insert(tk.END, f"{event.clock} - {event.label}")
        next_event = self.config.next_event_for_day(today, now.time())
        if next_event:
            self.today_list.insert(tk.END, f"Sıradaki: {next_event.clock} - {next_event.label}")
        elif events:
            self.today_list.insert(tk.END, "Bugün kalan zil yok")

    def _handle_event(self, event: BellEvent) -> None:
        if event.sound_type == "auto_shutdown":
            self._run_shutdown()
            return
        file_path = self.config.sound_files.get(event.sound_type, "")
        if not file_path:
            self._update_status(f"Ses atanmadı: {event.label}")
            return
        self.audio.play_file(file_path, event.label)
        if event.sound_type == "lesson_exit" and self.config.recess_music_enabled:
            self._play_recess_music()

    def _trigger_manual(self, key: str) -> None:
        sequences = self._build_manual_sequences()
        steps = sequences.get(key)
        if not steps:
            messagebox.showwarning("Ses bulunamadı", "Lütfen ses dosyalarını ayarlayın")
            return
        self.manual_override = True
        self.audio.play_sequence(steps, on_complete=lambda: setattr(self, "manual_override", False))

    def _build_manual_sequences(self) -> Dict[str, List[tuple[str, Optional[str]]]]:
        sounds = self.config.sound_files
        silence_one = ("silence", "60000")
        silence_two = ("silence", "120000")
        moment = sounds.get("moment_of_silence")
        if moment:
            silence_one = ("sound", moment)
            silence_two = ("sound", moment)
        return {
            "istiklal": [("sound", sounds.get("istiklal"))],
            "siren_istiklal": [("sound", sounds.get("siren")), ("sound", sounds.get("istiklal"))],
            "silence_60": [silence_one],
            "silence_120": [silence_two],
            "silence60_istiklal": [silence_one, ("sound", sounds.get("istiklal"))],
            "silence120_istiklal": [silence_two, ("sound", sounds.get("istiklal"))],
        }

    def _add_local_music(self) -> None:
        path = filedialog.askopenfilename(title="Müzik seç")
        if not path:
            return
        label = simpledialog.askstring("Başlık", "Listede nasıl görünsün?") or Path(path).stem
        start_min = simpledialog.askinteger("Başlangıç dakikası", "Müziğin kaçıncı dakikasından başlansın?", minvalue=0, initialvalue=0)
        item = {
            "label": label,
            "source": "file",
            "location": path,
            "start_minute": start_min or 0,
            "duration_sec": int(self._get_duration(path) or 0),
        }
        self.config.ceremony_playlist.append(item)
        self.config.save()
        self._refresh_ceremony_list()

    def _add_youtube_music(self) -> None:
        if yt_dlp is None:
            messagebox.showerror("Eksik paket", "YouTube sesini almak için yt_dlp kurulmalı")
            return
        url = simpledialog.askstring("YouTube", "Video bağlantısı")
        if not url:
            return
        label = simpledialog.askstring("Başlık", "Listede nasıl görünsün?") or url
        start_min = simpledialog.askinteger("Başlangıç dakikası", "Kaçıncı dakikadan başlasın?", minvalue=0, initialvalue=0)
        item = {
            "label": label,
            "source": "youtube",
            "location": url,
            "start_minute": start_min or 0,
            "duration_sec": None,
        }
        self.config.ceremony_playlist.append(item)
        self.config.save()
        self._refresh_ceremony_list()

    def _delete_ceremony_item(self) -> None:
        idx = self.ceremony_list.curselection()
        if not idx:
            return
        self.config.ceremony_playlist.pop(idx[0])
        self.config.save()
        self._refresh_ceremony_list()

    def _refresh_ceremony_list(self) -> None:
        self.ceremony_list.delete(0, tk.END)
        for item in self.config.ceremony_playlist:
            duration = item.get("duration_sec")
            duration_text = f" - {duration // 60:02d}:{duration % 60:02d}" if duration else ""
            self.ceremony_list.insert(
                tk.END,
                f"{item['label']} (başlangıç dk: {item.get('start_minute', 0)}){duration_text}",
            )

    def _play_selected_ceremony(self) -> None:
        idx = self.ceremony_list.curselection()
        if not idx:
            messagebox.showinfo("Seçim", "Lütfen bir müzik seçin")
            return
        self._ceremony_index = idx[0]
        self._play_ceremony_item(self.config.ceremony_playlist[self._ceremony_index])

    def _play_next_ceremony(self) -> None:
        if not self.config.ceremony_playlist:
            return
        self._ceremony_index = (self._ceremony_index + 1) % len(self.config.ceremony_playlist)
        self._play_ceremony_item(self.config.ceremony_playlist[self._ceremony_index])

    def _play_ceremony_item(self, item: Dict[str, object]) -> None:
        source = item.get("source")
        location = str(item.get("location"))
        start_minute = int(item.get("start_minute", 0))
        path = location
        if source == "youtube":
            path = self._download_youtube_audio(location)
            if not path:
                return
        start_ms = start_minute * 60 * 1000
        label = str(item.get("label", "Tören Müziği"))
        self.audio.play_file(self._slice_file(path, start_ms), label)

    def _slice_file(self, path: str, start_ms: int) -> str:
        if start_ms <= 0:
            return path
        audio = AudioSegment.from_file(path)  # type: ignore[name-defined]
        temp_file = Path(tempfile.gettempdir()) / f"slice_{int(time.time())}.wav"
        audio[start_ms:].export(temp_file, format="wav")
        return str(temp_file)

    def _download_youtube_audio(self, url: str) -> Optional[str]:
        if url in self._youtube_cache:
            return self._youtube_cache[url]
        if yt_dlp is None:
            messagebox.showerror("yt_dlp gerekli", "Lütfen pip ile yt-dlp kurun")
            return None
        temp_dir = Path(tempfile.gettempdir())
        outtmpl = str(temp_dir / "yt_audio.%(ext)s")
        opts = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "quiet": True,
            "noplaylist": True,
            "extractaudio": True,
            "audioformat": "mp3",
        }
        with yt_dlp.YoutubeDL(opts) as ydl:  # type: ignore[attr-defined]
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        self._youtube_cache[url] = file_path
        return file_path

    def _play_recess_music(self) -> None:
        path = self.config.sound_files.get("recess_music")
        if not path:
            return
        if self.recess_thread and self.recess_thread.is_alive():
            return
        duration = 5 * 60  # default 5 dk

        def worker() -> None:
            start = time.time()
            while time.time() - start < duration:
                self.audio.play_file(path, "Teneffüs Müziği")
                time.sleep(1)

        self.recess_thread = threading.Thread(target=worker, daemon=True)
        self.recess_thread.start()

    def _get_duration(self, path: str) -> Optional[int]:
        try:
            meta = MutagenFile(path)
            if meta and meta.info:
                return int(meta.info.length)
        except Exception:
            return None
        return None

    def _run_shutdown(self) -> None:
        if not self.config.auto_shutdown_enabled:
            return
        if os.name == "nt":
            subprocess.Popen(["shutdown", "/s", "/t", "0"])
        else:
            subprocess.Popen(["shutdown", "-h", "now"])

    def _minimize_to_tray(self) -> None:
        self.root.iconify()
        self._update_status("Arka planda çalışıyor")

    # endregion

    def _update_status(self, message: str) -> None:
        self.status_var.set(message)


if __name__ == "__main__":
    root = tk.Tk()
    app = BellApplication(root)
    root.mainloop()
