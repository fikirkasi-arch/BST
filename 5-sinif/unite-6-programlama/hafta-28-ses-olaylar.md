# HAFTA 28: SES VE OLAY BLOKLARI
**Sınıf:** 5
**Ünite:** 6 - Yazılım Tasarımı ve Programlama
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Ses Blokları, Olay Blokları, Etkileşimli Programlar

---

## 🎯 ÖĞRENME KAZANIMLARI

- Ses bloklarını kullanır
- Ses ekler ve çalar
- Olay bloklarını kullanır
- Tuş ve tıklama olaylarına tepki verir
- Etkileşimli program yapar

---

## 📚 KONU ÖZETİ

### Ses Blokları (Pembe/Mor)

**1. Ses Çal:**
- `[pop sesi çal]` → Sesi çalar (kod devam eder)
- `[pop sesi çal ve bitir]` → Ses bitene kadar bekler

**2. Sesi Durdur:**
`[tüm sesleri durdur]` → Çalan sesleri durdur

**3. Ses Efektleri:**
- Ses seviyesi: `[sesi %100 yap]`
- Efekt: Perde, sol/sağ hoparlör

**4. Nota Çal:**
`[60 notasını 0.5 vuruş çal]` → Müzik yapma

**Ses Ekleme:**
1. "Sesler" sekmesi
2. "Ses Seç" → Kütüphaneden veya kaydet
3. Kategoriler: Hayvanlar, Müzik, Etkiler...

### Olay Blokları (Sarı)

**1. Yeşil Bayrak:**
`(Yeşil bayrak tıklandığında)` → Program başlar

**2. Tuş Basıldığında:**
`(boşluk tuşuna basıldığında)` → Klavye kontrolü

**3. Sprite Tıklandığında:**
`(Bu sprite tıklandığında)` → Mouse tıklama

**4. Sahne Değiştiğinde:**
`(Sahne arka plan1'e değiştiğinde)`

**5. Mesaj Gönder/Al:**
- `[mesaj1 gönder]` → Diğer sprite'lara sinyal
- `(mesaj1 alındığında)` → Sinyali yakala

**Neden Önemli:**
Kullanıcı etkileşimi! Tuşlara basıp, tıklayıp kontrol edebilirsin.

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ (5 dk)

**Geçen Hafta:**
Hareket ve görünüm bloklarını hatırlama

**Bugün:**
"Programlarımız sesli olacak ve tuşlarla kontrol edeceğiz!"

**Demo:**
Öğretmen örnek proje gösterir (tuşla hareket eden, ses çalan karakter)

### 2. KONU ANLATIMI (20 dk)

**Ses Blokları (Projeksiyon):**

**Örnek 1: Ses Çalma**
```
(Yeşil bayrak tıklandığında)
[Miyav sesi çal]
[Merhaba! söyle]
```

**Ses Ekleme Demosu:**
- Sesler sekmesi
- Ses seç → "Kedi" seslerini incele
- Yeni ses ekle → Hayvanlar kategorisi

**Olay Blokları:**

**Örnek 2: Tuş Kontrolü**
```
(boşluk tuşuna basıldığında)
[Zıpladım! söyle]
[y yönünde 50 değiştir]
```

**Örnek 3: Tıklama**
```
(Bu sprite tıklandığında)
[Miyav sesi çal]
[boyutu 10 değiştir]
```

**Mesaj Gönderme:**
```
Sprite 1:
(Yeşil bayrak tıklandığında)
[başla mesajını gönder]

Sprite 2:
(başla alındığında)
[Hazırım! söyle]
```

### 3. UYGULAMALI ÇALIŞMA (50 dk)

**Görev 1: Müzikli Kedi (15 dk)**

**Amaç:** Tuşlara basınca farklı sesler çalsın

```
(boşluk tuşuna basıldığında)
[Miyav sesi çal]

(sağ ok tuşuna basıldığında)
[Kahkaha sesi çal]

(sol ok tuşuna basıldığında)
[Boing sesi çal]
```

**Öğrenciler:**
- Kedi sprite'ı
- En az 3 farklı tuş
- Her tuşa farklı ses

**Görev 2: Ok Tuşlarıyla Hareket (20 dk)**

**Amaç:** Sprite'ı klavye ile kontrol et

```
(sağ ok tuşuna basıldığında)
[x yönünde 10 değiştir]

(sol ok tuşuna basıldığında)
[x yönünde -10 değiştir]

(yukarı ok tuşuna basıldığında)
[y yönünde 10 değiştir]

(aşağı ok tuşuna basıldığında)
[y yönünde -10 değiştir]
```

**Öğrenciler:**
- Araba/uçak sprite'ı seç
- 4 ok tuşu ile hareket
- Arka plan ekle (yol, gökyüzü...)

**Görev 3: Tıklama Oyunu (15 dk)**

**Amaç:** Sprite'a tıklayınca puan kazanma

```
(Yeşil bayrak tıklandığında)
[Puan değişkenini 0 yap]

(Bu sprite tıklandığında)
[Yakaladın! sesi çal]
[Puan değişkenini 1 arttır]
[rastgele konuma git]
```

**Not:** Değişken kavramı henüz detaylı işlenmedi, öğretmen gösterir, öğrenciler aynen kopyalar.

### 4. KAPANIŞ (5 dk)

**Gösterim:**
Gönüllü öğrenciler projelerini gösterir

