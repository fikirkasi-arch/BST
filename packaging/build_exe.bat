@echo off
setlocal
if "%~1"=="" (
    set PY=python
) else (
    set PY=%~1
)
%PY% -m pip install --upgrade pip
%PY% -m pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm --noconsole --name "OkulZilAsistani" --add-data "bell_app;bell_app" main.py
endlocal
