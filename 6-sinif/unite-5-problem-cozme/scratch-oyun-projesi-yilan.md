# SCRATCH OYUN PROJESİ: YILAN OYUNU
**Zorluk:** İleri Seviye
**Tahmini Süre:** 4 Ders Saati (160 dakika)
**Sınıf:** 6. Sınıf

---

## 🎯 PROJE AMACI

Klasik yılan oyununu Scratch ile programlayarak:
- Karmaşık hareket kontrolü
- Listeler kullanımı
- Çarpışma kontrolü
- Skor sistemi
- Oyun sonu koşulları

---

## 🎮 OYUN MEKANİĞİ

**Oynanış:**
- Yılan ok tuşlarıyla hareket eder
- Elma yiyince büyür
- Kenarlara veya kendine çarparsa oyun biter
- Skor artar

---

## 🔬 MERAKLISININA

### İlginç Oyun Tarihi

**🐍 İlk Yılan Oyunu:**
1976 yılında "Blockade" adlı arcade oyununda ortaya çıktı!

**📱 Nokia Efsanesi:**
1998'de Nokia 6110 telefonuyla ünlendi. 400 MİLYONdan fazla telefonda vardı!

**🎯 Neden Bu Kadar Popüler?**
- Basit ama bağımlılık yapıcı
- Sonsuz oynanabilirlik
- Her oyun farklı

**💡 Algoritmik Zorluk:**
Yılanın kendini takip etmesi için "kuyruk dizisi" (array) kullanılır!

**🤔 Matematik Problemi:**
Teoride mükemmel oynarsanız, yılan tüm ekranı doldurabilir! Kaç hücre eder?

---

## 🎯 CAN ALICI HUSUSLAR

### Öğretmen İçin Kritik Noktalar:

**⚠️ Zorluk Seviyeleri:**
- Bu proje önceki Scratch deneyimi gerektirir
- Liste kavramı ilk kez öğretiliyor - sabırlı olun
- Koordinat sistemi anlaşılmalı

**💡 Başarı İçin:**
- Önce tek kare yılan ile başlayın
- Sonra uzama özelliği ekleyin
- Adım adım test edin

**🎯 Sık Yapılan Hatalar:**
- Yılanın çok hızlı hareket etmesi
- Çarpışma kontrolünün eksik olması
- Listelerin yanlış kullanımı

**📌 Mutlaka Öğretin:**
- X ve Y koordinatları
- Liste ekleme/silme mantığı
- Döngü içinde koşul kontrolü

---

## 📋 GEREKLİ BİLGİLER

### Ön Koşullar:
- Scratch temel blokları bilmek
- Değişken kullanımı
- Koşullu ifadeler (if-else)
- Döngüler (forever, repeat)

### Yeni Öğrenilecekler:
- **Listeler:** Birden fazla değer saklama
- **Klon oluşturma:** Aynı kukladan çoğaltma
- **Karmaşık hareket kontrolü**
- **Çarpışma algılama**

---

## 🎨 TASARIM

### Kuklalar (Sprites):

**1. Yılan Başı (Snake)**
- 20x20 piksel yeşil kare
- Gözleri olan basit tasarım

**2. Yılan Gövdesi (Body)**
- 20x20 piksel koyu yeşil kare
- Klonlanacak

**3. Elma (Apple)**
- Kırmızı elma çizimi veya emoji 🍎
- Rastgele konumda belirir

**4. Duvar (isteğe bağlı)**
- Ekran kenarlarını gösterir

### Sahne:
- Siyah veya koyu zemin
- Grid (ızgara) çizgileri (isteğe bağlı)
- Skor tablosu

---

## 💻 KOD YAPISI

### A) DEĞİŞKENLER

```
📊 Değişkenler (Tüm kuklalar için):
- skor (Sayı) = 0
- oyun_durumu (Metin) = "başla"
- hız (Sayı) = 10
- yön (Metin) = "sağ"

📊 Listeler:
- yılan_x (Sayı listesi) = []
- yılan_y (Sayı listesi) = []
```

