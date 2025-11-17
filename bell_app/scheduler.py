"""Scheduler thread that keeps track of bell events."""
from __future__ import annotations

import datetime as dt
import threading
import time
from typing import Callable, Optional

from .config import BellConfig, BellEvent, WEEKDAYS


class ScheduleRunner:
    def __init__(
        self,
        config: BellConfig,
        trigger_callback: Callable[[BellEvent], None],
        override_predicate: Callable[[], bool],
    ) -> None:
        self.config = config
        self.trigger_callback = trigger_callback
        self.override_predicate = override_predicate
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._last_triggered: dict[str, str] = {}

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join(timeout=1)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            now = dt.datetime.now()
            weekday = WEEKDAYS[now.weekday()]
            holiday = self.config.holiday_for(now.date())
            if holiday:
                self._last_triggered.pop(weekday, None)
                time.sleep(60)
                self._handle_auto_shutdown(now)
                continue
            current_clock = now.strftime("%H:%M")
            last_clock = self._last_triggered.get(weekday)
            if last_clock == current_clock:
                time.sleep(1)
                continue

            for event in sorted(self.config.daily_schedule.get(weekday, []), key=lambda e: e.clock):
                if event.clock == current_clock and not self.override_predicate():
                    self._last_triggered[weekday] = current_clock
                    self.trigger_callback(event)
                    break

            self._handle_auto_shutdown(now)
            time.sleep(1)

    def _handle_auto_shutdown(self, now: dt.datetime) -> None:
        if not self.config.auto_shutdown_enabled:
            return
        if not self.config.auto_shutdown_time:
            return
        if now.strftime("%H:%M") != self.config.auto_shutdown_time:
            return
        # Only shutdown once per day
        key = now.strftime("%Y-%m-%d")
        if self._last_triggered.get("shutdown") == key:
            return
        self._last_triggered["shutdown"] = key
        if now.strftime("%H:%M") == self.config.auto_shutdown_time:
            self.trigger_callback(
                BellEvent(
                    label="Bilgisayar Kapanışı",
                    clock=self.config.auto_shutdown_time,
                    sound_type="auto_shutdown",
                )
            )


