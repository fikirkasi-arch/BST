"""Configuration management for the bell scheduler application."""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import date, time
from pathlib import Path
from typing import Dict, List, Optional, TypedDict

CONFIG_PATH = Path("config.json")

WEEKDAYS = [
    "Pazartesi",
    "Salı",
    "Çarşamba",
    "Perşembe",
    "Cuma",
    "Cumartesi",
    "Pazar",
]


def parse_time(value: str) -> time:
    hour, minute = [int(part) for part in value.split(":", 1)]
    return time(hour=hour, minute=minute)


def time_to_str(value: time) -> str:
    return value.strftime("%H:%M")


class CeremonyItem(TypedDict, total=False):
    label: str
    source: str  # "file" or "youtube"
    location: str
    start_ms: int
    end_ms: Optional[int]
    duration_sec: Optional[int]


@dataclass
class BellEvent:
    label: str
    clock: str
    sound_type: str


@dataclass
class BellConfig:
    daily_schedule: Dict[str, List[BellEvent]] = field(
        default_factory=lambda: {day: [] for day in WEEKDAYS}
    )
    sound_files: Dict[str, str] = field(
        default_factory=lambda: {
            "student_entry": "",
            "teacher_entry": "",
            "lesson_exit": "",
            "recess_music": "",
            "istiklal": "",
            "siren": "",
            "moment_of_silence": "",
        }
    )
    volume: float = 0.8
    muted: bool = False
    auto_shutdown_enabled: bool = False
    auto_shutdown_time: Optional[str] = None
    ceremony_playlist: List[CeremonyItem] = field(default_factory=list)
    recess_music_enabled: bool = False
    holidays: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls) -> "BellConfig":
        if CONFIG_PATH.exists():
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            # Convert dicts to dataclasses
            schedule = {
                day: [BellEvent(**event) for event in events]
                for day, events in data.get("daily_schedule", {}).items()
            }
            playlist: List[CeremonyItem] = []
            for raw in data.get("ceremony_playlist", []):
                start_ms = raw.get("start_ms")
                if start_ms is None:
                    # eski sürümlerde dakika tutuluyordu
                    minute_val = raw.get("start_minute")
                    if minute_val is not None:
                        start_ms = int(minute_val) * 60 * 1000
                    else:
                        start_ms = 0
                item: CeremonyItem = {
                    "label": raw.get("label", "Tören Parçası"),
                    "source": raw.get("source", "file"),
                    "location": raw.get("location", ""),
                    "start_ms": int(start_ms),
                    "duration_sec": raw.get("duration_sec"),
                }
                end_ms = raw.get("end_ms")
                if end_ms is None and raw.get("end_minute") is not None:
                    end_ms = int(raw["end_minute"]) * 60 * 1000
                if end_ms is not None:
                    item["end_ms"] = int(end_ms)
                playlist.append(item)

            instance = cls(
                daily_schedule={**{day: [] for day in WEEKDAYS}, **schedule},
                sound_files=data.get("sound_files", {}),
                volume=data.get("volume", 0.8),
                muted=data.get("muted", False),
                auto_shutdown_enabled=data.get("auto_shutdown_enabled", False),
                auto_shutdown_time=data.get("auto_shutdown_time"),
                ceremony_playlist=playlist,
                recess_music_enabled=data.get("recess_music_enabled", False),
                holidays=data.get("holidays", {}),
            )
            return instance
        return cls()

    def save(self) -> None:
        serializable = asdict(self)
        serializable["daily_schedule"] = {
            day: [asdict(event) for event in events]
            for day, events in self.daily_schedule.items()
        }
        CONFIG_PATH.write_text(json.dumps(serializable, indent=2, ensure_ascii=False), encoding="utf-8")

    def next_event_for_day(self, day_name: str, current_time: time) -> Optional[BellEvent]:
        events = self.daily_schedule.get(day_name, [])
        for event in sorted(events, key=lambda evt: evt.clock):
            event_time = parse_time(event.clock)
            if (event_time.hour, event_time.minute) >= (current_time.hour, current_time.minute):
                return event
        return None

    def add_event(self, day: str, label: str, clock: str, sound_type: str) -> None:
        self.daily_schedule.setdefault(day, []).append(
            BellEvent(label=label, clock=clock, sound_type=sound_type)
        )
        # Keep events ordered
        self.daily_schedule[day].sort(key=lambda evt: evt.clock)
        self.save()

    def delete_event(self, day: str, index: int) -> None:
        if 0 <= index < len(self.daily_schedule.get(day, [])):
            self.daily_schedule[day].pop(index)
            self.save()

    def update_event(self, day: str, index: int, label: str, clock: str, sound_type: str) -> None:
        events = self.daily_schedule.setdefault(day, [])
        if 0 <= index < len(events):
            events[index] = BellEvent(label=label, clock=clock, sound_type=sound_type)
            events.sort(key=lambda evt: evt.clock)
            self.save()

    def copy_day_schedule(self, source_day: str, target_day: str) -> None:
        """Copy all bell events from source day to target day."""
        events = [
            BellEvent(label=event.label, clock=event.clock, sound_type=event.sound_type)
            for event in self.daily_schedule.get(source_day, [])
        ]
        self.daily_schedule[target_day] = events
        self.save()

    def copy_day_schedule_to_many(self, source_day: str, target_days: List[str]) -> None:
        for day in target_days:
            if day == source_day:
                continue
            self.copy_day_schedule(source_day, day)

    def add_holiday(self, date_str: str, description: str) -> None:
        self.holidays[date_str] = description
        self.save()

    def remove_holiday(self, date_str: str) -> None:
        if date_str in self.holidays:
            del self.holidays[date_str]
            self.save()

    def holiday_for(self, day: date) -> Optional[str]:
        return self.holidays.get(day.strftime("%Y-%m-%d"))


__all__ = ["BellConfig", "BellEvent", "WEEKDAYS", "parse_time", "time_to_str"]