---

### B) YILAN BAŞI KODU

#### 1. Oyun Başlatma

```scratch
🏁 Bayrak tıklandığında
  Skor = 0
  Hız = 10
  Yön = "sağ"
  Yılan_x listesini sil
  Yılan_y listesini sil

  // Başlangıç pozisyonu (0,0)
  Yılan_x listesine 0 ekle
  Yılan_y listesine 0 ekle

  X: 0, Y: 0 konumuna git
  Oyun_durumu = "devam"

  // Hareket döngüsünü başlat
  "hareket_et" mesajını gönder
```

---

#### 2. Hareket Kontrolü

```scratch
🎮 "hareket_et" mesajını aldığında
  Sonsuza kadar tekrarla:

    Eğer oyun_durumu = "devam" ise:

      // Yön tuşları kontrolü
      Eğer "sağ ok" tuşuna basılmış ise:
        Eğer yön ≠ "sol" ise:  // Geri gitmesini engelle
          Yön = "sağ"

      Eğer "sol ok" tuşuna basılmış ise:
        Eğer yön ≠ "sağ" ise:
          Yön = "sol"

      Eğer "yukarı ok" tuşuna basılmış ise:
        Eğer yön ≠ "aşağı" ise:
          Yön = "yukarı"

      Eğer "aşağı ok" tuşuna basılmış ise:
        Eğer yön ≠ "yukarı" ise:
          Yön = "aşağı"

      // Yeni başın konumunu hesapla
      Yeni_x = (yılan_x listesinin 1. elemanı)
      Yeni_y = (yılan_y listesinin 1. elemanı)

      Eğer yön = "sağ" ise:
        Yeni_x = Yeni_x + 20

      Eğer yön = "sol" ise:
        Yeni_x = Yeni_x - 20

      Eğer yön = "yukarı" ise:
        Yeni_y = Yeni_y + 20

      Eğer yön = "aşağı" ise:
        Yeni_y = Yeni_y - 20

      // Yeni pozisyonu listeye ekle (başa)
      Yılan_x listesinin başına Yeni_x ekle
      Yılan_y listesinin başına Yeni_y ekle

      // Kuyruğu sil (elma yenmediyse)
      Eğer "elma yendimi" değilse:
        Yılan_x listesinin son elemanını sil
        Yılan_y listesinin son elemanını sil
      Değilse:
        Elma_yendimi = hayır
        Skor = Skor + 10

      // Başı yeni konuma taşı
      X: Yeni_x, Y: Yeni_y konumuna git

      // Çarpışma kontrolü
      "çarpışma_kontrol" mesajını gönder

      // Gövdeyi güncelle
      "gövde_güncelle" mesajını gönder

      Hız / 10 saniye bekle
```

---

#### 3. Çarpışma Kontrolü

```scratch
📨 "çarpışma_kontrol" mesajını aldığında

  // Kenara çarpma kontrolü
  Eğer X_konumu > 220 veya X_konumu < -220 veya
     Y_konumu > 160 veya Y_konumu < -160 ise:
    "oyun_bitti" mesajını gönder

  // Kendine çarpma kontrolü
  I = 2 olsun
  (Yılan_x listesinin uzunluğu) kere tekrarla:
    Eğer Yılan_x[1] = Yılan_x[I] ve
       Yılan_y[1] = Yılan_y[I] ise:
      "oyun_bitti" mesajını gönder
    I = I + 1
```

---

#### 4. Elma Çarpışması

```scratch
Sonsuza kadar:
  Eğer Apple'a değiyorsa:
    Elma_yendimi = evet
    "yeni_elma" mesajını gönder
    "ye" sesini çal
```

---

### C) YILAN GÖVDESİ (Body) KODU

