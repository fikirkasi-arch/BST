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

SCHEDULE_SOUND_CHOICES = [
    ("Öğrenci Girişi", "student_entry"),
    ("Öğretmen Girişi", "teacher_entry"),
    ("Teneffüs Zili", "lesson_exit"),
    ("Teneffüs Müziği", "recess_music"),
]

SOUND_DISPLAY = {value: label for label, value in SCHEDULE_SOUND_CHOICES}


def _format_mmss(total_ms: Optional[int]) -> str:
    if total_ms is None:
        return "-"
    total_seconds = max(0, total_ms // 1000)
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


def _parse_minute_second(value: str) -> Optional[int]:
    text = value.strip()
    if not text:
        return None
    parts = text.split(":")
    if len(parts) == 1:
        total_seconds = int(parts[0])
    elif len(parts) == 2:
        minutes, seconds = parts
        total_seconds = int(minutes) * 60 + int(seconds)
    elif len(parts) == 3:
        hours, minutes, seconds = parts
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    else:
        raise ValueError("Zaman SS, MM:SS veya HH:MM:SS formatında olmalı")
    return total_seconds * 1000


class BellApplication:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("JinniBell Pro")
        self.root.option_add("*Font", "Segoe UI 10")
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=26)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.config = BellConfig.load()
        self.audio = AudioController()
        self.audio.set_state_callback(self._update_status)
        self.manual_override = False
        self.bells_paused = False
        self.status_var = tk.StringVar(value="Hazır")
        self.recess_thread: Optional[threading.Thread] = None
        self._youtube_cache: Dict[str, str] = {}
        self._youtube_meta_cache: Dict[str, tuple[str, Optional[int]]] = {}
        self._ceremony_index = 0
        self._schedule_selection: Optional[int] = None

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
        header = ttk.Frame(frame)
        header.pack(fill=tk.X, padx=12, pady=8)
        ttk.Label(header, text="Düzenlenen Gün", style="Bold.TLabel").pack(side=tk.LEFT)
        self.day_var = tk.StringVar(value=WEEKDAYS[0])
        day_combo = ttk.Combobox(header, values=WEEKDAYS, textvariable=self.day_var, state="readonly", width=15)
        day_combo.pack(side=tk.LEFT, padx=6)
        day_combo.bind("<<ComboboxSelected>>", lambda _: self._refresh_event_list())
        ttk.Button(header, text="Diğer Günlere Uygula", command=self._open_copy_dialog).pack(side=tk.RIGHT, padx=5)

        table_frame = ttk.Frame(frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 8))
        columns = ("clock", "label", "sound")
        self.event_list = ttk.Treeview(table_frame, columns=columns, show="headings", height=10, selectmode="browse")
        self.event_list.heading("clock", text="Saat")
        self.event_list.heading("label", text="Başlık")
        self.event_list.heading("sound", text="Kategori")
        self.event_list.column("clock", width=80, anchor=tk.CENTER)
        self.event_list.column("label", anchor=tk.W)
        self.event_list.column("sound", width=140, anchor=tk.CENTER)
        self.event_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.event_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.event_list.configure(yscrollcommand=scrollbar.set)
        self.event_list.tag_configure("student_entry", background="#edf7ff")
        self.event_list.tag_configure("teacher_entry", background="#f9f0ff")
        self.event_list.tag_configure("lesson_exit", background="#fff7ed")
        self.event_list.bind("<<TreeviewSelect>>", self._on_schedule_select)

        form = ttk.LabelFrame(frame, text="Yeni/Seçili Zil")
        form.pack(fill=tk.X, padx=12, pady=8)
        self.hour_var = tk.StringVar(value="08")
        self.minute_var = tk.StringVar(value="00")
        ttk.Label(form, text="Saat").grid(row=0, column=0, padx=4, pady=4, sticky=tk.W)
        hour_spin = ttk.Spinbox(form, from_=0, to=23, textvariable=self.hour_var, width=5, wrap=True, format="%02.0f")
        hour_spin.grid(row=1, column=0, padx=4, pady=2)
        ttk.Label(form, text=":").grid(row=1, column=1)
        minute_spin = ttk.Spinbox(form, from_=0, to=59, textvariable=self.minute_var, width=5, wrap=True, format="%02.0f")
        minute_spin.grid(row=1, column=2, padx=4, pady=2)

        ttk.Label(form, text="Kategori").grid(row=0, column=3, padx=4, sticky=tk.W)
        self.sound_choice_var = tk.StringVar(value=SCHEDULE_SOUND_CHOICES[0][0])
        ttk.Combobox(
            form,
            textvariable=self.sound_choice_var,
            values=[choice[0] for choice in SCHEDULE_SOUND_CHOICES],
            state="readonly",
            width=18,
        ).grid(row=1, column=3, padx=4, pady=2)

        ttk.Label(form, text="Açıklama").grid(row=0, column=4, padx=4, sticky=tk.W)
        self.label_var = tk.StringVar()
        self.label_combo = ttk.Combobox(
            form,
            textvariable=self.label_var,
            values=[choice[0] for choice in SCHEDULE_SOUND_CHOICES],
            width=24,
        )
        self.label_combo.grid(row=1, column=4, padx=4, pady=2, sticky=tk.W)
        self.sound_choice_var.trace_add("write", lambda *_: self._suggest_label())

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=5, padx=6)
        ttk.Button(btn_frame, text="Ekle", command=self._add_event, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Güncelle", command=self._update_selected_event, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Sil", command=self._delete_event, width=8).pack(side=tk.LEFT, padx=2)

        copy_frame = ttk.LabelFrame(frame, text="Program Kopyala")
        copy_frame.pack(fill=tk.X, padx=12, pady=8)
        ttk.Label(copy_frame, text="Hedef Gün").pack(side=tk.LEFT, padx=4)
        self.copy_target_var = tk.StringVar(value=WEEKDAYS[1])
        ttk.Combobox(
            copy_frame,
            textvariable=self.copy_target_var,
            values=WEEKDAYS,
            state="readonly",
            width=15,
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(copy_frame, text="Aktar", command=self._copy_schedule_to_day).pack(side=tk.LEFT, padx=4)

        holiday_frame = ttk.LabelFrame(frame, text="Tatil Günleri")
        holiday_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        self.holiday_list = tk.Listbox(holiday_frame, height=5)
        self.holiday_list.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        holiday_btns = ttk.Frame(holiday_frame)
        holiday_btns.pack(fill=tk.X, padx=6, pady=6)
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

        def preview() -> None:
            file_path = path_var.get()
            if not file_path:
                messagebox.showinfo("Ses seçin", f"Önce {label} için bir dosya belirleyin")
                return
            self.audio.play_file(file_path, label)

        ttk.Button(row, text="Test", command=preview).pack(side=tk.LEFT, padx=2)

    def _build_ceremony_tab(self, frame: ttk.Frame) -> None:
        container = ttk.Frame(frame)
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        tree_frame = ttk.Frame(container)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        columns = ("title", "source", "start", "end", "duration")
        self.ceremony_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse", height=12)
        self.ceremony_tree.heading("title", text="Başlık")
        self.ceremony_tree.heading("source", text="Kaynak")
        self.ceremony_tree.heading("start", text="Başlangıç")
        self.ceremony_tree.heading("end", text="Bitiş")
        self.ceremony_tree.heading("duration", text="Toplam")
        self.ceremony_tree.column("title", width=200, anchor=tk.W)
        self.ceremony_tree.column("source", width=90, anchor=tk.CENTER)
        self.ceremony_tree.column("start", width=80, anchor=tk.CENTER)
        self.ceremony_tree.column("end", width=80, anchor=tk.CENTER)
        self.ceremony_tree.column("duration", width=90, anchor=tk.CENTER)
        self.ceremony_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.ceremony_tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.ceremony_tree.configure(yscrollcommand=tree_scroll.set)
        self.ceremony_tree.bind("<<TreeviewSelect>>", self._on_ceremony_select)

        tree_btns = ttk.Frame(tree_frame)
        tree_btns.pack(fill=tk.X, pady=6)
        ttk.Button(tree_btns, text="Yukarı", command=lambda: self._move_ceremony_item(-1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(tree_btns, text="Aşağı", command=lambda: self._move_ceremony_item(1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(tree_btns, text="Sil", command=self._delete_ceremony_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(tree_btns, text="Seçileni Çal", command=self._play_selected_ceremony).pack(side=tk.RIGHT, padx=2)
        ttk.Button(tree_btns, text="Sıradaki", command=self._play_next_ceremony).pack(side=tk.RIGHT, padx=2)

        form = ttk.LabelFrame(container, text="Parça Detayı")
        form.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=4)
        self.ceremony_source_var = tk.StringVar(value="file")
        source_row = ttk.Frame(form)
        source_row.pack(fill=tk.X, padx=8, pady=(8, 4))
        ttk.Label(source_row, text="Kaynak Türü").pack(anchor=tk.W)
        ttk.Radiobutton(source_row, text="Dosya", value="file", variable=self.ceremony_source_var).pack(side=tk.LEFT)
        ttk.Radiobutton(source_row, text="YouTube", value="youtube", variable=self.ceremony_source_var).pack(
            side=tk.LEFT, padx=6
        )

        self.ceremony_location_var = tk.StringVar()
        location_row = ttk.Frame(form)
        location_row.pack(fill=tk.X, padx=8, pady=4)
        ttk.Label(location_row, text="Dosya yolu / link").pack(anchor=tk.W)
        ttk.Entry(location_row, textvariable=self.ceremony_location_var).pack(fill=tk.X, pady=2)
        loc_btns = ttk.Frame(location_row)
        loc_btns.pack(fill=tk.X, pady=2)
        ttk.Button(loc_btns, text="Dosya Seç", command=self._choose_ceremony_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(loc_btns, text="Link Sor", command=self._prompt_youtube_link).pack(side=tk.LEFT, padx=2)
        ttk.Button(loc_btns, text="Başlık/Video Bilgisi", command=self._fetch_ceremony_metadata).pack(side=tk.RIGHT, padx=2)

        self.ceremony_title_var = tk.StringVar()
        title_row = ttk.Frame(form)
        title_row.pack(fill=tk.X, padx=8, pady=4)
        ttk.Label(title_row, text="Listede Görünen Başlık").pack(anchor=tk.W)
        ttk.Entry(title_row, textvariable=self.ceremony_title_var).pack(fill=tk.X, pady=2)

        timing = ttk.Frame(form)
        timing.pack(fill=tk.X, padx=8, pady=4)
        self.ceremony_start_var = tk.StringVar(value="00:00")
        self.ceremony_end_var = tk.StringVar(value="")
        ttk.Label(timing, text="Başlangıç (MM:SS)").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(timing, textvariable=self.ceremony_start_var, width=10).grid(row=1, column=0, padx=2, pady=2)
        ttk.Label(timing, text="Bitiş (opsiyonel)").grid(row=0, column=1, padx=6, sticky=tk.W)
        ttk.Entry(timing, textvariable=self.ceremony_end_var, width=10).grid(row=1, column=1, padx=6, pady=2)
        ttk.Label(form, text="Bitiş boşsa parça sonuna kadar çalar.").pack(anchor=tk.W, padx=8, pady=(0, 8))

        action_row = ttk.Frame(form)
        action_row.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(action_row, text="Kaydet/Güncelle", command=self._save_ceremony_item).pack(side=tk.LEFT, padx=4)
        ttk.Button(action_row, text="Formu Temizle", command=self._clear_ceremony_form).pack(side=tk.RIGHT, padx=4)

        self._ceremony_edit_index: Optional[int] = None
        self._refresh_ceremony_list()
        self._clear_ceremony_form()

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

    def _collect_schedule_form(self) -> Optional[tuple[str, str, str]]:
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
        except ValueError:
            messagebox.showerror("Saat", "Saat ve dakika sayısal olmalı")
            return None
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            messagebox.showerror("Saat", "Saat 00-23, dakika 00-59 arasında olmalı")
            return None
        label = self.label_var.get().strip()
        if not label:
            label = self.sound_choice_var.get()
        sound_key = self._resolve_sound_choice()
        clock = f"{hour:02d}:{minute:02d}"
        return clock, label, sound_key

    def _resolve_sound_choice(self) -> str:
        choice = self.sound_choice_var.get()
        for friendly, key in SCHEDULE_SOUND_CHOICES:
            if friendly == choice:
                return key
        return SCHEDULE_SOUND_CHOICES[0][1]

    def _suggest_label(self) -> None:
        if not hasattr(self, "label_var"):
            return
        current = self.label_var.get().strip()
        if not current:
            self.label_var.set(self.sound_choice_var.get())

    def _add_event(self) -> None:
        values = self._collect_schedule_form()
        if values is None:
            return
        clock, label, sound_key = values
        self.config.add_event(self.day_var.get(), label, clock, sound_key)
        self._refresh_event_list()
        self._refresh_today()

    def _update_selected_event(self) -> None:
        if self._schedule_selection is None:
            messagebox.showinfo("Seçim", "Güncellenecek zili seçin")
            return
        values = self._collect_schedule_form()
        if values is None:
            return
        clock, label, sound_key = values
        self.config.update_event(self.day_var.get(), self._schedule_selection, label, clock, sound_key)
        self._refresh_event_list()
        self._refresh_today()

    def _delete_event(self) -> None:
        if self._schedule_selection is None:
            messagebox.showinfo("Uyarı", "Silinecek zil seçin")
            return
        self.config.delete_event(self.day_var.get(), self._schedule_selection)
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

    def _open_copy_dialog(self) -> None:
        source = self.day_var.get()
        dialog = tk.Toplevel(self.root)
        dialog.title("Gün Kopyalama")
        dialog.transient(self.root)
        dialog.grab_set()
        ttk.Label(dialog, text=f"{source} programını hangi günlere aktarmak istersiniz?").pack(
            fill=tk.X, padx=15, pady=(15, 5)
        )
        vars: List[tuple[str, tk.BooleanVar]] = []
        for day in WEEKDAYS:
            if day == source:
                continue
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(dialog, text=day, variable=var).pack(anchor=tk.W, padx=20)
            vars.append((day, var))

        def apply() -> None:
            targets = [day for day, var in vars if var.get()]
            if not targets:
                messagebox.showwarning("Seçim", "En az bir gün seçin")
                return
            self.config.copy_day_schedule_to_many(source, targets)
            dialog.destroy()
            if self.day_var.get() in targets:
                self._refresh_event_list()
            messagebox.showinfo(
                "Tamamlandı",
                f"{source} planı {', '.join(targets)} günlerine uygulandı. İstisna varsa şimdi düzenleyebilirsiniz.",
            )

        btns = ttk.Frame(dialog)
        btns.pack(fill=tk.X, padx=15, pady=15)
        ttk.Button(btns, text="Uygula", command=apply).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="İptal", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def _on_schedule_select(self, _event: object) -> None:
        selection = self.event_list.selection()
        if not selection:
            return
        idx = int(selection[0])
        events = self.config.daily_schedule.get(self.day_var.get(), [])
        if not (0 <= idx < len(events)):
            return
        event = events[idx]
        self._schedule_selection = idx
        hour, minute = event.clock.split(":", 1)
        self.hour_var.set(hour)
        self.minute_var.set(minute)
        friendly = SOUND_DISPLAY.get(event.sound_type, event.sound_type)
        self.sound_choice_var.set(friendly)
        self.label_var.set(event.label)

    def _clear_schedule_form(self, preserve_time: bool = True) -> None:
        self._schedule_selection = None
        if not preserve_time:
            self.hour_var.set("08")
            self.minute_var.set("00")
        self.label_var.set("")
        self.sound_choice_var.set(SCHEDULE_SOUND_CHOICES[0][0])
        if hasattr(self, "event_list"):
            self.event_list.selection_remove(self.event_list.selection())

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
        for item in self.event_list.get_children():
            self.event_list.delete(item)
        events = self.config.daily_schedule.get(self.day_var.get(), [])
        for idx, event in enumerate(events):
            friendly = SOUND_DISPLAY.get(event.sound_type, event.sound_type)
            self.event_list.insert(
                "",
                tk.END,
                iid=str(idx),
                values=(event.clock, event.label, friendly),
                tags=(event.sound_type,),
            )
        self._clear_schedule_form(preserve_time=True)

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

    def _choose_ceremony_file(self) -> None:
        path = filedialog.askopenfilename(title="Müzik seç")
        if not path:
            return
        self.ceremony_source_var.set("file")
        self.ceremony_location_var.set(path)
        self.ceremony_title_var.set(Path(path).stem)
        self.ceremony_start_var.set("00:00")
        self._fetch_ceremony_metadata(auto=True)

    def _prompt_youtube_link(self) -> None:
        url = simpledialog.askstring("YouTube", "Video bağlantısı")
        if not url:
            return
        self.ceremony_source_var.set("youtube")
        self.ceremony_location_var.set(url.strip())
        self._fetch_ceremony_metadata(auto=True)

    def _fetch_ceremony_metadata(self, auto: bool = False) -> None:
        source = self.ceremony_source_var.get()
        location = self.ceremony_location_var.get().strip()
        if not location:
            if not auto:
                messagebox.showinfo("Bilgi", "Önce dosya yolunu veya linki girin")
            return
        metadata = self._get_media_metadata(source, location, show_error=not auto)
        if metadata:
            title, duration = metadata
            if not self.ceremony_title_var.get().strip():
                self.ceremony_title_var.set(title)

    def _collect_ceremony_form(self) -> Optional[Dict[str, object]]:
        source = self.ceremony_source_var.get()
        location = self.ceremony_location_var.get().strip()
        if not location:
            messagebox.showwarning("Eksik bilgi", "Lütfen dosya yolunu veya YouTube linkini girin")
            return None
        if source == "file" and not Path(location).exists():
            messagebox.showerror("Dosya", "Seçilen dosya bulunamadı")
            return None
        title = self.ceremony_title_var.get().strip()
        try:
            start_ms = _parse_minute_second(self.ceremony_start_var.get() or "0") or 0
        except ValueError as exc:
            messagebox.showerror("Başlangıç", str(exc))
            return None
        end_text = self.ceremony_end_var.get().strip()
        end_ms: Optional[int] = None
        if end_text:
            try:
                end_ms = _parse_minute_second(end_text)
            except ValueError as exc:
                messagebox.showerror("Bitiş", str(exc))
                return None
        if end_ms is not None and end_ms <= start_ms:
            messagebox.showerror("Bitiş", "Bitiş süresi başlangıçtan büyük olmalı")
            return None

        metadata = self._get_media_metadata(source, location, show_error=False)
        duration_sec: Optional[int] = None
        if metadata:
            meta_title, duration_sec = metadata
            if not title:
                title = meta_title
        if not title:
            title = Path(location).stem if source == "file" else location

        item: Dict[str, object] = {
            "label": title,
            "source": source,
            "location": location,
            "start_ms": start_ms,
            "duration_sec": duration_sec,
        }
        if end_ms is not None:
            item["end_ms"] = end_ms
        return item

    def _save_ceremony_item(self) -> None:
        item = self._collect_ceremony_form()
        if item is None:
            return
        if self._ceremony_edit_index is None:
            self.config.ceremony_playlist.append(item)
        else:
            self.config.ceremony_playlist[self._ceremony_edit_index] = item
        self.config.save()
        self._refresh_ceremony_list()
        self._clear_ceremony_form()

    def _delete_ceremony_item(self) -> None:
        selection = self.ceremony_tree.selection()
        if not selection:
            messagebox.showinfo("Seçim", "Silmek için bir parça seçin")
            return
        idx = int(selection[0])
        if 0 <= idx < len(self.config.ceremony_playlist):
            self.config.ceremony_playlist.pop(idx)
            self.config.save()
            self._refresh_ceremony_list()

    def _refresh_ceremony_list(self) -> None:
        if not hasattr(self, "ceremony_tree"):
            return
        for item in self.ceremony_tree.get_children():
            self.ceremony_tree.delete(item)
        for idx, item in enumerate(self.config.ceremony_playlist):
            start_text = _format_mmss(int(item.get("start_ms", 0)))
            end_ms = item.get("end_ms")
            end_text = _format_mmss(end_ms) if end_ms is not None else "-"
            duration_sec = item.get("duration_sec")
            duration_text = _format_mmss(duration_sec * 1000 if duration_sec else None)
            source_text = "YouTube" if item.get("source") == "youtube" else "Dosya"
            self.ceremony_tree.insert(
                "",
                tk.END,
                iid=str(idx),
                values=(item.get("label", "Parça"), source_text, start_text, end_text, duration_text),
            )
        self._ceremony_edit_index = None
        self.ceremony_tree.selection_remove(self.ceremony_tree.selection())

    def _on_ceremony_select(self, _event: object) -> None:
        selection = self.ceremony_tree.selection()
        if not selection:
            return
        idx = int(selection[0])
        if not (0 <= idx < len(self.config.ceremony_playlist)):
            return
        item = self.config.ceremony_playlist[idx]
        self._ceremony_edit_index = idx
        self._ceremony_index = idx
        self.ceremony_source_var.set(item.get("source", "file"))
        self.ceremony_location_var.set(str(item.get("location", "")))
        self.ceremony_title_var.set(item.get("label", ""))
        self.ceremony_start_var.set(_format_mmss(int(item.get("start_ms", 0))))
        end_ms = item.get("end_ms")
        self.ceremony_end_var.set(_format_mmss(end_ms) if end_ms is not None else "")

    def _clear_ceremony_form(self) -> None:
        self._ceremony_edit_index = None
        self.ceremony_source_var.set("file")
        self.ceremony_location_var.set("")
        self.ceremony_title_var.set("")
        self.ceremony_start_var.set("00:00")
        self.ceremony_end_var.set("")
        self.ceremony_tree.selection_remove(self.ceremony_tree.selection())

    def _move_ceremony_item(self, offset: int) -> None:
        selection = self.ceremony_tree.selection()
        if not selection:
            return
        idx = int(selection[0])
        target = idx + offset
        playlist = self.config.ceremony_playlist
        if not (0 <= target < len(playlist)):
            return
        playlist[idx], playlist[target] = playlist[target], playlist[idx]
        self.config.save()
        self._refresh_ceremony_list()
        self.ceremony_tree.selection_set(str(target))
        self.ceremony_tree.see(str(target))

    def _get_media_metadata(
        self, source: str, location: str, show_error: bool = False
    ) -> Optional[tuple[str, Optional[int]]]:
        if source == "file":
            path = Path(location)
            if not path.exists():
                if show_error:
                    messagebox.showerror("Dosya", "Dosya bulunamadı")
                return None
            duration = self._get_duration(location)
            return (path.stem, duration)
        if source == "youtube":
            metadata = self._get_youtube_metadata(location)
            if metadata is None and show_error:
                messagebox.showerror(
                    "YouTube",
                    "Video bilgisi alınamadı. İnternet bağlantısını ve yt-dlp kurulumunu kontrol edin.",
                )
            return metadata
        return None

    def _get_youtube_metadata(self, url: str) -> Optional[tuple[str, Optional[int]]]:
        if not url:
            return None
        if not hasattr(self, "_youtube_meta_cache"):
            self._youtube_meta_cache: Dict[str, tuple[str, Optional[int]]] = {}
        if url in self._youtube_meta_cache:
            return self._youtube_meta_cache[url]
        if yt_dlp is None:
            return (url, None)
        opts = {
            "quiet": True,
            "noplaylist": True,
            "skip_download": True,
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:  # type: ignore[attr-defined]
                info = ydl.extract_info(url, download=False)
        except Exception:
            return None
        title = info.get("title") or url
        duration = info.get("duration")
        metadata = (title, duration)
        self._youtube_meta_cache[url] = metadata
        return metadata

    def _play_selected_ceremony(self) -> None:
        selection = self.ceremony_tree.selection()
        if not selection:
            messagebox.showinfo("Seçim", "Lütfen bir müzik seçin")
            return
        idx = int(selection[0])
        self._ceremony_index = idx
        self._play_ceremony_item(self.config.ceremony_playlist[idx])

    def _play_next_ceremony(self) -> None:
        if not self.config.ceremony_playlist:
            return
        self._ceremony_index = (self._ceremony_index + 1) % len(self.config.ceremony_playlist)
        self.ceremony_tree.selection_set(str(self._ceremony_index))
        self.ceremony_tree.see(str(self._ceremony_index))
        self._play_ceremony_item(self.config.ceremony_playlist[self._ceremony_index])

    def _play_ceremony_item(self, item: Dict[str, object]) -> None:
        source = item.get("source")
        location = str(item.get("location"))
        start_ms = int(item.get("start_ms", 0))
        end_ms = item.get("end_ms")
        path = location
        if source == "youtube":
            path = self._download_youtube_audio(location)
            if not path:
                return
        label = str(item.get("label", "Tören Müziği"))
        self.audio.play_file(self._slice_file(path, start_ms, end_ms), label)

    def _slice_file(self, path: str, start_ms: int, end_ms: Optional[int]) -> str:
        if start_ms <= 0 and not end_ms:
            return path
        audio = AudioSegment.from_file(path)  # type: ignore[name-defined]
        segment = audio[start_ms: end_ms] if end_ms else audio[start_ms:]
        temp_file = Path(tempfile.gettempdir()) / f"slice_{int(time.time())}.wav"
        segment.export(temp_file, format="wav")
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
        self._youtube_meta_cache[url] = (info.get("title") or url, info.get("duration"))
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
