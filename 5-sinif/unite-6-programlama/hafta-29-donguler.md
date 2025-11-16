# HAFTA 29: DÖNGÜLER
**Sınıf:** 5
**Ünite:** 6 - Yazılım Tasarımı ve Programlama
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Döngü Kavramı, Sonsuza Kadar, N Kez Tekrarla

---

## 🎯 ÖĞRENME KAZANIMLARI

- Döngü kavramını anlar
- "Sonsuza kadar" döngüsünü kullanır
- "N kez tekrarla" döngüsünü kullanır
- Döngü ile animasyon yapar
- Kodu daha kısa ve etkili yazar

---

## 📚 KONU ÖZETİ

### Döngü Nedir?

**Tanım:** Bir işi tekrar tekrar yapma

**Günlük Hayat Örnekleri:**
- Su kaynayana kadar beklemek
- 10 kere mekik çekmek
- Her gün okula gitmek

**Neden Kullanırız:**
- Kod kısalır
- Zaman tasarrufu
- Hata azalır

### Döngüsüz vs Döngülü Kod

**Döngüsüz (Kötü):**
```
[10 adım git]
[10 adım git]
[10 adım git]
[10 adım git]
[10 adım git]
```

**Döngülü (İyi):**
```
[5 kez tekrarla]
  [10 adım git]
```

### Döngü Türleri (Scratch)

**1. Sonsuza Kadar:**
```
[sonsuza kadar]
  [10 adım git]
  [kenara dokunduğunda sek]
```
→ Hiç durmazlar, yeşil bayrağı tekrar tıkla

**2. N Kez Tekrarla:**
```
[10 kez tekrarla]
  [10 adım git]
  [90 derece dön]
```
→ 10 kez yapar, durur

**3. Koşullu Döngü (İleri haftalarda):**
`[... olana kadar tekrarla]`

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ (10 dk)

**Günlük Döngüler:**
"Sabah 10 kere mekik çek" nasıl yazılır?

**Döngüsüz:**
1. Mekik çek
2. Mekik çek
3. Mekik çek
... (10 satır!)

**Döngülü:**
10 kez tekrarla: Mekik çek

**Soru:**
"Hangisi daha kolay?"

### 2. KONU ANLATIMI (20 dk)

**Döngü Bloğu Tanıtımı (Turuncu):**

**Örnek 1: Kare Çizme (Döngüsüz)**
Geçen hafta 16 blok kullanmıştık!

**Örnek 2: Kare Çizme (Döngülü)**
```
(Yeşil bayrak tıklandığında)
[4 kez tekrarla]
  [100 adım git]
  [90 derece dön]
```
Sadece 3 blok! 🎉

**Örnek 3: Sonsuza Kadar**
```
(Yeşil bayrak tıklandığında)
[sonsuza kadar]
  [10 adım git]
  [kenara dokunduğunda sek]
```
→ Top sürekli hareket eder

**İç İçe Döngü (Bonus):**
```
[4 kez tekrarla]
  [2 kez tekrarla]
    [50 adım git]
  [90 derece dön]
```

### 3. UYGULAMALI ÇALIŞMA (45 dk)

**Görev 1: Geometrik Şekiller (20 dk)**

**a) Kare (4 kenar):**
```
(Yeşil bayrak tıklandığında)
[4 kez tekrarla]
  [100 adım git]
  [90 derece dön]
```

**b) Üçgen (3 kenar):**
```
[3 kez tekrarla]
  [100 adım git]
  [120 derece dön]
```

**c) Altıgen (6 kenar):**
```
[6 kez tekrarla]
  [80 adım git]
  [60 derece dön]
```

**Öğrenciler:** Her şekli ayrı sprite veya aynı sprite farklı renklerde çizer

**Görev 2: Dans Eden Sprite (15 dk)**

**Amaç:** Sprite sürekli dans etsin

```
(Yeşil bayrak tıklandığında)
[sonsuza kadar]
  [kostüm2 seç]
  [0.3 saniye bekle]
  [kostüm3 seç]
  [0.3 saniye bekle]
```

**Öğrenciler:**
- İnsan/hayvan sprite seç (birden fazla kostümü olan)
- Kostümleri değiştirerek animasyon yap
- Bonus: Müzik ekle

**Görev 3: Renkli Spiral (10 dk)**

```
(Yeşil bayrak tıklandığında)
[kalemi sil]
[kalemi indir]
[100 kez tekrarla]
  [5 adım git]
  [10 derece dön]
  [kalem rengini 5 değiştir]
```

**Not:** "Kalem" eklentisini öğretmen ekler (Eklentiler → Kalem)

### 4. KAPANIŞ (5 dk)

**Gösterim:**
Öğrenciler şekillerini/danslarını gösterir

**Soru:**
"Döngü kullanınca ne avantaj sağladık?"

**Kayıt:**
"Hafta29-Donguler"

---

## 🏠 EV ÖDEVİ

**"Yıldız Çizici"**

**Görev:**
Döngü kullanarak 5 köşeli yıldız çiz

**İpucu:**
- Her köşe için 144 derece dön
- 5 kez tekrarla
- Adım sayısı: 100

