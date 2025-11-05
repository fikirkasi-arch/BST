# 🚀 Okul SMS Sistemi - Hızlı Başlangıç Kılavuzu

## 📋 Gereksinimler

Sistemi çalıştırmak için sadece **Docker** gereklidir:
- Docker Desktop (Windows/Mac)
- Docker + Docker Compose (Linux)

## 🎯 1 Dakikada Başlatma

### Windows Kullanıcıları

1. **Docker Desktop'ı başlatın**
2. Proje klasörüne gidin
3. `kurulum.bat` dosyasına çift tıklayın
4. **10 saniye bekleyin**
5. `ilk-kullanici-olustur.bat` dosyasına çift tıklayın
6. Bilgilerinizi girin
7. Tarayıcıda `http://localhost:3000` adresini açın
8. Giriş yapın!

### Mac/Linux Kullanıcıları

Terminal'de:

```bash
# Sistemi başlat
./kurulum.sh

# İlk kullanıcıyı oluştur
./ilk-kullanici-olustur.sh

# Tarayıcıda aç
open http://localhost:3000  # Mac
xdg-open http://localhost:3000  # Linux
```

## 📱 Sisteme Giriş

1. Tarayıcıda: `http://localhost:3000`
2. Oluşturduğunuz kullanıcı adı ve şifre ile giriş yapın
3. Ana sayfa açılacak!

## 🎓 İlk Adımlar

### 1. Öğrenci Ekleyin

- Sol menüden **Öğrenciler**'e tıklayın
- **Yeni Öğrenci** butonuna tıklayın
- Öğrenci ve veli bilgilerini girin
- Kaydedin!

### 2. Mesaj Gönderin

- Sol menüden **Mesaj Gönder**'e tıklayın
- Mesaj tipini seçin (SMS veya WhatsApp)
- Alıcıları seçin (Tüm veliler, belirli sınıf, vb.)
- Mesajınızı yazın
- Gönder!

### 3. Mesaj Şablonları Kullanın

Mesajlarınızda bu değişkenleri kullanabilirsiniz:
- `{ad}` - Alıcının adı
- `{soyad}` - Alıcının soyadı
- `{tam_ad}` - Alıcının tam adı

**Örnek:**
```
Sayın {tam_ad},

Çocuğunuz bugün okula gelmemiştir.
Lütfen okul idaresi ile iletişime geçiniz.

Saygılarımızla,
Okul İdaresi
```

## 🔌 SMS ve WhatsApp Kurulumu

### SMS Göndermek İçin

1. **NetGSM** (Türkiye) veya **Twilio** hesabı açın
2. `backend/.env` dosyasını düzenleyin:

```env
# NetGSM için
NETGSM_USERNAME=kullanici_adiniz
NETGSM_PASSWORD=sifreniz
NETGSM_HEADER=OKUL_ADINIZ

# veya Twilio için
TWILIO_ACCOUNT_SID=account_sid
TWILIO_AUTH_TOKEN=auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

3. Sistemi yeniden başlatın:
```bash
docker-compose restart backend
```

### WhatsApp Göndermek İçin

1. Backend loglarını açın:
```bash
docker-compose logs -f backend
```

2. QR kod göründüğünde, WhatsApp uygulamanızdan tarayın:
   - WhatsApp'ı açın
   - Ayarlar > Bağlı Cihazlar
   - Cihaz Bağla
   - QR kodu tarayın

3. Bağlantı kuruldu! Artık WhatsApp mesajı gönderebilirsiniz.

## 📊 Sistem Durumunu Görüntüleme

### Tüm servislerin durumunu kontrol et
```bash
docker-compose ps
```

### Logları görüntüle
```bash
# Tüm loglar
docker-compose logs -f

# Sadece backend
docker-compose logs -f backend

# Sadece frontend
docker-compose logs -f frontend
```

### Sistemi durdur
```bash
docker-compose down
```

### Sistemi yeniden başlat
```bash
docker-compose restart
```

## 🌐 Web Sunucusuna Kurulum

Sistemi internetten erişilebilir hale getirmek için:

### 1. Sunucu Gereksinimleri
- Ubuntu 20.04+ veya benzer Linux
- Docker ve Docker Compose kurulu
- Domain veya subdomain

### 2. Dosyaları Sunucuya Yükleyin

```bash
# Yerel bilgisayarınızdan
scp -r BST/ kullanici@sunucu-ip:/home/kullanici/
```

### 3. Ortam Değişkenlerini Ayarlayın

```bash
# Sunucuda
cd /home/kullanici/BST

# Backend .env dosyasını düzenleyin
nano backend/.env
```

Değiştirin:
```env
NODE_ENV=production
CORS_ORIGIN=https://sizin-domain.com
```

Frontend .env:
```env
VITE_API_URL=https://api.sizin-domain.com/api
```

### 4. Nginx ile Reverse Proxy Kurun

```bash
sudo apt install nginx

# Nginx konfigürasyonu
sudo nano /etc/nginx/sites-available/okul-sms
```

```nginx
server {
    listen 80;
    server_name sizin-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Aktif et
sudo ln -s /etc/nginx/sites-available/okul-sms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL Sertifikası Ekleyin (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d sizin-domain.com
```

### 6. Sistemi Başlatın

```bash
cd /home/kullanici/BST
./kurulum.sh
```

## 🛠️ Sorun Giderme

### "Port zaten kullanımda" Hatası

Başka bir uygulama portu kullanıyor. Portları değiştirin:

```bash
# docker-compose.yml dosyasını düzenleyin
nano docker-compose.yml
```

```yaml
ports:
  - "5001:5000"  # Backend için
  - "3001:3000"  # Frontend için
```

### Veritabanına Bağlanamıyor

```bash
# PostgreSQL loglarını kontrol edin
docker-compose logs postgres

# Container'ı yeniden başlatın
docker-compose restart postgres
```

### WhatsApp QR Kod Görünmüyor

```bash
# Backend loglarını kontrol edin
docker-compose logs backend

# Backend'i yeniden başlatın
docker-compose restart backend
```

## 📞 Destek

Sorun yaşıyorsanız:
1. Önce logları kontrol edin: `docker-compose logs -f`
2. Docker'ın çalıştığından emin olun
3. Port'ların boş olduğundan emin olun

## 🎉 Artık Hazırsınız!

Sistemin tüm özellikleri kullanıma hazır:
- ✅ Toplu SMS gönderimi
- ✅ Toplu WhatsApp mesajı
- ✅ Öğrenci ve veli yönetimi
- ✅ Mesaj geçmişi
- ✅ Zamanlanmış mesajlar
- ✅ Mesaj şablonları

**İyi kullanımlar!** 🏫📱
