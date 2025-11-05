#!/bin/bash

echo "=================================="
echo "🏫 Okul SMS Sistemi - Kurulum"
echo "=================================="
echo ""

# Docker kurulu mu kontrol et
if ! command -v docker &> /dev/null
then
    echo "❌ Docker kurulu değil!"
    echo "Docker'ı kurmak için: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null
then
    echo "❌ Docker Compose kurulu değil!"
    echo "Docker Compose'u kurmak için: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker ve Docker Compose kurulu"
echo ""

# Eski containerları durdur
echo "📦 Eski container'lar durduruluyor..."
docker-compose down

# Container'ları başlat
echo "🚀 Sistem başlatılıyor..."
docker-compose up -d

echo ""
echo "⏳ Veritabanının hazır olması bekleniyor..."
sleep 10

echo ""
echo "=================================="
echo "✅ Kurulum tamamlandı!"
echo "=================================="
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:5000"
echo "🗄️  Veritabanı: localhost:5432"
echo ""
echo "📋 İlk kullanıcı oluşturmak için:"
echo "   ./ilk-kullanici-olustur.sh"
echo ""
echo "📊 Logları görmek için:"
echo "   docker-compose logs -f"
echo ""
echo "⏹️  Durdurmak için:"
echo "   docker-compose down"
echo ""
