# 🎉 YENİ ÖZELLİKLER REHBERİ

Okul SMS sisteminize yeni özellikler eklendi! İşte ne yapabilirsiniz ve nasıl kullanırsınız.

---

## 📥 1. EXCEL/CSV İLE TOPLU ÖĞRENCİ EKLEME

### Ne İşe Yarar?

Yüzlerce öğrenci ve veli bilgisini tek seferde sisteme yükleyin! Artık tek tek eklemek yok.

### Nasıl Kullanılır?

#### Adım 1: Şablon Dosyasını İndirin

API üzerinden şablon indirebilirsiniz:

```bash
# Giriş yaptıktan sonra token'ınızla:
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/students/template/download \
     -o ogrenci-sablonu.xlsx
```

Veya tarayıcıda:
```
http://localhost:5000/api/students/template/download
```

#### Adım 2: Excel'i Doldurun

Şablon dosyasında şu sütunlar var:

| Öğrenci No | Ad | Soyad | Sınıf ID | Doğum Tarihi | Veli Ad | Veli Soyad | Veli Telefon | Veli Email | Yakınlık |
|------------|-------|--------|----------|--------------|---------|------------|--------------|------------|----------|
| 12345 | Ahmet | Yılmaz | 1 | 2010-01-15 | Mehmet | Yılmaz | 5551234567 | mehmet@example.com | baba |

**Önemli Notlar:**
- Öğrenci No, Ad, Soyad **zorunlu**
- Telefon numaraları **başında sıfır olmadan** yazın (5551234567 ✅, 05551234567 ❌)
- Tarih formatı: YYYY-MM-DD (örn: 2010-01-15)

#### Adım 3: Dosyayı Yükleyin

```bash
curl -X POST http://localhost:5000/api/students/import \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@ogrenci-listesi.xlsx"
```

Veya frontend'de dosya yükleme butonunu kullanın.

#### Sonuç:

```json
{
  "success": true,
  "message": "Import işlemi tamamlandı",
  "data": {
    "total": 100,
    "success": 95,
    "failed": 5,
    "errors": [
      // İlk 10 hata gösterilir
    ]
  }
}
```

---

## 📝 2. MESAJ ŞABLONLARI

### Ne İşe Yarar?

Sık kullandığınız mesajları şablon olarak kaydedin. Bir daha yazmayın!

### Şablon Kategorileri

- **Devamsızlık** - Öğrenci gelmediğinde
- **Toplantı** - Veli toplantıları için
- **Sınav** - Sınav bildirileri
- **Genel** - Diğer duyurular

### Nasıl Kullanılır?

#### Şablon Oluşturma:

```bash
curl -X POST http://localhost:5000/api/templates \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Devamsızlık Bildirimi",
    "content": "Sayın {tam_ad},\n\nÇocuğunuz bugün okula gelmemiştir.\n\nSaygılarımızla,\nOkul İdaresi",
    "message_type": "sms",
    "category": "devamsizlik",
    "variables": ["{ad}", "{soyad}", "{tam_ad}"]
  }'
```

#### Tüm Şablonları Görüntüleme:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/templates
```

#### Şablon Kullanarak Mesaj Gönderme:

1. Şablonu seçin
2. Alıcıları seçin
3. Değişkenler otomatik değişecek!

**Örnek:**
```
Şablon: Sayın {tam_ad}, çocuğunuz bugün okula gelmemiştir.
Gönderildiğinde: Sayın Ahmet Yılmaz, çocuğunuz bugün okula gelmemiştir.
```

---

## 📊 3. DETAYLI RAPORLAMA VE GRAFİKLER

### Genel İstatistikler

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/reports/general
```

**Sonuç:**
```json
{
  "success": true,
  "data": {
    "totalStudents": 500,
    "totalParents": 450,
    "totalMessages": 1250,
    "monthlyMessages": 120,
    "todayMessages": 15,
    "failedMessages": 8
  }
}
```

### Mesaj İstatistikleri (Grafik İçin)

```bash
# Son 7 gün
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "http://localhost:5000/api/reports/messages?period=7days"

# Son 30 gün
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "http://localhost:5000/api/reports/messages?period=30days"

# Son 12 ay
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "http://localhost:5000/api/reports/messages?period=12months"
```

### Sınıf Bazında İstatistikler

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/reports/classes
```

**Her sınıf için:**
- Öğrenci sayısı
- Veli sayısı
- Devam durumu
- Devamsızlık oranı

### Devamsızlık İstatistikleri

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "http://localhost:5000/api/reports/attendance?start_date=2024-01-01&end_date=2024-12-31"
```

### En Çok Devamsızlık Yapan Öğrenciler

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "http://localhost:5000/api/reports/top-absent?limit=10&days=30"
```

### Mesaj Teslimat Oranı

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/reports/delivery-rate
```

---

## 📧 4. EMAIL BİLDİRİMİ

### Nasıl Kurulur?

`backend/.env` dosyasını açın ve email ayarlarını yapın:

