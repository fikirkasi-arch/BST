"""Download and extract FFmpeg/FFprobe binaries for packaging.

This helper avoids relying on PowerShell so that the Windows build
script works on every edition/architecture supported by Python.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-6.0-essentials_build.zip"


def log(message: str) -> None:
    print(f"[get_ffmpeg] {message}")


def ensure_binaries(target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_path = target_dir / "ffmpeg.exe"
    ffprobe_path = target_dir / "ffprobe.exe"

    if ffmpeg_path.exists() and ffprobe_path.exists():
        log("FFmpeg already cached, skipping download")
        return

    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = Path(tmp_dir) / "ffmpeg.zip"
        log(f"Downloading FFmpeg package to {zip_path}")
        with urllib.request.urlopen(FFMPEG_URL) as response, open(zip_path, "wb") as dst:
            shutil.copyfileobj(response, dst)

        extract_dir = Path(tmp_dir) / "extract"
        log(f"Extracting archive into {extract_dir}")
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)

        bin_dir = next(extract_dir.glob("*/bin"), None)
        if bin_dir is None:
            raise RuntimeError("FFmpeg archive format not recognized; bin folder missing")

        shutil.copy2(bin_dir / "ffmpeg.exe", ffmpeg_path)
        shutil.copy2(bin_dir / "ffprobe.exe", ffprobe_path)
        log(f"Binaries copied into {target_dir}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python get_ffmpeg.py <target_dir>", file=sys.stderr)
        raise SystemExit(1)

    target_dir = Path(sys.argv[1])
    ensure_binaries(target_dir)


if __name__ == "__main__":
    main()
