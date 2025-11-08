# HAFTA 36: İLERİ SEVİYE PROJE 2 - QUIZ OYUNU
**Sınıf:** 5
**Ünite:** 6 - Yazılım Tasarımı ve Programlama
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Eğitici Quiz Oyunu Yapma

---

## 🎯 ÖĞRENME KAZANIMLARI

- Quiz oyunu tasarlar
- Liste ile soru-cevap sistemi yapar
- Puan sistemi ekler
- Kullanıcı etkileşimi tasarlar
- Geri bildirim sistemi yapar

---

## 📚 PROJE TANITIMI

### Quiz Oyunu Nedir?

**Örnekler:**
- Kim Milyoner Olmak İster
- Bilgi Yarışması
- Kahoot!

**Temel Mekanik:**
- Sorular sorulur
- Kullanıcı cevap verir
- Doğru/yanlış kontrolü
- Puan hesaplama
- Sonuç ekranı

### Kullanılacak Kavramlar

✅ **Listeler:** Sorular, cevaplar
✅ **Değişkenler:** Skor, soru numarası
✅ **Koşullar:** Doğru mu yanlış mı
✅ **Döngüler:** Tüm soruları sor
✅ **Metin:** Birleştirme, gösterme
✅ **Ses:** Doğru/yanlış sesleri

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. PLANLAMA (10 dk)

**Oyun Tasarımı:**

**Bileşenler:**
- Ana karakter (sunucu)
- Soru listesi
- Cevap listesi
- Skor göstergesi

**Akış:**
1. Başlangıç ekranı
2. Soru sor
3. Cevap al
4. Kontrol et
5. Puan ver
6. Sonraki soru
7. Sonuç göster

### 2. LİSTE HAZIRLAMA (10 dk)

**4 Liste Oluştur:**

```
1. Sorular
2. Cevap A
3. Cevap B
4. Doğru Cevap
```

**Örnek Sorular (Matematik):**

```
(Yeşil bayrak tıklandığında)

// Listeleri Temizle
[Sorular listesinin tüm elemanlarını sil]
[Cevap A listesinin tüm elemanlarını sil]
[Cevap B listesinin tüm elemanlarını sil]
[Doğru Cevap listesinin tüm elemanlarını sil]

// Soru 1
[2 + 2 kaç? Sorular listesine ekle]
[3 Cevap A listesine ekle]
[4 Cevap B listesine ekle]
[B Doğru Cevap listesine ekle]

// Soru 2
[5 x 3 kaç? Sorular listesine ekle]
[15 Cevap A listesine ekle]
[12 Cevap B listesine ekle]
[A Doğru Cevap listesine ekle]

// Soru 3
[10 - 6 kaç? Sorular listesine ekle]
[5 Cevap A listesine ekle]
[4 Cevap B listesine ekle]
[B Doğru Cevap listesine ekle]

// Soru 4
[20 / 4 kaç? Sorular listesine ekle]
[5 Cevap A listesine ekle]
[4 Cevap B listesine ekle]
[A Doğru Cevap listesine ekle]

// Soru 5
[7 + 8 kaç? Sorular listesine ekle]
[14 Cevap A listesine ekle]
[15 Cevap B listesine ekle]
[B Doğru Cevap listesine ekle]
```

### 3. ANA OYUN DÖNGÜSÜ (25 dk)

**Sprite: Sunucu (Karakter)**

