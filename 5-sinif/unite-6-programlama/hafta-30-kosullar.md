# HAFTA 30: KOŞULLAR (IF-ELSE)
**Sınıf:** 5
**Ünite:** 6 - Yazılım Tasarımı ve Programlama
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Koşul Kavramı, Eğer-O Halde, Eğer-Değilse, Karşılaştırma

---

## 🎯 ÖĞRENME KAZANIMLARI

- Koşul kavramını anlar
- "Eğer-o halde" bloğunu kullanır
- "Eğer-değilse" bloğunu kullanır
- Karşılaştırma operatörlerini kullanır
- Karar veren programlar yazar

---

## 📚 KONU ÖZETİ

### Koşul Nedir?

**Tanım:** Duruma göre karar verme

**Günlük Hayat:**
- **EĞER** yağmur yağıyorsa **O HALDE** şemsiye al
- **EĞER** acsın **O HALDE** ye, **DEĞİLSE** bekleme
- **EĞER** test 50'den fazla **O HALDE** geçtin, **DEĞİLSE** kaldın

**Programlamada:**
Bilgisayar duruma göre farklı işler yapar

### Koşul Blokları (Sarı/Turuncu)

**1. Eğer-O Halde:**
```
<EĞER [durum doğruysa]>
  [bunu yap]
```

**Örnek:**
```
<EĞER [kenara değdi mi?]>
  [sek]
```

**2. Eğer-Değilse:**
```
<EĞER [durum doğruysa]>
  [bunu yap]
<DEĞİLSE>
  [şunu yap]
```

**Örnek:**
```
<EĞER [fare imlecine değdi mi?]>
  [Merhaba söyle]
<DEĞİLSE>
  [Görüşürüz söyle]
```

### Karşılaştırma Operatörleri (Yeşil)

**1. Eşit mi:**
`< [50] = [50] >` → Doğru

**2. Büyük mü:**
`< [60] > [50] >` → Doğru

**3. Küçük mü:**
`< [40] < [50] >` → Doğru

**Örnekler:**
- Puan > 50 → Kazandın
- Hız = 0 → Duruyor
- Yaş < 18 → Çocuk

### Mantıksal Operatörler (Yeşil)

**VE (and):**
`< [koşul1] ve [koşul2] >` → Her ikisi de doğru olmalı

**VEYA (or):**
`< [koşul1] veya [koşul2] >` → Biri doğru yeter

**DEĞİL (not):**
`< [koşul] değil >` → Tersi

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ (10 dk)

**Günlük Karar:**
"Sabah kalkınca ne yaparsın?"

**EĞER** hafta içi **O HALDE** okula git
**DEĞİLSE** uyu 😊

**Soru:**
"Hayatımızda kaç tane koşul var?"

### 2. KONU ANLATIMI (25 dk)

**Koşul Bloğu Tanıtımı:**

**Örnek 1: Kenara Çarpma**
```
(Yeşil bayrak tıklandığında)
[sonsuza kadar]
  [10 adım git]
  <EĞER [kenara değdi mi?]>
    [180 derece dön]
```

**Örnek 2: Fare İmleci**
```
(Yeşil bayrak tıklandığında)
[sonsuza kadar]
  <EĞER [fare imlecine değdi mi?]>
    [Yakalandım! söyle]
    [rastgele konuma git]
```

**Örnek 3: Puan Kontrolü**
```
<EĞER <[puan] > [50]>>
  [Kazandın! söyle]
<DEĞİLSE>
  [Kaybettin! söyle]
```

**Karşılaştırma Operatörleri:**
Tahtada örnekler:
- 10 > 5 → Doğru
- 10 = 10 → Doğru
- 10 < 5 → Yanlış

**VE/VEYA:**
- Aç VE para var → Yemek al ✓
- Aç VE para yok → Yemek alama ✗
- Yağmur VEYA kar → Şemsiye al ✓

### 3. UYGULAMALI ÇALIŞMA (40 dk)

**Görev 1: Duvar Zıplaması (15 dk)**

**Amaç:** Top duvara çarpınca zıplasın

```
(Yeşil bayrak tıklandığında)
[x: -200 y: 0 git]
[90 yöne bak]
[sonsuza kadar]
  [10 adım git]
  <EĞER [kenara değdi mi?]>
    [kenara dokunduğunda sek]
  <EĞER [fare imlecine değdi mi?]>
    [Pop sesi çal]
```

**Görev 2: Renkli Arkaplan (15 dk)**

**Amaç:** Tuşa basınca arkaplan rengi değişsin

```
(boşluk tuşuna basıldığında)
<EĞER <[arkaplan] = [1]>>
  [arkaplan2 seç]
<DEĞİLSE>
  [arkaplan1 seç]
```

**Alternatif:** Rastgele arkaplan

**Görev 3: Basit Oyun - Yakalama (10 dk)**

**2 Sprite:** Kedi (oyuncu), Fare (hedef)

**Kedi (Ok tuşlarıyla kontrol):**
```
(Yeşil bayrak tıklandığında)
[sonsuza kadar]
  <EĞER [sağ ok tuşuna basıldı mı?]>
    [x yönünde 10 değiştir]
  <EĞER [sol ok tuşuna basıldı mı?]>
    [x yönünde -10 değiştir]
  ... (yukarı/aşağı)

  <EĞER [Fare'ye değdi mi?]>
    [Yakaladım! söyle]
```

**Fare:**
```
(Yeşil bayrak tıklandığında)
[sonsuza kadar]
  <EĞER [Kedi'ye değdi mi?]>
    [Kaçtım! söyle]
    [rastgele konuma git]
```

### 4. KAPANIŞ (5 dk)

