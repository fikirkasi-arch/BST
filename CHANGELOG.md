# Changelog

Okul SMS Sistemi için tüm önemli değişiklikler bu dosyada belgelenir.

Format [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standardına uygundur.

## [1.0.0] - 2024-11-07

### 🎉 İlk Yayın

Okul SMS/WhatsApp Sistemi'nin ilk kararlı sürümü!

### ✨ Eklenen Özellikler

#### Mesajlaşma
- Toplu SMS gönderimi (NetGSM ve Twilio entegrasyonu)
- Toplu WhatsApp mesajı (WhatsApp Web.js)
- Toplu Email gönderimi (nodemailer)
- Mesaj şablonları yönetimi
- Zamanlanmış mesaj gönderimi
- Mesaj değişkenleri desteği ({ad}, {soyad}, {tam_ad})

#### Öğrenci ve Veli Yönetimi
- Öğrenci CRUD işlemleri
- Veli CRUD işlemleri
- Sınıf yönetimi
- Excel/CSV ile toplu öğrenci içe aktarma
- Öğrenci-veli ilişkilendirme
- Excel şablonu indirme

#### Raporlama ve Analiz
- Genel istatistikler dashboard'u
- Mesaj istatistikleri (günlük, aylık, yıllık)
- Sınıf bazında raporlar
- Devamsızlık analizi
- Mesaj teslimat oranı raporları
- Grafik için hazır API'ler

#### Kullanıcı Yönetimi
- JWT tabanlı kimlik doğrulama
- Rol bazlı yetkilendirme (admin, manager, teacher)
- Şifre hashleme (bcrypt)
- Kullanıcı profili yönetimi

#### Otomasyon
- Otomatik devamsızlık bildirimi (günlük saat 10:00)
- Zamanlanmış mesaj gönderimi
- Cron job desteği

### 🔧 Teknik Özellikler

#### Backend
- Node.js + Express
- TypeScript
- PostgreSQL veritabanı
- JWT authentication
- RESTful API
- Error handling middleware
- Logging (Winston)
- File upload (Multer)

#### Frontend
- React + TypeScript
- Vite build tool
- Tailwind CSS
- React Query
- Zustand state management
- React Router
- React Hook Form

#### DevOps
- Docker ve Docker Compose desteği
- Production-ready Dockerfile'lar
- Nginx konfigürasyonu
- Kolay kurulum scriptleri (Windows/Linux/Mac)

### 📚 Dokümantasyon
- Detaylı README.md
- Sıfırdan kurulum rehberi (SIFIRDAN-KURULUM-REHBERI.md)
- Kolay kurulum kılavuzu (KOLAY-KURULUM-REHBERI.md)
- Başlatma kılavuzu (BASLATMA-KILAVUZU.md)
- Yeni özellikler rehberi (YENI-OZELLIKLER-REHBERI.md)
- API dokümantasyonu

### 🔒 Güvenlik
- JWT secret key yapılandırması
- Password hashing
- SQL injection koruması
- CORS yapılandırması
- Rate limiting
- Input validation

### 🐛 Bilinen Sorunlar
- WhatsApp bağlantısı bazen yavaş olabilir
- Çok büyük Excel dosyaları (10.000+ satır) yüklenirken timeout olabilir

### 📝 Notlar
- İlk kullanıcı oluşturma scripti eklendi
- Docker ile tek tuşla kurulum mümkün
- SMS sağlayıcı hesabı gereklidir (NetGSM veya Twilio)
- WhatsApp için ayrı hesap gerekmez

---

## [Gelecek Sürümler]

### Planlanan Özellikler (v1.1.0)
- [ ] E-Okul API entegrasyonu
- [ ] Gelişmiş raporlama ve grafik dashboard'u
- [ ] SMS kredi takip sistemi
- [ ] Çoklu dil desteği (İngilizce, Almanca)
- [ ] Bildirim tercih yönetimi

### Uzun Vadeli (v2.0.0)
- [ ] Mobil uygulama (React Native)
- [ ] Multi-tenant desteği (çoklu okul)
- [ ] Veli mobil uygulaması
- [ ] Öğrenci devam sistemi (QR kod)
- [ ] Online ödeme entegrasyonu

---

## Versiyon Notasyonu

Bu proje [Semantic Versioning](https://semver.org/) kullanır:
- MAJOR version: Geriye uyumsuz değişiklikler
- MINOR version: Geriye uyumlu yeni özellikler
- PATCH version: Geriye uyumlu hata düzeltmeleri

## Kategori Açıklamaları

- **Added** (Eklenen): Yeni özellikler
- **Changed** (Değiştirilen): Mevcut özelliklerde değişiklikler
- **Deprecated** (Kullanımdan Kaldırılan): Yakında kaldırılacak özellikler
- **Removed** (Kaldırılan): Kaldırılan özellikler
- **Fixed** (Düzeltilen): Hata düzeltmeleri
- **Security** (Güvenlik): Güvenlik yamalarıyla ilgili