```
(Yeşil bayrak tıklandığında)

[Skor değişkenini 0 yap]
[Soru No değişkenini 1 yap]

// Başlangıç
[Bilgi Yarışmasına Hoş Geldiniz! söyle] (2 saniye)
[[<Sorular listesinin uzunluğu> ve [ soru var!] birleştir söyle] (2 saniye)

// Soru Döngüsü
[<Sorular listesinin uzunluğu> kez tekrarla]

  // Soruyu Sor
  [Soru Metni değişkenini
    [[Soru ] ve [Soru No] ve [: ] ve <Sorular listesinin [Soru No]. elemanı> birleştir
  yap]
  [Soru Metni söyle] (3 saniye)

  // Seçenekleri Göster
  [Seçenekler değişkenini
    [[A) ] ve <Cevap A listesinin [Soru No]. elemanı> ve [ B) ] ve <Cevap B listesinin [Soru No]. elemanı> birleştir
  yap]
  [Seçenekler söyle] (3 saniye)

  // Kullanıcı Cevabı Al
  [Kullanıcı Cevabı değişkenini [Cevabın (A veya B)?] sor ve bekle]

  // Kontrolü Et
  <EĞER <[Kullanıcı Cevabı] = <Doğru Cevap listesinin [Soru No]. elemanı>>>
    [Doğru! söyle] (1 saniye)
    [Skor değişkenini 1 arttır]
    [Yaşasın sesi çal]
  <DEĞİLSE>
    [[Yanlış! Doğru cevap: ] ve <Doğru Cevap listesinin [Soru No]. elemanı> birleştir söyle] (2 saniye)
    [Hata sesi çal]

  [Soru No değişkenini 1 arttır]
  [1 saniye bekle]

// Sonuç Ekranı
[[Oyun Bitti! Skorun: ] ve [Skor] ve [ / ] ve <Sorular listesinin uzunluğu> birleştir söyle] (5 saniye)

<EĞER <[Skor] = <Sorular listesinin uzunluğu>>>
  [Mükemmel! Hepsini doğru bildin! söyle]
<DEĞİLSE>
  <EĞER <[Skor] >= <<Sorular listesinin uzunluğu> / [2]>>>
    [İyi iş! Başarılısın! söyle]
  <DEĞİLSE>
    [Daha çok çalışmalısın! söyle]
```

### 4. GÖRSEL İYİLEŞTİRME (15 dk)

**Arka Plan:**
- Quiz temalı arka plan

**Kostümler:**
- Mutlu kostüm (doğru cevap)
- Üzgün kostüm (yanlış cevap)

**Efektler:**
- Renk efekti
- Büyüme/küçülme

**Ses:**
- Doğru cevap sesi
- Yanlış cevap sesi
- Alkış sesi (sonuçta)

### 5. TEST ve OYNA (15 dk)

**Test:**
- Tüm sorular soruluyor mu?
- Cevap kontrolü doğru mu?
- Puan doğru hesaplanıyor mu?
- Sonuç ekranı çalışıyor mu?

**Oynat:**
Öğrenciler birbirlerinin oyunlarını oynar

### 6. PAYLAŞIM (5 dk)

Gönüllü öğrenciler oyunlarını gösterir

---

## 🏠 EV ÖDEVİ

**"Kendi Quiz'ini Yap"**

**Görev:**
Sevdiğin bir konu hakkında quiz oyunu yap

**Konular:**
- Hayvanlar
- Tarih
- Coğrafya
- Spor
- Film/Dizi
- Genel kültür

**Gereksinimler:**
1. En az 10 soru
2. Her soruda 2-4 seçenek
3. Puan sistemi
4. Başlangıç ve bitiş ekranı
5. Ses efektleri

**Bonus:**
- Zaman sınırı
- Joker hakkı
- Seviye sistemi (kolay, orta, zor)

---

## 📊 ÖZ DEĞERLENDİRME

**Kendimi Değerlendiriyorum:**

- ☐ Quiz oyunu tasarlayabiliyorum
- ☐ Liste ile soru-cevap sistemi yapabiliyorum
- ☐ Puan sistemi ekleyebildim
- ☐ Kullanıcı girdisi alıp kontrol ediyorum
- ☐ Geri bildirim veriyorum
- ☐ Eğitici oyun yapabiliyorum!

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Zorluk:**
- Listeler biraz karmaşık
- Adım adım gösterin
- Önce 3 soruyla başlayın, sonra genişletin

