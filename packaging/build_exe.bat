@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%.." >nul

if "%~1"=="" (
    set "PY=python"
) else (
    set "PY=%~1"
)

set "FFMPEG_CACHE=%SCRIPT_DIR%ffmpeg-bin"
if not exist "%FFMPEG_CACHE%" (
    mkdir "%FFMPEG_CACHE%"
)
echo [+] FFmpeg denetlemesi yapılıyor (Python tabanlı)...
%PY% packaging\get_ffmpeg.py "%FFMPEG_CACHE%"

%PY% -m pip install --upgrade pip
%PY% -m pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm --noconsole --name "JinniBellPro" ^
    --add-data "bell_app;bell_app" ^
    --add-binary "packaging\ffmpeg-bin\ffmpeg.exe;ffmpeg" ^
    --add-binary "packaging\ffmpeg-bin\ffprobe.exe;ffmpeg" ^
    main.py

popd >nul
endlocal
