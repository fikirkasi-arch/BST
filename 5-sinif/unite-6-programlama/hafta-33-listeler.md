# HAFTA 33: LİSTELER
**Sınıf:** 5
**Ünite:** 6 - Yazılım Tasarımı ve Programlama
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Liste Kavramı, Eleman Ekleme/Silme, Liste İşlemleri

---

## 🎯 ÖĞRENME KAZANIMLARI

- Liste kavramını anlar
- Liste oluşturur
- Listeye eleman ekler ve siler
- Liste uzunluğunu bulur
- Liste ile rastgele seçim yapar

---

## 📚 KONU ÖZETİ

### Liste Nedir?

**Tanım:** Birden fazla değeri saklayan değişken

**Günlük Hayat:**
- **Alışveriş Listesi:** Ekmek, süt, peynir...
- **Sınıf Listesi:** Ahmet, Ayşe, Mehmet...
- **Sayı Listesi:** 10, 20, 30, 40...

**Değişken vs Liste:**
- **Değişken:** Tek değer (Puan = 100)
- **Liste:** Çok değer (Puanlar = [100, 85, 92, 78])

### Liste İşlemleri (Scratch)

**1. Liste Oluşturma:**
Değişkenler → "Liste oluştur" → İsim ver

**2. Eleman Ekleme:**
`[Elma liste ekle]` → Listenin sonuna ekler

**3. Eleman Silme:**
`[Listenin 1. elemanını sil]` → Belirli elemanı siler
`[Listenin tüm elemanlarını sil]` → Tümünü temizler

**4. Eleman Değiştirme:**
`[Listenin 1. elemanını Portakal yap]` → Değiştirir

**5. Eleman Alma:**
`< Listenin [1]. elemanı >` → Elemana erişir

**6. Liste Uzunluğu:**
`< Listenin uzunluğu >` → Kaç eleman var

**7. Liste İçeriyor mu:**
`< Liste [Elma] içeriyor mu? >` → Var mı kontrol

### Rastgele Seçim

```
< Listenin <1 ile <Listenin uzunluğu> arası rastgele>. elemanı >
```
→ Listeden rastgele eleman seçer

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ (8 dk)

**Alışveriş Listesi:**
"Markete gidiyorsunuz, ne alacaksınız?"
- Ekmek
- Süt
- Peynir
- Zeytin
- ...

**Soru:**
"Bunları nasıl hatırlarsınız?"

**Cevap:**
Liste yazarsınız! Programlamada da aynı!

### 2. KONU ANLATIMI (22 dk)

**Liste Oluşturma (Projeksiyon):**

1. "Değişkenler" kategorisi
2. "Liste oluştur" butonu
3. İsim: "Meyveler"
4. Tamam

**Liste Blokları:**

**Örnek 1: Liste Doldurma**
```
(Yeşil bayrak tıklandığında)
[Meyveler listesinin tüm elemanlarını sil]
[Elma Meyveler listesine ekle]
[Muz Meyveler listesine ekle]
[Portakal Meyveler listesine ekle]
```

**Örnek 2: Listeyi Gösterme**
```
(Yeşil bayrak tıklandığında)
[Meyveler göster]
```
→ Sahnede liste kutucuğu görünür

**Örnek 3: Rastgele Meyve**
```
(boşluk tuşuna basıldığında)
[Rastgele Meyve değişkenini
  <Meyveler listesinin <1 ile <Meyveler listesinin uzunluğu> arası rastgele>. elemanı>
yap]
[[Bugünün meyvesi: ] ve [Rastgele Meyve] birleştir söyle]
```

**Örnek 4: Tüm Listeyi Okuma**
```
(Yeşil bayrak tıklandığında)
[Sayaç değişkenini 1 yap]
[<Meyveler listesinin uzunluğu> kez tekrarla]
  [<Meyveler listesinin [Sayaç]. elemanı> söyle] (1 saniye)
  [Sayaç değişkenini 1 arttır]
```

### 3. UYGULAMALI ÇALIŞMA (45 dk)

**Görev 1: İsim Listesi (15 dk)**

**Amaç:** Sınıf arkadaşlarının isimlerini listeye ekle

```
(Yeşil bayrak tıklandığında)
[İsimler listesinin tüm elemanlarını sil]
[5 kez tekrarla]
  [Cevap değişkenini [Bir isim gir:] sor ve bekle]
  [Cevap İsimler listesine ekle]
[İsimler göster]
```

**Bonus:** Kaç isim girildi göster (liste uzunluğu)

**Görev 2: Rastgele Seçici (15 dk)**

**Amaç:** Listeden rastgele eleman seç (örn: Sınıfta kim tahtaya çıkacak?)

```
(Yeşil bayrak tıklandığında)
[İsimler listesinin tüm elemanlarını sil]
[Ahmet İsimler listesine ekle]
[Ayşe İsimler listesine ekle]
[Mehmet İsimler listesine ekle]
[Zeynep İsimler listesine ekle]
[Fatma İsimler listesine ekle]

(boşluk tuşuna basıldığında)
[Seçilen değişkenini
  <İsimler listesinin <1 ile <İsimler listesinin uzunluğu> arası rastgele>. elemanı>
yap]
[[Tahtaya çıkan: ] ve [Seçilen] birleştir söyle] (3 saniye)
```

**Görev 3: Quiz Oyunu (15 dk)**

**Amaç:** Sorular listesi, rastgele soru sor

