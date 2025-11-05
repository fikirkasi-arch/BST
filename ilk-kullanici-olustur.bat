@echo off
chcp 65001 >nul

echo ==================================
echo 👤 İlk Admin Kullanıcısı Oluştur
echo ==================================
echo.

set /p username="Kullanıcı adı (örn: admin): "
set /p email="Email (örn: admin@okul.com): "
set /p password="Şifre: "
set /p fullname="Tam adınız (örn: Ahmet Yılmaz): "

echo.
echo Kullanıcı oluşturuluyor...

curl -X POST http://localhost:5000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"%username%\", \"email\": \"%email%\", \"password\": \"%password%\", \"full_name\": \"%fullname%\", \"role\": \"admin\"}"

echo.
echo.
echo ==================================
echo ✅ Kullanıcı oluşturuldu!
echo ==================================
echo.
echo Şimdi http://localhost:3000 adresinden giriş yapabilirsiniz.
echo.
pause
