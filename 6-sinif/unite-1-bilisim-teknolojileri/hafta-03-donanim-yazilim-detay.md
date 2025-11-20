# HAFTA 3: DONANIM VE YAZILIM DETAYLARİ
**Sınıf:** 6
**Ünite:** 1 - Bilişim Teknolojileri
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Donanım Bileşenleri Derinlemesine, Yazılım Kurulumu ve Güncelleme

---

## 🎯 ÖĞRENME KAZANIMLARI

- Bilgisayar donanımı bileşenlerini detaylı tanır ve işlevlerini açıklar
- Yazılım kurulum sürecini anlar ve uygular
- Yazılım güncellemenin önemini kavrar ve güncelleme yapar
- Donanım ve yazılım sorunlarını teşhis eder
- Bilgisayar performansını etkileyen faktörleri analiz eder

---

## 📚 KONU ÖZETİ

### DONANIM BİLEŞENLERİ - DERİNLEMESİNE

#### 1. İŞLEMCİ (CPU - Central Processing Unit)

**"Bilgisayarın Beyni"**

**Temel Özellikleri:**

**A) Hız (Clock Speed):**
- Ölçüm: GHz (Gigahertz)
- Örnek: 3.5 GHz = Saniyede 3.5 milyar işlem
- Daha yüksek = Daha hızlı (genellikle)

**B) Çekirdek Sayısı (Cores):**
- Tek çekirdek: Tek işlemci
- Çift çekirdek (Dual-Core): 2 işlemci birlikte
- Dört çekirdek (Quad-Core): 4 işlemci
- **Analoji:** 1 kişi vs 4 kişi birlikte çalışıyor

**C) Önbellek (Cache):**
- İşlemcinin kısa süreli belleği
- L1, L2, L3 seviyeleri
- Daha büyük = Daha hızlı erişim

**Popüler İşlemciler:**
- Intel: Core i3, i5, i7, i9
- AMD: Ryzen 3, 5, 7, 9
- Apple: M1, M2, M3 (Mac için)
- Qualcomm: Snapdragon (telefonlar için)

#### 2. BELLEK (RAM - Random Access Memory)

**"Kısa Süreli Çalışma Hafızası"**

**Özellikleri:**

**A) Kapasite:**
- 4 GB: Temel kullanım
- 8 GB: Normal kullanım (önerilen)
- 16 GB: Yoğun kullanım, oyun
- 32 GB+: Profesyonel iş

**B) Hız:**
- DDR4, DDR5 (yeni nesil)
- MHz cinsinden (örn: 3200 MHz)

**C) Uçucu Bellek:**
- Elektrik kesilince SİLİNİR!
- Geçici depolama

**RAM vs Sabit Disk Farkı:**
```
RAM:
- Çok HIZLI (nanosaniye)
- GEÇİCİ (kapanınca silinir)
- PAHALI
- Aktif programlar için

Sabit Disk:
- Daha YAVAŞ (milisaniye)
- KALICI (kapanınca da kalır)
- UCUZ
- Dosya depolama için
```

#### 3. DEPOLAMA CİHAZLARI

**A) HDD (Hard Disk Drive)**

**Özellikler:**
- Mekanik, dönen diskler
- Manyetik kayıt
- Ucuz, büyük kapasite
- Nispeten yavaş
- Titreşime duyarlı

**Hız:** 5400 RPM veya 7200 RPM
**Kapasite:** 500 GB - 10 TB
**Ömür:** 3-5 yıl

**B) SSD (Solid State Drive)**

**Özellikler:**
- Elektronik çipler (Flash bellek)
- Hareketli parça YOK
- Pahalı
- ÇOK HIZLI!
- Dayanıklı

**Hız:** HDD'den 5-10 kat daha hızlı!
**Kapasite:** 128 GB - 4 TB
**Ömür:** 5-10 yıl

**Karşılaştırma:**
| Özellik | HDD | SSD |
|---------|-----|-----|
| Hız | 🐢 100 MB/s | 🚀 550+ MB/s |
| Fiyat (1 TB) | 500 TL | 1500 TL |
| Dayanıklılık | Kırılgan | Sağlam |
| Ses | Gürültülü | Sessiz |
| Enerji | Fazla | Az |

