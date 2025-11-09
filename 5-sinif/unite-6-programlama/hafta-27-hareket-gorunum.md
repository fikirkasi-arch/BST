# HAFTA 27: HAREKET VE GÖRÜNÜM BLOKLARI
**Sınıf:** 5
**Ünite:** 6 - Yazılım Tasarımı ve Programlama
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Hareket Blokları, Görünüm Blokları, Koordinatlar

---

## 🎯 ÖĞRENME KAZANIMLARI

- Hareket bloklarını kullanır (git, dön, kayma)
- Koordinat sistemini anlar (x, y)
- Görünüm bloklarını kullanır (söyle, düşün, göster/gizle)
- Kostüm değiştirir
- Boyut ve efekt uygular

---

## 📚 KONU ÖZETİ

### Hareket Blokları (Mavi)

**1. Adım Git:**
`[10 adım git]` → Sprite 10 adım ilerler

**2. Dön:**
- `[15 derece dön ↻]` → Sağa döner
- `[15 derece dön ↺]` → Sola döner

**3. X, Y Konumuna Git:**
`[x: 0 y: 0 git]` → Belirli yere gider

**4. Kayarak Git:**
`[1 saniyede x: 100 y: 50 kaydir]` → Yavaşça hareket

**5. Kenara Dokunca Sek:**
`[Kenara dokunduğunda sek]` → Duvara çarpmaz

### Koordinat Sistemi

**Sahne Boyutu:** 480 x 360 piksel

**Koordinatlar:**
- **x:** Yatay (soldan sağa) → -240 ile +240 arası
- **y:** Dikey (aşağıdan yukarıya) → -180 ile +180 arası
- **Merkez:** x: 0, y: 0

**Örnekler:**
- Sağ üst köşe: x: 240, y: 180
- Sol alt köşe: x: -240, y: -180

### Görünüm Blokları (Mor)

**1. Söyle/Düşün:**
- `[Merhaba söyle]` → Konuşma balonu
- `[Hmm... düşün]` → Düşünce balonu

**2. Göster/Gizle:**
- `[göster]` → Sprite görünür
- `[gizle]` → Sprite kaybolur

**3. Kostüm Değiştir:**
`[kostüm2 seç]` → Görünümü değiştirir (animasyon için)

**4. Boyut:**
`[boyutu %100 yap]` → Sprite büyüklüğü
`[boyutu 10 değiştir]` → Büyüt/küçült

**5. Efekt:**
- Renk, balıkgözü, döndür, piksel, mozaik, parlaklık, hayalet

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ (5 dk)

**Geçen Hafta Hatırlama:**
- Scratch nedir?
- Sprite nedir?
- Blok nasıl birleşir?

**Bugün:**
"Karakterlerimizi hareket ettirip konuşturacağız!"

### 2. KONU ANLATIMI (20 dk)

**Hareket Blokları (Projeksiyon ile gösterim):**

**Örnek 1:**
```
(Yeşil bayrak tıklandığında)
[10 adım git]
[15 derece dön ↻]
```
Çalıştır, ne oluyor?

**Örnek 2:**
```
(Yeşil bayrak tıklandığında)
[x: 0 y: 0 git]
[1 saniyede x: 100 y: 50 kaydir]
```

**Koordinat Sistemi:**
- Tahtada koordinat çizimi
- x nereye gidiyor? (sağ/sol)
- y nereye gidiyor? (yukarı/aşağı)
- Öğrenciler tahmin: x: 100, y: 100 nerede?

**Görünüm Blokları:**

**Örnek 3:**
```
(Yeşil bayrak tıklandığında)
[Merhaba! söyle] (2 saniye)
[boyutu %150 yap]
```

**Kostüm Değiştirme:**
Sprite'ın farklı kostümleri gösterilir, değiştirme demosu

### 3. UYGULAMALI ÇALIŞMA (50 dk)

**Görev 1: Kare Çizme (15 dk)**
Sprite ile kare şekli oluştur

**Kod:**
```
(Yeşil bayrak tıklandığında)
[100 adım git]
[90 derece dön ↻]
[100 adım git]
[90 derece dön ↻]
[100 adım git]
[90 derece dön ↻]
[100 adım git]
```

**Görev 2: Konuşan Karakterler (15 dk)**
İki sprite ekle, sırayla konuşsunlar

**Sprite 1:**
```
(Yeşil bayrak tıklandığında)
[Merhaba! söyle] (2 saniye)
```

**Sprite 2:**
```
(Yeşil bayrak tıklandığında)
[2 saniye bekle]
[Nasılsın? söyle] (2 saniye)
```

**Görev 3: Sıçrayan Top (20 dk)**
Top sprite'ı ekle, ekranda zıplasın

**Kod:**
```
(Yeşil bayrak tıklandığında)
[x: -200 y: 0 git]
[kenara dokunduğunda sek]
[sonsuza kadar]
  [10 adım git]
```

**Bonus:** Renk efekti ekle

### 4. KAPANIŞ (5 dk)

**Öğrenci Gösterimi:**
2-3 öğrenci projesini gösterir

**Kayıt:**
"Hafta27-Hareket" olarak kaydet

---

