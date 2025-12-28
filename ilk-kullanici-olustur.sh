#!/bin/bash

echo "=================================="
echo "👤 İlk Admin Kullanıcısı Oluştur"
echo "=================================="
echo ""

read -p "Kullanıcı adı (örn: admin): " username
read -p "Email (örn: admin@okul.com): " email
read -s -p "Şifre: " password
echo ""
read -p "Tam adınız (örn: Ahmet Yılmaz): " fullname

echo ""
echo "Kullanıcı oluşturuluyor..."

curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$username\",
    \"email\": \"$email\",
    \"password\": \"$password\",
    \"full_name\": \"$fullname\",
    \"role\": \"admin\"
  }"

echo ""
echo ""
echo "=================================="
echo "✅ Kullanıcı oluşturuldu!"
echo "=================================="
echo ""
echo "Şimdi http://localhost:3000 adresinden giriş yapabilirsiniz."
echo ""
