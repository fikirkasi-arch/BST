# HAFTA 34: KLONLAMA
**Sınıf:** 5
**Ünite:** 6 - Yazılım Tasarımı ve Programlama
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Klon Kavramı, Sprite Çoğaltma, Dinamik Objeler

---

## 🎯 ÖĞRENME KAZANIMLARI

- Klon kavramını anlar
- Sprite'ı klonlar
- Klonları yönetir
- Klonları siler
- Oyun elemanları yaratır

---

## 📚 KONU ÖZETİ

### Klon Nedir?

**Tanım:** Sprite'ın kopyası

**Günlük Hayat:**
- **Fotokopi:** Orijinal kağıdın aynısı
- **İkiz:** Aynı görünen iki kişi
- **Çiçek Tohumları:** Aynı çiçekten çok çiçek

**Programlamada:**
Bir sprite'tan çok sprite yaratmak

**Neden Kullanırız:**
- Çok obje yaratmak (yıldızlar, düşmanlar, mermiler...)
- Dinamik içerik (kullanıcı tıklayınca obje çıkar)
- Oyun elemanları

### Klonlama Blokları (Kontrol - Sarı)

**1. Kendini Klonla:**
`[kendini klonla]` → Yeni klon yaratır

**2. Klonu Sil:**
`[bu klonu sil]` → Klonu ortadan kaldırır

**3. Klon Olayı:**
```
(Klon olarak oluşturulduğunda)
  [... yapılacaklar]
```
→ Klon yaratıldığında çalışır

### Nasıl Çalışır?

**Orijinal Sprite:** Ana obje (sahnede görünür)

**Klonlar:** Kopyalar (orijinal gibi davranır)

**Örnek Akış:**
1. Yeşil bayrak → Orijinal sprite gizlenir
2. Sürekli klon yaratılır
3. Her klon kendi kodunu çalıştırır
4. İşi bitince klon silinir

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ (8 dk)

**Soru:**
"Oyunlarda düşman nasıl çoğalıyor?"

**Cevap:**
Klonlama! Bir düşman sprite'ından binlerce klon yaratılır.

**Demo:**
Öğretmen örnek klonlama gösterisi (tıklayınca yıldız çıkan proje)

### 2. KONU ANLATIMI (22 dk)

**Basit Klonlama:**

**Örnek 1: Tıklayınca Yıldız**
```
(Yeşil bayrak tıklandığında)
[sonsuza kadar]
  <EĞER [fare tıklandı mı?]>
    [kendini klonla]

(Klon olarak oluşturulduğunda)
[fare konumuna git]
[göster]
[2 saniye bekle]
[bu klonu sil]
```

**Örnek 2: Yağan Kar Taneleri**
```
(Yeşil bayrak tıklandığında)
[gizle]
[sonsuza kadar]
  [kendini klonla]
  [0.5 saniye bekle]

(Klon olarak oluşturulduğunda)
[x: <-240 ile 240 arası rastgele> y: 180 git]
[göster]
[sonsuza kadar]
  [y yönünde -5 değiştir]
  <EĞER <[y konumu] < [-180]>>
    [bu klonu sil]
```

**Örnek 3: Ateş Etme**
```
(boşluk tuşuna basıldığında)
[kendini klonla]

(Klon olarak oluşturulduğunda)
[sonsuza kadar]
  [10 adım git]
  <EĞER [kenara değdi mi?]>
    [bu klonu sil]
```

### 3. UYGULAMALI ÇALIŞMA (45 dk)

**Görev 1: Renkli Nokta İzi (15 dk)**

**Amaç:** Fareyi hareket ettir, arkasında renkli iz bıraksın

**Sprite:** Küçük top/nokta

```
(Yeşil bayrak tıklandığında)
[gizle]
[sonsuza kadar]
  [fare imlecine git]
  [kendini klonla]

(Klon olarak oluşturulduğunda)
[göster]
[renk efektini <1 ile 200 arası rastgele> yap]
[1 saniye bekle]
[bu klonu sil]
```

**Görev 2: Yağmur Animasyonu (15 dk)**

**Amaç:** Yukarıdan yağmur damlaları yağsın

**Sprite:** Yağmur damlası (veya mavi çizgi)

```
(Yeşil bayrak tıklandığında)
[gizle]
[sonsuza kadar]
  [kendini klonla]
  [0.1 saniye bekle]

(Klon olarak oluşturulduğunda)
[x: <-240 ile 240 arası rastgele> y: 180 git]
[göster]
[sonsuza kadar]
  [y yönünde <-5 ile -15 arası rastgele> değiştir]
  <EĞER <[y konumu] < [-180]>>
    [bu klonu sil]
    [durdur]
```

**Görev 3: Basit Atari Oyunu (15 dk)**

**2 Sprite:**
1. **Top (Raket - Oyuncu):** Ok tuşlarıyla hareket
2. **Düşman:** Yukarıdan düşen objeler

**Raket:**
```
(Yeşil bayrak tıklandığında)
[x: 0 y: -150 git]
[sonsuza kadar]
  <EĞER [sağ ok tuşuna basıldı mı?]>
    [x yönünde 15 değiştir]
  <EĞER [sol ok tuşuna basıldı mı?]>
    [x yönünde -15 değiştir]
```

**Düşman:**
```
(Yeşil bayrak tıklandığında)
[gizle]
[sonsuza kadar]
  [kendini klonla]
  [1 saniye bekle]

(Klon olarak oluşturulduğunda)
[x: <-200 ile 200 arası rastgele> y: 180 git]
[göster]
[sonsuza kadar]
  [y yönünde -10 değiştir]
  <EĞER [Raket'e değdi mi?]>
    [Pop sesi çal]
    [bu klonu sil]
  <EĞER <[y konumu] < [-180]>>
    [bu klonu sil]
```

