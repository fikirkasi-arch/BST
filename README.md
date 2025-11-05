# 🏫 Okul Toplu SMS/WhatsApp Sistemi

Okullar için geliştirilmiş kapsamlı bir toplu mesajlaşma sistemi. Velilere, öğretmenlere ve personele SMS ve WhatsApp üzerinden toplu mesaj gönderebilirsiniz.

## ✨ Özellikler

### 📱 Mesajlaşma
- **Toplu SMS Gönderimi** - NetGSM, Twilio gibi sağlayıcılarla entegre
- **Toplu WhatsApp Mesajı** - WhatsApp Web API ile entegre
- **Kişiselleştirme** - Mesajlarda {ad}, {soyad}, {tam_ad} gibi değişkenler kullanın
- **Zamanlanmış Mesajlar** - Gelecek bir tarih/saat için mesaj zamanlayın
- **Mesaj Şablonları** - Sık kullanılan mesajlar için şablonlar oluşturun

### 👥 Alıcı Yönetimi
- **Sınıflara Göre** - Belirli sınıflara toplu mesaj gönderin
- **Öğrenci Numaralarına Göre** - Seçili öğrencilerin velilerine mesaj gönderin
- **Tüm Velilere** - Okuldaki tüm velilere mesaj gönderin
- **Personele** - Öğretmen ve diğer personele mesaj gönderin
- **Elle Numara Girişi** - Rehberde olmayan numaralara mesaj gönderin

### 🔔 Otomatik Bildirimler
- **Devamsızlık Bildirimi** - Her gün sabah 10:00'da otomatik devamsızlık SMS'i
- **Sınav Sonuçları** - Sınav notları girildiğinde otomatik bildirim
- **Veli Toplantıları** - Toplantı hatırlatmaları
- **Özel Günler** - Kutlama ve hatırlatma mesajları

### 📊 Raporlama
- **Mesaj Geçmişi** - Gönderilen tüm mesajları görüntüleyin
- **Teslimat Durumu** - Her mesajın gönderim durumunu takip edin
- **İstatistikler** - Toplam gönderilen, başarısız mesaj sayıları

### 👤 Kullanıcı Yönetimi
- **Rol Bazlı Erişim** - Admin, Müdür, Öğretmen rolleri
- **Alt Kullanıcılar** - Birden fazla kullanıcı ile çalışın
- **Güvenli Kimlik Doğrulama** - JWT token ile güvenli giriş

### 📥 E-Okul Entegrasyonu
- Excel dosyası ile toplu öğrenci/veli aktarımı
- Veli iletişim bilgilerini otomatik içe aktarma

## 🚀 Kurulum

### Gereksinimler
- Node.js 18+
- PostgreSQL 14+
- npm veya yarn

### 1. Veritabanını Kurun

```bash
# PostgreSQL'e giriş yapın
psql -U postgres

# Veritabanını oluşturun
CREATE DATABASE okul_sms_db;

# Veritabanından çıkın
\q

# Şemayı içe aktarın
psql -U postgres -d okul_sms_db -f database/schema.sql
```

### 2. Backend Kurulumu

```bash
cd backend

# Bağımlılıkları yükleyin
npm install

# .env dosyasını oluşturun
cp .env.example .env

# .env dosyasını düzenleyin
nano .env
```

**.env Dosyası Örneği:**
```env
NODE_ENV=development
PORT=5000

DB_HOST=localhost
DB_PORT=5432
DB_NAME=okul_sms_db
DB_USER=postgres
DB_PASSWORD=your_password

JWT_SECRET=your_secret_key_change_this

# NetGSM (Türkiye SMS Sağlayıcısı)
NETGSM_USERNAME=your_username
NETGSM_PASSWORD=your_password
NETGSM_HEADER=OKUL ADI

# Twilio (Alternatif)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# WhatsApp
WHATSAPP_ENABLED=true
WHATSAPP_SESSION_PATH=./whatsapp-session
```

```bash
# Backend'i başlatın
npm run dev
```

### 3. Frontend Kurulumu

```bash
cd frontend

# Bağımlılıkları yükleyin
npm install

# Frontend'i başlatın
npm run dev
```

### 4. İlk Kullanıcıyı Oluşturun

Backend çalışırken, API üzerinden ilk admin kullanıcısını oluşturun:

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@okul.com",
    "password": "admin123",
    "full_name": "Sistem Yöneticisi",
    "role": "admin"
  }'
