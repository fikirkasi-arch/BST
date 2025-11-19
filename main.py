"""JinniBell Pro okul zil ve tören programı yöneticisi."""
from __future__ import annotations

import calendar
import os
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
from datetime import datetime, date
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Dict, List, Optional, Tuple

from mutagen import File as MutagenFile
from pydub import AudioSegment

from bell_app.audio import AudioController
from bell_app.config import BellConfig, BellEvent, WEEKDAYS, SoundAsset
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

MANUAL_DELAY_CHOICES: List[Tuple[str, int]] = [
    ("Hemen", 0),
    ("3 sn", 3),
    ("5 sn", 5),
    ("7 sn", 7),
    ("10 sn", 10),
    ("15 sn", 15),
]

SCHEDULE_SOUND_CHOICES = [
    ("Öğrenci Girişi", "student_entry"),
    ("Öğretmen Girişi", "teacher_entry"),
    ("Teneffüs Zili", "lesson_exit"),
    ("Teneffüs Müziği", "recess_music"),
]

SOUND_DISPLAY = {value: label for label, value in SCHEDULE_SOUND_CHOICES}

STARTUP_SCRIPT_NAME = "JinniBellPro-AutoStart.bat"


def _is_windows() -> bool:
    return os.name == "nt"


def _startup_script_path() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise RuntimeError("APPDATA değişkeni bulunamadı")
    return (
        Path(appdata)
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
        / STARTUP_SCRIPT_NAME
    )


def _startup_launch_command() -> str:
    if getattr(sys, "frozen", False):
        exe_path = Path(sys.executable).resolve()
        return f'"{exe_path}" --autostart'
    python_exe = Path(sys.executable).resolve()
    script_path = Path(__file__).resolve()
    return f'"{python_exe}" "{script_path}" --autostart'


def enable_windows_startup() -> None:
    script_path = _startup_script_path()
    script_path.parent.mkdir(parents=True, exist_ok=True)
    command = _startup_launch_command()
    content = "\r\n".join(
        [
            "@echo off",
            "set \"JINNIBELL_AUTOSTART=1\"",
            f"start \"\" {command}",
            "",
        ]
    )
    script_path.write_text(content, encoding="utf-8")