**C) Diğer Depolama:**
- **USB Bellek:** Taşınabilir, küçük
- **Harici Disk:** Yedekleme için
- **SD Kart:** Kamera, telefon
- **Bulut Depolama:** İnternet üzerinden (Google Drive, OneDrive)

#### 4. EKRAN KARTI (GPU - Graphics Processing Unit)

**"Görüntü İşlemcisi"**

**Görevleri:**
- Ekrana görüntü gönderme
- 3D grafik işleme
- Video düzenleme
- Oyunlar için kritik!

**Türleri:**

**A) Entegre (Integrated):**
- Anakart/işlemci içinde
- Temel görevler için
- Ucuz, az enerji

**B) Ayrık (Dedicated):**
- Ayrı kart
- Güçlü, pahalı
- Oyun ve profesyonel iş için

**Popüler Markalar:**
- NVIDIA: GeForce RTX, GTX
- AMD: Radeon RX
- Intel: Arc

#### 5. ANA KART (Motherboard)

**"Bilgisayarın Ana Yolu"**

**İşlevi:**
- Tüm parçaları birbirine bağlar
- Elektrik dağıtır
- Veri iletimini sağlar

**Bileşenler:**
- CPU soketi
- RAM yuvaları
- Genişleme yuvaları (GPU, ses kartı)
- BIOS/UEFI çipi

#### 6. GÜÇ KAYNAĞI (PSU - Power Supply Unit)

**İşlevi:**
- Prizden gelen elektriği (220V AC) bilgisayar parçalarının kullanabileceği voltaja (12V, 5V, 3.3V DC) dönüştürür
- Doğru güç = Stabil çalışma

**Watt (W):**
- Temel kullanım: 300-450W
- Oyun bilgisayarı: 600-850W
- Yüksek performans: 1000W+

### YAZILIM KURULUMU VE YÖNETİMİ

#### Yazılım Kurulumu

**1. Güvenli Kaynaklardan İndirme:**

**✅ Güvenilir Kaynaklar:**
- Resmi web siteleri (örn: google.com/chrome)
- Microsoft Store, Google Play Store, App Store
- Bilinen platformlar (Steam, Epic Games)

**❌ Tehlikeli Kaynaklar:**
- Bilinmeyen siteler
- "Bedava" diye sunulan ücretli programlar
- E-posta ekleri (bilinmeyenden)
- Torrent siteleri (korsan)

**2. Kurulum Adımları:**

```
1. İndirme
   ↓
2. Kurulum dosyasını çalıştır (.exe, .msi)
   ↓
3. Kurulum sihirbazı açılır
   ↓
4. Lisans sözleşmesini oku ✅ Kabul et
   ↓
5. Kurulum yeri seç (varsayılan genelde uygun)
   ↓
6. Ekstra yazılımlar: DİKKAT! İstemediğiniz şeyleri seçmeyin!
   ↓
7. Kurulum başlar (ilerleme çubuğu)
   ↓
8. Tamamlandı! Program kullanıma hazır
```

**DİKKAT: Kurulum Sırasında Tuzaklar!**
- ☑ "Acme Toolbar yüklensin mi?" → ❌ KALDIR!
- ☑ "Varsayılan tarayıcı yap" → İstemiyorsanız kaldırın
- ☑ "Ek yazılımlar" → Gereksizleri kaldırın

#### Yazılım Güncelleme

**Neden Önemli?**

**1. Güvenlik:**
- Yeni virüslere karşı koruma
- Güvenlik açıklarını kapatma
- Hacker saldırılarını önleme

**2. Hata Düzeltme (Bug Fix):**
- Çökme sorunları giderilir
- Hatalar düzeltilir

**3. Yeni Özellikler:**
- Yeni fonksiyonlar eklenir
- Performans artışı

**4. Uyumluluk:**
- Yeni dosya formatları açılır
- Diğer yazılımlarla uyum

**Güncelleme Türleri:**

**A) Otomatik Güncelleme:**
- Program kendi günceller
- En güvenli yöntem
- Önerilen: AÇIK tutun

