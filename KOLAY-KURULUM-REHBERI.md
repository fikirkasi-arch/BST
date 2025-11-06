# 🎯 OKUL SMS SİSTEMİ - SÜPER KOLAY KURULUM REHBERİ

## 📌 Adım 1: Gerekli Programları Kurun

### Windows Kullanıyorsanız:

**Yöntem A: Docker ile (ÖNERİLEN - En Kolay!)**
1. Docker Desktop indirin: https://www.docker.com/products/docker-desktop/
2. Kurun ve bilgisayarı yeniden başlatın
3. ✅ Hazır! Adım 2'ye geçin

**Yöntem B: Manuel (Docker olmadan)**
1. Node.js indirin: https://nodejs.org/ (LTS versiyonu)
2. PostgreSQL indirin: https://www.postgresql.org/download/
3. Her ikisini de kurun
4. ✅ Hazır! Adım 3'e geçin

### Linux Kullanıyorsanız:

**Yöntem A: Docker ile (ÖNERİLEN)**
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo usermod -aG docker $USER
```
Sonra çıkış yapıp tekrar giriş yapın.

**Yöntem B: Manuel (Docker olmadan)**
```bash
sudo apt update
sudo apt install nodejs npm postgresql postgresql-contrib -y
```

---

## 📌 Adım 2: Programı İndirin

1. `/home/user/BST-proje.zip` dosyasını bulun
2. Masaüstüne kopyalayın
3. Sağ tık > "Tümünü ayıkla"
4. "BST" klasörü oluşacak

---

## 📌 Adım 3: AYARLARI YAPIN (ÖNEMLİ!)

### 🔧 Ayar Dosyası: `backend/.env`

Bu dosyayı bir metin editörü ile açın (Notepad++, VS Code, veya basit Notepad).

**Değiştirmeniz gereken yerler:**

```env
# Veritabanı Ayarları (Docker kullanıyorsanız DOKUNMAYIN!)
DB_HOST=postgres              # Manuel kurulumda: localhost
DB_PORT=5432
DB_NAME=okul_sms_db
DB_USER=postgres
DB_PASSWORD=postgres123       # İsterseniz değiştirin

# Güvenlik (ÇOK ÖNEMLİ - Mutlaka değiştirin!)
JWT_SECRET=kendi_gizli_anahtariniz_12345

# SMS Ayarları (Opsiyonel - SMS göndermek için gerekli)
# NetGSM kullanıyorsanız:
NETGSM_USERNAME=netgsm_kullanici_adiniz
NETGSM_PASSWORD=netgsm_sifreniz
NETGSM_HEADER=OKUL_ADINIZ

# Twilio kullanıyorsanız:
TWILIO_ACCOUNT_SID=twilio_account_sid
TWILIO_AUTH_TOKEN=twilio_auth_token
TWILIO_PHONE_NUMBER=+905551234567

# WhatsApp (Otomatik kurulacak, dokunmayın)
WHATSAPP_SESSION_PATH=./whatsapp-session

# CORS (Web'de yayınlıyorsanız değiştirin)
CORS_ORIGIN=http://localhost:3000
# Canlıda: https://sizin-domain.com
```

### 📝 SMS Sağlayıcı Nereden Alınır?

**NetGSM (Türkiye için):**
- Website: https://www.netgsm.com.tr/
- Hesap açın
- API bilgilerinizi alın
- `backend/.env` dosyasına yazın

**Twilio (Uluslararası):**
- Website: https://www.twilio.com/
- Hesap açın (ücretsiz deneme var)
- Account SID ve Auth Token'ı alın
- `backend/.env` dosyasına yazın

---

## 📌 Adım 4: Programı ÇALIŞTIRIN!

### 🐳 Docker ile (Süper Kolay!)

**Windows:**
1. Docker Desktop'ı açın (yeşil logo görünene kadar bekleyin)
2. `kurulum.bat` dosyasına çift tıklayın
3. 30 saniye bekleyin
4. ✅ HAZIR!

**Linux:**
```bash
cd BST
./kurulum.sh
```

### 🔧 Manuel Kurulum ile

**Windows:**
1. `manuel-kurulum.bat` dosyasına çift tıklayın (ilk seferlik)
2. `start-backend.bat` dosyasına çift tıklayın
3. `start-frontend.bat` dosyasına çift tıklayın
4. ✅ HAZIR!

**Linux:**
```bash
cd BST
./manuel-kurulum.sh          # İlk seferlik
./start-backend.sh &         # Terminal 1
./start-frontend.sh          # Terminal 2
```

---

## 📌 Adım 5: İlk Kullanıcıyı Oluşturun

**Windows:**
1. `ilk-kullanici-olustur.bat` dosyasına çift tıklayın
2. Bilgilerinizi girin:
   - Kullanıcı adı: `admin`
   - Email: `admin@okul.com`
   - Şifre: `admin123` (sonra değiştirebilirsiniz)
   - Tam ad: `Okul Yöneticisi`

**Linux:**
```bash
./ilk-kullanici-olustur.sh
```

---

## 📌 Adım 6: Tarayıcıda Açın!

1. Tarayıcınızı açın (Chrome, Firefox, Safari, vb.)
2. Adres çubuğuna yazın: `http://localhost:3000`
3. Giriş yapın:
   - Kullanıcı adı: `admin`
   - Şifre: `admin123`
4. 🎉 HAZIR! Ana sayfa açılacak

