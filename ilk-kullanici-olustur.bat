@echo off
chcp 65001 >nul 2>&1

echo ==========================================
echo Ilk Admin Kullanicisi Olustur
echo ==========================================
echo.

set /p username="Kullanici adi (ornek: admin): "
set /p email="Email (ornek: admin@okul.com): "
set /p password="Sifre: "
set /p fullname="Tam adiniz (ornek: Ahmet Yilmaz): "

echo.
echo Kullanici olusturuluyor...
echo.

curl -X POST http://localhost:5000/api/auth/register -H "Content-Type: application/json" -d "{\"username\": \"%username%\", \"email\": \"%email%\", \"password\": \"%password%\", \"full_name\": \"%fullname%\", \"role\": \"admin\"}"

echo.
echo.
echo ==========================================
echo Kullanici olusturuldu!
echo ==========================================
echo.
echo Simdi http://localhost:3000 adresinden giris yapabilirsiniz.
echo.
pause
