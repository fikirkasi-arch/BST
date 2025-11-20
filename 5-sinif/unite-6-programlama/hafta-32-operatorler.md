# HAFTA 32: OPERATÖRLER VE MATEMATİK
**Sınıf:** 5
**Ünite:** 6 - Yazılım Tasarımı ve Programlama
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Matematik Operatörleri, Karşılaştırma, Rastgele Sayı, Birleştirme

---

## 🎯 ÖĞRENME KAZANIMLARI

- Matematik operatörlerini kullanır (+, -, *, /)
- Rastgele sayı üretir
- Metin birleştirir
- Karakter uzunluğunu bulur
- Matematiksel işlemler yapar

---

## 📚 KONU ÖZETİ

### Matematik Operatörleri (Yeşil)

**1. Toplama (+):**
`< [5] + [3] >` → 8

**2. Çıkarma (-):**
`< [10] - [4] >` → 6

**3. Çarpma (*):**
`< [7] * [6] >` → 42

**4. Bölme (/):**
`< [20] / [4] >` → 5

**Değişkenle:**
```
[Puan değişkenini <[Puan] + [10]> yap]
```
→ Puan 10 artar

### Rastgele Sayı

**Kullanım:**
`< [1] ile [10] arası rastgele >`

**Ne İşe Yarar:**
- Zar atmak (1-6)
- Rastgele renk
- Rastgele konum
- Oyunlarda şans

**Örnek:**
```
[Zar değişkenini <1 ile 6 arası rastgele> yap]
```

### Metin İşlemleri

**1. Birleştirme:**
`< [Merhaba ] ve [Dünya] birleştir >` → "Merhaba Dünya"

**2. Harf Alma:**
`< [Merhaba]'nın [1]. harfi >` → "M"

**3. Uzunluk:**
`< [Merhaba]'nın uzunluğu >` → 7

**Örnek:**
```
[İsim değişkenini [Adın?] sor ve bekle]
[[Merhaba ] ve [İsim] ve [!] birleştir söyle]
```

### Mantıksal Operatörler (Tekrar)

**VE:**
`< [koşul1] ve [koşul2] >`

**VEYA:**
`< [koşul1] veya [koşul2] >`

**DEĞİL:**
`< [koşul] değil >`

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ (8 dk)

**Günlük Matematik:**
- Alışveriş: 15 TL + 25 TL = ?
- Kalan para: 100 TL - 40 TL = ?

**Bilgisayar:**
"Bilgisayar da aynı matematiği yapar!"

### 2. KONU ANLATIMI (22 dk)

**Matematik Operatörleri:**

**Örnek 1: Basit Toplama**
```
(Yeşil bayrak tıklandığında)
[Sonuç değişkenini <5 + 3> yap]
[Sonuç söyle]
```

**Örnek 2: Değişkenle İşlem**
```
(Yeşil bayrak tıklandığında)
[Sayı1 değişkenini [Birinci sayı?] sor ve bekle]
[Sayı2 değişkenini [İkinci sayı?] sor ve bekle]
[Sonuç değişkenini <[Sayı1] + [Sayı2]> yap]
[[Toplam: ] ve [Sonuç] birleştir söyle]
```

**Rastgele Sayı:**

**Örnek 3: Zar Atma**
```
(boşluk tuşuna basıldığında)
[Zar değişkenini <1 ile 6 arası rastgele> yap]
[[Zar: ] ve [Zar] birleştir söyle]
```

**Örnek 4: Rastgele Hareket**
```
(Yeşil bayrak tıklandığında)
[sonsuza kadar]
  [x: <-240 ile 240 arası rastgele> y: <-180 ile 180 arası rastgele> git]
  [1 saniye bekle]
```

**Metin İşlemleri:**

