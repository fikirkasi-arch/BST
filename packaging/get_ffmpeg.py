"""Download and extract FFmpeg/FFprobe binaries for packaging.

This helper avoids relying on PowerShell so that the Windows build
script works on every edition/architecture supported by Python.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from urllib.error import URLError

FFMPEG_URLS = (
    ("ffmpeg-7.0.1-essentials_build.zip", "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.0.1-essentials_build.zip"),
    ("ffmpeg-7.0-essentials_build.zip", "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.0-essentials_build.zip"),
    ("ffmpeg-release-essentials.zip", "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"),
    ("ffmpeg-master-latest-win64-gpl.zip", "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"),
)
LOCAL_ARCHIVE_NAMES = ("ffmpeg-offline.zip", "ffmpeg.zip")


def log(message: str) -> None:
    print(f"[get_ffmpeg] {message}")


def find_local_archive() -> Path | None:
    """Return a user supplied FFmpeg archive if one exists."""

    candidates: list[Path] = []
    env_path = os.environ.get("FFMPEG_ZIP_PATH")
    if env_path:
        candidates.append(Path(env_path))

    script_dir = Path(__file__).parent
    for name in LOCAL_ARCHIVE_NAMES:
        candidates.append(script_dir / name)
        candidates.append(script_dir / "cache" / name)
        candidates.append(script_dir / "assets" / name)

    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def download_archive(zip_path: Path) -> None:
    """Try downloading FFmpeg from known mirrors before failing."""

    errors: list[str] = []
    for label, url in FFMPEG_URLS:
        log(f"FFmpeg paketi indirilmeye çalışılıyor: {label} ({url})")
        try:
            with urllib.request.urlopen(url) as response, open(zip_path, "wb") as dst:
                shutil.copyfileobj(response, dst)
        except URLError as exc:
            errors.append(f"{label}: {exc}")
            log(f"İndirme başarısız ({label}): {exc}")
            continue

        log(f"İndirme tamamlandı: {label}")
        return

    error_lines = " ; ".join(errors) if errors else "Bilinmeyen hata"
    raise RuntimeError(
        "FFmpeg indirilemedi. Bilgisayarınız internete çıkamıyorsa veya SSL doğrulaması"
        " engelleniyorsa, https://www.gyan.dev/ffmpeg/builds/ ya da"
        " https://github.com/BtbN/FFmpeg-Builds/releases adreslerinden"
        " listelenen paketlerden birini indirip 'ffmpeg-offline.zip' adıyla"
        " packaging klasörüne kopyalayın veya FFMPEG_ZIP_PATH değişkeniyle yol gösterin."
        f" Denenen URL'ler: {error_lines}"
    )


def ensure_binaries(target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_path = target_dir / "ffmpeg.exe"
    ffprobe_path = target_dir / "ffprobe.exe"

    if ffmpeg_path.exists() and ffprobe_path.exists():
        log("FFmpeg already cached, skipping download")
        return

    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = Path(tmp_dir) / "ffmpeg.zip"
        local_archive = find_local_archive()
        if local_archive:
            log(f"Yerel FFmpeg arşivi bulundu: {local_archive}")
            shutil.copy2(local_archive, zip_path)
        else:
            download_archive(zip_path)

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
