@echo off
setlocal EnableExtensions EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "PROJECT_ROOT=%%~fI"
pushd "%PROJECT_ROOT%" >nul

if "%~1"=="" (
    set "PY=python"
) else (
    set "PY=%~1"
)

set "FFMPEG_CACHE=%SCRIPT_DIR%ffmpeg-bin"
if not exist "%FFMPEG_CACHE%" (
    mkdir "%FFMPEG_CACHE%"
)

set "LOGFILE=%SCRIPT_DIR%build_exe.log"
type nul >"%LOGFILE%"
echo === JinniBell Pro derleme kaydı: %DATE% %TIME% ===>>"%LOGFILE%"

echo [+] FFmpeg denetlemesi yapılıyor (Python tabanlı)...
call :run "%PY%" packaging\get_ffmpeg.py "%FFMPEG_CACHE%"

echo [+] pip güncelleniyor...
call :run "%PY%" -m pip install --upgrade pip

echo [+] Gerekli Python paketleri indiriliyor...
call :run "%PY%" -m pip install -r "%PROJECT_ROOT%\requirements.txt" pyinstaller

echo [+] PyInstaller ile JinniBell Pro oluşturuluyor...
call :run pyinstaller --noconfirm --noconsole --name "JinniBellPro" --add-data "%PROJECT_ROOT%\bell_app;bell_app" --add-binary "%FFMPEG_CACHE%\ffmpeg.exe;ffmpeg" --add-binary "%FFMPEG_CACHE%\ffprobe.exe;ffmpeg" "%PROJECT_ROOT%\main.py"

echo [✓] Derleme tamamlandı. Ayrıntılı günlük: "%LOGFILE%"
goto :finish

:run
set "CMD=%*"
echo     komut: %CMD%
echo --- %DATE% %TIME% : %CMD% --- >>"%LOGFILE%"
%CMD% >>"%LOGFILE%" 2>&1
if errorlevel 1 goto :fail
exit /b 0

:fail
echo [X] Hata oluştu. Ayrıntılar için "%LOGFILE%" dosyasına bakın.
set "BUILD_ERROR=1"
goto :finish

:finish
popd >nul
endlocal & set "BUILD_ERROR=%BUILD_ERROR%"
if defined BUILD_ERROR (
    if not "%NOPAUSE%"=="1" pause
    exit /b 1
)
if not "%NOPAUSE%"=="1" pause
exit /b 0