### 4. KAPANIŞ (5 dk)

**Gösterim:**
Öğrenciler projelerini gösterir

**Kayıt:**
"Hafta34-Klonlama"

---

## 🏠 EV ÖDEVİ

**"Balon Patlatma Oyunu"**

**Görev:**
Balonlar yukarıya uçuyor, tıklayıp patlat!

**Adımlar:**
1. Balon sprite'ı
2. Sürekli klon yarat (aşağıdan yukarıya)
3. Eğer balona tıklanırsa → "Pop" sesi ve klonu sil
4. Eğer balonu ıskalarsan → Puan kaybedersin
5. Puan sistemi ekle

**Bonus:** Hız artsın, zorluk artsın

---

## 📊 ÖZ DEĞERLENDİRME

**Kendimi Değerlendiriyorum:**

- ☐ Klon kavramını anlıyorum
- ☐ Sprite'ı klonlayabiliyorum
- ☐ Klon olayını kullanabiliyorum
- ☐ Klonları silebiliyorum
- ☐ Klonlama ile oyun yapabiliyorum

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Klon Kavramı:**
- 5. sınıf için soyut
- "Fotokopi" benzetmesi iyi çalışır
- Görsel gösterim önemli (tıklayınca obje çıkması)

**Orijinal vs Klon:**
- Orijinal genelde gizlenir (`[gizle]`)
- Klonlar gösterilir (`[göster]`)
- Karışıklığı önlemek için bu yapı önemli

**Sonsuz Klon:**
- Klonları silmezseniz bilgisayar yavaşlar!
- "bu klonu sil" bloğu kritik
- Test ederken dikkat (çok klon = donma)

**Sık Sorunlar:**
- "Klonlar çalışmıyor!" → "Klon olarak oluşturulduğunda" bloğu var mı?
- "Klonlar ekranda kalıyor!" → Silme bloğu eksik
- "Bilgisayar dondu!" → Çok hızlı klon yaratıyor, "bekle" bloğu ekle

---

## 💡 MERAKLISINA

**Klonlama Hakkında:**

🧬 **Gerçek Klonlama:** Bilim insanları hayvanları klonlayabiliyor (Dolly the Sheep - 1996)

🎮 **Oyunlarda:** Bir savaş oyununda 1000+ düşman aynı anda olabilir (hepsi klon!)

💻 **Performans:** Çok klon = yavaşlık (bilgisayar hafızası dolar)

🚀 **Uzay Oyunları:** Yıldızlar, asteroidler hep klonlama ile yapılır

**Eğlenceli:**
Bazı Scratch projelerinde 10,000+ klon yaratılmış!

---

## 🧩 EĞLENCE

**Klon Bulmacası:**

```
Başlangıç: 1 sprite
3 kez kendini klonla
Her klon da 2 kez kendini klonla
```

**Soru:** Toplam kaç sprite olur?

**Cevap:**
- Başlangıç: 1
- +3 klon = 4
- Her klon 2 klonlar: 3x2 = 6
- Toplam: 1 + 3 + 6 = 10 sprite

---

**Şaka:**

Sprite: "Öğretmenim, kendimi klonladım ama kayboldu!"
Öğretmen: "Silme bloğunu koydun mu?"
Sprite: "Evet, kendime koydum!" (Orijinali silmiş!) 😄

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Yaratıcılıkta sınır yoktur."
> **- Mustafa Kemal Atatürk ruhundan esinle**

Atatürk, yaratıcılığı desteklemiştir. Klonlama, bir objeden sonsuz yaratıcılık yapmanızı sağlar. Bir sprite'tan harika bir oyun dünyası yaratabilirsiniz!

---

## 💎 DEĞERLER EĞİTİMİ

**Yaratıcılık:**
Bir sprite'tan sonsuz obje yaratmak yaratıcılıktır.

**Verimlilik:**
Klonlama, her obje için ayrı sprite yaratmaktan daha verimlidir.

**Problem Çözme:**
Çok obje gerektiğinde klonlama en iyi çözümdür.

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta çocuğunuz **klonlama** kavramını öğrendi. Sprite'ları çoğaltıp dinamik oyunlar yapabiliyor artık!

**Öğrendikleri:**
- Klon kavramı
- Sprite klonlama
- Klon yönetimi
- Klonlama ile oyun yapma

**Ev Ödevi:**
"Balon Patlatma Oyunu" - Balonları tıklayıp patlatma

**Not:**
Klonlama, ileri seviye bir konudur. Çocuğunuz Scratch'in en güçlü özelliklerinden birini öğrendi. Artık karmaşık oyunlar yapabilir!

**Oyun Örnekleri:**
- Space Invaders (düşmanlar klon)
- Flappy Bird (borular klon)
- Fruit Ninja (meyveler klon)

---

## 📎 EK KAYNAKLAR

**Scratch Projeler:**
- "Kar Yağışı"
- "Ateş Etme"
- "Yakalama Oyunu"
- "Balon Patlatma"

**Videolar:**
- "Scratch Klonlama Türkçe"
- "Clone Blocks Tutorial"

**İleri Seviye:**
- Klon değişkenleri (her klon farklı değer)
- Performans optimizasyonu
- Partikül efektleri

**Eğlenceli Projeler:**
- "Havai Fişek"
- "Yıldız Yağmuru"
- "Bubble Pop"
- "Space Shooter"

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