```

## 📖 Kullanım

### Giriş Yapın
1. Tarayıcınızda `http://localhost:3000` adresine gidin
2. Oluşturduğunuz kullanıcı ile giriş yapın
3. Ana sayfada istatistiklerinizi görün

### Mesaj Gönderin
1. **Mesaj Gönder** menüsüne tıklayın
2. Mesaj tipini seçin (SMS veya WhatsApp)
3. Alıcı grubunu seçin
4. Mesajınızı yazın (değişkenler kullanabilirsiniz)
5. **Mesaj Gönder** butonuna tıklayın

### Mesaj Değişkenleri
Mesajlarınızda şu değişkenleri kullanabilirsiniz:
- `{ad}` - Alıcının adı
- `{soyad}` - Alıcının soyadı
- `{tam_ad}` - Alıcının tam adı

**Örnek:**
```
Sayın {tam_ad},

Çocuğunuz bugün okula gelmemiştir.
Detaylı bilgi için okul idaresi ile iletişime geçiniz.

Saygılarımızla,
Okul İdaresi
```

### WhatsApp Kurulumu
1. Backend terminalde QR kod görünecektir
2. WhatsApp uygulamanızı açın
3. **Ayarlar > Bağlı Cihazlar > Cihaz Bağla**
4. QR kodu tarayın
5. WhatsApp bağlantısı hazır!

## 📁 Proje Yapısı

```
BST/
├── backend/
│   ├── src/
│   │   ├── config/         # Veritabanı, ortam ayarları
│   │   ├── controllers/    # Route controller'ları
│   │   ├── middleware/     # Auth, error handling
│   │   ├── models/         # Veritabanı modelleri
│   │   ├── routes/         # API route'ları
│   │   ├── services/       # SMS, WhatsApp servisleri
│   │   ├── types/          # TypeScript type tanımları
│   │   └── index.ts        # Ana uygulama
│   ├── package.json
│   └── tsconfig.json
│
├── frontend/
│   ├── src/
│   │   ├── components/     # React bileşenleri
│   │   ├── pages/          # Sayfa bileşenleri
│   │   ├── services/       # API servisleri
│   │   ├── stores/         # State yönetimi (Zustand)
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
└── database/
    └── schema.sql          # Veritabanı şeması
```

## 🔌 API Endpoints

### Auth
- `POST /api/auth/register` - Kullanıcı kaydı
- `POST /api/auth/login` - Giriş yap
- `GET /api/auth/me` - Mevcut kullanıcı bilgileri
- `PUT /api/auth/password` - Şifre değiştir

### Mesajlar
- `POST /api/messages/bulk` - Toplu mesaj gönder
- `GET /api/messages` - Mesaj listesi
- `GET /api/messages/:id` - Mesaj detayı
- `DELETE /api/messages/:id/cancel` - Zamanlanmış mesajı iptal et

### Öğrenciler
- `GET /api/students` - Öğrenci listesi
- `GET /api/students/:id` - Öğrenci detayı
- `POST /api/students` - Öğrenci ekle
- `PUT /api/students/:id` - Öğrenci güncelle
- `DELETE /api/students/:id` - Öğrenci sil

## 🛠️ Teknolojiler

### Backend
- **Node.js** - Runtime
- **Express** - Web framework
- **TypeScript** - Type safety
- **PostgreSQL** - Veritabanı
- **JWT** - Kimlik doğrulama
- **Twilio/NetGSM** - SMS sağlayıcıları
- **WhatsApp Web.js** - WhatsApp entegrasyonu
- **Node-cron** - Zamanlanmış görevler

### Frontend
- **React** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Query** - Data fetching
- **Zustand** - State management
- **React Router** - Routing
- **React Hook Form** - Form yönetimi

## 🔒 Güvenlik

- JWT token ile kimlik doğrulama
- Bcrypt ile şifre hashleme
- Rol bazlı yetkilendirme
- SQL injection koruması
- CORS yapılandırması
- Rate limiting

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

## 🎯 Gelecek Özellikler

- [ ] E-Okul API entegrasyonu
- [ ] Excel/CSV ile toplu veri içe aktarma
- [ ] Mesaj şablonları yönetimi
- [ ] Detaylı raporlama ve grafik
- [ ] Email bildirimi desteği
- [ ] Mobil uygulama (React Native)
- [ ] Multi-tenant desteği (Çoklu okul)

---

**Not:** Bu sistem eğitim kurumları için geliştirilmiştir. Ticari kullanım için lütfen lisans koşullarını inceleyin.