**B) Manuel Güncelleme:**
- "Güncellemeleri kontrol et" düğmesi
- Siz başlatırsınız

**C) Windows Update:**
- İşletim sistemi güncellemeleri
- Ayda 1 kez "Patch Tuesday" (her ayın 2. Salısı)
- Önemli güvenlik güncellemeleri

**Güncelleme Nasıl Yapılır?**

**Windows Update:**
1. Ayarlar → Windows Update
2. "Güncellemeleri denetle"
3. İndir ve yükle
4. Yeniden başlat (gerekirse)

**Programlar:**
- Yardım → Güncellemeleri Kontrol Et
- Veya otomatik bildirim gelir

### Donanım ve Yazılım Sorunları

#### Yaygın Sorunlar:

**1. Bilgisayar Yavaş:**
- **Neden:** Yetersiz RAM, HDD (SSD değil), çok program açık
- **Çözüm:** RAM artırın, SSD alın, Görev Yöneticisi ile gereksiz programları kapatın

**2. Program Donuyor:**
- **Neden:** Yetersiz RAM, uyumsuzluk
- **Çözüm:** Görev Yöneticisi → "Görevi sonlandır"

**3. Mavi Ekran (BSOD - Blue Screen of Death):**
- **Neden:** Donanım hatası, sürücü sorunu
- **Çözüm:** Güncellemeleri yapın, donanım kontrolü

**4. Program Açılmıyor:**
- **Neden:** Bozuk kurulum, eksik dosya
- **Çözüm:** Kaldır, tekrar yükle

**5. Disk Doldu:**
- **Neden:** Çok dosya, büyük programlar
- **Çözüm:** Gereksizleri silin, Disk Temizleme aracı

---

## 🎯 CAN ALICI HUSUSLAR

### Öğretmen İçin Kritik Noktalar:

**⚠️ 1. Kurulum Güvenliği:**
- Öğrencilere SADECE güvenilir kaynaklardan indirme vurgusu
- Korsan yazılım tehlikelerini anlatın
- Okul bilgisayarlarına kurulum YAPTIRMAYİN!

**💡 2. Teknik Detay Seviyesi:**
- Çok teknik terimlere girmey in
- Analojiler kullanın (RAM = Masa, HDD = Dolap)
- Öğrencilerin seviyesine göre ayarlayın

**🎯 3. Pratik Önem:**
- Güncelleme pratiği MUTLAKA yaptırın
- Görev Yöneticisi kullanımını pekiştirin
- Gerçek senaryolar verin

**📊 4. Değerlendirme:**
- "Neden?" sorularını mutlaka sorun
- "RAM ne işe yarar?" değil, "RAM azsa ne olur?" sorun
- Uygulama odaklı değerlendirme

**🕐 5. Zaman Yönetimi:**
- Donanım: 25 dk (çok detaya girmeyin)
- Yazılım kurulum: 20 dk
- Güncelleme pratiği: 15 dk
- Sorun giderme: 10 dk

**🔒 6. Güvenlik:**
- Kurulum tuzaklarını gösterin
- "Bedava antivirus" gibi tehlikeli reklamlar
- Sosyal mühendislik farkındalığı

---

## 🔬 MERAKLISININA

### İleri Düzey Bilgiler

**💻 Moore Yasası ve Sonu:**

Gordon Moore (Intel kurucusu), 1965'te:
"İşlemci gücü her 2 yılda iki katına çıkacak!"

60 yıl doğru çıktı! Ama...

**Sorun:** Artık atom boyutuna yaklaştık!
- Transistörler 7nm (nanometre) boyutunda
- 1 nm = milyonda bir milimetre!
- Daha küçültülemez (kuantum etkiler)

**Çözüm:**
- Çok çekirdek (100+ çekirdekli işlemciler)
- 3D yığınlama
- Kuantum bilgisayarlar!

**🧠 RAM Teknolojisi Evrimi:**

```
1970: DRAM icat edildi
1980: 64 KB RAM (64.000 byte!)
1990: 1 MB RAM
2000: 128 MB RAM
2010: 4 GB RAM
2020: 16 GB RAM (standart)
2025: 32 GB RAM (yaygınlaşıyor)

X250.000 kat artış!
```