---

## 🎓 İLK KULLANIMDA NELER YAPABİLİRSİNİZ?

### 1️⃣ Öğrenci Ekleyin

1. Sol menüden **"Öğrenciler"** tıklayın
2. Sağ üstteki **"+ Yeni Öğrenci"** butonuna tıklayın
3. Formu doldurun:
   - Öğrenci numarası
   - Ad, Soyad
   - Sınıf
   - Veli bilgileri (ad, soyad, telefon)
4. **"Kaydet"** butonuna tıklayın

### 2️⃣ Mesaj Gönderin

1. Sol menüden **"Mesaj Gönder"** tıklayın
2. Mesaj tipini seçin (SMS veya WhatsApp)
3. Alıcıları seçin:
   - Tüm veliler
   - Belirli bir sınıf
   - Seçili öğrenciler
4. Mesajınızı yazın (değişkenler kullanabilirsiniz)
5. **"Gönder"** butonuna tıklayın

**Mesaj Değişkenleri:**
- `{ad}` - Alıcının adı
- `{soyad}` - Alıcının soyadı
- `{tam_ad}` - Alıcının tam adı

**Örnek mesaj:**
```
Sayın {tam_ad},

Çocuğunuz bugün okula gelmemiştir.
Lütfen okul idaresi ile iletişime geçiniz.

Saygılarımızla,
[Okul Adınız]
```

### 3️⃣ WhatsApp Bağlantısı Kurun

**İlk çalıştırmada:**
1. Backend loglarına bakın (konsol/terminal)
2. QR kod göreceksiniz
3. WhatsApp uygulamanızı açın
4. Ayarlar > Bağlı Cihazlar > Cihaz Bağla
5. QR kodu tarayın
6. ✅ Bağlantı kuruldu!

**Docker kullanıyorsanız logları görmek için:**
```bash
docker-compose logs -f backend
```

---

## 🔧 AYARLARI NEREDEN DEĞİŞTİRİRİM?

### Backend Ayarları:
📁 `backend/.env` dosyası
- Veritabanı ayarları
- SMS sağlayıcı bilgileri
- WhatsApp ayarları
- Güvenlik ayarları

### Frontend Ayarları:
📁 `frontend/.env` dosyası
- Backend API adresi
```env
VITE_API_URL=http://localhost:5000/api
```

Web'de yayınlıyorsanız:
```env
VITE_API_URL=https://api.sizin-domain.com/api
```

---

## 🌐 WEB SUNUCUSUNA KURULUM (Canlıya Alma)

### Gereksinimler:
- Ubuntu 20.04+ sunucu
- Domain adı (örn: okulsms.com)
- SSL sertifikası (Let's Encrypt ile ücretsiz)

### Hızlı Kurulum:

1. **Dosyaları sunucuya yükleyin:**
```bash
scp -r BST/ kullanici@sunucu-ip:/home/kullanici/
```

2. **Sunucuda ayarları yapın:**
```bash
cd BST
nano backend/.env
```

Değiştirin:
```env
NODE_ENV=production
CORS_ORIGIN=https://sizin-domain.com
```

```bash
nano frontend/.env
```

Değiştirin:
```env
VITE_API_URL=https://api.sizin-domain.com/api
```

3. **Nginx kurun:**
```bash
sudo apt install nginx certbot python3-certbot-nginx
```

4. **Nginx ayarları:**
```bash
sudo nano /etc/nginx/sites-available/okul-sms
```

Yapıştırın:
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

5. **Aktif edin:**
```bash
sudo ln -s /etc/nginx/sites-available/okul-sms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. **SSL ekleyin:**
```bash
sudo certbot --nginx -d sizin-domain.com
```

7. **Başlatın:**
```bash
./kurulum.sh
```

✅ **HAZIR! Siteniz canlıda!**

---

## 🆘 SORUN ÇÖZME

### "Port zaten kullanımda" hatası

**Çözüm:** Portları değiştirin

`docker-compose.yml` dosyasını açın:
```yaml
ports:
  - "5001:5000"  # Backend
  - "3001:3000"  # Frontend
```

### "Veritabanına bağlanamıyor" hatası

**Docker ile:**
```bash
docker-compose restart postgres
docker-compose logs postgres
```

**Manuel kurulumda:**
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

### WhatsApp QR kod görünmüyor

**Docker ile:**
```bash
docker-compose logs backend
```

**Manuel kurulumda:**
Backend terminaline bakın

### Programı nasıl durdururum?

**Docker ile:**
```bash
docker-compose down
```

**Manuel kurulumda:**
- Backend terminalinde: `Ctrl + C`
- Frontend terminalinde: `Ctrl + C`

---

## 📞 YARDIM

Sorun mu yaşıyorsunuz?

1. Logları kontrol edin
2. `.env` dosyalarını kontrol edin
3. Port'ların boş olduğundan emin olun
4. Docker çalışıyor mu kontrol edin

---

## 🎉 HAZIRSINIZ!

Artık:
- ✅ Toplu SMS gönderebilirsiniz
- ✅ Toplu WhatsApp mesajı gönderebilirsiniz
- ✅ Öğrenci ve veli yönetimi yapabilirsiniz
- ✅ Mesaj geçmişini görebilirsiniz
- ✅ Zamanlanmış mesajlar oluşturabilirsiniz

**İyi kullanımlar!** 🏫📱