```scratch
🏁 Bayrak tıklandığında
  Saklan  // Ana kukla görünmez

📨 "gövde_güncelle" mesajını aldığında
  // Tüm klonları sil
  Klonları sil

  // Her gövde parçası için klon oluştur
  I = 2 olsun
  (Yılan_x listesinin uzunluğu) kere tekrarla:
    Klonumu oluştur
    I = I + 1

🎭 Bir klonu oluşturulduğunda
  X: Yılan_x[I], Y: Yılan_y[I] konumuna git
  Göster
```

---

### D) ELMA (Apple) KODU

```scratch
🏁 Bayrak tıklandığında
  "yeni_elma" mesajını gönder

📨 "yeni_elma" mesajını aldığında
  Sonsuza kadar tekrarla:
    // Rastgele konum (20'nin katları)
    Rastgele_x = -200 ile 200 arasında rastgele sayı
    Rastgele_x = (Rastgele_x / 20) yuvarlat * 20

    Rastgele_y = -140 ile 140 arasında rastgele sayı
    Rastgele_y = (Rastgele_y / 20) yuvarlat * 20

    // Yılanın üstüne gelmesin kontrolü
    Uygun = evet
    Yılan_x listesinin her elemanı için:
      Eğer Rastgele_x = Yılan_x[i] ve
         Rastgele_y = Yılan_y[i] ise:
        Uygun = hayır

    Eğer Uygun = evet ise:
      X: Rastgele_x, Y: Rastgele_y konumuna git
      Döngüden çık
```

---

### E) OYUN BİTİŞİ

```scratch
📨 "oyun_bitti" mesajını aldığında (Yılan Başı)
  Oyun_durumu = "bitti"
  "Oyun Bitti!" de 2 saniye
  "Skorun: " ile Skor birleşimi de 2 saniye
  "Tekrar oynamak için Bayrak'a tıkla!" de

📨 "oyun_bitti" mesajını aldığında (Gövde)
  Klonları sil
  Saklan

📨 "oyun_bitti" mesajını aldığında (Elma)
  Saklan
```

---

## 🎨 GÖRSEL İYİLEŞTİRMELER (İsteğe Bağlı)

### 1. Animasyonlu Yılan
- Yılan başına göz ekleyin
- Yöne göre gözler hareket etsin

### 2. Ses Efektleri
- Elma yeme sesi
- Oyun bitişi sesi
- Arka plan müziği

### 3. Skorboard
- Ekranın üstüne skor yazısı
- Yüksek skor kaydetme

### 4. Seviyeler
- Her 50 puanda hız artar
- Farklı zorluk modları

### 5. Bonus Özellikler
- Özel elmalar (2x puan)
- Duvarlar/engeller
- Zaman modu

---

## ✅ TEST SENARYOLARI

### Test 1: Temel Hareket
- [ ] Yılan sağa hareket ediyor
- [ ] Yılan sola hareket ediyor
- [ ] Yılan yukarı hareket ediyor
- [ ] Yılan aşağı hareket ediyor
- [ ] Geri dönmesini engelliyor

### Test 2: Büyüme
- [ ] Elma yendiğinde yılan büyüyor
- [ ] Skor artıyor
- [ ] Yeni elma görünüyor

### Test 3: Çarpışma
- [ ] Sağ kenara çarpınca oyun bitiyor
- [ ] Sol kenara çarpınca oyun bitiyor
- [ ] Üst kenara çarpınca oyun bitiyor
- [ ] Alt kenara çarpınca oyun bitiyor
- [ ] Kendine çarpınca oyun bitiyor

### Test 4: Oyun Akışı
- [ ] Oyun başlatılıyor
- [ ] Oyun bitince "Oyun Bitti" mesajı görünüyor
- [ ] Tekrar oynatılabiliyor

---

## 🐛 SORUN GİDERME

### Problem 1: Yılan çok hızlı/yavaş
**Çözüm:** `hız` değişkenini ayarlayın (5-15 arası optimal)

### Problem 2: Yılan ekrandan çıkıyor ama oyun bitmiyor
**Çözüm:** Çarpışma kontrolündeki sınır değerlerini kontrol edin