**Gelecek:** DDR5, LPDDR5X → Daha hızlı, daha az enerji

**🤔 Felsefi Soru:**

"Bilgisayarlar her yıl daha güçlü oluyor ama insanlar 'yavaş' diyor. Problem donanım mı, yazılım mı, yoksa beklentilerimiz mi?"

**Cevap:** Yazılımlar da daha karmaşık hale geliyor. 2000'de Windows XP 128 MB RAM'de çalışıyordu. Bugün Chrome tek başına 2 GB RAM kullanıyor!

**⚡ SSD Devrimi:**

**2010 öncesi:** Sadece HDD vardı
**2010-2015:** SSD pahalı, sadece zenginler
**2015-2020:** SSD yaygınlaşıyor
**2020+:** SSD standart, HDD ölüyor

**Etki:**
- Windows 10 başlatma: HDD→90 sn, SSD→10 sn!
- Program açma 5-10 kat daha hızlı
- **En büyük performans artışı!**

**Öneri:** Eğer bilgisayarınız yavaşsa, SSD alın. En iyi yatırım!

**🌍 E-Atık Sorunu:**

Dünyada yılda 50 MİLYON TON elektronik atık!

**Sorun:**
- Eski bilgisayarlar çöpe atılıyor
- İçinde değerli madenler: Altın, gümüş, bakır
- Aynı zamanda zehirli: Kurşun, cıva

**Çözüm:**
- Geri dönüşüm
- İkinci el satış/bağış
- Tamir et, at ma!

**İlginç:** 1 ton cep telefonunda, 1 ton altın madeninden daha fazla altın var!

**🔐 Firmware Nedir?**

Donanım ve yazılım arası katman:

```
YAZILIM (Windows, Chrome) ← Değiştirilebilir
     ↓
FİRMWARE (BIOS, SSD firmware) ← Nadiren güncellenir
     ↓
DONANIM (İşlemci, RAM) ← Fiziksel
```

**Firmware:**
- Donanımı kontrol eden yazılım
- ROM'da saklanır
- Örnek: BIOS/UEFI (bilgisayar ilk açıldığında çalışır)
- Güncelleme riskli (yanlış olursa donanım bozulabilir!)

**💡 Quantum Computing (Kuantum Bilgisayarlar):**

Normal bilgisayar:
- Bit: 0 VEYA 1

Kuantum bilgisayar:
- Qubit: Aynı anda HEM 0 HEM 1!

**Süperpozisyon prensibi**

**Sonuç:**
- Belirli problemleri milyonlarca kat daha hızlı çözer
- Şifreleme kırma, ilaç geliştirme, hava tahmini

**Durum (2025):**
- Henüz deneysel
- Google, IBM çalışıyor
- 10-20 yıl içinde yaygınlaşabilir

---

## 🌟 İLGİNÇ BİLGİLER

1. **💾 İlk HDD (1956):** IBM 305 RAMAC - 3.75 MB kapasiteli, 1 TON ağırlığında, buzdolabı boyutunda! Şimdi 1 TB USB bellek 20 gram.

2. **🔥 İşlemci Sıcaklığı:** Modern işlemciler 100°C'ye kadar ısınabiliyor! Suyun kaynama noktası! Bu yüzden fanlar gerekli.

3. **💰 En Pahalı RAM:** Sunucu RAM'leri 1 TB kapasiteye ulaşabiliyor. Fiyat: 50.000+ TL!

4. **🎮 Oyun Konsolu vs PC:** PlayStation 5'in SSD'si bazı PC'lerden daha hızlı! Özel tasarlanmış donanım.

