#!/bin/bash

echo "╔════════════════════════════════════════╗"
echo "║  📱 Okul SMS Sistemi - Manuel Kurulum ║"
echo "╔════════════════════════════════════════╗"
echo ""

# Node.js kontrolü
if ! command -v node &> /dev/null; then
    echo "❌ Node.js kurulu değil!"
    echo ""
    echo "Node.js'i kurmak için:"
    echo "Ubuntu/Debian: sudo apt install nodejs npm"
    echo "veya"
    echo "https://nodejs.org/en/download/ adresinden indirin"
    exit 1
fi

# PostgreSQL kontrolü
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL kurulu değil!"
    echo ""
    echo "PostgreSQL'i kurmak için:"
    echo "Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    exit 1
fi

echo "✅ Node.js yüklü: $(node --version)"
echo "✅ PostgreSQL yüklü"
echo ""

# Veritabanını oluştur
echo "📦 Veritabanı oluşturuluyor..."
sudo -u postgres psql << EOF
-- Veritabanını sil (varsa)
DROP DATABASE IF EXISTS okul_sms_db;
-- Yeni veritabanı oluştur
CREATE DATABASE okul_sms_db;
-- Kullanıcı oluştur (varsa geç)
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'postgres') THEN
    CREATE USER postgres WITH PASSWORD 'postgres123';
  END IF;
END
\$\$;
-- Yetkileri ver
GRANT ALL PRIVILEGES ON DATABASE okul_sms_db TO postgres;
EOF

# Veritabanı şemasını yükle
echo "📋 Veritabanı şeması yükleniyor..."
sudo -u postgres psql -d okul_sms_db < database/schema.sql

# Backend bağımlılıklarını yükle
echo "📦 Backend bağımlılıkları yükleniyor..."
cd backend
npm install
cd ..

# Frontend bağımlılıklarını yükle
echo "📦 Frontend bağımlılıkları yükleniyor..."
cd frontend
npm install
cd ..

echo ""
echo "╔════════════════════════════════════════╗"
echo "║          ✅ KURULUM TAMAMLANDI!        ║"
echo "╔════════════════════════════════════════╗"
echo ""
echo "🚀 Programı başlatmak için:"
echo ""
echo "Terminal 1'de (Backend):"
echo "   cd backend"
echo "   npm run dev"
echo ""
echo "Terminal 2'de (Frontend):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "Sonra tarayıcıda: http://localhost:3000"
echo ""