### Problem 3: Gövde doğru görünmüyor
**Çözüm:** Gövde güncel leme mesajının doğru gönderildiğinden emin olun

### Problem 4: Elma yılanın içinde görünüyor
**Çözüm:** Elma konum kontrolünü düzgün yapın

### Problem 5: Kendine çarpma algılanmıyor
**Çözüm:** Çarpışma kontrolünde I=2'den başladığından emin olun (baş hariç)

---

## 🏆 DEĞERLENDİRME RUBRİĞİ

| Kriter | Mükemmel (25p) | İyi (20p) | Orta (15p) | Gelişmeli (10p) |
|--------|---------------|----------|-----------|----------------|
| **Hareket** | Tüm yönlerde kusursuz | Çoğu yönde çalışıyor | Bazı yönlerde sorun | Hareket çalışmıyor |
| **Büyüme** | Mükemmel çalışıyor | Çoğunlukla çalışıyor | Bazen sorun | Çalışmıyor |
| **Çarpışma** | Tüm durumlar kontrollü | Çoğu durum kontrollü | Bazı durumlar eksik | Kontrol yok |
| **Kod Kalitesi** | Temiz, yorumlu | İyi organize | Karışık ama çalışıyor | Dağınık |

**TOPLAM: 100 puan**

**Bonus:**
- Ses efektleri: +5
- Görsel iyileştirme: +5
- Özel özellik: +10

---

## 💡 GELİŞTİRME FİKİRLERİ

### Kolay Seviye:
- Farklı renkli elma (+5 puan)
- Arka plan müziği
- Başlangıç ekranı

### Orta Seviye:
- Hız artışı (her 50 puanda)
- Duvarlar/engeller ekle
- 2 oyuncu modu

### İleri Seviye:
- Yapay zeka rakip yılan
- Seviye sistemi
- Yüksek skor tablosu (bulut kaydı)
- Power-up'lar (yavaşlatma, hızlanma, hayalet mod)

---

## 📚 ÖĞRENME ÇIKTILARI

Bu projeyi tamamladığınızda:

✅ Liste veri yapısını kullanabileceksiniz
✅ Klon oluşturma ve yönetme bileceksiniz
✅ Karmaşık hareket kontrol ü programlayabileceksiniz
✅ Çarpışma algılama yapabileceksiniz
✅ Oyun mekaniği tasarlayabileceksiniz
✅ Koordinat sistemi kullanabileceksiniz

---

## 🏠 EV ÖDEVİ

### 1. Oyununuzu Özelleştirin
En az 3 özellik ekleyin:
- Farklı görünüm
- Ses efektleri
- Özel mod

### 2. Oyun Tasarım Belgesi
```
OYUN ADI: _____________________

ÖZELLİKLER:
- _____________________________
- _____________________________
- _____________________________

NASIL OYNANIR:
_______________________________
_______________________________

EN ZOR KISIM:
_______________________________

EN EĞLENCELI KISIM:
_______________________________

SKOR SİSTEMİ:
_______________________________
```

### 3. Video Kayıt (Bonus)
Oyununuzu oynarken kaydedin ve açıklayın!

---

## 👨‍🏫 ÖĞRETMEN İÇİN NOTLAR

### Ders Planı (4 x 40 dakika)

**1. Ders:** Tasarım ve temel hareket
**2. Ders:** Büyüme ve elma sistemi
**3. Ders:** Çarpışma kontrolü
**4. Ders:** İyileştirmeler ve test

### Önemli Noktalar:
- Listeler ilk kez öğretiliyor - bol örnek verin
- Koordinat sistemini tahtada çizin
- Adım adım ilerleyin, acele etmeyin
- Her öğrenci kendi hızında ilerlesin

### Yardım Stratejisi:
- Önce kendi denesinler
- Arkadaşına sorsunlar
- Sonra öğretmene sorsunlar

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Proje Seviyesi:** İleri
**Tahmini Süre:** 4 ders saati
**Sınıf:** 6. Sınıf
