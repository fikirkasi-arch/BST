# HAFTA 35: İLERİ SEVİYE PROJE 1 - PLATFORM OYUNU
**Sınıf:** 5
**Ünite:** 6 - Yazılım Tasarımı ve Programlama
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Tüm Öğrenilenleri Birleştirerek Oyun Yapma

---

## 🎯 ÖĞRENME KAZANIMLARI

- Tüm Scratch kavramlarını birleştirir
- Platform oyunu yapar
- Karakter kontrolü kodlar
- Yer çekimi simülasyonu yapar
- Oyun mekaniği tasarlar

---

## 📚 PROJE TANITIMI

### Platform Oyunu Nedir?

**Örnekler:**
- Super Mario
- Sonic
- Flappy Bird

**Temel Mekanik:**
- Karakter hareket eder (sağ/sol)
- Zıplar (yukarı)
- Yer çekimi var (aşağı düşer)
- Platformlara oturur
- Hedefe ulaşır

### Kullanılacak Kavramlar

✅ **Hareket:** Ok tuşlarıyla kontrol
✅ **Döngüler:** Sonsuza kadar
✅ **Koşullar:** Duvara değdi mi, zemine değdi mi
✅ **Değişkenler:** Hız, skor
✅ **Klonlama:** Düşmanlar, coinler
✅ **Ses:** Zıplama, coin toplama sesleri

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. PLANLAMA (10 dk)

**Oyun Tasarımı:**

**Karakterler:**
- Ana karakter (oyuncu)
- Düşman (opsiyonel)
- Coin/yıldız (toplanacak)

**Sahne:**
- Platform yapısı (zemin, duvarlar)

**Mekanik:**
- Sağ/Sol hareket
- Zıplama
- Yer çekimi
- Puan toplama

### 2. TEMEL KARAKTER KONTROLÜ (20 dk)

**Sprite: Karakter (Kedi veya diğer)**

**Hareket Kodu:**
```
(Yeşil bayrak tıklandığında)
[x: -200 y: -100 git]
[Hız Y değişkenini 0 yap]

[sonsuza kadar]
  // Sağ-Sol Hareket
  <EĞER [sağ ok tuşuna basıldı mı?]>
    [x yönünde 5 değiştir]
    [90 yöne bak]

  <EĞER [sol ok tuşuna basıldı mı?]>
    [x yönünde -5 değiştir]
    [-90 yöne bak]

  // Zıplama
  <EĞER <<yukarı ok tuşuna basıldı mı?> ve <[Zemin'e değdi mi?]>>>
    [Hız Y değişkenini 15 yap]

  // Yer Çekimi
  [Hız Y değişkenini -1 değiştir]
  [y yönünde [Hız Y] değiştir]

  // Zemine Oturma
  <EĞER [Zemin'e değdi mi?]>
    [y yönünde 5 değiştir]
    [Hız Y değişkenini 0 yap]
```

**Not:** "Zemin" sprite'ı ayrıca oluşturulmalı (yeşil çizgi veya platform)

### 3. SAHNE ve PLATFORMLAR (10 dk)

**Sprite: Zemin/Platform**

Basit yeşil dikdörtgen çizin (Paint editörde)

**Yerleştirme:**
- Altta zemin
- Ortada platformlar (atlama için)

**Kopya:**
Birden fazla platform için sprite'ı çoğaltabilir (sağ tık → duplicate)

### 4. PUAN SİSTEMİ (15 dk)

**Sprite: Coin/Yıldız**

```
(Yeşil bayrak tıklandığında)
[Skor değişkenini 0 yap]
[gizle]
[5 kez tekrarla]
  [kendini klonla]

(Klon olarak oluşturulduğunda)
[x: <-200 ile 200 arası rastgele> y: <-100 ile 150 arası rastgele> git]
[göster]
[sonsuza kadar]
  <EĞER [Karakter'e değdi mi?]>
    [Skor değişkenini 1 arttır]
    [Pop sesi çal]
    [bu klonu sil]
```

### 5. DÜŞMAN (Opsiyonel) (15 dk)

**Sprite: Düşman**

```
(Yeşil bayrak tıklandığında)
[x: 100 y: -100 git]
[sonsuza kadar]
  [5 adım git]
  <EĞER [kenara değdi mi?]>
    [180 derece dön]
  <EĞER [Karakter'e değdi mi?]>
    [Oyun Bitti! söyle]
    [tümünü durdur]
```

### 6. TEST ve İYİLEŞTİRME (10 dk)

**Test:**
- Zıplama çalışıyor mu?
- Karakterden düşmüyor mu?
- Coinler toplanıyor mu?
- Düşmana değince oyun bitiyor mu?

**İyileştirme:**
- Ses ekle
- Arka plan değiştir
- Seviye tasarımı

---

## 🏠 EV ÖDEVİ

