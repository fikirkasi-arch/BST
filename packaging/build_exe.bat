@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%.." >nul

if "%~1"=="" (
    set "PY=python"
) else (
    set "PY=%~1"
)

set "FFMPEG_URL=https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-6.0-essentials_build.zip"
set "FFMPEG_CACHE=%SCRIPT_DIR%ffmpeg-bin"
if not exist "%FFMPEG_CACHE%" (
    mkdir "%FFMPEG_CACHE%"
)
if not exist "%FFMPEG_CACHE%\ffmpeg.exe" (
    echo [+] FFmpeg bulunamadı, indiriliyor...
    powershell -NoLogo -NoProfile -Command ^
        "$ErrorActionPreference='Stop';" ^
        "$zip=Join-Path $env:TEMP 'ffmpeg-package.zip';" ^
        "Invoke-WebRequest -Uri '%FFMPEG_URL%' -OutFile $zip;" ^
        "$extract=Join-Path $env:TEMP 'ffmpeg-extract';" ^
        "if (Test-Path $extract) { Remove-Item $extract -Recurse -Force; }" ^
        "Expand-Archive -LiteralPath $zip -DestinationPath $extract -Force;" ^
        "$folder = Get-ChildItem $extract | Where-Object { $_.PSIsContainer } | Select-Object -First 1;" ^
        "Copy-Item (Join-Path $folder.FullName 'bin\\ffmpeg.exe') -Destination '%FFMPEG_CACHE%\ffmpeg.exe' -Force;" ^
        "Copy-Item (Join-Path $folder.FullName 'bin\\ffprobe.exe') -Destination '%FFMPEG_CACHE%\ffprobe.exe' -Force;" ^
        "Remove-Item $extract -Recurse -Force;" ^
        "Remove-Item $zip -Force;"
)

%PY% -m pip install --upgrade pip
%PY% -m pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm --noconsole --name "OkulZilAsistani" ^
    --add-data "bell_app;bell_app" ^
    --add-binary "packaging\ffmpeg-bin\ffmpeg.exe;ffmpeg" ^
    --add-binary "packaging\ffmpeg-bin\ffprobe.exe;ffmpeg" ^
    main.py

popd >nul
endlocal
