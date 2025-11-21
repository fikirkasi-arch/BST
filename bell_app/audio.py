"""Audio playback helpers."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Callable, Dict, Optional

try:  # pragma: no cover - winsound yalnızca Windows'ta mevcut
    import winsound
except Exception:  # pragma: no cover - diğer platformlar
    winsound = None

from pydub import AudioSegment


FFPLAY_PATH: Optional[Path] = None


def _configure_external_binaries() -> None:
    """Point pydub to bundled ffmpeg/ffprobe and locate ffplay."""

    def _resolve_binary(name: str) -> Optional[Path]:
        # explicit env override
        env_hint = os.environ.get(f"{name.upper()}_PATH") or os.environ.get("FFMPEG_HOME")
        if env_hint:
            candidate = Path(env_hint) / (name + (".exe" if os.name == "nt" else ""))
            if candidate.exists():
                return candidate

        search_roots = []
        if getattr(sys, "frozen", False):
            search_roots.append(Path(getattr(sys, "_MEIPASS")))
            search_roots.append(Path(sys.executable).parent)
        search_roots.append(Path(__file__).resolve().parents[1])

        for root in search_roots:
            binary = root / "ffmpeg" / (name + (".exe" if os.name == "nt" else ""))
            if binary.exists():
                return binary
        system_path = shutil.which(name)
        if system_path:
            return Path(system_path)
        return None

    global FFPLAY_PATH

    ffmpeg_path = _resolve_binary("ffmpeg")
    ffprobe_path = _resolve_binary("ffprobe")
    FFPLAY_PATH = _resolve_binary("ffplay")
    if ffmpeg_path:
        AudioSegment.converter = str(ffmpeg_path)
    if ffprobe_path:
        AudioSegment.ffprobe = str(ffprobe_path)


def _ffplay_dependency_error() -> Optional[str]:
    if FFPLAY_PATH is None:
        return "ffplay bulunamadı; ffmpeg klasörüne ffplay.exe ekleyin"
    if os.name == "nt":
        sdl_path = Path(FFPLAY_PATH).with_name("SDL2.dll")
        if not sdl_path.exists():
            return "SDL2.dll eksik; ffplay ses çıkışı için SDL2.dll'i ffmpeg klasörüne ekleyin"
    return None


_configure_external_binaries()


class AudioController:
    """Handles sound playback and volume."""

    def __init__(self) -> None:
        self._cache: Dict[str, AudioSegment] = {}
        self._current_play_obj = None
        self._lock = threading.Lock()
        self._muted = False
        self._volume = 0.8
        self._on_state_change: Optional[Callable[[str], None]] = None
        self._on_error: Optional[Callable[[str], None]] = None

    def set_state_callback(self, callback: Callable[[str], None]) -> None:
        self._on_state_change = callback

    def set_error_callback(self, callback: Callable[[str], None]) -> None:
        self._on_error = callback

    def set_volume(self, value: float) -> None:
        self._volume = max(0.0, min(value, 1.0))
        if self._current_play_obj is not None:
            self._current_play_obj.stop()

    def set_muted(self, muted: bool) -> None:
        self._muted = muted
        if muted and self._current_play_obj is not None:
            self._current_play_obj.stop()

    def stop(self) -> None:
        with self._lock:
            if self._current_play_obj is not None:
                self._current_play_obj.stop()
                self._current_play_obj = None

    def preload(self, label: str, file_path: str) -> None:
        if file_path and Path(file_path).exists():
            self._cache[file_path] = AudioSegment.from_file(file_path)

    def play_file(self, file_path: str, label: str = "") -> None:
        if not file_path:
            self._notify_error("Çalınacak bir ses dosyası seçilmedi")
            return
        if self._muted:
            return

        path = Path(file_path)
        if not path.exists():
            self._notify_error(f"Ses dosyası bulunamadı: {file_path}")
            return

        try:
            audio = self._cache.get(file_path)
            if audio is None:
                audio = AudioSegment.from_file(file_path)
                self._cache[file_path] = audio
            # apply volume
            gain = 20 * (self._volume - 1)
            segment = audio + gain if self._volume != 1.0 else audio
        except Exception as exc:  # pragma: no cover - platform/codec bağımlı
            self._notify_error(f"Ses dosyası yüklenemedi: {exc}")
            return

        self._play_segment(segment, label or path.stem)

    def play_sequence(
        self, segments: list[tuple[str, Optional[str]]], on_complete: Optional[Callable[[], None]] = None
    ) -> None:
        """Play a sequence of (action, payload)."""

        def worker() -> None:
            for action, payload in segments:
                if action == "sound" and payload:
                    self.play_file(payload, label=Path(payload).stem)
                    self._wait_until_idle()
                elif action == "silence" and payload:
                    duration = int(payload)
                    self._notify(f"Saygı duruşu {duration // 1000} sn")
                    time.sleep(duration / 1000)
            self._notify("Hazır")
            if on_complete:
                on_complete()

        threading.Thread(target=worker, daemon=True).start()

    def _play_segment(self, segment: AudioSegment, label: str) -> None:
        def worker() -> None:
            handle = None
            try:
                dep_error = _ffplay_dependency_error()
                if dep_error:
                    raise RuntimeError(dep_error)
                handle = _play_with_ffplay(segment)
            except Exception as exc:
                try:
                    handle = _try_winsound(segment, exc)
                except Exception as fallback_exc:
                    self._notify_error(str(fallback_exc))
                    return
            with self._lock:
                if self._current_play_obj is not None:
                    self._current_play_obj.stop()
                self._current_play_obj = handle
                self._notify(f"Çalıyor: {label}")
            try:
                handle.wait_done()
            finally:
                with self._lock:
                    self._current_play_obj = None
                self._notify("Hazır")

        threading.Thread(target=worker, daemon=True).start()

    def _notify(self, message: str) -> None:
        if self._on_state_change:
            self._on_state_change(message)

    def _notify_error(self, message: str) -> None:
        if self._on_error:
            self._on_error(message)

    def _wait_until_idle(self) -> None:
        while True:
            with self._lock:
                playing = self._current_play_obj is not None
            if not playing:
                break
            time.sleep(0.1)


class _FFplayHandle:
    def __init__(self, process: subprocess.Popen, temp_file: Path) -> None:
        self._process = process
        self._temp_file = temp_file

    def stop(self) -> None:
        if self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._process.kill()
        self._cleanup()

    def wait_done(self) -> None:
        try:
            self._process.wait()
        finally:
            self._cleanup()

    def _cleanup(self) -> None:
        if self._temp_file.exists():
            try:
                self._temp_file.unlink()
            except OSError:
                pass


def _play_with_ffplay(segment: AudioSegment) -> _FFplayHandle:
    if FFPLAY_PATH is None:
        raise RuntimeError("ffplay bulunamadı; lütfen FFmpeg paketinin ffplay.exe içeren bir sürümünü kullanın")

    fd, tmp_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    tmp_file = Path(tmp_path)
    segment.export(tmp_file, format="wav")

    process = subprocess.Popen(
        [str(FFPLAY_PATH), "-nodisp", "-autoexit", "-loglevel", "error", str(tmp_file)],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # SDL2.dll eksik gibi durumlarda süreç hemen kapanır; kısa bir süre gözlemleyelim.
    time.sleep(0.2)
    if process.poll() not in (None, 0):
        process.communicate(timeout=0.1)
        raise RuntimeError(
            "Ses oynatılırken ffplay başlatılamadı. FFmpeg paketindeki SDL2.dll dosyasının"
            " eksik olmadığından emin olun."
        )
    return _FFplayHandle(process, tmp_file)


class _WinsoundHandle:
    def __init__(self, temp_file: Path, duration: float) -> None:
        self._temp_file = temp_file
        self._duration = max(duration, 0.1)
        self._done = threading.Event()
        self._cleaned = False
        winsound.PlaySound(str(temp_file), winsound.SND_FILENAME | winsound.SND_ASYNC)  # type: ignore[arg-type]
        threading.Thread(target=self._timer, daemon=True).start()

    def _timer(self) -> None:
        time.sleep(self._duration)
        self._done.set()
        self._cleanup()

    def stop(self) -> None:
        winsound.PlaySound(None, winsound.SND_PURGE)
        self._done.set()
        self._cleanup()

    def wait_done(self) -> None:
        self._done.wait()
        self._cleanup()

    def _cleanup(self) -> None:
        if self._cleaned:
            return
        self._cleaned = True
        if self._temp_file.exists():
            try:
                self._temp_file.unlink()
            except OSError:
                pass


def _try_winsound(segment: AudioSegment, original_exc: Exception) -> Optional[object]:
    if winsound is None or os.name != "nt":
        raise original_exc
    fd, tmp_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    tmp_file = Path(tmp_path)
    segment.export(tmp_file, format="wav")
    duration = len(segment) / 1000
    return _WinsoundHandle(tmp_file, duration)