```
(Yeşil bayrak tıklandığında)
[Sorular listesinin tüm elemanlarını sil]
[2+2 kaç? Sorular listesine ekle]
[5*3 kaç? Sorular listesine ekle]
[10-4 kaç? Sorular listesine ekle]

[Cevaplar listesinin tüm elemanlarını sil]
[4 Cevaplar listesine ekle]
[15 Cevaplar listesine ekle]
[6 Cevaplar listesine ekle]

[Soru No değişkenini <1 ile <Sorular listesinin uzunluğu> arası rastgele> yap]

[Kullanıcı Cevabı değişkenini
  <Sorular listesinin [Soru No]. elemanı> sor ve bekle]

<EĞER <[Kullanıcı Cevabı] = <Cevaplar listesinin [Soru No]. elemanı>>>
  [Doğru! söyle]
<DEĞİLSE>
  [Yanlış! söyle]
```

### 4. KAPANIŞ (5 dk)

**Gösterim:**
Öğrenciler rastgele seçici/quiz oyununu gösterir

**Kayıt:**
"Hafta33-Listeler"

---

## 🏠 EV ÖDEVİ

**"Kelime Bulmaca"**

**Görev:**
Kelime listesi oluştur, kullanıcı harf harf tahmin etsin (Basit Adam Asmaca)

**Adımlar:**
1. "Kelimeler" listesi oluştur (Kedi, Köpek, Kuş...)
2. Rastgele kelime seç
3. Kullanıcıdan harf iste
4. Eğer kelimede varsa → "Var!"
5. Yoksa → "Yok!"

**Not:** Tam adam asmaca zor, basitleştirilmiş versiyon yeterli

---

## 📊 ÖZ DEĞERLENDİRME

**Kendimi Değerlendiriyorum:**

- ☐ Liste kavramını anlıyorum
- ☐ Liste oluşturabiliyorum
- ☐ Listeye eleman ekleyebiliyorum
- ☐ Listeden eleman silebiliyorum
- ☐ Rastgele eleman seçebiliyorum
- ☐ Liste ile program yazabiliyorum

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Liste Kavramı:**
- 5. sınıf için biraz soyut
- Alışveriş listesi, sınıf listesi gibi somut örnekler verin
- Liste = Değişkenler dizisi (ama bu terimi kullanmayın, karışır)

**Index (Sıra Numarası):**
- Liste 1'den başlar (0'dan değil, bu Python/Java'dan farklı!)
- "1. eleman" = İlk eleman

**Sık Sorunlar:**
- "Liste görünmüyor!" → Liste "göster" bloğu
- "Eleman eklemiyor!" → "listesinin tüm elemanlarını sil" blok koyduysa, her seferinde siliyor
- "Rastgele seçim çalışmıyor!" → Index rastgele olmalı, eleman değil

**Döngü İle Liste:**
- Tüm listeyi okumak için döngü + sayaç gerekli
- Biraz karmaşık, adım adım gösterin

---

## 💡 MERAKLISINA

**Listeler Hakkında:**

📊 **Array (Dizi):** Programlamada listelere "array" denir (İngilizce)

💾 **Veri Yapısı:** Liste, en temel veri yapılarından biri

🎮 **Oyunlarda:** Envanter (eşya listesi), düşman listesi, skor tablosu... hep liste!

📱 **Telefonunuz:** Rehber = İsim listesi, Galeri = Fotoğraf listesi

**Rekor:**
Bazı programlarda milyonlarca elemanlı listeler var!

---

## 🧩 EĞLENCE

**Liste Bulmacası:**

```
Meyveler = [Elma, Muz, Portakal]
Meyveler listesine "Çilek" ekle
Meyveler listesinin 2. elemanını sil
```

**Soru:** Liste nasıl olur?

**Cevap:** [Elma, Portakal, Çilek]

---

**Şaka:**

Programcı markete gidiyor.
Eşi: "Ekmek al, varsa 6 tane al!"
Programcı: *Alışveriş listesine "Ekmek x6" ekliyor*
😄

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Hayat bilmek ve bilmemek mücadelesidir."
> **- Mustafa Kemal Atatürk**

Atatürk, bilginin önemini vurgulamıştır. Listeler, bilgileri düzenli saklamanın ve kullanmanın bir yoludur. Bilgiyi organize ederek daha güçlü oluruz.

**Proje Fikri:** Türkiye'nin şehirleri listesi, rastgele şehir seçici!

---

## 💎 DEĞERLER EĞİTİMİ

**Düzen:**
Listeler bilgiyi düzenli tutar.

**Hafıza:**
Liste kullanarak çok bilgiyi hatırlayabiliriz.

**Organizasyon:**
Karmaşık bilgileri listeleyerek basitleştiririz.

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta çocuğunuz **listeler** kavramını öğrendi. Birden fazla bilgiyi saklayıp yönetebiliyor artık!

**Öğrendikleri:**
- Liste kavramı
- Eleman ekleme/silme
- Rastgele seçim
- Liste ile program yazma

**Ev Ödevi:**
"Kelime Bulmaca" - Basit adam asmaca tarzı oyun

**Günlük Hayat:**
Listeler her yerde:
- Alışveriş listesi
- Yapılacaklar listesi
- Telefon rehberi

Çocuğunuzla günlük liste örnekleri konuşabilirsiniz!

---

## 📎 EK KAYNAKLAR

**Scratch Projeler:**
- "Rastgele İsim Seçici"
- "Quiz Oyunu"
- "Alışveriş Listesi"
- "Basit Adam Asmaca"

**Videolar:**
- "Scratch Listeler Türkçe"
- "Array Nedir?"

**İleri Seviye:**
- 2D liste (liste içinde liste)
- Sıralama algoritmaları
- Arama algoritmaları

**Eğlenceli Projeler:**
- "Rastgele Şakalar"
- "Günün Sözü"
- "Kelime Eşleştirme"

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