def disable_windows_startup() -> None:
    script_path = _startup_script_path()
    if script_path.exists():
        script_path.unlink()


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
        # Tk, özellikle gömülü Tcl sürümlerinde boşluk içeren yazı tiplerini
        # doğru okumak için aile adını süslü parantez içinde bekler; aksi halde
        # "Segoe"yi aile, "UI"yi ise sayı gibi yorumlayarak "expected integer"
        # hatası üretir. Bu nedenle varsayılan yazı tipini {Segoe UI} şeklinde
        # tanımlıyoruz.
        self.root.option_add("*Font", "{Segoe UI} 10")
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
        self._suppress_day_event = False
        self._dragging_ceremony: Optional[int] = None
        self._launched_from_startup = ("--autostart" in sys.argv) or os.environ.get(
            "JINNIBELL_AUTOSTART"
        ) == "1"

        self.scheduler = ScheduleRunner(
            self.config,
            self._handle_event,
            lambda: self.manual_override or self.bells_paused,
        )
        self.scheduler.start()

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._minimize_to_tray)
        self._schedule_countdown_refresh()
        self.root.after(1200, self._auto_minimize_if_needed)

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

        delay_row = ttk.Frame(button_frame)
        delay_row.pack(fill=tk.X, padx=5, pady=(4, 2))
        ttk.Label(delay_row, text="Başlatma süresi:").pack(side=tk.LEFT)
        self.manual_delay_var = tk.StringVar(value=MANUAL_DELAY_CHOICES[0][0])
        ttk.Combobox(
            delay_row,
            state="readonly",
            textvariable=self.manual_delay_var,
            values=[label for label, _ in MANUAL_DELAY_CHOICES],
            width=12,
        ).pack(side=tk.LEFT, padx=6)
        ttk.Label(delay_row, text="(Tören butonları için)").pack(side=tk.LEFT)

        status_frame = ttk.Frame(frame)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(status_frame, text="Durum:").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)

        countdown_frame = tk.LabelFrame(frame, text="Geri Sayım ve Bildirim")
        countdown_frame.pack(fill=tk.X, padx=10, pady=5)
        self.countdown_var = tk.StringVar(value="Sonraki zil hesaplanıyor...")
        countdown_bg = countdown_frame.cget("background")
        tk.Label(
            countdown_frame,
            textvariable=self.countdown_var,
            font=("Segoe UI", 14, "bold"),
            fg="#0b5394",
            bg=countdown_bg,
        ).pack(fill=tk.X, padx=6, pady=4)
        self.pause_badge = tk.Label(
            countdown_frame,
            text="Tören modu kapalı",
            fg="#ffffff",
            bg="#2e7d32",
            font=("Segoe UI", 10, "bold"),
            padx=6,
            pady=2,
        )
        self.pause_badge.pack(fill=tk.X, padx=6, pady=(0, 6))

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

        startup_frame = ttk.LabelFrame(frame, text="Başlangıç / Arka Plan")
        startup_frame.pack(fill=tk.X, padx=10, pady=5)
        self.autostart_var = tk.BooleanVar(value=self.config.launch_on_boot)
        ttk.Checkbutton(
            startup_frame,
            text="Windows açıldığında JinniBell Pro otomatik başlasın (sisteme küçült)",
            variable=self.autostart_var,
            command=self._toggle_autostart,
        ).pack(fill=tk.X, padx=6, pady=(4, 2))
        ttk.Label(
            startup_frame,
            text="Bu seçenek yalnızca Windows'ta kullanılabilir ve oturum açıldığında programı arka plana alır.",
            wraplength=360,
        ).pack(fill=tk.X, padx=6, pady=(0, 4))

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
        self._update_pause_badge()

    def _build_schedule_tab(self, frame: ttk.Frame) -> None:
        container = ttk.Frame(frame)
        container.pack(fill=tk.BOTH, expand=True)

        calendar_panel = ttk.LabelFrame(container, text="Aylık Takvim")
        calendar_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=8)

        now = datetime.now()
        self.calendar_year_var = tk.IntVar(value=now.year)
        self.calendar_month_var = tk.IntVar(value=now.month)
        nav = ttk.Frame(calendar_panel)
        nav.pack(fill=tk.X, padx=6, pady=(6, 2))
        ttk.Button(nav, text="<", width=3, command=lambda: self._change_calendar_month(-1)).pack(side=tk.LEFT)
        ttk.Label(nav, text="Ay").pack(side=tk.LEFT, padx=(6, 2))
        month_combo = ttk.Combobox(
            nav,
            state="readonly",
            width=12,
            textvariable=self.calendar_month_var,
            values=list(range(1, 13)),
        )
        month_combo.pack(side=tk.LEFT)
        month_combo.bind("<<ComboboxSelected>>", lambda _e: self._render_calendar())
        ttk.Label(nav, text="Yıl").pack(side=tk.LEFT, padx=(8, 2))
        year_spin = ttk.Spinbox(nav, from_=now.year - 5, to=now.year + 5, textvariable=self.calendar_year_var, width=6)
        year_spin.pack(side=tk.LEFT)
        year_spin.bind("<FocusOut>", lambda _e: self._render_calendar())
        year_spin.bind("<Return>", lambda _e: self._render_calendar())
        ttk.Button(nav, text=">", width=3, command=lambda: self._change_calendar_month(1)).pack(side=tk.LEFT, padx=(6, 0))

        self.calendar_canvas = tk.Canvas(calendar_panel, width=320, height=260, highlightthickness=0)
        self.calendar_canvas.pack(padx=6, pady=4)
        self.calendar_canvas.bind("<Button-1>", self._on_calendar_click)
        self._calendar_cells: Dict[int, date] = {}
        self._calendar_day_rects: Dict[str, int] = {}
        self._selected_calendar_date: Optional[date] = None

        self.calendar_info_var = tk.StringVar(value="Gün seçin")
        ttk.Label(calendar_panel, textvariable=self.calendar_info_var, wraplength=300).pack(fill=tk.X, padx=6, pady=(4, 2))
        ttk.Button(calendar_panel, text="Bugüne Git", command=self._goto_today_from_calendar).pack(padx=6, pady=(0, 8), fill=tk.X)

        right_panel = ttk.Frame(container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=8)

        header = ttk.Frame(right_panel)
        header.pack(fill=tk.X)
        ttk.Label(header, text="Düzenlenen Gün", style="Bold.TLabel").pack(side=tk.LEFT)
        self.day_var = tk.StringVar(value=WEEKDAYS[now.weekday()])
        day_combo = ttk.Combobox(header, values=WEEKDAYS, textvariable=self.day_var, state="readonly", width=15)
        day_combo.pack(side=tk.LEFT, padx=6)
        day_combo.bind("<<ComboboxSelected>>", self._on_day_change)
        ttk.Button(header, text="Diğer Günlere Uygula", command=self._open_copy_dialog).pack(side=tk.RIGHT, padx=5)

        table_frame = ttk.Frame(right_panel)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(4, 8))
        columns = ("clock", "label", "sound")
        self.event_list = ttk.Treeview(table_frame, columns=columns, show="headings", height=11, selectmode="browse")
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

        form = ttk.LabelFrame(right_panel, text="Yeni/Seçili Zil")
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

        copy_frame = ttk.LabelFrame(right_panel, text="Program Kopyala")
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

        holiday_frame = ttk.LabelFrame(right_panel, text="Tatil Günleri")
        holiday_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        self.holiday_list = tk.Listbox(holiday_frame, height=5)
        self.holiday_list.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        holiday_btns = ttk.Frame(holiday_frame)
        holiday_btns.pack(fill=tk.X, padx=6, pady=6)
        ttk.Button(holiday_btns, text="Ekle", command=self._add_holiday).pack(side=tk.LEFT, padx=5)
        ttk.Button(holiday_btns, text="Sil", command=self._remove_holiday).pack(side=tk.LEFT, padx=5)

        simulation = ttk.LabelFrame(right_panel, text="Zil Testi Simülasyonu")
        simulation.pack(fill=tk.X, padx=12, pady=(0, 10))
        self.sim_day_var = tk.StringVar(value=self.day_var.get())
        ttk.Label(simulation, text="Gün").grid(row=0, column=0, padx=4, pady=4, sticky=tk.W)
        ttk.Combobox(simulation, values=WEEKDAYS, textvariable=self.sim_day_var, state="readonly", width=15).grid(
            row=1, column=0, padx=4, pady=2, sticky=tk.W
        )
        ttk.Label(simulation, text="Olay başına bekleme (sn)").grid(row=0, column=1, padx=4, pady=4, sticky=tk.W)
        self.sim_speed_var = tk.DoubleVar(value=0.8)
        ttk.Spinbox(simulation, from_=0.2, to=2.0, increment=0.1, textvariable=self.sim_speed_var, width=6).grid(
            row=1, column=1, padx=4, pady=2
        )
        ttk.Button(simulation, text="Simülasyonu Başlat", command=self._start_simulation).grid(
            row=1, column=2, padx=8, pady=2
        )

        self._render_calendar()
        self._refresh_event_list()

    def _build_sound_tab(self, frame: ttk.Frame) -> None:
        ttk.Label(frame, text="Her ses için dosya seçin").pack(anchor=tk.W, padx=10, pady=5)
        self.recess_var = tk.BooleanVar(value=self.config.recess_music_enabled)
        self._sound_path_vars: Dict[str, tk.StringVar] = {}
        self._library_comboboxes: List[ttk.Combobox] = []
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

        ttk.Separator(frame).pack(fill=tk.X, padx=10, pady=8)
        self._build_sound_library_section(frame)
        self._refresh_sound_library()

    def _build_sound_row(self, frame: ttk.Frame, key: str, label: str) -> None:
        row = ttk.Frame(frame)
        row.pack(fill=tk.X, padx=10, pady=2)
        ttk.Label(row, text=label, width=28).pack(side=tk.LEFT)
        path_var = tk.StringVar(value=self.config.sound_files.get(key, ""))
        self._sound_path_vars[key] = path_var
        entry = ttk.Entry(row, textvariable=path_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        def choose() -> None:
            file_path = filedialog.askopenfilename(title=label)
            if file_path:
                path_var.set(file_path)
                self.config.sound_files[key] = file_path
                self.config.save()

        ttk.Button(row, text="Seç", command=choose).pack(side=tk.LEFT)
        ttk.Button(row, text="Kaydet", command=lambda k=key, var=path_var: self._save_sound_path(k, var.get())).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(row, text="Test", command=lambda var=path_var: self.audio.play_file(var.get(), label)).pack(
            side=tk.LEFT, padx=2
        )

        lib_combo = ttk.Combobox(row, state="readonly", width=18)
        lib_combo.pack(side=tk.LEFT, padx=(6, 2))
        self._library_comboboxes.append(lib_combo)
        ttk.Button(
            row,
            text="Kitaplıktan",
            command=lambda c=lib_combo, sound_key=key, var=path_var: self._apply_library_selection(sound_key, var, c.get()),
        ).pack(side=tk.LEFT, padx=2)

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
        columns = ("title", "source", "status", "start", "end", "duration")
        self.ceremony_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse", height=12)
        self.ceremony_tree.heading("title", text="Başlık")
        self.ceremony_tree.heading("source", text="Kaynak")
        self.ceremony_tree.heading("status", text="Durum")
        self.ceremony_tree.heading("start", text="Başlangıç")
        self.ceremony_tree.heading("end", text="Bitiş")
        self.ceremony_tree.heading("duration", text="Toplam")
        self.ceremony_tree.column("title", width=200, anchor=tk.W)
        self.ceremony_tree.column("source", width=90, anchor=tk.CENTER)
        self.ceremony_tree.column("status", width=120, anchor=tk.W)
        self.ceremony_tree.column("start", width=80, anchor=tk.CENTER)
        self.ceremony_tree.column("end", width=80, anchor=tk.CENTER)
        self.ceremony_tree.column("duration", width=90, anchor=tk.CENTER)
        self.ceremony_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.ceremony_tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.ceremony_tree.configure(yscrollcommand=tree_scroll.set)
        self.ceremony_tree.bind("<<TreeviewSelect>>", self._on_ceremony_select)
        self.ceremony_tree.bind("<ButtonPress-1>", self._start_ceremony_drag)
        self.ceremony_tree.bind("<ButtonRelease-1>", self._complete_ceremony_drag)

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
        self._update_pause_badge()

    def _toggle_autostart(self) -> None:
        desired = self.autostart_var.get()
        if desired == self.config.launch_on_boot:
            return
        if not _is_windows():
            messagebox.showwarning(
                "Başlangıç Ayarı",
                "Bu özellik yalnızca Windows işletim sisteminde kullanılabilir.",
            )
            self.autostart_var.set(False)
            return
        try:
            if desired:
                enable_windows_startup()
            else:
                disable_windows_startup()
        except Exception as exc:  # pragma: no cover - ortam bağımlı
            messagebox.showerror(
                "Başlangıç Ayarı",
                f"Windows başlangıç ayarı uygulanamadı: {exc}",
            )
            self.autostart_var.set(self.config.launch_on_boot)
            return
        self.config.launch_on_boot = desired
        self.config.save()

    def _toggle_shutdown(self) -> None:
        self.config.auto_shutdown_enabled = self.shutdown_var.get()
        self.config.auto_shutdown_time = self.shutdown_entry.get()
        self.config.save()

    def _toggle_recess_music(self) -> None:
        self.config.recess_music_enabled = self.recess_var.get()
        self.config.save()

    def _build_sound_library_section(self, frame: ttk.Frame) -> None:
        library_frame = ttk.LabelFrame(frame, text="Ses Kütüphanesi ve Etiketler")
        library_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        columns = ("name", "tags", "path")
        self.library_tree = ttk.Treeview(library_frame, columns=columns, show="headings", height=6)
        self.library_tree.heading("name", text="İsim")
        self.library_tree.heading("tags", text="Etiketler")
        self.library_tree.heading("path", text="Dosya")
        self.library_tree.column("name", width=150, anchor=tk.W)
        self.library_tree.column("tags", width=160, anchor=tk.W)
        self.library_tree.column("path", anchor=tk.W)
        self.library_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)
        self.library_tree.bind("<Double-1>", lambda _e: self._play_selected_library_asset())
        btns = ttk.Frame(library_frame)
        btns.pack(fill=tk.X, padx=6, pady=4)
        ttk.Button(btns, text="Dosya Ekle", command=self._add_sound_asset).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="Etiketleri Düzenle", command=self._edit_sound_asset).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="Sil", command=self._remove_sound_asset).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="Test", command=self._play_selected_library_asset).pack(side=tk.RIGHT, padx=2)

    def _save_sound_path(self, key: str, value: str) -> None:
        if not value:
            messagebox.showwarning("Ses", "Lütfen dosya yolunu girin")
            return
        self.config.sound_files[key] = value
        self.config.save()
        messagebox.showinfo("Ses", "Dosya kaydedildi")

    def _apply_library_selection(self, sound_key: str, var: tk.StringVar, asset_name: str) -> None:
        if not asset_name:
            messagebox.showinfo("Ses", "Önce kütüphaneden bir isim seçin")
            return
        asset = self.config.find_sound_asset_by_name(asset_name)
        if not asset:
            messagebox.showerror("Ses", "Seçilen ses kütüphanede bulunamadı")
            return
        var.set(asset.get("path", ""))
        self._save_sound_path(sound_key, asset.get("path", ""))

    def _refresh_sound_library(self) -> None:
        if not hasattr(self, "library_tree"):
            return
        for item in self.library_tree.get_children():
            self.library_tree.delete(item)
        names: List[str] = []
        for asset in self.config.sound_library:
            names.append(asset.get("name", "Ses"))
            tags = ", ".join(asset.get("tags", []))
            self.library_tree.insert(
                "",
                tk.END,
                iid=asset.get("asset_id"),
                values=(asset.get("name", "Ses"), tags, asset.get("path", "")),
            )
        for combo in getattr(self, "_library_comboboxes", []):
            combo.configure(values=names)

    def _add_sound_asset(self) -> None:
        file_path = filedialog.askopenfilename(title="Ses dosyası ekle")
        if not file_path:
            return
        default_name = Path(file_path).stem
        name = simpledialog.askstring("İsim", "Kütüphanede görünecek isim", initialvalue=default_name)
        if not name:
            messagebox.showwarning("Ses", "İsim gerekli")
            return
        tag_text = simpledialog.askstring("Etiketler", "Virgülle ayırın", initialvalue="")
        tags = [tag.strip() for tag in (tag_text or "").split(",") if tag.strip()]
        self.config.add_sound_asset(name, file_path, tags)
        self._refresh_sound_library()

    def _edit_sound_asset(self) -> None:
        asset_id = self._get_selected_asset_id()
        if not asset_id:
            messagebox.showinfo("Ses", "Önce bir satır seçin")
            return
        asset = self.config.get_sound_asset(asset_id)
        if not asset:
            return
        name = simpledialog.askstring("İsim", "Yeni isim", initialvalue=asset.get("name", ""))
        if name is None:
            return
        tag_text = simpledialog.askstring(
            "Etiketler",
            "Virgülle ayırın",
            initialvalue=", ".join(asset.get("tags", [])),
        )
        tags = [tag.strip() for tag in (tag_text or "").split(",") if tag.strip()]
        self.config.update_sound_asset(asset_id, name=name, tags=tags)
        self._refresh_sound_library()

    def _remove_sound_asset(self) -> None:
        asset_id = self._get_selected_asset_id()
        if not asset_id:
            messagebox.showinfo("Ses", "Silmek için bir satır seçin")
            return
        if not messagebox.askyesno("Sil", "Seçili ses kütüphaneden silinsin mi?"):
            return
        self.config.remove_sound_asset(asset_id)
        self._refresh_sound_library()

    def _play_selected_library_asset(self) -> None:
        asset_id = self._get_selected_asset_id()
        if not asset_id:
            return
        asset = self.config.get_sound_asset(asset_id)
        if not asset:
            return
        path = asset.get("path", "")
        if not Path(path).exists():
            messagebox.showerror("Ses", "Dosya bulunamadı")
            return
        self.audio.play_file(path, asset.get("name", "Ses"))

    def _get_selected_asset_id(self) -> Optional[str]:
        if not hasattr(self, "library_tree"):
            return None
        selection = self.library_tree.selection()
        if not selection:
            return None
        return selection[0]

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

    def _on_day_change(self, _event: object | None = None) -> None:
        if getattr(self, "_suppress_day_event", False):
            return
        self._refresh_event_list()
        if hasattr(self, "sim_day_var"):
            self.sim_day_var.set(self.day_var.get())
        self._focus_calendar_to_weekday(self.day_var.get())

    def _change_calendar_month(self, delta: int) -> None:
        month = int(self.calendar_month_var.get()) + delta
        year = int(self.calendar_year_var.get())
        if month < 1:
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1
        self.calendar_month_var.set(month)
        self.calendar_year_var.set(year)
        self._render_calendar()

    def _render_calendar(self) -> None:
        if not hasattr(self, "calendar_canvas"):
            return
        self.calendar_canvas.delete("all")
        self._calendar_cells.clear()
        self._calendar_day_rects.clear()
        width = 320
        height = 240
        cell_w = width / 7
        cell_h = height / 6
        year = int(self.calendar_year_var.get())
        month = int(self.calendar_month_var.get())
        cal = calendar.Calendar(firstweekday=0)
        today = date.today()
        if self._selected_calendar_date is None and today.year == year and today.month == month:
            self._selected_calendar_date = today
        for row_idx, week in enumerate(cal.monthdayscalendar(year, month)):
            for col_idx, day in enumerate(week):
                x0 = col_idx * cell_w
                y0 = row_idx * cell_h
                x1 = x0 + cell_w
                y1 = y0 + cell_h
                if day == 0:
                    rect_id = self.calendar_canvas.create_rectangle(x0, y0, x1, y1, fill="#f4f4f4", outline="#d0d7de")
                    continue
                current = date(year, month, day)
                weekday_name = WEEKDAYS[current.weekday()]
                event_count = len(self.config.daily_schedule.get(weekday_name, []))
                holiday = self.config.holiday_for(current)
                fill = "#ffffff"
                if holiday:
                    fill = "#ffebee"
                elif event_count == 0:
                    fill = "#f4f8fb"
                elif event_count < 4:
                    fill = "#e3f2fd"
                else:
                    fill = "#fff3e0"
                rect_id = self.calendar_canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="#d0d7de")
                text_lines = [str(day)]
                if holiday:
                    text_lines.append("Tatil")
                elif event_count:
                    text_lines.append(f"{event_count} zil")
                text_id = self.calendar_canvas.create_text(
                    (x0 + x1) / 2,
                    (y0 + y1) / 2,
                    text="\n".join(text_lines),
                    font=("Segoe UI", 9),
                )
                for item_id in (rect_id, text_id):
                    self._calendar_cells[item_id] = current
                self._calendar_day_rects[current.isoformat()] = rect_id
        self._highlight_calendar_day(self._selected_calendar_date)
        if self._selected_calendar_date:
            self._update_calendar_info(self._selected_calendar_date)

    def _on_calendar_click(self, event: tk.Event) -> None:
        if not hasattr(self, "calendar_canvas"):
            return
        clicked = self.calendar_canvas.find_withtag("current")
        if not clicked:
            clicked = self.calendar_canvas.find_closest(event.x, event.y)
        if not clicked:
            return
        current_date = self._calendar_cells.get(clicked[0])
        if current_date:
            self._select_calendar_date(current_date)

    def _select_calendar_date(self, day_date: date, *, sync_combo: bool = True, refresh: bool = True) -> None:
        self._selected_calendar_date = day_date
        self._highlight_calendar_day(day_date)
        self._update_calendar_info(day_date)
        weekday_name = WEEKDAYS[day_date.weekday()]
        if sync_combo:
            self._suppress_day_event = True
            self.day_var.set(weekday_name)
            self._suppress_day_event = False
        if hasattr(self, "sim_day_var"):
            self.sim_day_var.set(weekday_name)
        if refresh:
            self._refresh_event_list()

    def _highlight_calendar_day(self, current: Optional[date]) -> None:
        if not hasattr(self, "calendar_canvas"):
            return
        for rect_id in self._calendar_day_rects.values():
            self.calendar_canvas.itemconfigure(rect_id, width=1, outline="#d0d7de")
        if current is None:
            return
        key = current.isoformat()
        rect_id = self._calendar_day_rects.get(key)
        if rect_id:
            self.calendar_canvas.itemconfigure(rect_id, width=3, outline="#0b5394")

    def _update_calendar_info(self, current: date) -> None:
        if not hasattr(self, "calendar_info_var"):
            return
        weekday_name = WEEKDAYS[current.weekday()]
        events = self.config.daily_schedule.get(weekday_name, [])
        holiday = self.config.holiday_for(current)
        if holiday:
            info = f"{current.strftime('%d.%m.%Y')} ({weekday_name}) - Tatil: {holiday}"
        else:
            info = f"{current.strftime('%d.%m.%Y')} ({weekday_name}) - {len(events)} zil"
        self.calendar_info_var.set(info)

    def _goto_today_from_calendar(self) -> None:
        today = date.today()
        self.calendar_year_var.set(today.year)
        self.calendar_month_var.set(today.month)
        self._render_calendar()
        self._select_calendar_date(today)

    def _focus_calendar_to_weekday(self, weekday_name: str) -> None:
        year = int(self.calendar_year_var.get())
        month = int(self.calendar_month_var.get())
        cal = calendar.Calendar(firstweekday=0)
        for day_date in cal.itermonthdates(year, month):
            if day_date.month != month:
                continue
            if WEEKDAYS[day_date.weekday()] == weekday_name:
                self._select_calendar_date(day_date, sync_combo=False, refresh=False)
                break

    def _start_simulation(self) -> None:
        day = self.sim_day_var.get()
        events = sorted(self.config.daily_schedule.get(day, []), key=lambda evt: evt.clock)
        if not events:
            messagebox.showinfo("Simülasyon", f"{day} için tanımlı zil yok")
            return
        speed = float(self.sim_speed_var.get())
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{day} Simülasyonu")
        dialog.geometry("520x360")
        text = tk.Text(dialog, state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)

        def append_line(line: str) -> None:
            text.configure(state=tk.NORMAL)
            text.insert(tk.END, line + "\n")
            text.see(tk.END)
            text.configure(state=tk.DISABLED)

        append_line(f"{day} günü için {len(events)} zil simülasyonu başlatıldı (x{speed:.1f} hız)")
        collision_map: Dict[str, List[str]] = {}
        for event in events:
            collision_map.setdefault(event.clock, []).append(event.label)

        def schedule_event(idx: int) -> None:
            if idx >= len(events):
                append_line("Simülasyon tamamlandı.")
                for clock, labels in collision_map.items():
                    if len(labels) > 1:
                        append_line(f"⚠️ {clock} saatinde {len(labels)} zil çakışıyor: {', '.join(labels)}")
                return
            event = events[idx]
            append_line(f"{event.clock} -> {event.label} ({SOUND_DISPLAY.get(event.sound_type, event.sound_type)})")
            self.root.after(int(speed * 1000), lambda: schedule_event(idx + 1))

        self.root.after(int(speed * 1000), lambda: schedule_event(0))

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
        delay_seconds = self._get_manual_delay_seconds()
        if delay_seconds > 0:
            self._update_status(f"Manuel çalma {delay_seconds} sn sonra başlayacak")
            self.root.after(delay_seconds * 1000, lambda: self._execute_manual_sequence(steps))
        else:
            self._execute_manual_sequence(steps)

    def _execute_manual_sequence(self, steps: List[tuple[str, Optional[str]]]) -> None:
        self.audio.play_sequence(steps, on_complete=lambda: setattr(self, "manual_override", False))

    def _get_manual_delay_seconds(self) -> int:
        if not hasattr(self, "manual_delay_var"):
            return 0
        selected = self.manual_delay_var.get()
        for label, seconds in MANUAL_DELAY_CHOICES:
            if label == selected:
                return seconds
        return 0

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

    def _prepare_ceremony_item(
        self, item: Dict[str, object], existing: Optional[Dict[str, object]] = None
    ) -> Dict[str, object]:
        source = item.get("source")
        location = str(item.get("location", ""))
        if source == "file":
            status = "Hazır" if Path(location).exists() else "Dosya bulunamadı"
            detail = Path(location).name if location else ""
            item["status"] = status
            item["status_detail"] = detail
            item.pop("cache_path", None)
        else:
            same_resource = existing and existing.get("location") == location
            if same_resource and existing.get("status") == "Hazır":
                item["status"] = "Hazır"
                item["status_detail"] = existing.get("status_detail")
                if existing.get("cache_path"):
                    item["cache_path"] = existing.get("cache_path")
            else:
                item["status"] = "Bekliyor"
                item["status_detail"] = "İndirme bekleniyor"
                item.pop("cache_path", None)
        return item

    def _save_ceremony_item(self) -> None:
        item = self._collect_ceremony_form()
        if item is None:
            return
        if self._ceremony_edit_index is None:
            prepared = self._prepare_ceremony_item(item)
            self.config.ceremony_playlist.append(prepared)
        else:
            existing = self.config.ceremony_playlist[self._ceremony_edit_index]
            prepared = self._prepare_ceremony_item(item, existing)
            self.config.ceremony_playlist[self._ceremony_edit_index] = prepared
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
            status_text = self._describe_ceremony_status(item)
            self.ceremony_tree.insert(
                "",
                tk.END,
                iid=str(idx),
                values=(
                    item.get("label", "Parça"),
                    source_text,
                    status_text,
                    start_text,
                    end_text,
                    duration_text,
                ),
            )
        self._ceremony_edit_index = None
        self.ceremony_tree.selection_remove(self.ceremony_tree.selection())

    def _describe_ceremony_status(self, item: Dict[str, object]) -> str:
        status = item.get("status") or ("Hazır" if item.get("source") == "file" else "Bekliyor")
        detail = item.get("status_detail")
        if detail:
            return f"{status} - {detail}"
        return str(status)

    def _set_ceremony_status(
        self, index: int, status: str, detail: Optional[str] = None, cache_path: Optional[str] = None
    ) -> None:
        if not (0 <= index < len(self.config.ceremony_playlist)):
            return
        item = self.config.ceremony_playlist[index]
        item["status"] = status
        if detail is not None:
            item["status_detail"] = detail
        if cache_path is not None:
            item["cache_path"] = cache_path
        self.config.save()
        self._refresh_ceremony_list()

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

    def _start_ceremony_drag(self, event: tk.Event) -> None:
        row = self.ceremony_tree.identify_row(event.y)
        if row:
            self._dragging_ceremony = int(row)

    def _complete_ceremony_drag(self, event: tk.Event) -> None:
        if self._dragging_ceremony is None:
            return
        row = self.ceremony_tree.identify_row(event.y)
        if not row:
            target = len(self.config.ceremony_playlist) - 1
        else:
            target = int(row)
        source = self._dragging_ceremony
        self._dragging_ceremony = None
        playlist = self.config.ceremony_playlist
        if not (0 <= source < len(playlist) and 0 <= target < len(playlist)):
            return
        if source == target:
            return
        item = playlist.pop(source)
        playlist.insert(target, item)
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
        self._play_ceremony_item(idx)

    def _play_next_ceremony(self) -> None:
        if not self.config.ceremony_playlist:
            return
        self._ceremony_index = (self._ceremony_index + 1) % len(self.config.ceremony_playlist)
        self.ceremony_tree.selection_set(str(self._ceremony_index))
        self.ceremony_tree.see(str(self._ceremony_index))
        self._play_ceremony_item(self._ceremony_index)

    def _play_ceremony_item(self, index: int) -> None:
        if not (0 <= index < len(self.config.ceremony_playlist)):
            return
        item = self.config.ceremony_playlist[index]
        source = item.get("source")
        location = str(item.get("location", ""))
        start_ms = int(item.get("start_ms", 0))
        end_ms = item.get("end_ms")
        path = location
        if source == "youtube":
            self._set_ceremony_status(index, "İndiriliyor", "YouTube bağlantısı hazırlanıyor")
            path = self._download_youtube_audio(location, playlist_index=index)
            if not path:
                self._set_ceremony_status(index, "Hata", "İndirme başarısız")
                return
        elif not Path(path).exists():
            self._set_ceremony_status(index, "Hata", "Dosya bulunamadı")
            messagebox.showerror("Dosya", "Seçilen dosya bulunamadı")
            return
        label = str(item.get("label", "Tören Müziği"))
        self.audio.play_file(self._slice_file(path, start_ms, end_ms), label)
        self._set_ceremony_status(index, "Hazır", "Çalmaya hazır")

    def _slice_file(self, path: str, start_ms: int, end_ms: Optional[int]) -> str:
        if start_ms <= 0 and not end_ms:
            return path
        audio = AudioSegment.from_file(path)  # type: ignore[name-defined]
        segment = audio[start_ms: end_ms] if end_ms else audio[start_ms:]
        temp_file = Path(tempfile.gettempdir()) / f"slice_{int(time.time())}.wav"
        segment.export(temp_file, format="wav")
        return str(temp_file)

    def _download_youtube_audio(self, url: str, playlist_index: Optional[int] = None) -> Optional[str]:
        if playlist_index is not None and 0 <= playlist_index < len(self.config.ceremony_playlist):
            cache_path = self.config.ceremony_playlist[playlist_index].get("cache_path")
            if cache_path and Path(cache_path).exists():
                return str(cache_path)
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
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:  # type: ignore[attr-defined]
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
        except Exception as exc:  # pragma: no cover - ağ hatası
            if playlist_index is not None:
                self._set_ceremony_status(playlist_index, "Hata", str(exc))
            messagebox.showerror("YouTube", f"İndirme başarısız: {exc}")
            return None
        self._youtube_meta_cache[url] = (info.get("title") or url, info.get("duration"))
        self._youtube_cache[url] = file_path
        if playlist_index is not None:
            self._set_ceremony_status(playlist_index, "Hazır", "İndirildi", cache_path=file_path)
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

    def _auto_minimize_if_needed(self) -> None:
        if getattr(self, "root", None) is None:
            return
        if self.config.launch_on_boot and self._launched_from_startup:
            self._minimize_to_tray()

    # endregion

    def _update_status(self, message: str) -> None:
        self.status_var.set(message)
        self._update_pause_badge()
        self._update_countdown_label()

    def _schedule_countdown_refresh(self) -> None:
        if not hasattr(self, "root"):
            return
        self._update_countdown_label()
        self.root.after(1000, self._schedule_countdown_refresh)

    def _update_countdown_label(self) -> None:
        if not hasattr(self, "countdown_var"):
            return
        now = datetime.now()
        holiday = self.config.holiday_for(date.today())
        if holiday:
            self.countdown_var.set(f"Bugün tatil: {holiday}")
            return
        today_name = WEEKDAYS[now.weekday()]
        next_event = self.config.next_event_for_day(today_name, now.time())
        if not next_event:
            self.countdown_var.set("Bugün kalan zil yok")
            return
        try:
            target_time = datetime.strptime(next_event.clock, "%H:%M")
            target_dt = datetime.combine(date.today(), target_time.time())
        except ValueError:
            self.countdown_var.set("Sıradaki zil hesaplanamadı")
            return
        remaining = int((target_dt - now).total_seconds())
        if remaining < 0:
            remaining = 0
        minutes, seconds = divmod(remaining, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            formatted = f"{minutes:02d}:{seconds:02d}"
        prefix = "(Tören Modu) " if self.bells_paused else ""
        self.countdown_var.set(
            f"{prefix}Sonraki zil {next_event.label} için {formatted} sonra ({next_event.clock})"
        )

    def _update_pause_badge(self) -> None:
        if not hasattr(self, "pause_badge"):
            return
        if getattr(self, "bells_paused", False):
            self.pause_badge.configure(
                text="Tören modu aktif - otomatik ziller kapalı",
                bg="#b71c1c",
            )
        else:
            self.pause_badge.configure(text="Tören modu kapalı", bg="#2e7d32")


if __name__ == "__main__":
    root = tk.Tk()
    app = BellApplication(root)
    root.mainloop()