5. **📱 Telefon Gücü:** iPhone 13, 1990'ların TÜM süperbilgisayarlarından daha güçlü! Apollo 11'in (Ay'a giden roket) bilgisayarından 100.000 kat güçlü!

6. **🐛 İlk "Bug":** 1947'de bilgisayarda gerçek bir böcek (moth) bulundu, sorun yarattı. O günden beri yazılım hatasına "bug" denir!

7. **💡 Güç Tasarrufu:** Bilgisayarınızı "Uyku Modu"na almak yerine kapatırsanız, yılda 100-200 TL elektrik tasarrufu!

8. **🖱️ İlk Mouse:** Douglas Engelbart 1964'te tahta kutud an yaptı. Patent almayı unuttu, zengin olamadı!

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ VE GÜDÜLEME (7 dakika)

**Dikkat Çekme: "Yavaş Bilgisayar Hikayesi"**

"Ahmet'in bilgisayarı çok yavaş. Açılması 5 dakika sürüyor. Oyun oynarken takılıyor. Ne yapmalı?"

**Beyin Fırtınası:**
- Öğrenciler fikir versin
- Tahtaya yazın: Daha fazla RAM, SSD, vb.

**Cevap:**
"Bugün donanımı detaylı öğrenince, Ahmet'e nasıl yardım edeceğinizi bileceksiniz!"

**Günün Bilmeceleri:**

🧩 **Bilmece 1:**
```
Bilgisayarın beyni benim,
GHz ile hızımı söylerim.
Core i5, i7, Ryzen de olur,
İşlemciyim, bil artık! (Cevap: İşlemci/CPU)
```

🧩 **Bilmece 2:**
```
Geçici belleğim ben,
Kapanınca silirim.
RAM denir bana dostum,
Çalışma masasıyım! (Cevap: RAM)
```

### 2. KONU ANLATIMI - BÖLÜM 1: İşlemci ve RAM (18 dakika)

**İşlemci Sunumu:**

**Görsel: İşlemci fotoğrafı gösterin**

**"Bilgisayarın Beyni"**

**Özellikler:**

**1. Hız (GHz):**
- Tahtaya yazın: 3.5 GHz = 3.5 milyar işlem/saniye!
- "Saniyede adınızı 3.5 milyar kez yazabilir!"

**2. Çekirdek Sayısı:**
- Tek çekirdek = 1 kişi çalışıyor
- Dört çekirdek = 4 kişi birlikte çalışıyor
- "Hangi daha hızlı tamamlar?"

**3. Markalar:**
- Intel vs AMD
- Logoları gösterin

**RAM Sunumu:**

**"Çalışma Masası Analojisi" (Tekrar, Pekiştirme):**

Fiziksel gösterim yapın:

- Küçük masa gösterin (veya çizin): "2 GB RAM - Sadece 2 kitap sığar, sık sık değiştirirsin"
- Büyük masa: "16 GB RAM - 10 kitap aynı anda, hızlı çalışırsın!"

**RAM vs Sabit Disk:**

Tahtaya tablo çizin (öğrencilerle doldurun):

| Özellik | RAM | Sabit Disk |
|---------|-----|------------|
| Hız | ⚡ Çok hızlı | 🐢 Yavaş |
| Kalıcı mı? | ❌ Geçici | ✅ Kalıcı |
| Ne için? | Açık programlar | Dosyalar |

### 3. KONU ANLATIMI - BÖLÜM 2: Depolama (HDD vs SSD) (15 dakika)

**HDD Tanıtımı:**

**Görsel:** İç kısmı göster (dönen diskler)

**Analoji:**
"Gramofon gibi! Dönen disk, okuma kafası."

**Özellikler:**
- Mekanik, titreşime duyarlı
- Ucuz, büyük kapasite
- Yavaş

**SSD Tanıtımı:**

**Görsel:** SSD fotoğrafı

**Analoji:**
"USB bellek gibi! Elektronik çipler, hareketli parça YOK."

**Özellikler:**
- Çok hızlı!
- Dayanıklı
- Pahalı

**Canlı Karşılaştırma Videosu:**
YouTube'dan "HDD vs SSD speed test" videosu gösterin (2-3 dk)

**Öğrenciler görsün:**
- HDD: Windows 90 saniyede açılıyor
- SSD: Windows 10 saniyede açılıyor!

**"Vay be!" tepkisi alacaksınız 😊**

### 4. KONU ANLATIMI - BÖLÜM 3: Ekran Kartı (8 dakika)

**"Görüntü İşlemcisi"**

**Görevleri:**
- Ekrana görüntü gönderir
- 3D grafikleri işler
- Oyunlar için çok önemli!

**Entegre vs Ayrık:**

Tahtaya çizin:

```
ENTEGmE (Dahili):
├─ Anakart içinde
├─ Zayıf
└─ Temel işler için

AYRIK (Harici):
├─ Ayrı kart
├─ Güçlü
└─ Oyun ve profesyonel iş
```

**Örnekler:**
- NVIDIA GeForce RTX (oyunculara gösterin logo)
- AMD Radeon

### 5. KONU ANLATIMI - BÖLÜM 4: Yazılım Kurulumu (12 dakika)

**Canlı Demo: Güvenli Program Kurulumu**

**Seçenek 1: Microsoft Store'dan Kurulum (En Güvenli!)**

Projeksiyon ile gösterin:

1. Başlat → Microsoft Store
2. Bir uygulama arayın (örn: "Paint 3D" veya ücretsiz bir oyun)
3. "İndir" veya "Al" tuşuna bas
4. Otomatik indirilir ve kurulur
5. Başlat menüsünde görünür

**"Çok kolay ve GÜVENLİ!"**

**Seçenek 2: Web'den Kurulum (Dikkatli Olunmalı!)**

**Demo yapın (ama kurmayın, sadece gösterin):**

1. Güvenilir siteye gidin (örn: google.com/chrome)
2. "İndir" tuşu
3. İndirilen dosyayı çalıştır (.exe)
4. Kurulum sihirbazı
5. **DİKKAT ANI!**
   - "Extra Toolbar yüklensin mi?" → ❌ KALD IR!
   - "Varsayılan tarayıcı yap" → İstemiyorsanız kaldırın

**Tuzak Örneği Gösterin:**
- Sahte "İndir" butonu (reklam)
- Gerçek "İndir" butonu
- "Hangisine tıklamalıyız?"

### 6. KONU ANLATIMI - BÖLÜM 5: Güncelleme (8 dakika)

**"Neden Güncelleriz?"**

Tahtaya yazın:
1. Güvenlik (en önemli!)
2. Hata düzeltme
3. Yeni özellikler

**Windows Update Demo:**

Canlı gösterin:

1. Ayarlar → Windows Update
2. "Güncellemeleri denetle"
3. Eğer güncelleme varsa: İndir
4. "Şu an güncelleme yok" mesajı bile gösterin

**Vurgu:**
"Hiçbir zaman 'Sonra' demeyin! Hemen güncelleyin!"

### 7. PRATİK ETKİNLİK: Sorun Teşhisi (9 dakika)

**Senaryo Analizi - Grup Çalışması (3-4 kişilik):**

Her gruba bir senaryo kartı verin:

**Senaryo 1:**
"Bilgisayarım çok yavaş açılıyor. 5 dakika sürüyor."
**Soru:** Hangi donanım yükseltmesi en çok yarar?"
**Cevap:** SSD almak!

**Senaryo 2:**
"Oyun oynarken her şey takılıyor, donuyor."
**Soru:** Hangi donanım yetersiz olabilir?"
**Cevap:** Ekran kartı veya RAM yetersiz

**Senaryo 3:**
"Programı açtım ama 'Güncelleme gerekli' diyor."
**Soru:** Ne yapmalıyım?"
**Cevap:** Hemen güncellemeli!

**Senaryo 4:**
"Bilgisayarım 'Disk doldu' diyor."
**Soru:** Çözüm nedir?"
**Cevap:** Gereksiz dosyaları sil, Disk Temizleme çalıştır

**Gruplar tartışır (3 dk), sonuç ları paylaşır (6 dk)**

### 8. ÖLÇME VE DEĞERLENDİRME (2 dakika)

**Hızlı Sorular:**

1. "RAM nedir, ne işe yarar?" - 1 öğrenci
2. "HDD ve SSD farkı?" - 1 öğrenci
3. "Yazılım neden güncellenir?" - 1 öğrenci

### 9. KAPANIŞ VE ÖDEV (1 dakika)

**Özet:**
- İşlemci = Beyin, hız önemli
- RAM = Çalışma masası, fazlası iyi
- SSD >> HDD (çok daha hızlı!)
- Güncelleme = Güvenlik!

---

## 😄 GÜNÜN FIKRASI

**RAM Fakirliği**

Temel bilgisayar alıyor:
- **Satıcı:** "Bu bilgisayarda 8 GB RAM var."
- **Temel:** "Çok az! 16 GB olsun!"
- **Satıcı:** "Tamam, 16 GB yapalım. 500 TL ekstra."
- **Temel:** "Çok pahalı! 8 GB yeterli aslında."
- **Satıcı:** "Karar verin, 8 mi 16 mı?"
- **Temel:** "İkisini de alayım! 8+16=24 GB olsun!" 😄

---

**HDD vs SSD**

Bilgisayar mağazasında:
- **Müşteri:** "SSD neden bu kadar pahalı?"
- **Satıcı:** "Çünkü çok hızlı! HDD'den 10 kat!"
- **Müşteri:** "Peki ben fark eder miyim?"
- **Satıcı:** "Tabii ki! Windows 10 saniyede açılır!"
- **Müşteri:** "Ben genelde bilgisayarı kapalı tutuyorum." 😂

---

## 🏠 EV ÖDEVİ

### Ödev: "Donanım Uzmanı ve Yazılım Yöneticisi"

**BÖLÜM 1: Donanım Analizi**

Evinizde kullandığınız bilgisayar/laptop'ta:

**Görev 1: Donanım Özellikleri**

1. "Bu Bilgisayar" → Sağ tık → Özellikler

Yazın:
- **İşlemci:** ________________
  - Kaç çekirdek? _____ (Google'da arayın: "[işlemci modeli] core count")
  - Hızı: _____ GHz
- **RAM:** _____ GB
- **Depolama:**
  - ☐ HDD ☐ SSD ☐ İkisi de
  - Kapasite: _____ GB/TB

**Görev 2: Performans Testi**

Görev Yöneticisi'ni açın (Ctrl+Shift+Esc):

**Boş durumdayken (hiçbir program açık değil):**
- CPU kullanımı: _____%
- RAM kullanımı: _____ GB / _____ GB (____%)

**Bir oyun/program açtıktan sonra:**
- CPU kullanımı: _____%
- RAM kullanımı: _____ GB / _____ GB (____%)

**Fark:** _____ % CPU artışı, _____ GB RAM artışı

**BÖLÜM 2: Yükseltme Önerisi**

Bilgisayarınızın en zayıf noktası hangisi? (birini seç)

☐ İşlemci (çok eski/yavaş)
☐ RAM (yetersiz, sık sık %90+ kullanılıyor)
☐ HDD (SSD yok, yavaş)
☐ Ekran kartı (oyunlar takılıyor)

**Öneriniz:**
"Bilgisayarımı hızlandırmak için _____________ yükseltmeli/eklemeliyim."

**Neden?**
_________________________________________________

**BÖLÜM 3: Yazılım Güncellemeleri**

**Görev 1: Windows Güncellemesi Kontrolü**

1. Ayarlar → Windows Update
2. "Güncellemeleri denetle" tuşuna bas

**Sonuç:**
☐ Güncelleme var → İndir ve yükle (veli izniyle)
☐ Güncelleme yok → Ekran görüntüsü al

**En son güncelleme tarihi:** ___/___/202___

**Görev 2: Program Güncellemeleri**

3 program seçin, güncelleme durumunu kontrol edin:

| Program | Versiyon | Güncelleme Var mı? |
|---------|----------|-----------------------|
| Örnek: Chrome | 121.0 | ☐ Evet ☐ Hayır |
| | | ☐ Evet ☐ Hayır |
| | | ☐ Evet ☐ Hayır |
| | | ☐ Evet ☐ Hayır |

**BÖLÜM 4: Araştırma**

İnternetten araştırın:

**1. SSD Fiyatları:**
- 500 GB SSD fiyatı: _____ TL (kaynak: __________)
- 1 TB SSD fiyatı: _____ TL

**2. RAM Fiyatları:**
- 8 GB RAM fiyatı: _____ TL
- 16 GB RAM fiyatı: _____ TL

**3. Karşılaştırma:**
Hangisi daha uygun fiyatlı yükseltme?
☐ SSD eklemek
☐ RAM eklemek

**BONUS (+15 puan):**

**Gerçek Kurulum Deneyimi:**

Microsoft Store'dan ÜCRETSIZ bir uygulama indirin ve kurun (veli izniyle).

Örnek uygulamalar:
- Ubuntu (Linux deneme)
- Paint 3D
- Code.org oyunları
- Herhangi bir ücretsiz oyun

**Rapor:**
1. Hangi uygulamayı kurdunuz? ___________
2. Kurulum ne kadar sürdü? _____ dakika
3. Sorun yaşadınız mı? ☐ Evet ☐ Hayır
4. Uygulamayı test ettiniz mi? Nasıldı?
   _____________________________________________

**Veli İmzası:** ________________

**Değerlendirme:**

| Kriter | Puan |
|--------|------|
| Donanım özellikleri bulunmuş | 20 puan |
| Performans testi yapılmış | 15 puan |
| Yükseltme önerisi sunulmuş | 15 puan |
| Güncelleme kontrolü yapılmış | 20 puan |
| Fiyat araştırması | 20 puan |
| Rapor düzenli | 10 puan |
| **TOPLAM** | **100 puan** |

**Teslim:** Gelecek hafta

---

## 📊 ÖZ DEĞERLENDİRME

| Konu | Anladım | Kısmen Anladım | Anlamadım |
|------|---------|----------------|-----------|
| İşlemci özellikleri | ☐ | ☐ | ☐ |
| RAM işlevi | ☐ | ☐ | ☐ |
| HDD vs SSD farkı | ☐ | ☐ | ☐ |
| Yazılım kurulumu | ☐ | ☐ | ☐ |
| Güncelleme önemi | ☐ | ☐ | ☐ |

**En ilginç bulduğum bilgi:**
_________________________________________________

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Hayatta en hakiki mürşit ilimdir, fendir."
> **- Mustafa Kemal ATATÜRK**

**Derste Bahset:**
- Teknolojide yerli üretim: ASELSAN, HAVELSAN, STM
- Türk mühendisleri dünyada başarılı
- Milli teknoloji hamleleri

**Tartışma:**
"Türkiye kendi işlemcisini üretebilir mi?"

---

## 💎 DEĞERLER EĞİTİMİ

**DÜRÜSTLİK:**
- Korsan yazılım kullanmayın
- Emeğe saygı

**TASARRUF:**
- Donanımı koru, uzun kullan
- Gereksiz yükseltme yapma

**BİLİMSELLİK:**
- Donanım karmaşık mühendislik
- Sürekli gelişim

---

## 👨‍🏫 ÖĞRETMEN İÇİN NOTLAR

### Hazırlık:
- Projeksiyon
- HDD ve SSD fotoğrafları/videoları
- Microsoft Store erişimi
- YouTube: HDD vs SSD karşılaştırma videosu

### Dikkat:
- Öğrencilere okul bilgisayarlarına kurulum YAPTIRMAYIN!
- Sadece gösterimi yapın

### Alternatifler:
- Fiziksel donanım parçası varsa gösterin
- İçi açılabilir eski bilgisayar

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Veli,**

Bu hafta **Donanım ve Yazılım Detayları** öğrendik.

✅ İşlemci, RAM, SSD/HDD
✅ Yazılım kurulumu
✅ Güncelleme önemi

**Destek:**
- Çocuğunuzun bilgisayar donanımını birlikte inceleyin
- Güncelleme yapmalarına izin verin (güvenlidir)
- Microsoft Store'dan ücretsiz uygulama deneyebilirsiniz

**Ödev:**
- Donanım analizi
- Güncelleme kontrolü
- Fiyat araştırması

**Uyarı:**
Bilinmeyen sitelerden program indirmeyin! Sadece resmi kaynaklar.

Saygılarımla,
**Bilişim Teknolojileri Öğretmeni**

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