**Liste Yönetimi:**
- 4 liste birden (Sorular, Cevap A, Cevap B, Doğru Cevap)
- İndexler eşleşmeli (Soru 1 → Cevaplar 1)
- Hata yapılabilir, dikkatli olunmalı

**Alternatif Basit Versiyon:**
Eğer 4 liste çok zorsa:
- 2 liste: Sorular, Cevaplar
- Kullanıcı direkt cevabı yazar (A/B seçmez)

**Sık Sorunlar:**
- "Cevap hep yanlış!" → Liste indexleri yanlış eşleşmiş
- "Sorular tekrar ediyor!" → Soru No arttırılmamış
- "Liste boş!" → Listeleri temizlemeden doldurmamış

**Eğlenceli Konu:**
Öğrencilerin ilgi alanlarına göre soru konusu seçsinler (oyun, film vb.)

---

## 💡 MERAKLISINA

**Quiz Oyunları:**

📺 **Kim Milyoner:** 1998'de başladı, hala popüler!

🎓 **Kahoot!:** Eğitimde en çok kullanılan quiz platformu

🧠 **Trivia Crack:** 500+ milyon oyuncu!

💰 **Ödüllü Quizler:** Gerçek hayatta para kazanılan quiz oyunları var!

**Türkiye:**
Riziko, Kelime Oyunu, Bilgi Yarışmaları çok seviliyor!

---

## 🧩 EĞLENCE

**Quiz Sorusu:**

**Soru:** Dünyanın en büyük okyanusu?
A) Atlas
B) Pasifik

**Cevap:** B (Pasifik)

---

**Şaka:**

Quiz: "2 + 2 kaç?"
Öğrenci: "İstediğinize göre değişir!"
Sunucu: "Nasıl yani?"
Öğrenci: "Programda değişken kullandıysanız!" 😄

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Öğrendiklerini başkalarına öğretmek en büyük erdemos."
> **- Mustafa Kemal Atatürk ruhundan**

Atatürk, bilgiyi paylaşmayı önemsemiştir. Quiz oyunları, öğrendiklerinizi başkalarıyla paylaşmanın eğlenceli yoludur!

**Proje Fikri:** Atatürk ve Türkiye Cumhuriyeti hakkında quiz oyunu yapabilirsin!

---

## 💎 DEĞERLER EĞİTİMİ

**Öğrenme Sevgisi:**
Quiz oyunları öğrenmeyi eğlenceli hale getirir.

**Paylaşma:**
Bilgini quiz olarak paylaşırsın.

**Yarışma Ruhu:**
Sağlıklı rekabet, öğrenmeyi artırır.

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta çocuğunuz **Quiz Oyunu** yaptı. Eğitici bir proje hazırladı!

**Proje İçeriği:**
- Soru-cevap sistemi
- Liste yönetimi
- Puan hesaplama
- Geri bildirim mekanizması

**Ev Ödevi:**
Sevdiği konu hakkında 10 soruluk quiz oyunu yapmak

**Not:**
Quiz oyunları hem eğlenceli hem eğiticidir. Çocuğunuz öğrenmeyi oyunlaştırmayı öğrendi!

**Birlikte:**
Ailenizle quiz oynayabilirsiniz. Çocuğunuzun yaptığı oyunu deneyin!

---

## 📎 EK KAYNAKLAR

**Quiz Konuları:**
- Hayvanlar Alemi
- Türkiye Coğrafyası
- Matematik İşlemleri
- Tarih Olayları
- Spor Bilgisi
- Genel Kültür

**Scratch Projeler:**
- "Simple Quiz Game"
- "Trivia Game"
- "Multiple Choice Quiz"

**Videolar:**
- "Scratch Quiz Oyunu Türkçe"
- "Making a Quiz Game"

**İleri Seviye:**
- Zamanlayıcı ekleme
- Joker sistemi (50:50, telefon joker)
- Seviye atlama
- Liderlik tablosu

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
