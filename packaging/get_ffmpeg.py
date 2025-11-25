"""Download and extract FFmpeg/FFprobe/FFplay binaries for packaging.

This helper avoids relying on PowerShell so that the Windows build
script works on every edition/architecture supported by Python.
"""
from __future__ import annotations

import os
import shutil
import socket
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from urllib.error import URLError

_console_fallback = None

FFMPEG_URLS = (
    ("ffmpeg-7.0.1-essentials_build.zip", "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.0.1-essentials_build.zip"),
    ("ffmpeg-7.0-essentials_build.zip", "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.0-essentials_build.zip"),
    ("ffmpeg-release-essentials.zip", "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"),
    ("ffmpeg-master-latest-win64-gpl.zip", "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"),
)
SDL2_URLS = (
    (
        "SDL2-2.30.7-win32-x64.zip",
        "https://github.com/libsdl-org/SDL/releases/download/release-2.30.7/SDL2-2.30.7-win32-x64.zip",
    ),
    (
        "SDL2-2.30.5-win32-x64.zip",
        "https://github.com/libsdl-org/SDL/releases/download/release-2.30.5/SDL2-2.30.5-win32-x64.zip",
    ),
)
SDL2_LOCAL_NAMES = ("sdl2-offline.zip", "sdl2.zip")
LOCAL_ARCHIVE_NAMES = ("ffmpeg-offline.zip", "ffmpeg.zip")
DOWNLOAD_TIMEOUT = int(os.environ.get("FFMPEG_TIMEOUT", "45"))

MANUAL_INSTRUCTIONS = (
    "1) İnternet erişiminiz kısıtlıysa https://www.gyan.dev/ffmpeg/builds/ adresindeki",
    "   *latest release* sayfasından `ffmpeg-release-essentials.zip` veya",
    "   https://github.com/BtbN/FFmpeg-Builds/releases adresinden `ffmpeg-master-latest-win64-gpl.zip`",
    "   paketlerinden birini indirin.",
    "2) Arşivi açmadan, zip dosyasını `packaging/ffmpeg-offline.zip` adıyla kopyalayın",
    "   ya da doğrudan dışarıda tuttuğunuz yol için `FFMPEG_ZIP_PATH` ortam değişkenini set edin.",
    "3) SDL2 için https://github.com/libsdl-org/SDL/releases sayfasından",
    "   `SDL2-*-win32-x64.zip` dosyasını indirip `packaging/sdl2-offline.zip` adıyla kopyalayın",
    "   ya da `SDL2_ZIP_PATH` ile yol gösterin.",
    "4) Alternatif olarak, bir kez indirip hazırladığınız `packaging/ffmpeg-bin` klasörünü",
    "   olduğu gibi PyInstaller komutunda `--add-data` ile ekleyebilir veya oluşan `dist/ffmpeg`",
    "   klasörünü son kullanıcı dizinine manuel kopyalayabilirsiniz.",
)


def _write_console(line: str) -> None:
    """Best-effort mirror of log lines to the visible console on Windows."""

    global _console_fallback  # noqa: PLW0603 - cache handle for reuse

    if os.name != "nt":  # Only Windows exposes CONOUT$
        return

    try:
        is_tty = sys.stdout.isatty()
    except Exception:  # pragma: no cover - very unlikely on Windows
        is_tty = False

    if is_tty:
        return

    if _console_fallback is None:
        try:
            _console_fallback = open("CONOUT$", "w", encoding="utf-8", errors="ignore")
        except OSError:
            _console_fallback = False
            return

    if _console_fallback:
        _console_fallback.write(line + "\n")
        _console_fallback.flush()


def log(message: str) -> None:
    line = f"[get_ffmpeg] {message}"
    print(line, flush=True)
    _write_console(line)


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
            with urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT) as response, open(
                zip_path, "wb"
            ) as dst:
                shutil.copyfileobj(response, dst)
        except (URLError, TimeoutError, socket.timeout) as exc:
            errors.append(f"{label}: {exc}")
            log(f"İndirme başarısız ({label}): {exc}")
            continue

        log(f"İndirme tamamlandı: {label}")
        return

    error_lines = " ; ".join(errors) if errors else "Bilinmeyen hata"
    guide = "\n".join(MANUAL_INSTRUCTIONS)
    raise RuntimeError(
        "FFmpeg indirilemedi. Bilgisayarınız internete çıkamıyorsa veya SSL doğrulaması"
        " engelleniyorsa aşağıdaki adımları izleyin:\n\n"
        f"{guide}\n\n"
        f"Denenen URL'ler: {error_lines}"
    )