**Kayıt:**
"Hafta28-SesOlay" olarak kaydet

---

## 🏠 EV ÖDEVİ

**"Müzik Enstrümanı"**

**Görev:**
Basit bir piyano/davul yaratıcısı yap

**Gereksinimler:**
1. En az 5 sprite (her biri bir nota/ses)
2. Her sprite'a tıklayınca farklı ses çalsın
3. Arka plan: Müzik temalı
4. Bonus: Tuşlarla da çalınsın (a, s, d, f, g...)

**Örnek:**
- Sprite 1 (Do notası): Tıklayınca "60 notasını çal"
- Sprite 2 (Re notası): Tıklayınca "62 notasını çal"
- ...

**Alternatif:** Davul seti (her sprite farklı davul sesi)

---

## 📊 ÖZ DEĞERLENDİRME

**Kendimi Değerlendiriyorum:**

- ☐ Ses ekleyip çalabiliyorum
- ☐ Ses bloklarını kullanabiliyorum
- ☐ Tuş olaylarını kullanabiliyorum
- ☐ Tıklama olaylarını kullanabiliyorum
- ☐ Mesaj gönderip alabiliyorum
- ☐ Etkileşimli program yapabiliyorum

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Ses Konusunda:**
- **Ses Yüksekliği:** Bilgisayar sesini kontrol edin
- **Çok Ses:** Öğrenciler sürekli ses çalabilir (gürültü!) → Kulaklık önerin
- **Ses Bulunamıyor:** Sesler sekmesini gösterin

**Olay Blokları:**
- Her olay bloğu BAĞIMSIZ bir kod başlatır
- Aynı tuşa birden fazla olay atanabilir (karışıklık olabilir)

**Görev 3 (Tıklama Oyunu):**
- Değişken henüz tam anlatılmadı
- Basit şekilde gösterin, ilerki hafta detaylandırılacak
- Amacı: Etkileşimli program fikri

**Zaman Yönetimi:**
- Görevler uzun sürebilir
- Bitiremeyen öğrenciler ev ödevinde devam edebilir

---

## 💡 MERAKLISINA

**Ses ve Müzik:**

🎵 **MIDI Notalar:** Scratch 60=Do, 62=Re, 64=Mi... (standart müzik sistemi)

🎹 **Piyano:** 88 tuş → 88 farklı nota

🔊 **Desibel:** Ses yüksekliği birimi. Scratch %0-%200 arası

🎼 **Ünlü Bestekarlar:** Mozart, Beethoven müzikleri Scratch'te kodlanabilir!

**Eğlenceli Proje:**
Scratch'te "Baby Shark" müziği yapılmış! 🦈

---

## 🧩 EĞLENCE

**Müzik Bulmacası:**

Hangi tuşlar bir akor oluşturur?
- Do (60)
- Mi (64)
- Sol (67)

**Cevap:** Do majör akor! 🎶

---

**Şaka:**

Programcı piyanist soruyor: "Bu hangi nota?"
Cevap: "MIDI 60"
Diğer piyanist: "O da ne, ben sadece 'Do' biliyorum!" 😄

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Sanatta, fikirde, ilimde, hâsılı, hayatın her safhasında muvaffak olmak için milli olduğu kadar da beynelmilel olmak lâzımdır."
> **- Mustafa Kemal Atatürk**

Atatürk, sanatta ve müzikte uluslararası olmayı desteklemiştir. Scratch ile hem müzik yaratabilir, hem de dünya çapında projelerinizi paylaşabilirsiniz.

**Proje Fikri:** İstiklal Marşı'nın bir kısmını Scratch ile kodlayabilirsin!

---

## 💎 DEĞERLER EĞİTİMİ

**Yaratıcılık:**
Müzik ve ses kullanarak sanat eseri yaratmak.

**Dikkat ve Konsantrasyon:**
Tuş olaylarını doğru kodlamak dikkat gerektirir.

**Sanat Sevgisi:**
Müzik ve programlamayı birleştirerek sanatı sevmek.

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta çocuğunuz Scratch'te **ses ve olay bloklarını** öğrendi. Programlarına ses ekledi ve tuş/tıklama ile kontrol etti.

**Öğrendikleri:**
- Ses ekleme ve çalma
- Tuş olayları (klavye kontrolü)
- Tıklama olayları (mouse etkileşimi)
- Mesaj gönderme

**Ev Ödevi:**
"Müzik Enstrümanı" - Tıklanabilir piyano/davul yapma

**Not:**
Çocuğunuz artık etkileşimli programlar yapabiliyor! Bu, oyun geliştirmenin temelidir.

**Evde:**
- Projesini dinleyin
- Birlikte basit bir melodi kodlayabilirsiniz
- Ses yüksekliğine dikkat (kulaklık önerilir)

---

## 📎 EK KAYNAKLAR

**Ses Kütüphaneleri:**
- Scratch yerleşik sesler
- Freesound.org (ücretsiz ses efektleri - öğretmen kontrolünde)

**Müzik Notaları:**
- MIDI nota listesi (60=Do, 62=Re...)
- "Twinkle Twinkle Little Star" Scratch kodu

**Videolar:**
- "Scratch Ses Blokları Türkçe"
- "Scratch ile Müzik Yapımı"

**Proje Örnekleri:**
- Basit Piyano
- Davul Seti
- Müzik Kutusu

**İleri Seviye:**
- Scratch Music Extensions (ek müzik blokları)

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