**"Oyununu Geliştir"**

**Görev:**
Sınıfta yaptığın platform oyununu geliştir

**Eklenecekler:**
1. En az 3 farklı platform
2. En az 5 coin
3. Bir düşman
4. Başlangıç ekranı ("Başla" butonu)
5. Bitiş ekranı ("Kazandın!" veya "Kaybettin!")

**Bonus:**
- Seviye 2 ekle
- Can sistemi (3 can)
- Zamanlayıcı

---

## 📊 ÖZ DEĞERLENDİRME

**Kendimi Değerlendiriyorum:**

- ☐ Karakter kontrolü yapabiliyorum
- ☐ Yer çekimi simülasyonu yapabildim
- ☐ Platform yapısı oluşturdum
- ☐ Puan sistemi ekledim
- ☐ Tüm kavramları birleştirdim
- ☐ Oyun yapabiliyorum!

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Zorluk Seviyesi:**
- Bu proje 5. sınıf için zorlayıcı olabilir
- Adım adım ilerleyin, acele etmeyin
- Herkesin temel kısmı yapması yeterli

**Yer Çekimi:**
- En zor kısım!
- "Hız Y" değişkeni sürekli azalır (yer çekimi)
- Zemine değince sıfırlanır
- Basit fizik simülasyonu

**Zıplama Kontrolü:**
- Sadece zemindeyken zıplama
- Yoksa sonsuz zıplama olur (hava'da zıplar)

**Sık Sorunlar:**
- "Zemindan geçiyor!" → "y yönünde 5 değiştir" bloğu eksik
- "Zıplayamıyor!" → Zemin sprite adı yanlış veya koşul hatalı
- "Çok hızlı düşüyor!" → Yer çekimi değerini azaltın (-1 yerine -0.5)

**Alternatif:**
Yer çekimi çok zorsa, basit yukarı-aşağı hareket ile başlayın

---

## 💡 MERAKLISINA

**Platform Oyunları:**

🎮 **Super Mario (1985):** İlk ünlü platform oyunu

🦔 **Sonic:** Hızlı platform oyunu

🐦 **Flappy Bird:** Basit ama bağımlılık yapan platform oyunu (2013)

🏆 **En Çok Satan:** Super Mario Bros - 40+ milyon kopya!

**Fizik Motoru:**
Gerçek oyunlarda karmaşık fizik motorları var (Unity, Unreal Engine)

---

## 🧩 EĞLENCE

**Oyun Tasarım Sorusu:**

Karakterin zıplama yüksekliği 15, yer çekimi -1.
En yüksek noktaya ne zaman ulaşır?

**Cevap:** 15 kare sonra (her karede -1, 15'ten 0'a düşer)

---

**Şaka:**

Programcı çocuk: "Babacığım, oyunumda yer çekimi çalışmıyor!"
Baba: "Ne oluyor?"
Çocuk: "Karakterim uzaya uçtu!" 🚀😄

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Bir ulusun kurtuluşu için fikir ve akıl gücü gereklidir."
> **- Mustafa Kemal Atatürk**

Atatürk, akıl ve fikir gücünün önemini vurgulamıştır. Oyun tasarlarken de akıl ve fikir kullanıyorsunuz. Yaratıcı düşünerek harika projeler yapabilirsiniz!

---

## 💎 DEĞERLER EĞİTİMİ

**Sabır:**
Karmaşık proje, sabır gerektirir. Hata yapsan da sabırla düzelt.

**Problem Çözme:**
Oyun çalışmıyorsa, problemi bul ve çöz.

**Yaratıcılık:**
Kendi oyun tasarımını yap, yaratıcı ol!

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta çocuğunuz **ileri seviye proje** yaptı. Platform oyunu tasarladı!

**Proje İçeriği:**
- Karakter kontrolü
- Yer çekimi simülasyonu
- Puan sistemi
- Düşman mekaniği

**Ev Ödevi:**
Oyunu geliştirmek ve zenginleştirmek

**Not:**
Bu proje, tüm öğrenilen kavramları birleştirir. Çocuğunuz Scratch'te artık gerçek oyunlar yapabiliyor! Projesini izleyin, teşvik edin.

**Oyun Geliştirme:**
Çocuğunuz gelecekte oyun geliştiricisi olabilir. Bu proje, ilk adımıdır!

---

## 📎 EK KAYNAKLAR

**Platform Oyun Örnekleri:**
- "Simple Platformer" (Scratch)
- "Jumping Game Tutorial"

**Videolar:**
- "Scratch Platform Oyunu Türkçe"
- "Gravity in Scratch"

**Fizik:**
- Yer çekimi simülasyonu
- Sürtünme (friction)
- Hız (velocity)

**İleri Seviye:**
- Çift zıplama (double jump)
- Duvar zıplaması (wall jump)
- Kayma (slide)

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
