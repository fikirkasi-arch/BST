"""JinniBell Pro okul zil ve tören programı yöneticisi."""
from __future__ import annotations

import argparse
import calendar
import os
import signal
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime, date
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Callable, Dict, List, Optional, Tuple
from uuid import uuid4

from mutagen import File as MutagenFile
from pydub import AudioSegment

import bell_app.audio as audio
from bell_app.audio import AudioController
from bell_app.config import BellConfig, BellEvent, WEEKDAYS, ensure_media_dir
from bell_app.scheduler import ScheduleRunner

try:  # pragma: no cover - opsiyonel
    import yt_dlp  # type: ignore
except Exception:  # pragma: no cover - opsiyonel
    yt_dlp = None

try:  # pragma: no cover - sistem tepsisi için gerekli
    import pystray  # type: ignore
    from PIL import Image, ImageDraw  # type: ignore
except Exception:  # pragma: no cover - tepsi desteği opsiyonel
    pystray = None
    Image = None  # type: ignore
    ImageDraw = None  # type: ignore

try:  # pragma: no cover - bildirimler için
    from plyer import notification as plyer_notification  # type: ignore
except Exception:  # pragma: no cover - opsiyonel
    plyer_notification = None

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
TABLE_SOUND_TYPES = ["student_entry", "teacher_entry", "lesson_exit"]
TABLE_DEFAULT_ROWS = 16
TABLE_MAX_ROWS = 24
SOUND_HINTS = {
    "student_entry": "Öğrencilerin sınıfa giriş zili. Ders başlamadan hemen önce çalar.",
    "teacher_entry": "Öğretmen yoklaması ya da ders başlangıcı duyurusu olarak kullanılır.",
    "lesson_exit": "Ders bitişi/teneffüs başlangıcında çalar.",
    "recess_music": "Teneffüs boyunca döngüye alınacak isteğe bağlı müzik.",
    "istiklal": "İstiklal Marşı butonları ve tören listesinde kullanılır.",
    "siren": "Siren + İstiklal seçenekleri için zorunlu değildir ama tavsiye edilir.",
    "moment_of_silence": "1 dk / 2 dk saygı duruşu tuşları bu dosyayı kullanır; boşsa sessiz bekler.",
}

STARTUP_SCRIPT_NAME = "JinniBellPro-AutoStart.bat"
SERVICE_TASK_NAME = "JinniBellProService"
MEDIA_DIR = ensure_media_dir()

SHUTDOWN_MODES: List[Tuple[str, str]] = [
    ("Kapalı", "disabled"),
    ("Belirli Saatte Kapat", "time"),
    ("Son zil sonrası kapat", "after_last_bell"),
]


def _is_windows() -> bool:
    return os.name == "nt"


def _slugify(value: str) -> str:
    cleaned = []
    for char in value.strip().lower():
        if char.isalnum():
            cleaned.append(char)
        elif char in {" ", "-", "_"}:
            cleaned.append("-")
    slug = "".join(cleaned).strip("-")
    return slug or "ses"


def _copy_into_media(source_path: str, name_hint: str = "") -> str:
    path = Path(source_path)
    if not path.exists():
        raise FileNotFoundError(source_path)
    ensure_media_dir()
    base_name = _slugify(name_hint or path.stem)
    suffix = path.suffix.lower()
    candidate = MEDIA_DIR / f"{base_name}{suffix}"
    counter = 1
    while True:
        try:
            if candidate.exists() and path.samefile(candidate):
                return str(candidate)
        except OSError:
            pass
        if not candidate.exists():
            shutil.copy2(path, candidate)
            return str(candidate)
        candidate = MEDIA_DIR / f"{base_name}-{counter}{suffix}"
        counter += 1


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


def _service_task_command() -> str:
    if getattr(sys, "frozen", False):
        exe_path = Path(sys.executable).resolve()
        return f'"{exe_path}" --service'
    python_exe = Path(sys.executable).resolve()
    script_path = Path(__file__).resolve()
    return f'"{python_exe}" "{script_path}" --service'


class ToolTip:
    def __init__(self, widget: tk.Widget, text: str):
        self.widget = widget
        self.text = text
        self.tip: Optional[tk.Toplevel] = None
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)
        widget.bind("<ButtonPress>", self._hide)

    def _show(self, _event: object) -> None:
        if self.tip or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 25
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tip,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Segoe UI", 9),
            padx=6,
            pady=4,
        )
        label.pack()

    def _hide(self, _event: object) -> None:
        if self.tip:
            self.tip.destroy()
            self.tip = None


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