```env
# Email Ayarları
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=okul@example.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_NAME=Okul SMS Sistemi
```

### Gmail İçin:

1. Gmail hesabınıza giriş yapın
2. **Ayarlar** → **Güvenlik**
3. **2 Adımlı Doğrulama**'yı açın
4. **Uygulama şifreleri** oluşturun
5. Oluşturulan şifreyi `SMTP_PASSWORD` olarak kullanın

### Diğer Email Sağlayıcıları:

**Outlook/Hotmail:**
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

**Yahoo:**
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Yandex:**
```env
SMTP_HOST=smtp.yandex.com
SMTP_PORT=587
```

### Email Gönderme:

Email servisi otomatik çalışır. Mesaj gönderirken `message_type` olarak `email` seçin:

```json
{
  "message_type": "email",
  "recipients": ["veli1@example.com", "veli2@example.com"],
  "subject": "Veli Toplantısı Duyurusu",
  "content": "Sayın velimiz, yarın saat 14:00'te okul salonunda veli toplantısı yapılacaktır."
}
```

---

## 🚀 HEPSİNİ BİRLİKTE KULLANMA ÖRNEĞİ

### Senaryo: Yeni Dönem Başlangıcı

#### 1. Öğrencileri Toplu Yükleyin

```bash
# Şablonu indirin
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:5000/api/students/template/download \
     -o sablon.xlsx

# Excel'i doldurun (Excel programında)
# Şimdi yükleyin
curl -X POST http://localhost:5000/api/students/import \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@ogrenci-listesi-2024.xlsx"
```

✅ **Sonuç:** 500 öğrenci ve velisi 2 dakikada yüklendi!

#### 2. Hoşgeldin Mesajı Şablonu Oluşturun

```bash
curl -X POST http://localhost:5000/api/templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hoşgeldin Mesajı",
    "content": "Sayın {tam_ad},\n\n{ogrenci_adi} öğrencimizi okulumuza kaydettik.\nİyi bir eğitim yılı dileriz!\n\nOkul İdaresi",
    "message_type": "sms",
    "category": "genel"
  }'
```

#### 3. Tüm Velilere Mesaj Gönderin

Frontend'den veya API ile:
- Şablonu seçin
- "Tüm Veliler" seçeneğini seçin
- Gönder!

#### 4. İstatistikleri Kontrol Edin

```bash
# Mesajlar gönderildi mi?
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:5000/api/reports/general

# Teslimat oranı nedir?
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:5000/api/reports/delivery-rate
```

---

## 💡 İPUÇLARI

### Excel Import İçin:

✅ **Yapın:**
- Şablon dosyasını kullanın
- Telefon numaralarını kontrol edin
- Küçük gruplar halinde test edin (önce 10 öğrenci)

❌ **Yapmayın:**
- Sütun isimlerini değiştirmeyin
- Boş satırlar eklemeyin
- Özel karakterler kullanmayın (Türkçe karakterler OK)

### Şablonlar İçin:

✅ **Yapın:**
- Anlamlı isimler verin
- Kategorileri kullanın
- Değişkenleri test edin

❌ **Yapmayın:**
- Çok uzun mesajlar yazmayın (SMS 160 karakter)
- Gereksiz değişkenler eklemeyin

### Raporlama İçin:

✅ **Yapın:**
- Günlük istatistikleri kontrol edin
- Devamsızlık raporlarını takip edin
- Teslimat oranlarını gözlemleyin

---

## 🆘 SORUN GİDERME

### Excel yüklenmiyor

**Hata:** "Dosya yüklenmedi"

**Çözüm:**
```bash
# uploads klasörünün var olduğundan emin olun
mkdir -p backend/uploads
chmod 777 backend/uploads
```

### Email gönderilmiyor

**Hata:** "Email servisi yapılandırılmadı"

**Çözüm:**
1. `.env` dosyasında SMTP ayarlarını kontrol edin
2. Gmail kullanıyorsanız "Uygulama şifresi" oluşturun
3. Backend'i yeniden başlatın

### Şablon değişkenleri çalışmıyor

**Hata:** Mesajda `{ad}` yazıyor, isim gözükmüyor

**Çözüm:**
- Değişken isimlerini doğru yazdığınızdan emin olun
- Desteklenen değişkenler: `{ad}`, `{soyad}`, `{tam_ad}`
- Süslü parantezleri unutmayın: `{ad}` ✅, `ad` ❌

---

## 📞 DESTEK

Sorunuz mu var?

1. `KOLAY-KURULUM-REHBERI.md` dosyasına bakın
2. Logları kontrol edin: `docker-compose logs -f backend`
3. GitHub'da issue açın

---

## 🎉 ARTIK HAZIRSINIZ!

Yeni özellikler sayesinde:
- ✅ Öğrenci kaydı 10 kat daha hızlı
- ✅ Mesaj gönderimi çok daha kolay
- ✅ Detaylı raporlarla her şey kontrol altında
- ✅ Email ile daha profesyonel iletişim

**İyi kullanımlar!** 🚀