**Kod Taslağı:**
```
(Yeşil bayrak tıklandığında)
[kalemi indir]
[5 kez tekrarla]
  [100 adım git]
  [144 derece dön]
```

**Bonus:** Renkli yap (kalem rengi değiştir)

---

## 📊 ÖZ DEĞERLENDİRME

**Kendimi Değerlendiriyorum:**

- ☐ Döngü kavramını anlıyorum
- ☐ "N kez tekrarla" bloğunu kullanabiliyorum
- ☐ "Sonsuza kadar" bloğunu kullanabiliyorum
- ☐ Döngü ile kod kısaltabiliyorum
- ☐ Geometrik şekiller çizebiliyorum

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Döngü Mantığı:**
- 5. sınıf için soyut olabilir
- Fiziksel örneklerle başlayın (mekik, zıplama...)
- "İçindeki kodlar tekrarlanır" vurgusunu yapın

**Kalem Eklentisi:**
- Eklentiler butonu → Kalem ekle
- Kalemi indir/kaldır/sil bloklarını gösterin
- Renkli çizim için: "kalem rengini değiştir"

**Sık Sorunlar:**
- "Şeklim yarım kaldı!" → Açı yanlış
- "Sprite ekrandan çıktı!" → Başlangıçta x:0 y:0'a git ekle
- "Kalemi göremiyorum!" → Sahneye bakıyor mu? "kalemi indir" yazdı mı?

**Geometri Bilgisi:**
- Kare: 90 derece (4x90=360)
- Üçgen: 120 derece (3x120=360)
- Altıgen: 60 derece (6x60=360)
- Genel kural: 360 / kenar sayısı

---

## 💡 MERAKLISINA

**Döngüler Hakkında:**

🔁 **Sonsuz Döngü Felaketi:** 1990'larda bir programcı sonsuz döngü hatası yaptı, tüm şirketin interneti çöktü!

🎮 **Oyunlarda:** Tüm oyunlar "game loop" (oyun döngüsü) kullanır - sonsuza kadar tekrarla

🌀 **Fibonacci:** Ünlü matematik dizisi döngü ile hesaplanır

⏰ **Saat:** Saat kolları sonsuz döngüdedir!

**Rekor:**
Dünyanın en uzun Scratch döngüsü: 999,999,999 kez tekrarla! (bitene kadar yıllar sürer)

---

## 🧩 EĞLENCE

**Döngü Bulmacası:**

Bu kod kaç adım gider?

```
[10 kez tekrarla]
  [5 adım git]
```

**Cevap:** 50 adım (10 x 5)

---

**Şaka:**

Öğretmen: "Döngüyü ne zaman durdurmalıyız?"
Öğrenci: "Döngüyü ne zaman durdurmalıyız?"
Öğretmen: "Döngüyü ne zaman durdurmalıyız?"
... (Sonsuz döngü!) 😄

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Hayat demek, mücadele etmek demektir."
> **- Mustafa Kemal Atatürk**

Atatürk, hayatın sürekli mücadele olduğunu söylemiştir. Programlamada da döngüler, bir işi defalarca deneyip başarmaktır. İlk seferde olmayabilir, döngü gibi tekrar deneriz!

**Proje Fikri:** Türk bayrağının yıldızını döngü ile çizebilirsin!

---

## 💎 DEĞERLER EĞİTİMİ

**Sebat ve Azim:**
Döngü, bir işi tekrar tekrar denemektir. Başarısız olsan da tekrar dene!

**Verimlilik:**
Döngü kullanarak kodu kısaltmak, verimli çalışmaktır.

**Matematiksel Düşünme:**
Geometrik şekiller çizerken matematik ve programlama birleşir.

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta çocuğunuz **döngü** kavramını öğrendi. Kodları daha kısa ve etkili yazmayı başardı.

**Öğrendikleri:**
- Döngü kavramı
- "N kez tekrarla" bloğu
- "Sonsuza kadar" bloğu
- Geometrik şekiller çizme

**Ev Ödevi:**
Döngü ile yıldız çizme

**Günlük Hayat:**
Çocuğunuzla döngü örnekleri konuşabilirsiniz:
- "Her gün diş fırçalamak" (sonsuza kadar döngü)
- "10 kere zıplamak" (10 kez tekrarla döngü)

**Not:** Döngü, programlamanın en önemli kavramlarından biridir. Çocuğunuz temel bir beceri kazandı!

---

## 📎 EK KAYNAKLAR

**Scratch Projeler:**
- "Geometrik Şekiller"
- "Spiral Çizici"
- "Dönen Yıldız"

**Videolar:**
- "Scratch Döngüler Türkçe"
- "Loop Nedir?"

**Oyunlar:**
- Code.org - Loop (Döngü) dersleri
- Lightbot - Döngü bölümü

**Geometri Açıları:**
- Kare: 90°
- Üçgen: 120°
- Beşgen: 72°
- Altıgen: 60°
- Genel: 360° / kenar sayısı

**İleri Seviye:**
- İç içe döngüler
- Fraktal desenler

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