def _download_sdl2(target_dir: Path) -> bool:
    """SDL2.dll eksikse yerel arşiv veya internetten indirme ile tamamla."""

    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = Path(tmp_dir) / "sdl2.zip"

        local_archive = find_local_sdl_archive()
        if local_archive:
            log(f"Yerel SDL2 arşivi bulundu: {local_archive}")
            shutil.copy2(local_archive, zip_path)
            sources = [(zip_path.name, str(local_archive))]
        else:
            sources = SDL2_URLS

        for label, url in sources:
            if not local_archive:
                log(f"SDL2 paketi indirilmeye çalışılıyor: {label} ({url})")
                try:
                    with urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT) as response, open(
                        zip_path, "wb"
                    ) as dst:
                        shutil.copyfileobj(response, dst)
                except (URLError, TimeoutError, socket.timeout) as exc:
                    log(f"SDL2 indirilemedi ({label}): {exc}")
                    continue

            try:
                with zipfile.ZipFile(zip_path) as zf:
                    candidates = [name for name in zf.namelist() if name.lower().endswith("sdl2.dll")]
                    if not candidates:
                        log(f"SDL2 arşivinde DLL bulunamadı: {label}")
                        continue
                    dll_name = candidates[0]
                    extract_dir = Path(tmp_dir) / "sdl_extract"
                    zf.extract(dll_name, extract_dir)
                    src_path = extract_dir / dll_name
                    shutil.copy2(src_path, target_dir / "SDL2.dll")
                    log("SDL2.dll indirildi ve ffmpeg klasörüne kopyalandı")
                    return True
            except zipfile.BadZipFile as exc:  # pragma: no cover - bozuk arşiv durumunda
                log(f"SDL2 arşivi açılamadı: {exc}")
                continue

    return False


def find_local_sdl_archive() -> Path | None:
    """Kullanıcı tarafından sağlanan SDL2 arşivini bul."""

    candidates: list[Path] = []
    env_path = os.environ.get("SDL2_ZIP_PATH")
    if env_path:
        candidates.append(Path(env_path))

    script_dir = Path(__file__).parent
    for name in SDL2_LOCAL_NAMES:
        candidates.append(script_dir / name)
        candidates.append(script_dir / "cache" / name)
        candidates.append(script_dir / "assets" / name)

    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def ensure_binaries(target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    required = ["ffmpeg.exe", "ffprobe.exe", "ffplay.exe"]
    optional = ["SDL2.dll"] if os.name == "nt" else []
    if all((target_dir / name).exists() for name in required):
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
        for child in target_dir.iterdir():
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                shutil.rmtree(child)
        for item in bin_dir.iterdir():
            destination = target_dir / item.name
            if item.is_dir():
                shutil.copytree(item, destination)
            else:
                shutil.copy2(item, destination)
        missing = [name for name in required if not (target_dir / name).exists()]
        if missing:
            raise RuntimeError(
                "FFmpeg arşivinde eksik dosyalar var: " + ", ".join(missing) + ". Lütfen tam paket indirin."
            )

        missing_optional = [name for name in optional if not (target_dir / name).exists()]
        if missing_optional:
            log("FFmpeg arşivinde isteğe bağlı dosyalar eksik: " + ", ".join(missing_optional))
            if _download_sdl2(target_dir):
                missing_optional = [name for name in optional if not (target_dir / name).exists()]

        if missing_optional:
            guide = "\n".join(MANUAL_INSTRUCTIONS)
            raise RuntimeError(
                "SDL2.dll bulunamadı. ffplay ses çıkışı için SDL2.dll zorunludur. Aşağıdaki"
                " çevrimdışı kopyalama adımlarını izleyin:\n\n" + guide
            )
        log(f"Binaries copied into {target_dir}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python get_ffmpeg.py <target_dir>", file=sys.stderr)
        raise SystemExit(1)

    target_dir = Path(sys.argv[1])
    ensure_binaries(target_dir)


if __name__ == "__main__":
    main()
