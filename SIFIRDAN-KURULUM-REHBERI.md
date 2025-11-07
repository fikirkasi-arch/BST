# 🎓 OKUL SMS SİSTEMİ - SIFIRDAN KURULUM REHBERİ

## 👋 Hoş Geldiniz!

Bu rehber, hiç bilgisayar bilginiz olmasa bile programı çalıştırmanıza yardımcı olacak.
Her adımı tek tek, basit bir dille anlatacağım.

---

## 📋 İÇİNDEKİLER

1. [Hangi yöntemi seçmeliyim?](#1-hangi-yöntemi-seçmeliyim)
2. [Bilgisayarımı hazırlıyorum](#2-bilgisayarımı-hazırlıyorum)
3. [Programı indiriyorum](#3-programı-indiriyorum)
4. [Programı çalıştırıyorum](#4-programı-çalıştırıyorum)
5. [İlk girişimi yapıyorum](#5-ilk-girişimi-yapıyorum)
6. [İlk ayarları yapıyorum](#6-ilk-ayarları-yapıyorum)
7. [SMS/WhatsApp ayarları](#7-smswhatsapp-ayarları)

---

## 1. HANGİ YÖNTEMİ SEÇMELİYİM?

### ⭐ YÖNTEM A: Docker ile (EN KOLAY - ÖNERİLEN)

**Nedir?** Docker, programı tek tuşla çalıştırmanızı sağlar.

**Avantajları:**
- ✅ Çok kolay
- ✅ Tek tuşla başlatma
- ✅ Sorun çıkması çok zor
- ✅ Herhangi bir ayar gerektirmez

**Dezavantajları:**
- ❌ Docker kurulumu gerekiyor (ama sadece bir kez)

**Kimler için?**
- Bilgisayar bilgisi az olanlar
- Hızlı başlamak isteyenler
- Sorun yaşamak istemeyenler

---

### YÖNTEM B: Manuel Kurulum (Daha Teknik)

**Nedir?** Node.js ve PostgreSQL'i kendiniz kurarsınız.

**Avantajları:**
- ✅ Daha fazla kontrol
- ✅ Docker gerektirmez

**Dezavantajları:**
- ❌ Daha karmaşık
- ❌ Daha fazla program kurmak gerekir
- ❌ Sorun yaşama ihtimali daha fazla

**Kimler için?**
- Bilgisayar bilen kişiler
- Docker kullanamayan durumlar

---

## 🎯 BEN HANGİSİNİ SEÇMELİYİM?

**Cevap: YÖNTEM A - Docker ile!**

Neden? Çünkü:
- 5 dakikada kurulur
- Tek tuşla çalışır
- Sorun yaşama ihtimali çok düşük

---

# YÖNTEM A: DOCKER İLE KURULUM

## 2. BİLGİSAYARIMI HAZIRLIYORUM

### ADIM 1: Docker'ı İndirin

#### Windows Kullanıyorsanız:

**2.1. Docker Desktop'ı İndirin**

1. Tarayıcınızı açın (Chrome, Edge, Firefox, vb.)
2. Şu adrese gidin: **https://www.docker.com/products/docker-desktop/**
3. Sayfada **"Download for Windows"** yazan mavi butona tıklayın
4. İndirme başlayacak (yaklaşık 500 MB)

**2.2. Docker'ı Kurun**

1. İndirilen dosyayı bulun (genellikle "İndirilenler" klasöründe)
2. Dosya adı: **"Docker Desktop Installer.exe"**
3. Dosyaya çift tıklayın
4. **"Evet"** diyin (Windows izin isterse)
5. Kurulum ekranı açılacak
6. **"OK"** veya **"İleri"** butonlarına tıklayın
7. Kurulum bitince **"Finish"** deyin
8. **Bilgisayarı yeniden başlatın** (çok önemli!)

**2.3. Docker'ı Başlatın**

1. Bilgisayar açıldıktan sonra
2. Masaüstünde **"Docker Desktop"** ikonunu arayın
3. İkona çift tıklayın
4. Docker açılacak (ilk açılış 1-2 dakika sürebilir)
5. **Yeşil bir işaret** görene kadar bekleyin (sağ altta)
6. Yeşil işaret = Docker hazır!

#### Mac Kullanıyorsanız:

**2.1. Docker Desktop'ı İndirin**

1. Tarayıcınızı açın
2. Şu adrese gidin: **https://www.docker.com/products/docker-desktop/**
3. **"Download for Mac"** butonuna tıklayın
4. Mac'iniz Intel mi Apple Silicon (M1/M2) mi kontrol edin:
   - Sol üst köşede Apple logosu → About This Mac
   - "Chip" veya "Processor" kısmına bakın
   - Intel yazıyorsa: Intel versiyonu indirin
   - M1/M2 yazıyorsa: Apple Silicon versiyonu indirin

**2.2. Docker'ı Kurun**

1. İndirilen .dmg dosyasını açın
2. Docker ikonunu Applications klasörüne sürükleyin
3. Applications klasöründen Docker'ı açın
4. İlk açılışta güvenlik uyarısı gelirse **"Open"** deyin

**2.3. Docker'ı Başlatın**

1. Docker açılacak
2. Üstte menü çubuğunda Docker ikonunu göreceksiniz
3. İkon yeşil olana kadar bekleyin
4. Yeşil = Hazır!

#### Linux Kullanıyorsanız:

**Terminal'i açın** (Ctrl + Alt + T) ve şu komutları çalıştırın:

```bash
# Docker'ı kur
sudo apt update
sudo apt install docker.io docker-compose -y

# Docker'ı başlat
sudo systemctl start docker

# Kullanıcınızı Docker grubuna ekle (şifresiz kullanım için)
sudo usermod -aG docker $USER

# Çıkış yapıp tekrar giriş yapın (önemli!)
```

Çıkış yap-giriş yap yaptıktan sonra terminal'de test edin:

```bash
docker --version
```

Bir versiyon numarası görüyorsanız, Docker hazır!

---

## 3. PROGRAMI İNDİRİYORUM

### ADIM 2: Proje Dosyalarını Alın

**Dosyalar nerede?**

Dosyalar şu anda bu bilgisayarda: `/home/user/BST/`

**Ne yapmalıyım?**

#### Seçenek 1: ZIP Dosyasını Kullan (KOLAY)

1. **Dosya yöneticinizi açın** (Windows: Dosya Gezgini, Mac: Finder)
2. Şu klasöre gidin: `/home/user/`
3. **"BST-proje.zip"** adlı dosyayı bulun
4. Bu dosyayı **masaüstüne kopyalayın** (sağ tık → kopyala → masaüstüne yapıştır)
5. Masaüstündeki ZIP dosyasına **sağ tıklayın**
6. **"Tümünü ayıkla"** veya **"Extract All"** seçin
7. **"Masaüstü"** seçin ve **"Ayıkla"** deyin
8. Masaüstünde **"BST"** adlı yeni bir klasör oluşacak
9. **BU KLASÖRÜ AÇIN**

#### Seçenek 2: Direkt Klasörü Kopyala

1. `/home/user/BST/` klasörünü bulun
2. Tüm klasörü masaüstüne kopyalayın
3. Masaüstündeki BST klasörünü açın

**Şimdi ne görmem gerekiyor?**

BST klasörünün içinde şunları görmelisiniz:
- 📁 backend (klasör)
- 📁 frontend (klasör)
- 📁 database (klasör)
- 📄 docker-compose.yml (dosya)
- 📄 kurulum.sh (Linux/Mac için)
- 📄 kurulum.bat (Windows için)
- 📄 README.md
- ve diğer dosyalar...

**Görmüyorum, ne yapmalıyım?**
- ZIP'i düzgün açtığınızdan emin olun
- "BST" klasörünün İÇİNE girdiğinizden emin olun

---

## 4. PROGRAMI ÇALIŞTIRIYORUM

### ADIM 3: Kurulumu Başlatın

Şimdi süper kolay kısım! 🎉

#### Windows Kullanıcıları:

**4.1. Docker'ın Çalıştığından Emin Olun**

1. Ekranın sağ altına (sistem tepsisine) bakın
2. Docker ikonunu bulun (balina resmi)
3. İkona tıklayın
4. **"Docker Desktop is running"** yazıyorsa ✅ hazır
5. Yazmıyorsa, Docker Desktop'ı açın ve yeşil işaret görene kadar bekleyin

**4.2. Kurulum Dosyasını Çalıştırın**

1. Masaüstünde **"BST"** klasörünü açın
2. **"kurulum.bat"** dosyasını bulun
3. Bu dosyaya **ÇİFT TIKLAYIN**
4. Siyah bir ekran (komut istemi) açılacak
5. Ekranda yazılar akacak (korkMAYIN, bu normal!)
6. Şunları göreceksiniz:
   ```
   📦 Eski container'lar durduruluyor...
   🚀 Sistem başlatılıyor...
   ⏳ Veritabanının hazır olması bekleniyor...
   ```
7. **30-60 saniye bekleyin**
8. Sonunda şunu göreceksiniz:
   ```
   ✅ Kurulum tamamlandı!
   🌐 Frontend: http://localhost:3000
   ```

**HAZIR! Program çalışıyor!** 🎉

#### Mac/Linux Kullanıcıları:

**4.1. Terminal'i Açın**

- Mac: Spotlight'ı açın (Cmd + Space) → "Terminal" yazın → Enter
- Linux: Ctrl + Alt + T

**4.2. BST Klasörüne Gidin**

```bash
cd ~/Desktop/BST
```

(Eğer masaüstüne kopyaladıysanız)

**4.3. Kurulum Scriptini Çalıştırın**

```bash
./kurulum.sh
```

Eğer "Permission denied" hatası alırsanız:

```bash
chmod +x kurulum.sh
./kurulum.sh
```

**4.4. Bekleyin**

30-60 saniye içinde kurulum tamamlanacak ve şunu göreceksiniz:

```
✅ Kurulum tamamlandı!
🌐 Frontend: http://localhost:3000
```

**HAZIR!** 🎉

---

## 5. İLK GİRİŞİMİ YAPIYORUM

### ADIM 4: Tarayıcıda Açın

**5.1. Tarayıcınızı Açın**

Herhangi bir tarayıcı: Chrome, Firefox, Edge, Safari, vb.

**5.2. Adres Çubuğuna Yazın**

```
http://localhost:3000
```

Tam olarak bu şekilde yazın ve **Enter**'a basın.

**5.3. Ne Göreceğim?**

Bir giriş ekranı göreceksiniz:
- "Kullanıcı Adı" kutusu
- "Şifre" kutusu
- "Giriş Yap" butonu

**AMA HENÜZ GİREMEZSİNİZ!** Çünkü kullanıcı oluşturmadık.

---

### ADIM 5: İlk Kullanıcıyı Oluşturun

Geri dönün, kullanıcı oluşturacağız.

#### Windows:

**5.1. BST Klasöründe**

1. **"ilk-kullanici-olustur.bat"** dosyasını bulun
2. **ÇİFT TIKLAYIN**
3. Siyah ekran açılacak
4. Size sorular soracak:

```
Kullanıcı adı (örn: admin):
```

**Ne yazmalıyım?**

```
admin
```

(yazın ve Enter'a basın)

```
Email (örn: admin@okul.com):
```

**Ne yazmalıyım?**

```
admin@okul.com
```

(yazın ve Enter'a basın)

```
Şifre:
```

**Ne yazmalıyım?**

```
admin123
```

(yazın ve Enter'a basın - şifre görünmez, normal!)

```
Tam adınız (örn: Ahmet Yılmaz):
```

**Ne yazmalıyım?**

```
Okul Müdürü
```

(veya kendi adınız)

**5.2. Bekleyin**

Birkaç saniye sonra:

```
✅ Kullanıcı oluşturuldu!
Şimdi http://localhost:3000 adresinden giriş yapabilirsiniz.
```

#### Mac/Linux:

Terminal'de:

```bash
cd ~/Desktop/BST
./ilk-kullanici-olustur.sh
```

Aynı soruları soracak, aynı şekilde cevaplayın.

---

### ADIM 6: Giriş Yapın!

**6.1. Tarayıcıya Dönün**

http://localhost:3000 açık olmalı

**6.2. Giriş Bilgilerinizi Girin**

- **Kullanıcı adı:** admin
- **Şifre:** admin123

**6.3. "Giriş Yap" Butonuna Tıklayın**

**6.4. BAŞARILI!** 🎉

Ana sayfa açılacak! Şunları göreceksiniz:
- Öğrenci sayısı: 0
- Mesaj sayısı: 0
- Sol tarafta menü
- Üstte hoşgeldin mesajı

**PROGRAM ÇALIŞIYOR!** 🚀

---

## 6. İLK AYARLARI YAPIYORUM

### ADIM 7: Ayar Dosyasını Düzenleyin

Şimdi SMS ve WhatsApp için ayarları yapacağız.

**7.1. Ayar Dosyasını Bulun**

1. BST klasörünü açın
2. **"backend"** klasörüne girin
3. **".env"** adlı dosyayı bulun

**Görmüyorum!**

Windows'ta gizli dosyalar kapalı olabilir:
1. Dosya Gezgini'ni açın
2. Üstte "Görünüm" sekmesine tıklayın
3. "Gizli öğeler" kutucuğunu işaretleyin
4. Şimdi .env dosyasını göreceksiniz

**7.2. Dosyayı Açın**

- **Sağ tıklayın** → "Birlikte Aç" → "Not Defteri" seçin
- Veya Notepad++, VS Code gibi bir editör kullanın

**7.3. Ne Görüyorum?**

Bir sürü ayar göreceksiniz. ŞİMDİLİK bunları değiştirin:

**GÜVENLİK ANAHTARI (ÇOK ÖNEMLİ!):**

Bulun:
```env
JWT_SECRET=okul_sms_jwt_secret_key_development_12345
```

Değiştirin:
```env
JWT_SECRET=benim_cok_gizli_anahtarim_12345678
```

(Karışık bir şey yazın, kimseye söylemeyin!)

**VERİTABANI ŞİFRESİ:**

İsterseniz değiştirin:
```env
DB_PASSWORD=postgres123
```

**7.4. Kaydedin ve Kapatın**

Dosya → Kaydet → Kapat

---

## 7. SMS/WHATSAPP AYARLARI

### SMS İçin (Opsiyonel)

SMS göndermek için bir SMS sağlayıcıya ihtiyacınız var.

#### Türkiye'deyseniz: NetGSM

**1. NetGSM Hesabı Açın**

1. https://www.netgsm.com.tr/ adresine gidin
2. "Üye Ol" veya "Kayıt Ol" butonuna tıklayın
3. Bilgilerinizi girin
4. Hesap açılacak (kredi yüklemeniz gerekebilir)

**2. API Bilgilerinizi Alın**

1. NetGSM paneline giriş yapın
2. API ayarları bölümünü bulun
3. **Kullanıcı Adı** ve **Şifre**'yi not alın
4. **Başlık** (Header) belirleyin (örn: OKUL ADI)

**3. .env Dosyasına Yazın**

```env
NETGSM_USERNAME=netgsm_kullanici_adi
NETGSM_PASSWORD=netgsm_sifre
NETGSM_HEADER=OKUL_ADI
```

**4. Programı Yeniden Başlatın**

Windows:
- Komut istemi penceresinde Ctrl+C
- Tekrar `kurulum.bat` çalıştırın

Docker ile:
```bash
docker-compose restart backend
```

#### Yurt Dışındaysanız: Twilio

**1. Twilio Hesabı Açın**

1. https://www.twilio.com/ adresine gidin
2. "Sign Up" tıklayın
3. Ücretsiz hesap açın

**2. Bilgilerinizi Alın**

1. Twilio Dashboard'a girin
2. **Account SID** ve **Auth Token**'ı kopyalayın
3. Bir **telefon numarası** alın (Twilio'dan)

**3. .env Dosyasına Yazın**

```env
TWILIO_ACCOUNT_SID=twilio_account_sid_buraya
TWILIO_AUTH_TOKEN=twilio_auth_token_buraya
TWILIO_PHONE_NUMBER=+1234567890
```

**4. Programı Yeniden Başlatın**

---

### WhatsApp İçin

WhatsApp için hiçbir kayıt gerekmez! Otomatik çalışır.

**İlk Kullanımda:**

1. Backend loglarını görmek için:

**Windows:**
```
docker-compose logs -f backend
```

**Mac/Linux:**
```bash
docker-compose logs -f backend
```

2. Terminal'de bir QR kod göreceksiniz
3. **WhatsApp uygulamanızı açın** (telefonunuzda)
4. **Ayarlar** → **Bağlı Cihazlar**
5. **"Cihaz Bağla"** butonuna tıklayın
6. **QR kodu tarayın** (telefon kamerasıyla)
7. Bağlantı kuruldu! ✅

Artık WhatsApp mesajı gönderebilirsiniz!

---

## ✅ KURULUM TAMAMLANDI!

### Şimdi Ne Yapabilirim?

#### 1. Öğrenci Ekleyin

1. Sol menüden **"Öğrenciler"** tıklayın
2. Sağ üstte **"+ Yeni Öğrenci"** butonuna tıklayın
3. Formu doldurun:
   - Öğrenci numarası
   - Ad, Soyad
   - Sınıf (önce sınıf oluşturmanız gerekebilir)
   - Veli bilgileri (ad, soyad, telefon)
4. **"Kaydet"** butonuna tıklayın

#### 2. Mesaj Gönderin

1. Sol menüden **"Mesaj Gönder"** tıklayın
2. **Mesaj tipi** seçin (SMS, WhatsApp, Email)
3. **Alıcılar** seçin (Tüm veliler, belirli sınıf, vb.)
4. **Mesajınızı yazın**
5. **"Gönder"** butonuna tıklayın

#### 3. Excel ile Toplu Öğrenci Ekleyin

1. API'den şablon indirin (tarayıcıda):
   ```
   http://localhost:5000/api/students/template/download
   ```
2. Excel'i açın ve doldurun
3. Frontend'den yükleyin (veya API ile)

---

## 🆘 SORUN GİDERME

### "Docker bulunamadı" hatası

**Çözüm:** Docker'ı kurun (Adım 2.1)

### "localhost:3000 açılmıyor" hatası

**Kontrol listesi:**
1. Docker çalışıyor mu? (Docker Desktop açık mı?)
2. `kurulum.bat` veya `kurulum.sh` çalıştırdınız mı?
3. Yeşil "✅ Kurulum tamamlandı!" mesajını gördünüz mü?
4. Doğru yazdınız mı? `http://localhost:3000` (httpS değil, http!)

**Hala çalışmıyor:**
```bash
docker-compose ps
```

Tüm servisler "Up" durumunda olmalı.

### "İlk kullanıcı oluşturulamadı" hatası

**Çözüm:**
```bash
# Backend çalışıyor mu kontrol edin
docker-compose logs backend

# Yeniden başlatın
docker-compose restart backend

# 10 saniye bekleyin, tekrar deneyin
```

### "Permission denied" hatası (Linux/Mac)

**Çözüm:**
```bash
chmod +x kurulum.sh ilk-kullanici-olustur.sh
```

### Docker çok yavaş (Windows)

**Çözüm:**
1. Docker Desktop ayarlarını açın
2. Resources → Advanced
3. CPU ve Memory'i artırın
4. Apply & Restart

---

## 💡 İPUÇLARI

### Programı Durdurmak

**Windows:** Komut istemi penceresinde Ctrl+C

**Veya:**
```bash
docker-compose down
```

### Programı Yeniden Başlatmak

```bash
docker-compose restart
```

### Logları Görüntülemek

```bash
docker-compose logs -f
```

(Ctrl+C ile çıkın)

### Veritabanını Sıfırlamak

```bash
docker-compose down
docker-compose up -d
```

(Tüm veriler silinir!)

---

## 📞 YARDIM

### Daha Fazla Bilgi İçin:

1. **KOLAY-KURULUM-REHBERI.md** - Detaylı kurulum
2. **YENI-OZELLIKLER-REHBERI.md** - Yeni özellikler
3. **README.md** - Genel bakış

### Sorun mu yaşıyorsunuz?

1. Logları kontrol edin: `docker-compose logs -f`
2. Docker çalışıyor mu kontrol edin
3. .env dosyasını kontrol edin
4. Bana sorun, yardımcı olurum! 😊

---

## 🎉 TEBRİKLER!

Programı başarıyla kurdunuz ve çalıştırdınız!

Artık:
- ✅ Öğrenci ekleyebilirsiniz
- ✅ Mesaj gönderebilirsiniz
- ✅ Raporları görüntüleyebilirsiniz
- ✅ Şablonlar oluşturabilirsiniz

**İyi kullanımlar!** 🚀

---

**Unutmayın:** Herhangi bir sorunuz olursa, bana sorun. Size yardımcı olmak için buradayım! 😊
