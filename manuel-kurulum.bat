@echo off
chcp 65001 >nul

echo ╔════════════════════════════════════════╗
echo ║  📱 Okul SMS Sistemi - Manuel Kurulum ║
echo ╔════════════════════════════════════════╗
echo.

REM Node.js kontrolü
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js kurulu değil!
    echo.
    echo Node.js'i kurmak için:
    echo https://nodejs.org/en/download/ adresinden indirin
    pause
    exit /b 1
)

REM PostgreSQL kontrolü
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL kurulu değil!
    echo.
    echo PostgreSQL'i kurmak için:
    echo https://www.postgresql.org/download/ adresinden indirin
    pause
    exit /b 1
)

echo ✅ Node.js yüklü
echo ✅ PostgreSQL yüklü
echo.

REM Veritabanını oluştur
echo 📦 Veritabanı oluşturuluyor...
psql -U postgres -c "DROP DATABASE IF EXISTS okul_sms_db;"
psql -U postgres -c "CREATE DATABASE okul_sms_db;"

REM Veritabanı şemasını yükle
echo 📋 Veritabanı şeması yükleniyor...
psql -U postgres -d okul_sms_db -f database\schema.sql

REM Backend bağımlılıklarını yükle
echo 📦 Backend bağımlılıkları yükleniyor...
cd backend
call npm install
cd ..

REM Frontend bağımlılıklarını yükle
echo 📦 Frontend bağımlılıkları yükleniyor...
cd frontend
call npm install
cd ..

echo.
echo ╔════════════════════════════════════════╗
echo ║          ✅ KURULUM TAMAMLANDI!        ║
echo ╔════════════════════════════════════════╗
echo.
echo 🚀 Programı başlatmak için:
echo.
echo 1. start-backend.bat dosyasına çift tıklayın
echo 2. start-frontend.bat dosyasına çift tıklayın
echo 3. Tarayıcıda http://localhost:3000 açın
echo.
pause