**Örnek 5: İsim Birleştirme**
```
[Ad değişkenini [Adın?] sor ve bekle]
[Soyad değişkenini [Soyadın?] sor ve bekle]
[Tam İsim değişkenini <[Ad] ve [ ] ve [Soyad] birleştir> yap]
[[Merhaba ] ve [Tam İsim] birleştir söyle]
```

### 3. UYGULAMALI ÇALIŞMA (45 dk)

**Görev 1: Hesap Makinesi (15 dk)**

**Amaç:** 4 işlem yapan hesap makinesi

```
(Yeşil bayrak tıklandığında)
[Sayı1 değişkenini [Birinci sayı?] sor ve bekle]
[Sayı2 değişkenini [İkinci sayı?] sor ve bekle]
[İşlem değişkenini [Hangi işlem? (+, -, *, /)] sor ve bekle]

<EĞER <[İşlem] = [+]>>
  [Sonuç değişkenini <[Sayı1] + [Sayı2]> yap]
<EĞER <[İşlem] = [-]>>
  [Sonuç değişkenini <[Sayı1] - [Sayı2]> yap]
... (çarpma, bölme)

[[Sonuç: ] ve [Sonuç] birleştir söyle]
```

**Görev 2: Zar Oyunu (15 dk)**

**Amaç:** İki zar at, toplamları bul

```
(boşluk tuşuna basıldığında)
[Zar1 değişkenini <1 ile 6 arası rastgele> yap]
[Zar2 değişkenini <1 ile 6 arası rastgele> yap]
[Toplam değişkenini <[Zar1] + [Zar2]> yap]
[[Zar 1: ] ve [Zar1] ve [ | Zar 2: ] ve [Zar2] ve [ | Toplam: ] ve [Toplam] birleştir söyle]
```

**Bonus:** Eğer toplam 7 ise "KAZANDIN!" de

**Görev 3: İsim Analiz Edici (15 dk)**

**Amaç:** İsmin kaç harfli olduğunu bul

```
(Yeşil bayrak tıklandığında)
[İsim değişkenini [Adın ne?] sor ve bekle]
[Uzunluk değişkenini <[İsim]'nın uzunluğu> yap]
[[Senin adın ] ve [Uzunluk] ve [ harflidir!] birleştir söyle] (3 saniye)
[[İlk harfin: ] ve <[İsim]'nın [1]. harfi> birleştir söyle] (3 saniye)
```

**Bonus:** Son harfi de bul

### 4. KAPANIŞ (5 dk)

**Gösterim:**
Öğrenciler hesap makinesi/zar oyununu gösterir

**Kayıt:**
"Hafta32-Operatorler"

---

## 🏠 EV ÖDEVİ

**"Matematiksel Tahmin Oyunu"**

**Görev:**
Bilgisayar rastgele iki sayı seçer, kullanıcı toplamı tahmin eder

**Adımlar:**
1. Sayı1, Sayı2 (rastgele 1-10)
2. Toplam = Sayı1 + Sayı2
3. Kullanıcıdan tahmin iste
4. Eğer doğru → "Bildin! Toplam: X"
5. Değilse → "Yanlış! Toplam: X"

**Bonus:** Çarpma versiyonu yap

---

## 📊 ÖZ DEĞERLENDİRME

**Kendimi Değerlendiriyorum:**

- ☐ Matematik operatörlerini kullanabiliyorum
- ☐ Rastgele sayı üretebiliyorum
- ☐ Metin birleştirebiliyorum
- ☐ Karakter uzunluğunu bulabiliyorum
- ☐ Matematiksel program yazabiliyorum

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Matematik Seviyesi:**
- 5. sınıf matematik bilgisi yeterli
- Bölme biraz zor olabilir (ondalık sayılar)
- Basit örneklerle başlayın

**Operatör Sembolü:**
- Scratch: + - * /
- Çarpma: * (yıldız) NOT: x değil!
- Bölme: / (slash)

**Rastgele Sayı:**
- Tam sayı üretir (10.5 gibi ondalık olmaz)
- Her seferinde farklı sonuç (tahmin edilemez)