## 🏠 EV ÖDEVİ

**"Hikaye Anlatıcısı"**

**Görev:**
İki karakter arasında kısa diyalog oluştur

**Gereksinimler:**
1. En az 2 sprite
2. Arka plan seç
3. Karakterler sırayla konuşsun (en az 3 diyalog)
4. En az bir karakter hareket etsin
5. En az bir kostüm değişikliği

**Örnek Hikaye:**
- Kedi: "Merhaba köpek!"
- Köpek: "Selam kedi, oynayalım mı?" (hareket eder)
- Kedi: "Olur!" (kostüm değişir, mutlu olur)

---

## 📊 ÖZ DEĞERLENDİRME

**Kendimi Değerlendiriyorum:**

- ☐ Hareket bloklarını kullanabiliyorum
- ☐ Koordinat sistemini anlıyorum
- ☐ Sprite'ı istediğim yere gönderebiliyorum
- ☐ Görünüm bloklarıyla konuşturabiliyorum
- ☐ Kostüm değiştirebiliyorum
- ☐ Boyut ve efekt uygulayabiliyorum

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Koordinat Sistemi:**
- 5. sınıf için zorlayıcı olabilir
- Tahtada fiziksel gösterim yapın (şekil çizin)
- Basit örneklerle başlayın (merkez, köşeler)
- Negatif sayılar yeni olabilir (sol ve aşağı = eksi)

**Uygulama Sırası:**
- Her görev için zaman verin
- Bitiremeyen öğrenciler ev ödevinde devam edebilir
- Hızlı öğrenciler ekstra animasyon eklesin

**Sık Sorunlar:**
- "Sprite ekranımdan çıktı!" → x: 0 y: 0 git bloğu
- "Ters döndü!" → Dönme stili kontrol et (üstte ok işareti)

**İpucu:**
Koordinat anlaması için online "Coordinate Game" oynatabilirsiniz.

---

## 💡 MERAKLISINA

**Koordinat Sistemi Tarihi:**

📐 **René Descartes:** 1637'de koordinat sistemini keşfetti (Kartezyen koordinat)

🎮 **Oyunlarda:** Tüm oyunlar koordinat sistemi kullanır

🗺️ **Haritalar:** GPS koordinatları (enlem-boylam)

🚀 **Uzay:** Uydular koordinatlarla yönlendirilir

**Scratch'te:**
- Sahne: 480 x 360 piksel
- Piksel: Ekranın en küçük noktası

---

## 🧩 EĞLENCE

**Koordinat Bulmacası:**

Sprite şu sırayla gidiyor:
1. x: 0, y: 0
2. x: 100, y: 0
3. x: 100, y: 100
4. x: 0, y: 100
5. x: 0, y: 0

**Soru:** Hangi şekli çizdi?

**Cevap:** Kare

---

**Şaka:**

Sprite: "Öğretmenim, kayboldum!"
Öğretmen: "Koordinatların ne?"
Sprite: "x: 999, y: 999"
Öğretmen: "O zaman Mars'taymışsın!" 😄

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Bir milletin yükselme sırrı eğitimdedir."
> **- Mustafa Kemal Atatürk**

Atatürk, eğitimin önemini vurgulamıştır. Bugün Scratch ile koordinat, matematik ve mantık öğreniyorsunuz. Bu, eğitiminizin bir parçasıdır.

**Proje Fikri:** Türk bayrağını koordinatlarla çizebilirsin!

---

## 💎 DEĞERLER EĞİTİMİ

**Problem Çözme:**
Sprite istediğim yere gitmiyor → Koordinatları değiştir, dene, öğren.

**Matematiksel Düşünme:**
Koordinat sistemi matematiğin bir dalıdır.

**Sanat ve Yaratıcılık:**
Hareket ve görünüm birleşimi ile sanat eseri oluşturabilirsin.

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta çocuğunuz Scratch'te **hareket ve görünüm bloklarını** öğrendi. Karakterleri hareket ettirip konuşturdu.

**Öğrendikleri:**
- Hareket blokları (git, dön, kayma)
- Koordinat sistemi (x, y)
- Görünüm blokları (söyle, kostüm, efekt)

**Ev Ödevi:**
"Hikaye Anlatıcısı" - İki karakter arasında diyalog oluşturma projesi

**Evde Destek:**
- Çocuğunuzla hikaye konusunu konuşun
- Scratch projesini izleyin
- Koordinat sistemini günlük hayattan anlatın (adres sistemi gibi)

**Not:** Scratch öğrenirken aynı zamanda matematik (koordinat), yaratıcılık ve mantık geliştiriyor!

---

## 📎 EK KAYNAKLAR

**Scratch Kartları:**
- "Hareket Blokları" kartı
- "Koordinat Oyunu" kartı
- "Görünüm Efektleri" kartı

**Online Oyunlar:**
- Coordinate Plane Game
- Scratch Coordinate Tutorial

**Videolar:**
- "Scratch Hareket Blokları Türkçe"
- "Koordinat Sistemi Nedir?"

**Proje Örnekleri:**
- "Kare Çizme"
- "Zıplayan Top"
- "Diyalog Animasyonu"

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