**Gösterim:**
Öğrenciler oyunlarını gösterir

**Soru:**
"Koşul ne işe yarıyor?"

**Kayıt:**
"Hafta30-Kosullar"

---

## 🏠 EV ÖDEVİ

**"Tahmin Oyunu"**

**Görev:**
Bilgisayar 1-10 arası rastgele sayı tutar, kullanıcı tahmin eder

**Adımlar:**
1. "Gizli sayı" değişkeni oluştur
2. Başlangıçta 1-10 arası rastgele sayı ata
3. Kullanıcıdan tahmin sor
4. EĞER tahmin = gizli sayı → "Bildin!" de
5. DEĞİLSE → "Yanlış, tekrar dene!" de

**Kod Taslağı:**
```
(Yeşil bayrak tıklandığında)
[gizli sayı değişkenini [1 ile 10 arası rastgele] yap]
[Tahminin değişkenini [1 ile 10 arası tahmin et?] sor ve bekle]
<EĞER <[tahmin] = [gizli sayı]>>
  [Bildin! söyle]
<DEĞİLSE>
  [Yanlış! söyle]
```

---

## 📊 ÖZ DEĞERLENDİRME

**Kendimi Değerlendiriyorum:**

- ☐ Koşul kavramını anlıyorum
- ☐ "Eğer-o halde" bloğunu kullanabiliyorum
- ☐ "Eğer-değilse" bloğunu kullanabiliyorum
- ☐ Karşılaştırma operatörlerini biliyorum (>, <, =)
- ☐ Karar veren program yazabiliyorum

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Koşul Mantığı:**
- Günlük hayat örnekleriyle başlayın
- "Doğru/Yanlış" kavramını vurgulayın
- Blokların içine blok yerleştirme biraz zor olabilir, gösterin

**Karşılaştırma:**
- Matematik bilgisi gerekir (>, <, =)
- Eşitlik (=) ile atama farklı! (Scratch'te kafası karışmaz ama ileride önemli)

**Sık Sorunlar:**
- "Koşul çalışmıyor!" → Koşul hiç doğru olmuyor mu? Test edin
- "Sürekli tetikleniyor!" → Sonsuza kadar döngü içinde mi? Bekle bloğu ekleyin
- "Değdi mi? bloğu" → İki sprite adı doğru yazılmalı

**Değişken:**
- Tahmin oyunu için değişken gerekli
- Basit şekilde gösterin, gelecek hafta detaylı anlatılacak

---

## 💡 MERAKLISINA

**Koşullar Hakkında:**

🤖 **AI Kararlar:** Yapay zeka milyonlarca koşul kullanır

🚦 **Trafik Işıkları:** EĞER kırmızı → DUR, DEĞİLSE → GEÇ

🎮 **Oyunlar:** Tüm oyunlar koşullarla çalışır (EĞER düşmana değdi → oyun bitti)

⚖️ **Hukuk:** Yasalar koşul cümleleridir (EĞER hırsızlık yaparsa → ceza)

**Eğlenceli:**
Bir oyunda 1000+ koşul olabilir!

---

## 🧩 EĞLENCE

**Mantık Bulmacası:**

```
EĞER (Yağmur yağıyor VE şemsiyem var)
  O HALDE: Dışarı çık
DEĞİLSE
  Evde kal
```

**Soru:** Yağmur yağıyor ama şemsiye yok. Ne yaparsın?

**Cevap:** Evde kalırsın (çünkü VE operatörü her ikisi de doğru olmalı)

---

**Şaka:**

Programcı çocuğu:
Anne: "EĞER markette ekmek varsa 6 tane al."
Çocuk: *6 ekmek getiriyor*
Anne: "NEDEN 6 tane?"
Çocuk: "Çünkü koşul DOĞRU!" 😄

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "İyi düşün, doğru karar ver."
> **- Mustafa Kemal Atatürk**

Atatürk, doğru kararlar vermenin önemini vurgulamıştır. Programlamada da koşullar, doğru kararlar vermektir. Durumu analiz et, doğru seçeneği seç!

---

## 💎 DEĞERLER EĞİTİMİ

**Analitik Düşünme:**
Koşullar, durumu analiz edip karar vermeyi öğretir.

**Problem Çözme:**
Farklı durumlar için farklı çözümler bulmak.

**Mantık:**
Doğru/yanlış, evet/hayır, 1/0 → Mantıksal düşünme

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta çocuğunuz **koşullar** kavramını öğrendi. Programlarına karar verme yeteneği kazandırdı.

**Öğrendikleri:**
- Koşul kavramı (EĞER-O HALDE)
- Eğer-değilse yapısı
- Karşılaştırma (>, <, =)
- Mantıksal operatörler (VE, VEYA)

**Ev Ödevi:**
"Tahmin Oyunu" - Kullanıcı sayı tahmin eder, program kontrol eder

**Günlük Hayat:**
Koşullar hayatımızın her yerinde:
- "EĞER yeşil ışık → geç"
- "EĞER tok değilsen → ye"

Çocuğunuzla koşul örnekleri konuşabilirsiniz!

---

## 📎 EK KAYNAKLAR

**Scratch Projeler:**
- "Labirent Oyunu" (duvar kontrolü)
- "Tahmin Oyunu"
- "Yakalama Oyunu"

**Videolar:**
- "Scratch Koşullar Türkçe"
- "If-Else Nedir?"

**Oyunlar:**
- Code.org - Conditionals (Koşullar)
- Scratch - Örnek projeler (keşfet bölümü)

**Mantık Oyunları:**
- "Boolean Logic Game"
- "Lightbot" (koşullar bölümü)

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