**Metin İşlemleri:**
- Boşluk önemli! "Merhaba" + "Dünya" = "MerhabaDünya" (yanlış!)
- Doğru: "Merhaba " + "Dünya" (boşluklu)

**Sık Hatalar:**
- Bölme sıfırla → Hata! (kullanıcıdan sıfır gelebilir, kontrol edin)
- Metin + Sayı → Scratch yapabilir ama mantıksal hata ("Puan" + 5 = "Puan5")

---

## 💡 MERAKLISINA

**Matematik ve Programlama:**

🧮 **Bilgisayar:** Aslında dev bir hesap makinesi!

🎲 **Rastgele:** Bilgisayar gerçek rastgele sayı üretemez (algoritma kullanır = "pseudo-random")

🔢 **Büyük Sayılar:** Bilgisayarlar saniyede milyarlarca işlem yapar!

💻 **Hesap Hatası:** 1994'te Intel işlemci bölme hatası yaptı, milyonlarca dolar zarar!

**Eğlenceli:**
Dünyad en hızlı bilgisayar saniyede 1,000,000,000,000,000,000 işlem yapıyor!

---

## 🧩 EĞLENCE

**Operatör Bulmacası:**

```
< <5 + 3> * <10 - 8> >
```

**Soru:** Sonuç kaç?

**Adımlar:**
1. 5 + 3 = 8
2. 10 - 8 = 2
3. 8 * 2 = 16

**Cevap:** 16

---

**Şaka:**

Öğretmen: "2 + 2 kaç?"
Programcı öğrenci: "İstediğinize göre değişir!"
Öğretmen: "Nasıl yani?"
Öğrenci: "Binary'de 100, decimal'de 4!" 😄

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Matematiksiz hiçbir şey yapılamaz."
> **- Mustafa Kemal Atatürk**

Atatürk, matematiğin her alanda kullanıldığını vurgulamıştır. Programlamada da matematik temeldir. Bugün öğrendiğiniz operatörler, bilgisayar biliminin matematik yönünü gösteriyor.

---

## 💎 DEĞERLER EĞİTİMİ

**Matematiksel Düşünme:**
Operatörler matematiği programlamaya taşır.

**Hassasiyet:**
Matematik işlemlerde dikkatli olmak gerekir (+ yerine - yazmak sonucu değiştirir!)

**Yaratıcılık:**
Basit operatörlerle karmaşık programlar yapabilirsin.

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta çocuğunuz **operatörler** konusunu öğrendi. Matematiği programlamaya entegre etti!

**Öğrendikleri:**
- Matematik operatörleri (+, -, *, /)
- Rastgele sayı üretme
- Metin birleştirme
- Karakter uzunluğu bulma

**Ev Ödevi:**
"Matematiksel Tahmin Oyunu" - Rastgele sayıları toplatma oyunu

**Matematik Bağlantısı:**
Çocuğunuz programlama yaparken aynı zamanda matematik pratiği yapıyor:
- Toplama, çıkarma, çarpma, bölme
- Rastgele sayı kavramı
- Problem çözme

**Not:** Programlama ve matematik el ele gider. Çocuğunuzun matematiği sevmesi için güzel bir fırsat!

---

## 📎 EK KAYNAKLAR

**Scratch Projeler:**
- "Hesap Makinesi"
- "Zar Oyunu"
- "Matematik Quiz"
- "Rastgele Sayı Tahmin"

**Videolar:**
- "Scratch Operatörler Türkçe"
- "Rastgele Sayı Nasıl Çalışır?"

**Matematik Oyunları:**
- "Math Quiz Scratch"
- "Zar Toplama Yarışması"

**İleri Seviye:**
- Mod (kalan) operatörü
- Üs alma (power)
- Yuvarlama (round, floor, ceil)

**Eğlenceli Projeler:**
- "Rastgele Şifre Üreteci"
- "Matematik Yarışması"

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
