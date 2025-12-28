@echo off
chcp 65001 >nul 2>&1

echo ==========================================
echo Okul SMS Sistemi - Kurulum
echo ==========================================
echo.

REM Docker kontrolu
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: Docker kurulu degil!
    echo.
    echo Docker'i indirmek icin:
    echo https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: Docker Compose kurulu degil!
    pause
    exit /b 1
)

echo OK: Docker ve Docker Compose kurulu
echo.

REM Eski container'lari durdur
echo Eski container'lar durduruluyor...
docker-compose down 2>nul

REM Container'lari baslat
echo.
echo Sistem baslatiliyor...
docker-compose up -d

echo.
echo Veritabaninin hazir olmasi bekleniyor...
timeout /t 15 /nobreak >nul

echo.
echo ==========================================
echo KURULUM TAMAMLANDI!
echo ==========================================
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:5000
echo Veritabani: localhost:5432
echo.
echo Ilk kullanici olusturmak icin:
echo    ilk-kullanici-olustur.bat
echo.
echo Loglari gormek icin:
echo    docker-compose logs -f
echo.
echo Durdurmak icin:
echo    docker-compose down
echo.
pause