def enable_windows_service_start() -> None:
    if not _is_windows():
        raise RuntimeError("Bu özellik yalnızca Windows'ta kullanılabilir")
    command = _service_task_command()
    result = subprocess.run(
        [
            "schtasks",
            "/Create",
            "/SC",
            "ONSTART",
            "/RL",
            "HIGHEST",
            "/TN",
            SERVICE_TASK_NAME,
            "/TR",
            command,
            "/F",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())


def disable_windows_service_start() -> None:
    if not _is_windows():
        return
    subprocess.run(["schtasks", "/Delete", "/TN", SERVICE_TASK_NAME, "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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


class Notifier:
    def __init__(self) -> None:
        self._available = plyer_notification is not None

    def notify(self, title: str, message: str) -> None:
        if not self._available:
            return
        try:  # pragma: no cover - işletim sistemi bağımlı
            plyer_notification.notify(title=title, message=message, app_name="JinniBell Pro", timeout=5)
        except Exception:
            pass


class TrayController:
    def __init__(self, app: "BellApplication") -> None:
        self.app = app
        self.icon: Optional[pystray.Icon] = None
        self._thread: Optional[threading.Thread] = None

    def ensure(self) -> None:
        if pystray is None or Image is None or ImageDraw is None:
            return
        if self.icon:
            return
        image = self._create_icon()
        menu = pystray.Menu(
            pystray.MenuItem("Göster", self._menu_callback(self.app._restore_from_tray)),
            pystray.MenuItem(
                "Tören Modu",
                self._menu_callback(self.app._toggle_pause_from_tray),
                checked=lambda item: self.app.is_ceremony_mode_active(),
            ),
            pystray.MenuItem("Çıkış", self._menu_callback(self.app._quit_from_tray)),
        )
        self.icon = pystray.Icon("JinniBellPro", image, "JinniBell Pro", menu)
        self._thread = threading.Thread(target=self.icon.run, daemon=True)
        self._thread.start()

    def hide_if_visible(self) -> None:
        if self.icon:
            self.icon.stop()
            self.icon = None
            self._thread = None

    def _menu_callback(self, func: Callable[[], None]) -> Callable[[object, object], None]:
        def wrapper(_icon: object, _item: object) -> None:
            if getattr(self.app, "root", None):
                self.app.root.after(0, func)
            else:
                func()

        return wrapper

    @staticmethod
    def _create_icon() -> "Image.Image":  # type: ignore[name-defined]
        image = Image.new("RGB", (64, 64), color="#0b5394")  # type: ignore[name-defined]
        draw = ImageDraw.Draw(image)  # type: ignore[name-defined]
        draw.rectangle((8, 40, 56, 56), fill="#ffffff")
        draw.rectangle((20, 20, 44, 44), outline="#ffffff", width=3)
        draw.ellipse((28, 10, 36, 18), fill="#ffffff")
        return image


def _execute_bell_event(
    config: BellConfig,
    audio: AudioController,
    notifier: Optional[Notifier],
    event: BellEvent,
    play_recess: Callable[[], None],
    run_shutdown: Callable[[], None],
) -> None:
    if event.sound_type == "auto_shutdown":
        run_shutdown()
        if notifier:
            notifier.notify("JinniBell Pro", "Otomatik kapanış başlatıldı")
        return

    file_path = config.sound_files.get(event.sound_type, "")
    if not file_path:
        if notifier:
            notifier.notify("Ses atanmadı", f"{event.label} için ses bulunamadı")
        return

    if notifier:
        notifier.notify("Zil Başladı", f"{event.clock} - {event.label}")

    steps: List[tuple[str, Optional[str]]] = [("sound", file_path)]
    announcement = config.announcement_for(event.sound_type)
    if announcement:
        steps.append(("sound", announcement["path"]))

    def after_sequence() -> None:
        if event.sound_type == "lesson_exit" and config.recess_music_enabled:
            play_recess()

    callback = after_sequence if (event.sound_type == "lesson_exit" and config.recess_music_enabled) else None
    audio.play_sequence(steps, on_complete=callback)


class HeadlessBellService:
    def __init__(self) -> None:
        self.config = BellConfig.load()
        self.audio = AudioController()
        self.notifier = Notifier()
        self._recess_thread: Optional[threading.Thread] = None
        self.scheduler = ScheduleRunner(self.config, self._handle_event, lambda: False)
        self._running = False

    def run(self) -> None:
        self._running = True
        for sig in (getattr(signal, "SIGINT", None), getattr(signal, "SIGTERM", None)):
            if sig is not None:
                signal.signal(sig, lambda *_args: self.stop())
        self.scheduler.start()
        self.notifier.notify("JinniBell Pro", "Servis modu başlatıldı")
        try:
            while self._running:
                time.sleep(1)
        finally:
            self.scheduler.stop()
            self.audio.stop()

    def stop(self) -> None:
        self._running = False

    def _handle_event(self, event: BellEvent) -> None:
        _execute_bell_event(
            self.config,
            self.audio,
            self.notifier,
            event,
            self._play_recess_music,
            self._run_shutdown,
        )

    def _play_recess_music(self) -> None:
        path = self.config.sound_files.get("recess_music")
        if not path:
            return
        if self._recess_thread and self._recess_thread.is_alive():
            return

        def worker() -> None:
            start = time.time()
            duration = 5 * 60
            while time.time() - start < duration and self._running:
                self.audio.play_file(path, "Teneffüs Müziği")
                time.sleep(1)

        self._recess_thread = threading.Thread(target=worker, daemon=True)
        self._recess_thread.start()

    def _run_shutdown(self) -> None:
        mode = self.config.auto_shutdown_mode or ("time" if self.config.auto_shutdown_enabled else "disabled")
        if mode == "disabled":
            return
        self.notifier.notify("JinniBell Pro", "Servis modunda otomatik kapanış başlatılıyor")
        if os.name == "nt":
            subprocess.Popen(["shutdown", "/s", "/t", "0"])
        else:
            subprocess.Popen(["shutdown", "-h", "now"])


class BellApplication:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("JinniBell Pro")
        self._init_window_size()
        self.ui_font_family = self._init_default_font()
        self.config = BellConfig.load()
        self.theme_var = tk.StringVar(value=self.config.theme_mode)
        self.touch_mode_var = tk.BooleanVar(value=self.config.touch_mode)
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        self._palette: Dict[str, str] = {}
        self._setup_styles()
        self.audio = AudioController()
        self.audio.set_state_callback(self._update_status)
        self.audio.set_error_callback(self._on_audio_error)
        self.notifier = Notifier()
        self.tray = TrayController(self)
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
        self._tooltips: List[ToolTip] = []
        self._announcement_vars: Dict[str, Dict[str, tk.Variable]] = {}
        self._last_audio_error = ""
        self._last_audio_error_time = 0.0
        self._tray_hint_shown = False
        self.queue_now_var = tk.StringVar(value="Hazır")
        self.queue_next_var = tk.StringVar(value="Sonraki zil hesaplanıyor")
        self.ceremony_now_var = tk.StringVar(value="Tören listesi beklemede")
        self.ceremony_next_var = tk.StringVar(value="Sırada tören parçası yok")
        self.stage_now_var = tk.StringVar(value="Sahne modu hazır")
        self.stage_next_var = tk.StringVar(value="Sırada parça yok")
        self._current_ceremony_zones: List[str] = []

        self.scheduler = ScheduleRunner(
            self.config,
            self._handle_event,
            lambda: self.manual_override or self.bells_paused,
        )
        self.scheduler.start()

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close_request)
        self._schedule_countdown_refresh()
        self.root.after(1200, self._auto_minimize_if_needed)

    # region UI
    def _init_window_size(self) -> None:
        try:
            self.root.update_idletasks()
            screen_w = self.root.winfo_screenwidth() or 1366
            screen_h = self.root.winfo_screenheight() or 768
            target_w = max(960, min(1180, int(screen_w * 0.7)))
            target_h = max(620, min(860, int(screen_h * 0.75)))
            self.root.geometry(f"{target_w}x{target_h}")
            self.root.minsize(900, 600)
        except tk.TclError:
            pass

    def _setup_styles(self) -> None:
        palette = self._get_palette(self.theme_var.get())
        self._palette = palette
        primary = palette["primary"]
        accent = palette["accent"]
        surface = palette["surface"]
        canvas = palette["canvas"]
        muted = palette["muted"]
        text = palette["text"]
        table_sel = palette["table_sel"]
        try:
            self.root.configure(background=canvas)
        except tk.TclError:
            pass

        style = ttk.Style(self.root)
        pad_base = 10 if self.touch_mode_var.get() else 6
        font_size = 11 if self.touch_mode_var.get() else 10

        style.configure("TFrame", background=canvas)
        style.configure("App.TFrame", background=canvas)
        style.configure("Card.TFrame", background=surface, relief=tk.GROOVE, borderwidth=0)
        style.configure("Card.TLabelframe", background=surface, borderwidth=0, padding=12)
        style.configure("Card.TLabelframe.Label", background=surface, font=(self.ui_font_family, font_size, "bold"))
        style.configure("Muted.TLabel", background=surface, foreground=muted)
        style.configure("Accent.TLabel", background=surface, foreground=accent, font=(self.ui_font_family, font_size + 1, "bold"))
        style.configure("Bold.TLabel", font=(self.ui_font_family, font_size, "bold"))
        style.configure("TLabel", foreground=text)
        style.configure("TButton", padding=(pad_base + 1, pad_base - 2), font=(self.ui_font_family, font_size))
        style.map(
            "TButton",
            background=[("active", palette["button_active"])],
            relief=[("pressed", "sunken")],
        )
        style.configure(
            "Primary.TButton",
            padding=(pad_base + 4, pad_base - 1),
            background=primary,
            foreground="white",
            borderwidth=0,
            focusthickness=3,
            focustcolor=primary,
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
            foreground=[("disabled", "#e5e7eb")],
        )
        style.configure(
            "Success.TButton",
            padding=(12, 8),
            background="#16a34a",
            foreground="white",
            borderwidth=0,
        )
        style.map(
            "Success.TButton",
            background=[("active", "#15803d"), ("pressed", "#166534")],
            foreground=[("disabled", "#e5e7eb")],
        )
        style.configure(
            "Danger.TButton",
            padding=(12, 8),
            background="#dc2626",
            foreground="white",
            borderwidth=0,
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#b91c1c"), ("pressed", "#991b1b")],
            foreground=[("disabled", "#e5e7eb")],
        )
        style.configure("TNotebook", background=canvas, tabmargins=(6, 4, 6, 0))
        style.configure("TNotebook.Tab", padding=(10, 6), font=(self.ui_font_family, font_size, "bold"))
        style.configure(
            "Treeview",
            background=surface,
            fieldbackground=surface,
            bordercolor=palette["divider"],
            relief="flat",
        )
        style.map("Treeview", background=[("selected", table_sel)])
        row_height = 30 if self.touch_mode_var.get() else 26
        style.configure("Treeview", rowheight=row_height)
        style.configure("Treeview.Heading", font=(self.ui_font_family, font_size, "bold"))

    def _get_palette(self, mode: str) -> Dict[str, str]:
        if mode == "dark":
            return {
                "primary": "#60a5fa",
                "accent": "#e5e7eb",
                "surface": "#111827",
                "canvas": "#0b1220",
                "muted": "#9ca3af",
                "text": "#e5e7eb",
                "divider": "#1f2937",
                "button_active": "#1f2937",
                "table_sel": "#1e3a8a",
            }
        if mode == "minimal":
            return {
                "primary": "#2563eb",
                "accent": "#0f172a",
                "surface": "#fbfbfc",
                "canvas": "#f6f8fb",
                "muted": "#6b7280",
                "text": "#0f172a",
                "divider": "#e5e7eb",
                "button_active": "#e2e8f0",
                "table_sel": "#e0e7ff",
            }
        return {
            "primary": "#2563eb",
            "accent": "#111827",
            "surface": "#ffffff",
            "canvas": "#f5f7fb",
            "muted": "#6b7280",
            "text": "#111827",
            "divider": "#e5e7eb",
            "button_active": "#e5e7eb",
            "table_sel": "#dbeafe",
        }

    def _init_default_font(self) -> str:
        preferred = "Segoe UI"
        fallback = "Arial"
        try:
            default_font = tkfont.nametofont("TkDefaultFont")
            fallback = default_font.cget("family") or fallback
        except tk.TclError:
            pass

        try:
            families = {name.lower(): name for name in tkfont.families()}
        except tk.TclError:
            families = {}

        chosen = preferred
        if preferred.lower() not in families and not _is_windows():
            if fallback.lower() in families:
                chosen = families[fallback.lower()]
            else:
                chosen = fallback
        elif preferred.lower() in families:
            chosen = families[preferred.lower()]

        spec = self._font_string(chosen, 10)
        try:
            self.root.option_add("*Font", spec)
        except tk.TclError:
            backup = self._font_string(fallback, 10)
            self.root.option_add("*Font", backup)
            chosen = fallback
        return chosen

    @staticmethod
    def _font_string(family: str, size: int, weight: str | None = None, slant: str | None = None) -> str:
        safe_family = family
        if " " in safe_family and not safe_family.startswith("{"):
            safe_family = f"{{{safe_family}}}"
        parts = [safe_family, str(size)]
        if weight:
            parts.append(weight)
        if slant:
            parts.append(slant)
        return " ".join(parts)

    def _build_ui(self) -> None:
        shell = ttk.Frame(self.root, padding=12, style="App.TFrame")
        shell.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(shell)
        notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook = notebook

        control_frame = ttk.Frame(notebook, style="App.TFrame", padding=6)
        schedule_frame = ttk.Frame(notebook, style="App.TFrame", padding=6)
        sound_frame = ttk.Frame(notebook, style="App.TFrame", padding=6)
        ceremony_frame = ttk.Frame(notebook, style="App.TFrame", padding=6)

        notebook.add(control_frame, text="Kontrol")
        notebook.add(schedule_frame, text="Ders Programı")
        notebook.add(sound_frame, text="Ses Ayarları")
        notebook.add(ceremony_frame, text="Tören")

        self._tabs = {
            "control": control_frame,
            "schedule": schedule_frame,
            "sound": sound_frame,
            "ceremony": ceremony_frame,
        }

        self._build_control_tab(control_frame)
        self._build_schedule_tab(schedule_frame)
        self._build_sound_tab(sound_frame)
        self._build_ceremony_tab(ceremony_frame)
        self._refresh_holidays()

    def _switch_tab(self, name: str) -> None:
        if hasattr(self, "notebook") and hasattr(self, "_tabs") and name in self._tabs:
            self.notebook.select(self._tabs[name])

    def _add_hint(self, widget: tk.Widget, text: str) -> None:
        self._tooltips.append(ToolTip(widget, text))

    def _build_control_tab(self, frame: ttk.Frame) -> None:
        header = ttk.Frame(frame, style="App.TFrame")
        header.pack(fill=tk.X, padx=6, pady=(2, 4))
        ttk.Label(header, text="Kontrol Paneli", style="Accent.TLabel").pack(side=tk.LEFT)
        ttk.Label(header, text="Günlük işlemleri tek ekrandan yönetebilirsiniz.", style="Muted.TLabel").pack(
            side=tk.LEFT, padx=8
        )
        ttk.Combobox(
            header,
            state="readonly",
            width=12,
            textvariable=self.theme_var,
            values=["light", "dark", "minimal"],
        ).pack(side=tk.RIGHT, padx=4)
        self.theme_var.trace_add("write", lambda *_a: self._toggle_theme())
        ttk.Checkbutton(
            header,
            text="🤏 Dokunmatik Mod",
            variable=self.touch_mode_var,
            command=self._toggle_touch_mode,
        ).pack(side=tk.RIGHT, padx=4)

        shortcut = ttk.LabelFrame(frame, text="Kısayol Şeridi", style="Card.TLabelframe")
        shortcut.pack(fill=tk.X, padx=6, pady=6)
        bar = ttk.Frame(shortcut, style="Card.TFrame")
        bar.pack(fill=tk.X)
        btn_width = 14
        ttk.Button(bar, text="📅 Ders Programı", command=lambda: self._switch_tab("schedule"), width=btn_width).pack(
            side=tk.LEFT, padx=3, pady=3
        )
        ttk.Button(bar, text="🎵 Ses Ayarları", command=lambda: self._switch_tab("sound"), width=btn_width).pack(
            side=tk.LEFT, padx=3, pady=3
        )
        ttk.Button(bar, text="▶ Zil Simülasyonu", command=self._start_simulation, width=btn_width).pack(
            side=tk.LEFT, padx=3, pady=3
        )
        ttk.Button(bar, text="🔇 Sustur / Aç", command=self._flip_mute_from_shortcut, width=btn_width - 2).pack(
            side=tk.RIGHT, padx=3, pady=3
        )
        ttk.Button(bar, text="⏸ Tören Modu", command=self._toggle_pause_from_button, width=btn_width - 2).pack(
            side=tk.RIGHT, padx=3, pady=3
        )

        button_frame = ttk.LabelFrame(frame, text="Hızlı Tören Kısayolları", style="Card.TLabelframe")
        button_frame.pack(fill=tk.X, padx=6, pady=4)
        grid = ttk.Frame(button_frame, style="Card.TFrame")
        grid.pack(fill=tk.X)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        for idx, (label, key) in enumerate(MANUAL_BUTTONS.items()):
            btn = ttk.Button(
                grid,
                text=label,
                style="Primary.TButton" if idx == 0 else "TButton",
                command=lambda k=key: self._trigger_manual(k),
            )
            row, col = divmod(idx, 2)
            btn.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
            hint = (
                "Seçtiğiniz tören sesleri öncelikli çalar. 1 dk/2 dk butonları 'Saygı Duruşu' "
                "dosyasını kullanır, boşsa sessiz bekler."
            )
            self._add_hint(btn, hint)

        delay_row = ttk.Frame(button_frame, style="Card.TFrame")
        delay_row.pack(fill=tk.X, padx=4, pady=(6, 0))
        ttk.Label(delay_row, text="Başlatma süresi:").pack(side=tk.LEFT)
        self.manual_delay_var = tk.StringVar(value=MANUAL_DELAY_CHOICES[0][0])
        delay_combo = ttk.Combobox(
            delay_row,
            state="readonly",
            textvariable=self.manual_delay_var,
            values=[label for label, _ in MANUAL_DELAY_CHOICES],
            width=12,
        )
        delay_combo.pack(side=tk.LEFT, padx=6)
        self._add_hint(delay_combo, "Tören butonunun kaç saniye sonra devreye gireceğini seçin.")
        ttk.Label(delay_row, text="(Tören butonları için)", style="Muted.TLabel").pack(side=tk.LEFT)

        status_frame = ttk.Frame(frame, style="App.TFrame")
        status_frame.pack(fill=tk.X, padx=6, pady=(6, 2))
        ttk.Label(status_frame, text="Durum:", style="Bold.TLabel").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)

        countdown_frame = ttk.LabelFrame(frame, text="Geri Sayım ve Bildirim", style="Card.TLabelframe")
        countdown_frame.pack(fill=tk.X, padx=6, pady=4)
        self.countdown_var = tk.StringVar(value="Sonraki zil hesaplanıyor...")
        default_bg = self._palette.get(
            "surface", ttk.Style(self.root).lookup("Card.TLabelframe", "background")
        )
        tk.Label(
            countdown_frame,
            textvariable=self.countdown_var,
            font=(self.ui_font_family, 12, "bold"),
            fg="#0b5394",
            bg=default_bg,
            wraplength=540,
        ).pack(fill=tk.X, padx=6, pady=4)
        self.pause_badge = ttk.Button(
            countdown_frame,
            text="Tören modu kapalı",
            style="Success.TButton",
            command=self._toggle_pause_from_button,
        )
        self.pause_badge.pack(fill=tk.X, padx=6, pady=(0, 6))

        queue_frame = ttk.LabelFrame(frame, text="Şimdi / Sıradaki Kuyruk", style="Card.TLabelframe")
        queue_frame.pack(fill=tk.X, padx=6, pady=4)
        row1 = ttk.Frame(queue_frame, style="Card.TFrame")
        row1.pack(fill=tk.X, padx=4, pady=2)
        ttk.Label(row1, text="Aktif Zil / Tören:", style="Bold.TLabel").pack(side=tk.LEFT)
        ttk.Label(row1, textvariable=self.queue_now_var).pack(side=tk.LEFT, padx=6)
        ttk.Label(row1, textvariable=self.ceremony_now_var, style="Muted.TLabel").pack(side=tk.RIGHT)
        row2 = ttk.Frame(queue_frame, style="Card.TFrame")
        row2.pack(fill=tk.X, padx=4, pady=2)
        ttk.Label(row2, text="Sıradaki Zil:", style="Bold.TLabel").pack(side=tk.LEFT)
        ttk.Label(row2, textvariable=self.queue_next_var).pack(side=tk.LEFT, padx=6)
        ttk.Label(row2, textvariable=self.ceremony_next_var, style="Muted.TLabel").pack(side=tk.RIGHT)

        volume_frame = ttk.LabelFrame(frame, text="Ses", style="Card.TLabelframe")
        volume_frame.pack(fill=tk.X, padx=6, pady=4)
        self.volume_var = tk.DoubleVar(value=self.config.volume)
        self.volume_percent_var = tk.StringVar(value=self._format_volume_percent(self.config.volume))
        slider = ttk.Scale(
            volume_frame,
            from_=0,
            to=1,
            orient=tk.HORIZONTAL,
            variable=self.volume_var,
            command=lambda _: self._change_volume(),
        )
        slider.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(volume_frame, textvariable=self.volume_percent_var, anchor=tk.E).pack(fill=tk.X, padx=6, pady=(0, 4))
        self._add_hint(slider, "Zil sesini yüzde cinsinden ayarlar.")

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

        startup_frame = ttk.LabelFrame(frame, text="Başlangıç / Arka Plan", style="Card.TLabelframe")
        startup_frame.pack(fill=tk.X, padx=6, pady=4)
        self.autostart_var = tk.BooleanVar(value=self.config.launch_on_boot)
        autostart_chk = ttk.Checkbutton(
            startup_frame,
            text="Windows açıldığında JinniBell Pro otomatik başlasın (sisteme küçült)",
            variable=self.autostart_var,
            command=self._toggle_autostart,
        )
        autostart_chk.pack(fill=tk.X, padx=6, pady=(4, 2))
        self._add_hint(autostart_chk, "Oturum açıldığında programı arka plana gönderir.")
        self.service_autostart_var = tk.BooleanVar(value=self.config.launch_on_boot_service)
        service_chk = ttk.Checkbutton(
            startup_frame,
            text="Windows açılır açılmaz (Görev Zamanlayıcı ile) servis modunda başlat",
            variable=self.service_autostart_var,
            command=self._toggle_service_autostart,
        )
        service_chk.pack(fill=tk.X, padx=6, pady=2)
        self._add_hint(
            service_chk,
            "Görev Zamanlayıcı kaydı oluşturur. Yönetici izinleri gerekebilir ve program arayüz göstermeden çalışır.",
        )
        ttk.Label(
            startup_frame,
            text="Her iki seçenek birlikte kullanılabilir. Servis modu arayüzü açmadan yalnızca zilleri çalıştırır.",
            wraplength=360,
        ).pack(fill=tk.X, padx=6, pady=(0, 4))

        bottom_actions = ttk.Frame(frame, style="App.TFrame")
        bottom_actions.pack(fill=tk.X, padx=6, pady=4)
        ttk.Button(bottom_actions, text="Arka Plana Al", command=self._minimize_to_tray, width=16).pack(
            side=tk.LEFT, padx=3, pady=2
        )
        ttk.Button(bottom_actions, text="Programı Kapat", command=self._cleanup_and_exit, width=16).pack(
            side=tk.RIGHT, padx=3, pady=2
        )

        shutdown_frame = ttk.LabelFrame(frame, text="Otomatik Kapatma", style="Card.TLabelframe")
        shutdown_frame.pack(fill=tk.X, padx=6, pady=4)
        mode_label = self._get_shutdown_mode_label(
            self.config.auto_shutdown_mode or ("time" if self.config.auto_shutdown_enabled else "disabled")
        )
        self.shutdown_mode_var = tk.StringVar(value=mode_label)
        ttk.Label(shutdown_frame, text="Kural:").grid(row=0, column=0, padx=4, pady=4, sticky=tk.W)
        mode_combo = ttk.Combobox(
            shutdown_frame,
            state="readonly",
            values=[label for label, _ in SHUTDOWN_MODES],
            textvariable=self.shutdown_mode_var,
            width=22,
        )
        mode_combo.grid(row=0, column=1, padx=4, pady=4, sticky=tk.W)
        mode_combo.bind("<<ComboboxSelected>>", lambda _e: self._apply_shutdown_settings())
        self._add_hint(mode_combo, "Belirli saatte veya son zil sonrası otomatik kapanışı seçin.")

        ttk.Label(shutdown_frame, text="Saat:").grid(row=1, column=0, padx=4, pady=2, sticky=tk.W)
        self.shutdown_time_var = tk.StringVar(value=self.config.auto_shutdown_time or "20:00")
        self.shutdown_entry = ttk.Entry(shutdown_frame, textvariable=self.shutdown_time_var, width=10)
        self.shutdown_entry.grid(row=1, column=1, padx=4, pady=2, sticky=tk.W)
        self.shutdown_entry.bind("<FocusOut>", lambda _e: self._apply_shutdown_settings())
        self._attach_time_validation(self.shutdown_entry, self.shutdown_time_var)

        ttk.Label(shutdown_frame, text="Son zil sonrası (dk):").grid(row=2, column=0, padx=4, pady=2, sticky=tk.W)
        self.shutdown_delay_var = tk.IntVar(value=int(self.config.auto_shutdown_delay_minutes or 10))
        self.shutdown_delay_spin = ttk.Spinbox(
            shutdown_frame, from_=1, to=120, textvariable=self.shutdown_delay_var, width=8
        )
        self.shutdown_delay_spin.grid(row=2, column=1, padx=4, pady=2, sticky=tk.W)
        self.shutdown_delay_spin.bind("<FocusOut>", lambda _e: self._apply_shutdown_settings())
        self.shutdown_delay_spin.bind("<Return>", lambda _e: self._apply_shutdown_settings())

        ttk.Label(
            shutdown_frame,
            text="'Son zil' modu seçiliyse belirtilen dakika dolunca bilgisayar kapanır.",
            foreground="#555",
            wraplength=360,
        ).grid(row=3, column=0, columnspan=2, padx=4, pady=(2, 4), sticky=tk.W)

        self._update_shutdown_inputs()

        today_frame = ttk.LabelFrame(frame, text="Bugünkü Ziller", style="Card.TLabelframe")
        today_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.today_list = tk.Listbox(today_frame)
        self.today_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._refresh_today()

        ttk.Label(
            frame,
            text="© 2026 Emre Esen tarafından kodlandı",
            font=(self.ui_font_family, 9, "italic"),
        ).pack(anchor=tk.W, padx=12, pady=(0, 10))
        self._update_pause_badge()

    def _build_schedule_tab(self, frame: ttk.Frame) -> None:
        container = ttk.Frame(frame)
        container.pack(fill=tk.BOTH, expand=True)

        calendar_panel = ttk.LabelFrame(container, text="Aylık Takvim", style="Card.TLabelframe")
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

        filter_row = ttk.Frame(right_panel)
        filter_row.pack(fill=tk.X, pady=(2, 4))
        ttk.Label(filter_row, text="Filtre", style="Bold.TLabel").pack(side=tk.LEFT, padx=(0, 4))
        self.schedule_filter_var = tk.StringVar()
        self.schedule_filter_var.trace_add("write", lambda *_: self._refresh_event_list())
        search = ttk.Entry(filter_row, textvariable=self.schedule_filter_var, width=18)
        search.pack(side=tk.LEFT, padx=2)
        self.schedule_filter_sound_var = tk.StringVar(value="Tümü")
        self.schedule_filter_sound_var.trace_add("write", lambda *_: self._refresh_event_list())
        ttk.Combobox(
            filter_row,
            state="readonly",
            width=16,
            textvariable=self.schedule_filter_sound_var,
            values=["Tümü"] + [choice[0] for choice in SCHEDULE_SOUND_CHOICES],
        ).pack(side=tk.LEFT, padx=6)
        self.schedule_count_var = tk.StringVar(value="")
        ttk.Label(filter_row, textvariable=self.schedule_count_var, style="Muted.TLabel").pack(side=tk.RIGHT)

        table_frame = ttk.Frame(right_panel)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(4, 8))
        columns = ("clock", "label", "sound")
        self.event_list = ttk.Treeview(table_frame, columns=columns, show="headings", height=11, selectmode="browse")
        self.event_list.heading("clock", text="Saat")
        self.event_list.heading("label", text="Başlık")
        self.event_list.heading("sound", text="Kategori")
        self.event_list.column("clock", width=72, anchor=tk.CENTER)
        self.event_list.column("label", anchor=tk.W, stretch=True)
        self.event_list.column("sound", width=120, anchor=tk.CENTER)
        self.event_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.event_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.event_list.configure(yscrollcommand=scrollbar.set)
        self.event_list.tag_configure("student_entry", background="#edf7ff")
        self.event_list.tag_configure("teacher_entry", background="#f9f0ff")
        self.event_list.tag_configure("lesson_exit", background="#fff7ed")
        self.event_list.bind("<<TreeviewSelect>>", self._on_schedule_select)

        quick_frame = ttk.LabelFrame(right_panel, text="Tablo Halinde Zil Girişi", style="Card.TLabelframe")
        quick_frame.pack(fill=tk.X, padx=12, pady=(4, 6))
        ttk.Label(
            quick_frame,
            text="Aşağıdaki tablo 1. dersten 16. derse kadar tüm öğrenci/öğretmen giriş ve ders çıkışlarını"
            " aynı anda düzenlemenizi sağlar.",
            wraplength=460,
        ).pack(anchor=tk.W, padx=6, pady=(4, 2))
        ttk.Label(
            quick_frame,
            text="HH:MM formatında saat girin. Bir hücre boş bırakılırsa o olay o gün için eklenmez.",
            foreground="#555",
        ).pack(anchor=tk.W, padx=6, pady=(0, 4))

        header_row = ttk.Frame(quick_frame)
        header_row.pack(fill=tk.X, padx=6)
        ttk.Label(header_row, text="Menü", width=10).grid(row=0, column=0, padx=4, sticky=tk.W)
        for idx, (title, _key) in enumerate(
            [("Öğrenci Girişi", "student_entry"), ("Öğretmen Girişi", "teacher_entry"), ("Ders Çıkışı", "lesson_exit")]
        ):
            ttk.Label(header_row, text=title, width=14).grid(row=0, column=idx + 1, padx=6)

        self._table_rows: List[Dict[str, object]] = []
        self.table_rows_frame = ttk.Frame(quick_frame)
        self.table_rows_frame.pack(fill=tk.X, padx=6, pady=(2, 4))
        for _ in range(TABLE_DEFAULT_ROWS):
            self._add_schedule_table_row()

        quick_btns = ttk.Frame(quick_frame)
        quick_btns.pack(fill=tk.X, padx=6, pady=(2, 4))
        ttk.Button(quick_btns, text="Tabloyu Temizle", command=self._clear_schedule_table).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_btns, text="Günü Tabloya Aktar", command=self._load_day_into_table).pack(
            side=tk.RIGHT, padx=2
        )
        ttk.Button(quick_btns, text="Tabloyu Güne Kaydet", command=self._apply_table_to_day).pack(
            side=tk.RIGHT, padx=2
        )

        row_control = ttk.Frame(quick_frame)
        row_control.pack(fill=tk.X, padx=6, pady=(0, 4))
        ttk.Label(row_control, text="Ders sayısı").pack(side=tk.LEFT)
        self.table_row_target = tk.IntVar(value=TABLE_DEFAULT_ROWS)
        row_spin = ttk.Spinbox(
            row_control,
            from_=4,
            to=TABLE_MAX_ROWS,
            textvariable=self.table_row_target,
            width=5,
            command=self._sync_schedule_table_rows,
        )
        row_spin.pack(side=tk.LEFT, padx=4)
        row_spin.bind("<FocusOut>", lambda _e: self._sync_schedule_table_rows())
        row_spin.bind("<Return>", lambda _e: self._sync_schedule_table_rows())
        self._add_hint(row_spin, "Tabloda kaç ders satırı olacağını belirler.")
        ttk.Label(row_control, text="(Tabloyu kaydetmeden önce satır sayısını ayarlayın)", foreground="#555").pack(
            side=tk.LEFT, padx=6
        )

        form = ttk.LabelFrame(right_panel, text="Yeni/Seçili Zil", style="Card.TLabelframe")
        form.pack(fill=tk.X, padx=12, pady=8)
        self.hour_var = tk.StringVar(value="08")
        self.minute_var = tk.StringVar(value="00")
        ttk.Label(form, text="Saat").grid(row=0, column=0, padx=4, pady=4, sticky=tk.W)
        hour_spin = ttk.Spinbox(form, from_=0, to=23, textvariable=self.hour_var, width=5, wrap=True, format="%02.0f")
        hour_spin.grid(row=1, column=0, padx=4, pady=2)
        ttk.Label(form, text=":").grid(row=1, column=1)
        minute_spin = ttk.Spinbox(form, from_=0, to=59, textvariable=self.minute_var, width=5, wrap=True, format="%02.0f")
        minute_spin.grid(row=1, column=2, padx=4, pady=2)
        adjust = ttk.Frame(form)
        adjust.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=2, pady=(0, 4))
        ttk.Button(adjust, text="+5 dk", width=7, command=lambda: self._nudge_time(5)).pack(side=tk.LEFT, padx=2)
        ttk.Button(adjust, text="-5 dk", width=7, command=lambda: self._nudge_time(-5)).pack(side=tk.LEFT, padx=2)
        ttk.Button(adjust, text="Şimdi", width=6, command=self._set_current_time).pack(side=tk.LEFT, padx=2)

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

        copy_frame = ttk.LabelFrame(right_panel, text="Program Kopyala", style="Card.TLabelframe")
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

        holiday_frame = ttk.LabelFrame(right_panel, text="Tatil Günleri", style="Card.TLabelframe")
        holiday_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        self.holiday_list = tk.Listbox(holiday_frame, height=5)
        self.holiday_list.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        holiday_btns = ttk.Frame(holiday_frame)
        holiday_btns.pack(fill=tk.X, padx=6, pady=6)
        ttk.Button(holiday_btns, text="Ekle", command=self._add_holiday).pack(side=tk.LEFT, padx=5)
        ttk.Button(holiday_btns, text="Sil", command=self._remove_holiday).pack(side=tk.LEFT, padx=5)

        simulation = ttk.LabelFrame(right_panel, text="Zil Testi Simülasyonu", style="Card.TLabelframe")
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
        self._load_day_into_table()

    def _build_sound_tab(self, frame: ttk.Frame) -> None:
        intro = ttk.LabelFrame(frame, text="Ses Motoru Hazırlığı", style="Card.TLabelframe")
        intro.pack(fill=tk.X, padx=8, pady=(6, 6))
        ttk.Label(
            intro,
            text=(
                "FFmpeg/ffplay ve SDL2.dll eksiksiz bulunduğunda testler sorunsuz çalışır."
                " Aşağıdaki göstergeden durumu takip edip talimatlarla manuel kopya yapabilirsiniz."
            ),
            foreground="#4b5563",
            wraplength=620,
        ).pack(anchor=tk.W, padx=8, pady=(6, 4))
        self.audio_status_var = tk.StringVar(value=self._describe_audio_dependencies())
        ttk.Label(intro, textvariable=self.audio_status_var, foreground="#0f172a", wraplength=640).pack(
            anchor=tk.W, padx=8, pady=(0, 6)
        )
        status_row = ttk.Frame(intro)
        status_row.pack(fill=tk.X, padx=8, pady=(0, 6))
        ttk.Button(status_row, text="Durumu Yenile", command=self._refresh_audio_status, width=16).pack(
            side=tk.LEFT, padx=(0, 6)
        )
        ttk.Button(status_row, text="Adım Adım Talimat", command=self._show_ffmpeg_help, width=18).pack(side=tk.LEFT)
        self._route_labels: Dict[str, tk.StringVar] = {}
        self._build_zone_manager(frame)
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
        self._seed_library_from_config()
        self._refresh_sound_library()

    def _describe_audio_dependencies(self) -> str:
        parts = []
        if audio.FFMPEG_PATH and Path(audio.FFMPEG_PATH).exists():
            parts.append(f"ffmpeg: {audio.FFMPEG_PATH}")
        else:
            parts.append("ffmpeg: bulunamadı")
        if audio.FFPROBE_PATH and Path(audio.FFPROBE_PATH).exists():
            parts.append(f"ffprobe: {audio.FFPROBE_PATH}")
        else:
            parts.append("ffprobe: bulunamadı")
        dep_err = audio._ffplay_dependency_error()
        if dep_err:
            parts.append(dep_err)
        elif audio.FFPLAY_PATH:
            parts.append(f"ffplay: {audio.FFPLAY_PATH}")
        runtime_root = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
        ffmpeg_dir = runtime_root / "ffmpeg"
        parts.append(f"Klasör: {ffmpeg_dir}")
        return " \u2022 ".join(parts)

    def _refresh_audio_status(self) -> None:
        audio._configure_external_binaries()
        self.audio_status_var.set(self._describe_audio_dependencies())

    def _show_ffmpeg_help(self) -> None:
        guide = audio._dependency_hint(FileNotFoundError())
        messagebox.showinfo(
            "FFmpeg / ffplay",
            (
                "Ses oynatımı için gereken bileşenler eksikse aşağıdaki adımları izleyin:\n\n"
                "- ffmpeg klasöründe ffmpeg.exe, ffprobe.exe, ffplay.exe ve SDL2.dll bulunduğundan emin olun.\n"
                "- packaging/ffmpeg-bin içeriğini derlenen exe'nin yanına 'ffmpeg' klasörü olarak kopyalayın.\n"
                "- Çevrimdışı arşivler için 'ffmpeg-offline.zip' ve 'sdl2-offline.zip' dosyalarını packaging klasörüne koyup"
                " build_exe'yi yeniden çalıştırabilirsiniz.\n\n"
                f"Durum: {self._describe_audio_dependencies()}\n\n"
                f"İpucu:\n{guide}"
            ),
        )

    def _build_zone_manager(self, frame: ttk.Frame) -> None:
        zone_frame = ttk.LabelFrame(frame, text="Uzamsal Ses Bölgeleri", style="Card.TLabelframe")
        zone_frame.pack(fill=tk.X, padx=8, pady=(0, 6))
        ttk.Label(
            zone_frame,
            text="Ses çıkışlarını kat, bina veya alanlara göre gruplayıp her zili ilgili bölgelere yönlendirebilirsiniz.",
            foreground="#555",
            wraplength=560,
        ).pack(anchor=tk.W, padx=6, pady=(4, 2))
        columns = ("name", "status", "note")
        self.zone_tree = ttk.Treeview(zone_frame, columns=columns, show="headings", height=4)
        self.zone_tree.heading("name", text="Bölge")
        self.zone_tree.heading("status", text="Durum")
        self.zone_tree.heading("note", text="Not")
        self.zone_tree.column("name", width=140, anchor=tk.W)
        self.zone_tree.column("status", width=80, anchor=tk.CENTER)
        self.zone_tree.column("note", anchor=tk.W)
        self.zone_tree.pack(fill=tk.X, padx=6, pady=(0, 2))
        btns = ttk.Frame(zone_frame)
        btns.pack(fill=tk.X, padx=6, pady=(0, 4))
        ttk.Button(btns, text="Bölge Ekle", command=self._add_zone_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="Düzenle", command=self._edit_zone_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="Aç/Kapat", command=self._toggle_zone_enable).pack(side=tk.LEFT, padx=2)
        self._refresh_zone_tree()

    def _refresh_zone_tree(self) -> None:
        if not hasattr(self, "zone_tree"):
            return
        for item in self.zone_tree.get_children():
            self.zone_tree.delete(item)
        for zone in self.config.sound_zones:
            status = "Açık" if zone.get("enabled", True) else "Kapalı"
            self.zone_tree.insert(
                "",
                tk.END,
                iid=zone.get("zone_id"),
                values=(zone.get("name", "Bölge"), status, zone.get("note", "")),
            )
        for key, label_var in self._route_labels.items():
            label_var.set(self._format_zone_summary(key))

    def _add_zone_dialog(self) -> None:
        name = simpledialog.askstring("Yeni Bölge", "Bölge adı", parent=self.root)
        if not name:
            return
        note = simpledialog.askstring("Not", "Kısa açıklama (opsiyonel)", parent=self.root) or ""
        new_zone = {
            "zone_id": uuid4().hex,
            "name": name,
            "color": "#2563eb",
            "enabled": True,
            "note": note,
        }
        self.config.sound_zones.append(new_zone)
        self.config.save()
        self._refresh_zone_tree()

    def _get_selected_zone_id(self) -> Optional[str]:
        selection = getattr(self, "zone_tree", None)
        if not selection:
            return None
        picked = selection.selection()
        if not picked:
            return None
        return picked[0]

    def _edit_zone_dialog(self) -> None:
        zone_id = self._get_selected_zone_id()
        if not zone_id:
            messagebox.showinfo("Bölge", "Önce düzenlemek için bir satır seçin")
            return
        for zone in self.config.sound_zones:
            if zone.get("zone_id") == zone_id:
                current_name = zone.get("name", "Bölge")
                new_name = simpledialog.askstring("Bölge Adı", "Yeni ad", initialvalue=current_name, parent=self.root)
                if new_name:
                    zone["name"] = new_name
                new_note = simpledialog.askstring("Not", "Açıklama", initialvalue=zone.get("note", ""), parent=self.root)
                if new_note is not None:
                    zone["note"] = new_note
                break
        self.config.save()
        self._refresh_zone_tree()

    def _toggle_zone_enable(self) -> None:
        zone_id = self._get_selected_zone_id()
        if not zone_id:
            messagebox.showinfo("Bölge", "Lütfen aç/kapat için bir satır seçin")
            return
        for zone in self.config.sound_zones:
            if zone.get("zone_id") == zone_id:
                zone["enabled"] = not zone.get("enabled", True)
                break
        self.config.save()
        self._refresh_zone_tree()

    def _pick_ceremony_zones(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Bölge Seç")
        dialog.transient(self.root)
        dialog.grab_set()
        ttk.Label(dialog, text="Parçanın çalacağı bölgeleri işaretleyin").pack(padx=12, pady=6)
        vars: List[tuple[str, tk.BooleanVar]] = []
        for zone in self.config.sound_zones:
            var = tk.BooleanVar(value=zone.get("zone_id") in self._current_ceremony_zones)
            ttk.Checkbutton(dialog, text=zone.get("name", "Bölge"), variable=var).pack(
                anchor=tk.W, padx=14, pady=2
            )
            vars.append((zone.get("zone_id"), var))

        def _apply() -> None:
            self._current_ceremony_zones = [zone_id for zone_id, var in vars if var.get()]
            self.ceremony_zone_label.set(
                ", ".join(self._current_ceremony_zones) if self._current_ceremony_zones else "Genel"
            )
            dialog.destroy()

        btn_row = ttk.Frame(dialog)
        btn_row.pack(fill=tk.X, padx=12, pady=(6, 10))
        ttk.Button(btn_row, text="Kaydet", command=_apply).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_row, text="Vazgeç", command=dialog.destroy).pack(side=tk.RIGHT, padx=4)

    def _format_zone_summary(self, sound_key: str) -> str:
        routes = self.config.sound_routes.get(sound_key) or ["main"]
        names = []
        for zone_id in routes:
            zone = next((z for z in self.config.sound_zones if z.get("zone_id") == zone_id), None)
            names.append(zone.get("name") if zone else zone_id)
        if not names:
            return "Bölge atanmadı"
        return f"Bölgeler: {', '.join(names)}"

    def _open_route_dialog(self, sound_key: str, title: str) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{title} için bölgeler")
        dialog.transient(self.root)
        dialog.grab_set()
        ttk.Label(dialog, text="Bu zil hangi bölgelere gitsin?", style="Bold.TLabel").pack(padx=12, pady=8)
        vars: List[tuple[str, tk.BooleanVar]] = []
        current = set(self.config.sound_routes.get(sound_key) or [])
        for zone in self.config.sound_zones:
            var = tk.BooleanVar(value=zone.get("zone_id") in current)
            ttk.Checkbutton(dialog, text=zone.get("name", "Bölge"), variable=var).pack(anchor=tk.W, padx=14)
            vars.append((zone.get("zone_id"), var))
        ttk.Label(
            dialog,
            text="Bölge listesi boşsa önce ses ayarları ekranındaki bölge yöneticisinden yeni bölge ekleyin.",
            wraplength=360,
            foreground="#6b7280",
        ).pack(padx=12, pady=(6, 2))

        def apply() -> None:
            picked = [zone_id for zone_id, var in vars if var.get()]
            if not picked:
                messagebox.showwarning("Bölge", "En az bir bölge seçin")
                return
            self.config.sound_routes[sound_key] = picked
            self.config.save()
            self._route_labels[sound_key].set(self._format_zone_summary(sound_key))
            dialog.destroy()

        btns = ttk.Frame(dialog)
        btns.pack(fill=tk.X, padx=12, pady=10)
        ttk.Button(btns, text="Kaydet", command=apply).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="İptal", command=dialog.destroy).pack(side=tk.RIGHT, padx=4)

    def _build_sound_row(self, frame: ttk.Frame, key: str, label: str) -> None:
        row = ttk.LabelFrame(frame, text=label, style="Card.TLabelframe")
        row.pack(fill=tk.X, padx=8, pady=3)
        row.columnconfigure(1, weight=1)
        path_var = tk.StringVar(value=self.config.sound_files.get(key, ""))
        self._sound_path_vars[key] = path_var

        ttk.Label(row, text="Dosya:").grid(row=0, column=0, padx=4, pady=2, sticky=tk.W)
        entry = ttk.Entry(row, textvariable=path_var)
        entry.grid(row=0, column=1, padx=4, pady=2, sticky=tk.EW)

        def choose() -> None:
            file_path = filedialog.askopenfilename(title=label)
            if not file_path:
                return
            stored = self._import_user_media(file_path, label)
            if stored:
                path_var.set(stored)
                self._save_sound_path(key, stored, show_message=False)

        btn = ttk.Button(row, text="Seç", command=choose)
        btn.grid(row=0, column=2, padx=4, pady=2)
        self._add_hint(btn, "Dosyayı seçtiğinizde otomatik olarak JinniBell klasörüne kopyalanır.")

        save_btn = ttk.Button(
            row,
            text="Kaydet",
            command=lambda k=key, var=path_var: self._save_sound_path(k, var.get()),
        )
        save_btn.grid(row=0, column=3, padx=2, pady=2)
        self._add_hint(save_btn, "Girilen yolu kalıcı olarak kaydeder ve zillere uygular.")

        test_btn = ttk.Button(row, text="Test", command=lambda var=path_var: self.audio.play_file(var.get(), label))
        test_btn.grid(row=0, column=4, padx=2, pady=2)
        self._add_hint(test_btn, "Seçilen sesi hemen dinleyebilirsiniz.")

        clear_btn = ttk.Button(row, text="Temizle", command=lambda k=key: self._clear_sound_path(k))
        clear_btn.grid(row=0, column=5, padx=2, pady=2)
        self._add_hint(clear_btn, "Bu zilde kayıtlı dosya yolunu siler.")

        ttk.Label(row, text="Kitaplıktan:").grid(row=1, column=0, padx=4, pady=2, sticky=tk.W)
        lib_combo = ttk.Combobox(row, state="readonly", width=22)
        lib_combo.grid(row=1, column=1, padx=4, pady=2, sticky=tk.W)
        self._library_comboboxes.append(lib_combo)
        ttk.Button(
            row,
            text="Uygula",
            command=lambda c=lib_combo, sound_key=key, var=path_var: self._apply_library_selection(sound_key, var, c.get()),
        ).grid(row=1, column=2, padx=4, pady=2, sticky=tk.W)

        info = SOUND_HINTS.get(key)
        if info:
            ttk.Label(row, text=info, wraplength=420, foreground="#555").grid(
                row=1, column=3, columnspan=2, padx=4, pady=2, sticky=tk.W
            )

        route_var = tk.StringVar(value=self._format_zone_summary(key))
        self._route_labels[key] = route_var
        route_row = ttk.Frame(row)
        route_row.grid(row=2, column=0, columnspan=6, sticky=tk.EW, padx=4, pady=(4, 0))
        ttk.Label(route_row, textvariable=route_var, foreground="#0f172a").pack(side=tk.LEFT)
        ttk.Button(
            route_row,
            text="Bölge Ata",
            command=lambda k=key, title=label: self._open_route_dialog(k, title),
        ).pack(side=tk.RIGHT, padx=2)

        announce_frame = ttk.Frame(row)
        announce_frame.grid(row=3, column=0, columnspan=6, sticky=tk.EW, padx=4, pady=(4, 2))
        announce_frame.columnconfigure(2, weight=1)
        config_ann = self.config.announcement_settings.get(key, {"enabled": False, "path": ""})
        enabled_var = tk.BooleanVar(value=bool(config_ann.get("enabled")))
        path_ann_var = tk.StringVar(value=config_ann.get("path", ""))
        self._announcement_vars[key] = {"enabled": enabled_var, "path": path_ann_var}

        chk = ttk.Checkbutton(
            announce_frame,
            text="Anons ekle (zil bittikten sonra çalsın)",
            variable=enabled_var,
            command=lambda k=key: self._save_announcement_settings(k),
        )
        chk.grid(row=0, column=0, padx=4, pady=2, sticky=tk.W)
        self._add_hint(chk, "Bu ders tipinden sonra seçtiğiniz anons otomatik oynatılır.")

        ann_entry = ttk.Entry(announce_frame, textvariable=path_ann_var)
        ann_entry.grid(row=0, column=2, padx=4, pady=2, sticky=tk.EW)

        def choose_ann() -> None:
            file_path = filedialog.askopenfilename(title=f"{label} için anons seç")
            if not file_path:
                return
            stored = self._import_user_media(file_path, f"anons-{label}")
            if stored:
                path_ann_var.set(stored)
                self._save_announcement_settings(key)

        ttk.Button(announce_frame, text="Seç", command=choose_ann).grid(row=0, column=3, padx=2, pady=2)
        ttk.Button(
            announce_frame,
            text="Temizle",
            command=lambda k=key: self._clear_announcement_path(k),
        ).grid(row=0, column=4, padx=2, pady=2)

        ann_combo = ttk.Combobox(announce_frame, state="readonly", width=18)
        ann_combo.grid(row=1, column=2, padx=4, pady=2, sticky=tk.W)
        self._library_comboboxes.append(ann_combo)
        ttk.Button(
            announce_frame,
            text="Kitaplıktan",
            command=lambda c=ann_combo, sound_key=key, var=path_ann_var: self._apply_library_selection(
                sound_key, var, c.get(), is_announcement=True
            ),
        ).grid(row=1, column=3, padx=2, pady=2)
        ttk.Button(
            announce_frame,
            text="Kaydet",
            command=lambda k=key: self._save_announcement_settings(k),
        ).grid(row=1, column=4, padx=2, pady=2)
        ttk.Button(
            announce_frame,
            text="Test",
            command=lambda: self.audio.play_file(path_ann_var.get(), f"{label} anons")
        ).grid(row=1, column=5, padx=2, pady=2)

        if key == "moment_of_silence":
            ttk.Label(
                row,
                text="Bu kayıt 1 dk/2 dk saygı duruşu butonlarında kullanılacaktır.",
                foreground="#0b5394",
            ).grid(row=3, column=0, columnspan=6, padx=4, pady=(2, 4), sticky=tk.W)

    def _build_ceremony_tab(self, frame: ttk.Frame) -> None:
        container = ttk.Frame(frame)
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        tree_frame = ttk.Frame(container)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        columns = ("title", "source", "status", "start", "end", "duration", "zones")
        self.ceremony_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse", height=12)
        self.ceremony_tree.heading("title", text="Başlık")
        self.ceremony_tree.heading("source", text="Kaynak")
        self.ceremony_tree.heading("status", text="Durum")
        self.ceremony_tree.heading("start", text="Başlangıç")
        self.ceremony_tree.heading("end", text="Bitiş")
        self.ceremony_tree.heading("duration", text="Toplam")
        self.ceremony_tree.heading("zones", text="Bölgeler")
        self.ceremony_tree.column("title", width=180, anchor=tk.W)
        self.ceremony_tree.column("source", width=80, anchor=tk.CENTER)
        self.ceremony_tree.column("status", width=110, anchor=tk.W)
        self.ceremony_tree.column("start", width=70, anchor=tk.CENTER)
        self.ceremony_tree.column("end", width=70, anchor=tk.CENTER)
        self.ceremony_tree.column("duration", width=80, anchor=tk.CENTER)
        self.ceremony_tree.column("zones", width=120, anchor=tk.W)
        self.ceremony_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.ceremony_tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.ceremony_tree.configure(yscrollcommand=tree_scroll.set)
        self.ceremony_tree.bind("<<TreeviewSelect>>", self._on_ceremony_select)
        self.ceremony_tree.bind("<ButtonPress-1>", self._start_ceremony_drag)
        self.ceremony_tree.bind("<ButtonRelease-1>", self._complete_ceremony_drag)

        tree_btns = ttk.Frame(tree_frame)
        tree_btns.pack(fill=tk.X, pady=6)
        up_btn = ttk.Button(tree_btns, text="Yukarı", command=lambda: self._move_ceremony_item(-1))
        up_btn.pack(side=tk.LEFT, padx=2)
        self._add_hint(up_btn, "Seçili parçayı bir üst sıraya taşır.")
        down_btn = ttk.Button(tree_btns, text="Aşağı", command=lambda: self._move_ceremony_item(1))
        down_btn.pack(side=tk.LEFT, padx=2)
        self._add_hint(down_btn, "Seçili parçayı bir alt sıraya taşır.")
        del_btn = ttk.Button(tree_btns, text="Sil", command=self._delete_ceremony_item)
        del_btn.pack(side=tk.LEFT, padx=2)
        self._add_hint(del_btn, "Listeden tamamen kaldırır.")
        file_btn = ttk.Button(tree_btns, text="Bilgisayardan Ekle", command=self._quick_add_ceremony_file)
        file_btn.pack(side=tk.LEFT, padx=2)
        self._add_hint(file_btn, "Dosya seçip listeye otomatik ekler.")
        yt_btn = ttk.Button(tree_btns, text="YouTube Linki Ekle", command=self._quick_add_ceremony_youtube)
        yt_btn.pack(side=tk.LEFT, padx=2)
        self._add_hint(yt_btn, "YouTube linkini ve başlangıç/bitişi sorarak listeye ekler.")
        play_btn = ttk.Button(tree_btns, text="Seçileni Çal", command=self._play_selected_ceremony)
        play_btn.pack(side=tk.RIGHT, padx=2)
        self._add_hint(play_btn, "Listeden seçtiğiniz parçayı hemen çalar.")
        next_btn = ttk.Button(tree_btns, text="Sıradaki", command=self._play_next_ceremony)
        next_btn.pack(side=tk.RIGHT, padx=2)
        self._add_hint(next_btn, "Sıradaki parçayı çalar ve durum sütununu günceller.")

        form = ttk.LabelFrame(container, text="Parça Detayı", style="Card.TLabelframe")
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
        self.ceremony_highlight_var = tk.StringVar(value="")
        ttk.Label(timing, text="Başlangıç (MM:SS)").grid(row=0, column=0, sticky=tk.W)
        start_entry = ttk.Entry(timing, textvariable=self.ceremony_start_var, width=10)
        start_entry.grid(row=1, column=0, padx=2, pady=2)
        ttk.Label(timing, text="Bitiş (opsiyonel)").grid(row=0, column=1, padx=6, sticky=tk.W)
        end_entry = ttk.Entry(timing, textvariable=self.ceremony_end_var, width=10)
        end_entry.grid(row=1, column=1, padx=6, pady=2)
        ttk.Label(timing, text="Vurgu (MM:SS)").grid(row=0, column=2, padx=6, sticky=tk.W)
        highlight_entry = ttk.Entry(timing, textvariable=self.ceremony_highlight_var, width=10)
        highlight_entry.grid(row=1, column=2, padx=6, pady=2)
        self._attach_ms_validation(start_entry, self.ceremony_start_var)
        self._attach_ms_validation(end_entry, self.ceremony_end_var)
        self._attach_ms_validation(highlight_entry, self.ceremony_highlight_var)
        ttk.Label(form, text="Bitiş boşsa parça sonuna kadar çalar.").pack(anchor=tk.W, padx=8, pady=(0, 8))

        action_row = ttk.Frame(form)
        action_row.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(action_row, text="Kaydet/Güncelle", command=self._save_ceremony_item).pack(side=tk.LEFT, padx=4)
        ttk.Button(action_row, text="Formu Temizle", command=self._clear_ceremony_form).pack(side=tk.RIGHT, padx=4)

        zone_row = ttk.Frame(form)
        zone_row.pack(fill=tk.X, padx=8, pady=(0, 6))
        ttk.Label(zone_row, text="Çıkış Bölgesi / Mekânsal Alan").pack(side=tk.LEFT)
        self.ceremony_zone_label = tk.StringVar(value="Genel")
        ttk.Button(zone_row, textvariable=self.ceremony_zone_label, command=self._pick_ceremony_zones).pack(
            side=tk.LEFT, padx=6
        )

        self._ceremony_edit_index: Optional[int] = None
        self._refresh_ceremony_list()
        self._clear_ceremony_form()

        stage_frame = ttk.LabelFrame(frame, text="Sahne Modu", style="Card.TLabelframe")
        stage_frame.pack(fill=tk.X, padx=12, pady=6)
        cards = ttk.Frame(stage_frame, style="Card.TFrame")
        cards.pack(fill=tk.X, padx=6, pady=4)
        now_card = ttk.Frame(cards, style="Card.TFrame")
        now_card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)
        ttk.Label(now_card, text="Şimdi Çalan", style="Bold.TLabel").pack(anchor=tk.W)
        ttk.Label(now_card, textvariable=self.stage_now_var, wraplength=260).pack(anchor=tk.W, pady=2)
        next_card = ttk.Frame(cards, style="Card.TFrame")
        next_card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)
        ttk.Label(next_card, text="Sıradaki", style="Bold.TLabel").pack(anchor=tk.W)
        ttk.Label(next_card, textvariable=self.stage_next_var, wraplength=260).pack(anchor=tk.W, pady=2)
        ttk.Button(stage_frame, text="Sahne Panelini Aç", command=self._open_stage_view).pack(
            anchor=tk.E, padx=8, pady=(4, 6)
        )

    # endregion

    # region EVENT HANDLERS
    def _change_volume(self) -> None:
        value = self.volume_var.get()
        self.config.volume = value
        self.config.save()
        self.audio.set_volume(value)
        if hasattr(self, "volume_percent_var"):
            self.volume_percent_var.set(self._format_volume_percent(value))

    @staticmethod
    def _format_volume_percent(value: float) -> str:
        return f"%{int(round(value * 100))}"

    def _toggle_mute(self) -> None:
        state = self.mute_var.get()
        self.config.muted = state
        self.config.save()
        self.audio.set_muted(state)

    def _flip_mute_from_shortcut(self) -> None:
        if hasattr(self, "mute_var"):
            self.mute_var.set(not self.mute_var.get())
        self._toggle_mute()

    def _toggle_pause(self) -> None:
        self.bells_paused = self.pause_var.get()
        if self.bells_paused:
            self._update_status("Tören modu: Otomatik zil kapalı")
        else:
            self._update_status("Hazır")
        self._update_pause_badge()

    def _toggle_pause_from_button(self) -> None:
        if hasattr(self, "pause_var"):
            self.pause_var.set(not self.pause_var.get())
        self._toggle_pause()

    def _toggle_pause_from_tray(self) -> None:
        if hasattr(self, "pause_var"):
            self.pause_var.set(not self.pause_var.get())
            self._toggle_pause()

    def is_ceremony_mode_active(self) -> bool:
        if hasattr(self, "pause_var"):
            return bool(self.pause_var.get())
        return False

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

    def _toggle_service_autostart(self) -> None:
        desired = self.service_autostart_var.get()
        if desired == self.config.launch_on_boot_service:
            return
        if not _is_windows():
            messagebox.showwarning(
                "Servis Modu",
                "Görev Zamanlayıcı kaydı yalnızca Windows'ta oluşturulabilir.",
            )
            self.service_autostart_var.set(False)
            return
        try:
            if desired:
                enable_windows_service_start()
            else:
                disable_windows_service_start()
        except Exception as exc:  # pragma: no cover - ortam bağımlı
            messagebox.showerror(
                "Servis Modu",
                f"Görev Zamanlayıcı kaydı güncellenemedi: {exc}",
            )
            self.service_autostart_var.set(self.config.launch_on_boot_service)
            return
        self.config.launch_on_boot_service = desired
        self.config.save()

    def _apply_shutdown_settings(self) -> None:
        mode = self._current_shutdown_mode()
        self._update_shutdown_inputs()
        time_value = self.shutdown_time_var.get().strip() or "20:00"
        delay_value = max(1, int(self.shutdown_delay_var.get() or 1))
        self.shutdown_time_var.set(time_value)
        self.shutdown_delay_var.set(delay_value)
        self.config.auto_shutdown_mode = mode
        self.config.auto_shutdown_enabled = mode != "disabled"
        self.config.auto_shutdown_time = time_value
        self.config.auto_shutdown_delay_minutes = delay_value
        self.config.save()

    def _update_shutdown_inputs(self) -> None:
        if not hasattr(self, "shutdown_entry"):
            return
        mode = self._current_shutdown_mode()
        time_state = tk.NORMAL if mode == "time" else tk.DISABLED
        delay_state = tk.NORMAL if mode == "after_last_bell" else tk.DISABLED
        self.shutdown_entry.configure(state=time_state)
        if hasattr(self, "shutdown_delay_spin"):
            self.shutdown_delay_spin.configure(state=delay_state)

    def _get_shutdown_mode_label(self, value: str) -> str:
        for label, mode in SHUTDOWN_MODES:
            if mode == value:
                return label
        return SHUTDOWN_MODES[0][0]

    def _current_shutdown_mode(self) -> str:
        current = getattr(self, "shutdown_mode_var", tk.StringVar(value=SHUTDOWN_MODES[0][0])).get()
        for label, value in SHUTDOWN_MODES:
            if label == current:
                return value
        return "disabled"

    def _toggle_recess_music(self) -> None:
        self.config.recess_music_enabled = self.recess_var.get()
        self.config.save()

    def _toggle_theme(self) -> None:
        mode = self.theme_var.get() or "light"
        self.config.theme_mode = mode
        self.config.save()
        self._setup_styles()
        self.root.update_idletasks()

    def _toggle_touch_mode(self) -> None:
        enabled = bool(self.touch_mode_var.get())
        self.config.touch_mode = enabled
        self.config.save()
        self._setup_styles()
        if enabled:
            self._update_status("Dokunmatik mod: büyük butonlar ve satırlar aktif")

    def _build_sound_library_section(self, frame: ttk.Frame) -> None:
        library_frame = ttk.LabelFrame(frame, text="Ses Kütüphanesi ve Etiketler", style="Card.TLabelframe")
        library_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        filter_bar = ttk.Frame(library_frame)
        filter_bar.pack(fill=tk.X, padx=6, pady=(4, 2))
        ttk.Label(filter_bar, text="Ara / Etiket", style="Bold.TLabel").pack(side=tk.LEFT, padx=(0, 4))
        self.library_filter_var = tk.StringVar()
        self.library_filter_var.trace_add("write", lambda *_: self._refresh_sound_library())
        ttk.Entry(filter_bar, textvariable=self.library_filter_var, width=22).pack(side=tk.LEFT, padx=4)
        columns = ("name", "tags", "path")
        self.library_tree = ttk.Treeview(library_frame, columns=columns, show="headings", height=6)
        self.library_tree.heading("name", text="İsim")
        self.library_tree.heading("tags", text="Etiketler")
        self.library_tree.heading("path", text="Dosya")
        self.library_tree.column("name", width=140, anchor=tk.W)
        self.library_tree.column("tags", width=140, anchor=tk.W)
        self.library_tree.column("path", anchor=tk.W)
        self.library_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)
        self.library_tree.bind("<Double-1>", lambda _e: self._play_selected_library_asset())
        btns = ttk.Frame(library_frame)
        btns.pack(fill=tk.X, padx=6, pady=4)
        ttk.Button(btns, text="Dosya Ekle", command=self._add_sound_asset).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="Etiketleri Düzenle", command=self._edit_sound_asset).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="Kitaplıktan Sil", command=self._remove_sound_asset).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="Test", command=self._play_selected_library_asset).pack(side=tk.RIGHT, padx=2)

    def _save_sound_path(self, key: str, value: str, show_message: bool = True) -> None:
        if not value:
            messagebox.showwarning("Ses", "Lütfen dosya yolunu girin")
            return
        stored = value
        path_obj = Path(value)
        if path_obj.exists() and MEDIA_DIR not in path_obj.parents:
            stored_path = self._import_user_media(value, SOUND_DISPLAY.get(key, key))
            if not stored_path:
                return
            stored = stored_path
        self.config.sound_files[key] = stored
        self.config.save()
        self._ensure_library_entry(stored, SOUND_DISPLAY.get(key, key))
        if show_message:
            messagebox.showinfo("Ses", "Dosya kaydedildi")

    def _clear_sound_path(self, key: str) -> None:
        var = self._sound_path_vars.get(key)
        if var:
            var.set("")
        self.config.sound_files[key] = ""
        self.config.save()

    def _apply_library_selection(
        self, sound_key: str, var: tk.StringVar, asset_name: str, *, is_announcement: bool = False
    ) -> None:
        if not asset_name:
            messagebox.showinfo("Ses", "Önce kütüphaneden bir isim seçin")
            return
        asset = self.config.find_sound_asset_by_name(asset_name)
        if not asset:
            messagebox.showerror("Ses", "Seçilen ses kütüphanede bulunamadı")
            return
        path = asset.get("path", "")
        var.set(path)
        if is_announcement:
            if sound_key not in self.config.announcement_settings:
                self.config.announcement_settings[sound_key] = {"enabled": True, "path": path}
            self.config.announcement_settings[sound_key]["path"] = path
            self.config.announcement_settings[sound_key]["enabled"] = True
            self.config.save()
        else:
            self._save_sound_path(sound_key, path, show_message=False)

    def _clear_announcement_path(self, sound_key: str) -> None:
        vars_map = self._announcement_vars.get(sound_key)
        if not vars_map:
            return
        vars_map["path"].set("")
        vars_map["enabled"].set(False)
        self._save_announcement_settings(sound_key)

    def _refresh_sound_library(self) -> None:
        if not hasattr(self, "library_tree"):
            return
        for item in self.library_tree.get_children():
            self.library_tree.delete(item)
        names: List[str] = []
        filter_text = ""
        if hasattr(self, "library_filter_var"):
            filter_text = self.library_filter_var.get().strip().lower()
        matched = 0
        for asset in self.config.sound_library:
            name = asset.get("name", "Ses")
            names.append(name)
            tags_list = asset.get("tags", [])
            tags = ", ".join(tags_list)
            path_value = asset.get("path", "")
            if filter_text:
                combined = " ".join([name, tags, Path(path_value).stem]).lower()
                if filter_text not in combined:
                    continue
            self.library_tree.insert(
                "",
                tk.END,
                iid=asset.get("asset_id"),
                values=(name, tags, path_value),
            )
            matched += 1
        if matched == 0:
            self.library_tree.insert("", tk.END, iid="__empty__", values=("Sonuç bulunamadı", "", ""))
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
        stored = self._import_user_media(file_path, name)
        if not stored:
            return
        self.config.add_sound_asset(name, stored, tags)
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
        if selection[0] == "__empty__":
            return None
        return selection[0]

    def _import_user_media(self, file_path: str, label: str, *, add_to_library: bool = True) -> Optional[str]:
        try:
            stored = _copy_into_media(file_path, label)
        except FileNotFoundError:
            messagebox.showerror("Ses", "Dosya bulunamadı")
            return None
        except Exception as exc:  # pragma: no cover - dosya sistemi
            messagebox.showerror("Ses", f"Dosya kopyalanamadı: {exc}")
            return None
        if add_to_library:
            self._ensure_library_entry(stored, label)
        return stored

    def _ensure_library_entry(self, path: str, name_hint: str) -> None:
        if not path:
            return
        if self.config.find_sound_asset_by_path(path):
            return
        self.config.add_sound_asset(name_hint or Path(path).stem, path)
        self._refresh_sound_library()

    def _seed_library_from_config(self) -> None:
        for key, path in self.config.sound_files.items():
            if path:
                self._ensure_library_entry(path, SOUND_DISPLAY.get(key, Path(path).stem))

    def _save_announcement_settings(self, sound_key: str) -> None:
        vars_map = self._announcement_vars.get(sound_key)
        if not vars_map:
            return
        enabled = bool(vars_map["enabled"].get())
        path = str(vars_map["path"].get()).strip()
        data = self.config.announcement_settings.setdefault(sound_key, {"enabled": False, "path": ""})
        data["enabled"] = enabled and bool(path)
        data["path"] = path
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

    def _on_day_change(self, _event: object | None = None) -> None:
        if getattr(self, "_suppress_day_event", False):
            return
        self._refresh_event_list()
        self._load_day_into_table()
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
                    font=(self.ui_font_family, 9),
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

    def _add_schedule_table_row(self) -> None:
        if not hasattr(self, "table_rows_frame"):
            return
        if len(getattr(self, "_table_rows", [])) >= TABLE_MAX_ROWS:
            messagebox.showinfo("Tablo", f"En fazla {TABLE_MAX_ROWS} ders satırı ekleyebilirsiniz.")
            return
        row_index = len(getattr(self, "_table_rows", []))
        row_frame = ttk.Frame(self.table_rows_frame)
        row_frame.grid(row=row_index, column=0, sticky="ew", pady=1)
        ttk.Label(row_frame, text=f"{row_index + 1}. Ders").grid(row=0, column=0, padx=4, sticky=tk.W)
        row_data: Dict[str, object] = {"frame": row_frame}
        for col, sound_key in enumerate(TABLE_SOUND_TYPES, start=1):
            var = tk.StringVar()
            entry = ttk.Entry(row_frame, textvariable=var, width=8, justify=tk.CENTER)
            entry.grid(row=0, column=col, padx=4)
            self._add_hint(entry, f"{SOUND_DISPLAY.get(sound_key)} saatini HH:MM olarak girin")
            entry.bind("<FocusOut>", lambda _e, v=var, w=entry: self._validate_time_cell(v, w))
            var.trace_add("write", lambda *_a, v=var, w=entry: self._validate_time_cell(v, w))
            row_data[sound_key] = var
        self._table_rows.append(row_data)

    def _remove_schedule_table_row(self, *, force: bool = False) -> None:
        if not getattr(self, "_table_rows", []):
            return
        if len(self._table_rows) == 1 and not force:
            for key in TABLE_SOUND_TYPES:
                cast_var = self._table_rows[0].get(key)
                if isinstance(cast_var, tk.StringVar):
                    cast_var.set("")
            return
        row = self._table_rows.pop()
        frame = row.get("frame")
        if isinstance(frame, (ttk.Frame, tk.Frame)):
            frame.destroy()

    def _clear_schedule_table(self) -> None:
        for row in getattr(self, "_table_rows", []):
            for key in TABLE_SOUND_TYPES:
                var = row.get(key)
                if isinstance(var, tk.StringVar):
                    var.set("")

    def _sync_schedule_table_rows(self) -> None:
        if not hasattr(self, "_table_rows"):
            return
        try:
            desired = int(self.table_row_target.get())
        except (tk.TclError, ValueError, AttributeError):
            desired = len(self._table_rows)
        desired = max(1, min(TABLE_MAX_ROWS, desired))
        if hasattr(self, "table_row_target"):
            self.table_row_target.set(desired)
        while len(self._table_rows) < desired:
            self._add_schedule_table_row()
        while len(self._table_rows) > desired:
            self._remove_schedule_table_row(force=True)

    def _load_day_into_table(self) -> None:
        if not hasattr(self, "_table_rows"):
            return
        day = self.day_var.get()
        events = sorted(self.config.daily_schedule.get(day, []), key=lambda evt: evt.clock)
        self._clear_schedule_table()
        pointer = 0
        for event in events:
            if event.sound_type not in TABLE_SOUND_TYPES:
                continue
            while len(self._table_rows) <= pointer:
                self._add_schedule_table_row()
            target_var = self._table_rows[pointer].get(event.sound_type)
            if isinstance(target_var, tk.StringVar) and target_var.get():
                pointer += 1
                while len(self._table_rows) <= pointer:
                    self._add_schedule_table_row()
                target_var = self._table_rows[pointer].get(event.sound_type)
            if isinstance(target_var, tk.StringVar):
                target_var.set(event.clock)
            if event.sound_type == "lesson_exit":
                pointer += 1

    def _apply_table_to_day(self) -> None:
        if not hasattr(self, "_table_rows"):
            return
        day = self.day_var.get()
        base_events = [
            event
            for event in self.config.daily_schedule.get(day, [])
            if event.sound_type not in TABLE_SOUND_TYPES
        ]
        new_events: List[BellEvent] = []
        for idx, row in enumerate(getattr(self, "_table_rows", [])):
            for sound_key in TABLE_SOUND_TYPES:
                var = row.get(sound_key)
                if not isinstance(var, tk.StringVar):
                    continue
                value = var.get().strip()
                if not value:
                    continue
                try:
                    clock = self._normalize_clock(value)
                except ValueError as exc:
                    messagebox.showerror(
                        "Saat formatı",
                        f"{idx + 1}. satır {SOUND_DISPLAY.get(sound_key)} için hata: {exc}",
                    )
                    return
                label = f"{idx + 1}. Ders {SOUND_DISPLAY.get(sound_key)}"
                new_events.append(BellEvent(label=label, clock=clock, sound_type=sound_key))
        combined = base_events + new_events
        combined.sort(key=lambda evt: evt.clock)
        self.config.daily_schedule[day] = combined
        self.config.save()
        self._refresh_event_list()
        messagebox.showinfo("Tablo", f"{day} için tablo kaydedildi. Farklı günlere kopyalayabilirsiniz.")

    @staticmethod
    def _normalize_clock(value: str) -> str:
        text = value.strip()
        if not text:
            raise ValueError("Saat girilmedi")
        if text.isdigit() and len(text) in {3, 4}:
            text = text.zfill(4)
            hour = int(text[:2])
            minute = int(text[2:])
        else:
            parts = text.split(":")
            if len(parts) != 2:
                raise ValueError("HH:MM formatı kullanılmalı")
            hour, minute = int(parts[0]), int(parts[1])
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError("Saat 00-23, dakika 00-59 aralığında olmalı")
        return f"{hour:02d}:{minute:02d}"

    def _validate_time_cell(self, var: tk.StringVar, widget: tk.Widget) -> None:
        value = var.get().strip()
        try:
            self._normalize_clock(value)
        except Exception:
            try:
                widget.configure(foreground="#dc2626")
            except tk.TclError:
                pass
        else:
            try:
                widget.configure(foreground=self._palette.get("text", "#111827"))
            except tk.TclError:
                pass

    def _attach_time_validation(self, entry: tk.Widget, var: tk.StringVar) -> None:
        entry.bind("<FocusOut>", lambda _e: self._validate_time_cell(var, entry))
        var.trace_add("write", lambda *_a: self._validate_time_cell(var, entry))

    def _attach_ms_validation(self, entry: tk.Widget, var: tk.StringVar) -> None:
        def _validate() -> None:
            text = var.get().strip()
            try:
                if text:
                    _parse_minute_second(text)
                entry.configure(foreground=self._palette.get("text", "#111827"))
            except Exception:
                entry.configure(foreground="#dc2626")

        entry.bind("<FocusOut>", lambda _e: _validate())
        var.trace_add("write", lambda *_a: _validate())

    def _nudge_time(self, minutes: int) -> None:
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
        except ValueError:
            hour, minute = 8, 0
        total = (hour * 60 + minute + minutes) % (24 * 60)
        self.hour_var.set(f"{total // 60:02d}")
        self.minute_var.set(f"{total % 60:02d}")

    def _set_current_time(self) -> None:
        now = datetime.now()
        self.hour_var.set(f"{now.hour:02d}")
        self.minute_var.set(f"{now.minute:02d}")

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
        filter_text = ""
        if hasattr(self, "schedule_filter_var"):
            filter_text = self.schedule_filter_var.get().strip().lower()
        selected_sound = "Tümü"
        if hasattr(self, "schedule_filter_sound_var"):
            selected_sound = self.schedule_filter_sound_var.get()

        shown = 0
        for idx, event in enumerate(events):
            friendly = SOUND_DISPLAY.get(event.sound_type, event.sound_type)
            if selected_sound and selected_sound != "Tümü" and friendly != selected_sound:
                continue
            if filter_text and (
                filter_text not in event.label.lower()
                and filter_text not in friendly.lower()
                and filter_text not in event.clock.lower()
            ):
                continue
            self.event_list.insert(
                "",
                tk.END,
                iid=str(idx),
                values=(event.clock, event.label, friendly),
                tags=(event.sound_type,),
            )
            shown += 1
        if hasattr(self, "schedule_count_var"):
            total = len(events)
            self.schedule_count_var.set(f"{shown} / {total} zil listeleniyor")
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
        _execute_bell_event(
            self.config,
            self.audio,
            self.notifier,
            event,
            self._play_recess_music,
            self._run_shutdown,
        )

    def _trigger_manual(self, key: str) -> None:
        sequences = self._build_manual_sequences()
        steps = sequences.get(key)
        if not steps:
            messagebox.showwarning("Ses bulunamadı", "Lütfen ses dosyalarını ayarlayın")
            return
        self.manual_override = True
        delay_seconds = self._get_manual_delay_seconds()
        self.notifier.notify("Manuel Çalma", f"{self.manual_delay_var.get()} sonra seçilen tören başlatılacak")
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

    def _quick_add_ceremony_file(self) -> None:
        old_source = self.ceremony_source_var.get()
        old_location = self.ceremony_location_var.get()
        old_title = self.ceremony_title_var.get()
        self._choose_ceremony_file()
        if not self.ceremony_location_var.get():
            self.ceremony_source_var.set(old_source)
            self.ceremony_location_var.set(old_location)
            self.ceremony_title_var.set(old_title)
            return
        self._save_ceremony_item()
        self._clear_ceremony_form()

    def _quick_add_ceremony_youtube(self) -> None:
        url = simpledialog.askstring("YouTube", "Video bağlantısı")
        if not url:
            return
        start = simpledialog.askstring("Başlangıç", "MM:SS formatında (opsiyonel)", initialvalue="00:00")
        end = simpledialog.askstring("Bitiş", "MM:SS formatında (opsiyonel)", initialvalue="")
        self.ceremony_source_var.set("youtube")
        self.ceremony_location_var.set(url.strip())
        if start:
            self.ceremony_start_var.set(start)
        if end is not None:
            self.ceremony_end_var.set(end)
        self._fetch_ceremony_metadata(auto=True)
        self._save_ceremony_item()
        self._clear_ceremony_form()

    def _choose_ceremony_file(self) -> None:
        path = filedialog.askopenfilename(title="Müzik seç")
        if not path:
            return
        stored = self._import_user_media(path, Path(path).stem, add_to_library=False)
        if not stored:
            return
        self.ceremony_source_var.set("file")
        self.ceremony_location_var.set(stored)
        self.ceremony_title_var.set(Path(stored).stem)
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

        highlight_ms: Optional[int] = None
        highlight_text = self.ceremony_highlight_var.get().strip()
        if highlight_text:
            try:
                highlight_ms = _parse_minute_second(highlight_text)
            except ValueError as exc:
                messagebox.showerror("Vurgu", str(exc))
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
        if highlight_ms is not None:
            item["highlight_ms"] = highlight_ms
        item["zones"] = list(self._current_ceremony_zones)
        return item

    def _prepare_ceremony_item(
        self, item: Dict[str, object], existing: Optional[Dict[str, object]] = None
    ) -> Dict[str, object]:
        if existing:
            if "highlight_ms" not in item and existing.get("highlight_ms") is not None:
                item["highlight_ms"] = existing.get("highlight_ms")
            if not item.get("zones") and existing.get("zones"):
                item["zones"] = existing.get("zones")
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
            zone_text = ", ".join(item.get("zones", [])) if item.get("zones") else "Genel"
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
                    zone_text,
                ),
            )
        self._ceremony_edit_index = None
        self.ceremony_tree.selection_remove(self.ceremony_tree.selection())
        self._refresh_queue_snapshot()

    def _describe_ceremony_status(self, item: Dict[str, object]) -> str:
        status = item.get("status") or ("Hazır" if item.get("source") == "file" else "Bekliyor")
        detail = item.get("status_detail")
        if detail:
            return f"{status} - {detail}"
        return str(status)

    def _format_ceremony_badge(self, item: Optional[Dict[str, object]]) -> str:
        if not item:
            return "-"
        title = item.get("label") or "Tören Parçası"
        source = item.get("source") or "file"
        start_text = _format_mmss(int(item.get("start_ms", 0)))
        highlight = item.get("highlight_ms")
        marker = f" · vurgu { _format_mmss(int(highlight))}" if highlight is not None else ""
        zones = item.get("zones") or []
        zone_tag = f" · {', '.join(zones)}" if zones else ""
        return f"{title} ({'YouTube' if source == 'youtube' else 'Dosya'}) · {start_text}{marker}{zone_tag}"

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
        highlight_ms = item.get("highlight_ms")
        self.ceremony_highlight_var.set(_format_mmss(int(highlight_ms)) if highlight_ms is not None else "")
        self._current_ceremony_zones = list(item.get("zones", []))
        self.ceremony_zone_label.set(", ".join(self._current_ceremony_zones) if self._current_ceremony_zones else "Genel")

    def _clear_ceremony_form(self) -> None:
        self._ceremony_edit_index = None
        self.ceremony_source_var.set("file")
        self.ceremony_location_var.set("")
        self.ceremony_title_var.set("")
        self.ceremony_start_var.set("00:00")
        self.ceremony_end_var.set("")
        self.ceremony_highlight_var.set("")
        self._current_ceremony_zones = []
        self.ceremony_zone_label.set("Genel")
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

    def _open_stage_view(self) -> None:
        if getattr(self, "_stage_win", None) and self._stage_win.winfo_exists():
            self._stage_win.lift()
            return
        win = tk.Toplevel(self.root)
        self._stage_win = win
        win.title("Sahne Modu")
        win.geometry("640x380")
        ttk.Label(win, text="Sahne Modu", style="Accent.TLabel").pack(anchor=tk.W, padx=12, pady=6)
        ttk.Label(win, text="YouTube + yerel müzikleri dokunmatik uyumlu listeden yönetin.").pack(
            anchor=tk.W, padx=12
        )
        listbox = tk.Listbox(win, height=14)
        listbox.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)
        for idx, item in enumerate(self.config.ceremony_playlist):
            badge = self._format_ceremony_badge(item)
            listbox.insert(tk.END, f"{idx + 1}. {badge}")
        ttk.Button(win, text="Kapat", command=win.destroy).pack(anchor=tk.E, padx=12, pady=(0, 8))

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

    def _on_audio_error(self, message: str) -> None:
        now = time.time()
        if message == getattr(self, "_last_audio_error", "") and (now - getattr(self, "_last_audio_error_time", 0)) < 10:
            return
        self._last_audio_error = message
        self._last_audio_error_time = now

        def show() -> None:
            messagebox.showerror(
                "Ses Çalma Hatası",
                message
                + "\n\nFFmpeg klasöründeki ffplay.exe ve SDL2.dll dosyalarını kontrol edin"
                + " veya Ses sekmesinden yeni bir dosya seçerek tekrar deneyin.",
            )

        self.root.after(0, show)

    def _run_shutdown(self) -> None:
        mode = self.config.auto_shutdown_mode or ("time" if self.config.auto_shutdown_enabled else "disabled")
        if mode == "disabled":
            return
        if self.notifier:
            self.notifier.notify("JinniBell Pro", "Otomatik kapanış başlatılıyor")
        if os.name == "nt":
            subprocess.Popen(["shutdown", "/s", "/t", "0"])
        else:
            subprocess.Popen(["shutdown", "-h", "now"])

    def _minimize_to_tray(self) -> None:
        self.root.withdraw()
        if self.tray:
            self.tray.ensure()
        self._update_status("Arka planda çalışıyor")
        self._maybe_show_tray_hint()

    def _restore_from_tray(self) -> None:
        self.root.deiconify()
        self.root.after(0, self.root.lift)
        self.root.after(0, self.root.focus_force)

    def _quit_from_tray(self) -> None:
        self._cleanup_and_exit()

    def _cleanup_and_exit(self) -> None:
        try:
            self.scheduler.stop()
        except Exception:
            pass
        try:
            self.audio.stop()
        except Exception:
            pass
        if self.tray:
            self.tray.hide_if_visible()
        self.root.destroy()

    def _on_close_request(self) -> None:
        self._minimize_to_tray()

    def _auto_minimize_if_needed(self) -> None:
        if getattr(self, "root", None) is None:
            return
        if self.config.launch_on_boot and self._launched_from_startup:
            self._minimize_to_tray()

    def _maybe_show_tray_hint(self) -> None:
        if self._tray_hint_shown:
            return
        if pystray is None:
            return
        self._tray_hint_shown = True

        def show() -> None:
            messagebox.showinfo(
                "Sistem Tepsisi",
                "Program kapanmadı; Windows saatinin yanındaki JinniBell Pro simgesine sağ tıklayarak"
                " tekrar açabilir veya tamamen kapatabilirsiniz.",
            )

        self.root.after(0, show)

    # endregion

    def _update_status(self, message: str) -> None:
        self.status_var.set(message)
        self._update_pause_badge()
        self._update_countdown_label()
        self._refresh_queue_snapshot()

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
            self._refresh_queue_snapshot()
            return
        today_name = WEEKDAYS[now.weekday()]
        next_event = self.config.next_event_for_day(today_name, now.time())
        if not next_event:
            self.countdown_var.set("Bugün kalan zil yok")
            self._refresh_queue_snapshot()
            return
        try:
            target_time = datetime.strptime(next_event.clock, "%H:%M")
            target_dt = datetime.combine(date.today(), target_time.time())
        except ValueError:
            self.countdown_var.set("Sıradaki zil hesaplanamadı")
            self._refresh_queue_snapshot()
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
        self._refresh_queue_snapshot()

    def _refresh_queue_snapshot(self) -> None:
        today = date.today()
        now = datetime.now()
        today_name = WEEKDAYS[today.weekday()]
        next_event = self.config.next_event_for_day(today_name, now.time())
        if next_event:
            self.queue_next_var.set(f"{next_event.clock} · {next_event.label}")
        else:
            self.queue_next_var.set("Planlı zil yok")
        self.queue_now_var.set(self.status_var.get())

        if self.config.ceremony_playlist:
            idx = min(self._ceremony_index, len(self.config.ceremony_playlist) - 1)
            current = self.config.ceremony_playlist[idx]
            nxt = (
                self.config.ceremony_playlist[(idx + 1) % len(self.config.ceremony_playlist)]
                if len(self.config.ceremony_playlist) > 1
                else None
            )
            self.ceremony_now_var.set(self._format_ceremony_badge(current))
            self.ceremony_next_var.set(self._format_ceremony_badge(nxt) if nxt else "Sırada yok")
            self.stage_now_var.set(self.ceremony_now_var.get())
            self.stage_next_var.set(self.ceremony_next_var.get())
        else:
            self.ceremony_now_var.set("Tören listesi boş")
            self.ceremony_next_var.set("Sıradaki parça yok")
            self.stage_now_var.set("Sahne modu hazır")
            self.stage_next_var.set("Sırada parça yok")

    def _update_pause_badge(self) -> None:
        if not hasattr(self, "pause_badge"):
            return
        if getattr(self, "bells_paused", False):
            self.pause_badge.configure(
                text="Tören modu aktif - otomatik ziller kapalı",
                style="Danger.TButton",
            )
        else:
            self.pause_badge.configure(text="Tören modu kapalı", style="Success.TButton")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="JinniBell Pro")
    parser.add_argument("--autostart", action="store_true", help="Windows başlangıcında arayüzü gizler")
    parser.add_argument("--service", action="store_true", help="Arayüz açmadan servis modunda çalıştır")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.service:
        HeadlessBellService().run()
        return
    root = tk.Tk()
    app = BellApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
