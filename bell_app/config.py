"""Configuration management for the bell scheduler application."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import date, time
from pathlib import Path
from typing import Dict, List, Optional, TypedDict
from uuid import uuid4

def _resolve_data_dir() -> Path:
    """Kullanılabilir en iyi veri dizinini belirle."""

    override = os.environ.get("JINNIBELL_DATA_DIR")
    if override:
        return Path(override)

    if os.name == "nt":
        appdata = os.environ.get("APPDATA") or os.environ.get("LOCALAPPDATA")
        if appdata:
            return Path(appdata) / "JinniBellPro"

    try:
        return Path.home() / ".jinnibellpro"
    except Exception:
        # Bazı ortamlarda kullanıcı dizini çözümlenemez; çalışma dizinine düş.
        return Path.cwd() / "jinnibellpro_data"


DATA_DIR = _resolve_data_dir()
CONFIG_PATH = DATA_DIR / "config.json"
MEDIA_DIR = DATA_DIR / "JinniBellSesler"
SOUND_ROUTE_KEYS = [
    "student_entry",
    "teacher_entry",
    "lesson_exit",
    "recess_music",
    "istiklal",
    "siren",
    "moment_of_silence",
]

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


def ensure_data_dir() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR


def ensure_media_dir() -> Path:
    ensure_data_dir()
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    return MEDIA_DIR


class CeremonyItem(TypedDict, total=False):
    label: str
    source: str  # "file" or "youtube"
    location: str
    start_ms: int
    end_ms: Optional[int]
    duration_sec: Optional[int]
    status: str
    status_detail: Optional[str]
    cache_path: Optional[str]


class SoundAsset(TypedDict, total=False):
    asset_id: str
    name: str
    path: str
    tags: List[str]


class SoundZone(TypedDict, total=False):
    zone_id: str
    name: str
    color: str
    enabled: bool
    note: str


def _default_announcement_settings() -> Dict[str, Dict[str, object]]:
    keys = ["student_entry", "teacher_entry", "lesson_exit", "recess_music"]
    return {key: {"enabled": False, "path": ""} for key in keys}


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
    auto_shutdown_mode: str = "disabled"
    auto_shutdown_delay_minutes: int = 10
    ceremony_playlist: List[CeremonyItem] = field(default_factory=list)
    recess_music_enabled: bool = False
    holidays: Dict[str, str] = field(default_factory=dict)
    sound_library: List[SoundAsset] = field(default_factory=list)
    launch_on_boot: bool = False
    launch_on_boot_service: bool = False
    announcement_settings: Dict[str, Dict[str, object]] = field(
        default_factory=_default_announcement_settings
    )
    theme_mode: str = "light"
    touch_mode: bool = False
    sound_zones: List[SoundZone] = field(
        default_factory=lambda: [
            {
                "zone_id": "main",
                "name": "Genel Salon",
                "color": "#2563eb",
                "enabled": True,
                "note": "Varsayılan çıkış",
            }
        ]
    )
    sound_routes: Dict[str, List[str]] = field(
        default_factory=lambda: {key: ["main"] for key in SOUND_ROUTE_KEYS}
    )

    @classmethod
    def load(cls) -> "BellConfig":
        ensure_data_dir()
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

            library: List[SoundAsset] = []
            for raw_asset in data.get("sound_library", []):
                tags = raw_asset.get("tags") or []
                if isinstance(tags, str):
                    tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
                asset: SoundAsset = {
                    "asset_id": raw_asset.get("asset_id") or uuid4().hex,
                    "name": raw_asset.get("name", "Ses Dosyası"),
                    "path": raw_asset.get("path", ""),
                    "tags": list(tags),
                }
                library.append(asset)

            announcement_settings = _default_announcement_settings()
            raw_announcements = data.get("announcement_settings") or {}
            for key, value in raw_announcements.items():
                if key not in announcement_settings:
                    announcement_settings[key] = {"enabled": False, "path": ""}
                announcement_settings[key]["enabled"] = bool(value.get("enabled", False))
                announcement_settings[key]["path"] = value.get("path", "")

            zones: List[SoundZone] = []
            for raw in data.get("sound_zones", []):
                if not raw:
                    continue
                zones.append(
                    {
                        "zone_id": raw.get("zone_id") or uuid4().hex,
                        "name": raw.get("name", "Bölge"),
                        "color": raw.get("color", "#2563eb"),
                        "enabled": bool(raw.get("enabled", True)),
                        "note": raw.get("note", ""),
                    }
                )
            if not zones:
                zones = [
                    {
                        "zone_id": "main",
                        "name": "Genel Salon",
                        "color": "#2563eb",
                        "enabled": True,
                        "note": "Varsayılan çıkış",
                    }
                ]

            routes: Dict[str, List[str]] = {key: ["main"] for key in SOUND_ROUTE_KEYS}
            raw_routes = data.get("sound_routes") or {}
            for key, value in raw_routes.items():
                if isinstance(value, list):
                    routes[key] = [str(v) for v in value if v]
                elif isinstance(value, str):
                    routes[key] = [v.strip() for v in value.split(",") if v.strip()]

            instance = cls(
                daily_schedule={**{day: [] for day in WEEKDAYS}, **schedule},
                sound_files=data.get("sound_files", {}),
                volume=data.get("volume", 0.8),
                muted=data.get("muted", False),
                auto_shutdown_enabled=data.get("auto_shutdown_enabled", False),
                auto_shutdown_time=data.get("auto_shutdown_time"),
                auto_shutdown_mode=data.get("auto_shutdown_mode")
                or ("time" if data.get("auto_shutdown_enabled") else "disabled"),
                auto_shutdown_delay_minutes=data.get("auto_shutdown_delay_minutes", 10),
                ceremony_playlist=playlist,
                recess_music_enabled=data.get("recess_music_enabled", False),
                holidays=data.get("holidays", {}),
                sound_library=library,
                launch_on_boot=data.get("launch_on_boot", False),
                launch_on_boot_service=data.get("launch_on_boot_service", False),
                announcement_settings=announcement_settings,
                theme_mode=data.get("theme_mode", "light"),
                touch_mode=bool(data.get("touch_mode", False)),
                sound_zones=zones,
                sound_routes=routes,
            )
            return instance
        return cls()

    def save(self) -> None:
        ensure_data_dir()
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

    # region sound library helpers
    def add_sound_asset(self, name: str, path: str, tags: Optional[List[str]] = None) -> SoundAsset:
        asset: SoundAsset = {
            "asset_id": uuid4().hex,
            "name": name or Path(path).stem,
            "path": path,
            "tags": list(tags or []),
        }
        self.sound_library.append(asset)
        self.save()
        return asset

    def update_sound_asset(self, asset_id: str, *, name: Optional[str] = None, tags: Optional[List[str]] = None) -> None:
        for asset in self.sound_library:
            if asset.get("asset_id") == asset_id:
                if name is not None:
                    asset["name"] = name
                if tags is not None:
                    asset["tags"] = list(tags)
                self.save()
                break

    def remove_sound_asset(self, asset_id: str) -> None:
        self.sound_library = [asset for asset in self.sound_library if asset.get("asset_id") != asset_id]
        self.save()

    def get_sound_asset(self, asset_id: str) -> Optional[SoundAsset]:
        for asset in self.sound_library:
            if asset.get("asset_id") == asset_id:
                return asset
        return None

    def find_sound_asset_by_name(self, name: str) -> Optional[SoundAsset]:
        name_lower = name.strip().lower()
        for asset in self.sound_library:
            if asset.get("name", "").strip().lower() == name_lower:
                return asset
        return None

    def find_sound_asset_by_path(self, path: str) -> Optional[SoundAsset]:
        normalized = str(Path(path))
        for asset in self.sound_library:
            if str(Path(asset.get("path", ""))) == normalized:
                return asset
        return None

    def announcement_for(self, sound_key: str) -> Optional[Dict[str, str]]:
        data = self.announcement_settings.get(sound_key)
        if not data or not data.get("enabled"):
            return None
        path = data.get("path", "")
        if not path:
            return None
        return {"path": path}

    # endregion


__all__ = [
    "BellConfig",
    "BellEvent",
    "WEEKDAYS",
    "parse_time",
    "time_to_str",
    "SoundAsset",
    "MEDIA_DIR",
    "ensure_media_dir",
]
