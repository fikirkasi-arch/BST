"""Audio playback helpers."""
from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Callable, Dict, Optional

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio  # type: ignore


class AudioController:
    """Handles sound playback and volume."""

    def __init__(self) -> None:
        self._cache: Dict[str, AudioSegment] = {}
        self._current_play_obj = None
        self._lock = threading.Lock()
        self._muted = False
        self._volume = 0.8
        self._on_state_change: Optional[Callable[[str], None]] = None

    def set_state_callback(self, callback: Callable[[str], None]) -> None:
        self._on_state_change = callback

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
            self._cache[label] = AudioSegment.from_file(file_path)

    def play_file(self, file_path: str, label: str = "") -> None:
        if not file_path:
            return
        if self._muted:
            return
        audio = self._cache.get(file_path)
        if audio is None:
            audio = AudioSegment.from_file(file_path)
            self._cache[file_path] = audio
        # apply volume
        gain = 20 * (self._volume - 1)
        segment = audio + gain if self._volume != 1.0 else audio
        self._play_segment(segment, label or Path(file_path).stem)

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
            with self._lock:
                if self._current_play_obj is not None:
                    self._current_play_obj.stop()
                self._notify(f"Çalıyor: {label}")
                self._current_play_obj = _play_with_simpleaudio(segment)
            self._current_play_obj.wait_done()
            with self._lock:
                self._current_play_obj = None
                self._notify("Hazır")

        threading.Thread(target=worker, daemon=True).start()

    def _notify(self, message: str) -> None:
        if self._on_state_change:
            self._on_state_change(message)

    def _wait_until_idle(self) -> None:
        while True:
            with self._lock:
                playing = self._current_play_obj is not None
            if not playing:
                break
            time.sleep(0.1)


