@echo off
chcp 65001 >nul

echo ==================================
echo 🏫 Okul SMS Sistemi - Kurulum
echo ==================================
echo.

REM Docker kurulu mu kontrol et
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker kurulu değil!
    echo Docker'ı kurmak için: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose kurulu değil!
    pause
    exit /b 1
)

echo ✅ Docker ve Docker Compose kurulu
echo.

REM Eski containerları durdur
echo 📦 Eski container'lar durduruluyor...
docker-compose down

REM Container'ları başlat
echo 🚀 Sistem başlatılıyor...
docker-compose up -d

echo.
echo ⏳ Veritabanının hazır olması bekleniyor...
timeout /t 10 /nobreak >nul

echo.
echo ==================================
echo ✅ Kurulum tamamlandı!
echo ==================================
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔌 Backend API: http://localhost:5000
echo 🗄️  Veritabanı: localhost:5432
echo.
echo 📋 İlk kullanıcı oluşturmak için:
echo    ilk-kullanici-olustur.bat
echo.
echo 📊 Logları görmek için:
echo    docker-compose logs -f
echo.
echo ⏹️  Durdurmak için:
echo    docker-compose down
echo.
pause
