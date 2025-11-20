# HAFTA 31: DEĞİŞKENLER
**Sınıf:** 5
**Ünite:** 6 - Yazılım Tasarımı ve Programlama
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Değişken Kavramı, Oluşturma, Kullanma, Puan Sistemi

---

## 🎯 ÖĞRENME KAZANIMLARI

- Değişken kavramını anlar
- Değişken oluşturur
- Değişkenin değerini değiştirir
- Puan sistemi yapar
- Sayaç kullanır

---

## 📚 KONU ÖZETİ

### Değişken Nedir?

**Tanım:** Bilgiyi saklayan kutu

**Günlük Hayat:**
- **Kumbara:** Para miktarını saklar
- **Skor Tahtası:** Puan saklar
- **Termometre:** Sıcaklık saklar

**Programlamada:**
Değişken = İsimli hafıza kutusu

**Örnek:**
- `Puan` değişkeni → 0, 10, 25...
- `İsim` değişkeni → "Ahmet", "Ayşe"...
- `Hız` değişkeni → 50, 100...

### Değişken İşlemleri

**1. Oluşturma:**
Değişkenler → "Değişken oluştur" → İsim ver

**2. Değer Atama:**
`[Puan değişkenini 0 yap]` → Puan = 0

**3. Değiştirme:**
`[Puan değişkenini 1 arttır]` → Puan = Puan + 1
`[Puan değişkenini -1 değiştir]` → Puan azalır

**4. Gösterme/Gizleme:**
`[Puan göster]` → Sahnede görünür
`[Puan gizle]` → Sahnede gizlenir

### Değişken Türleri (Scratch'te basit)

**Sayısal:**
0, 10, -5, 3.14...

**Metin:**
"Merhaba", "Ahmet"...

**Scratch'te:**
Her değişken her şeyi saklayabilir (tip yok)

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ (10 dk)

**Kumbara Örneği:**

"Kumbarada 0 TL var.
+5 TL ekledim → 5 TL
+10 TL ekledim → 15 TL
-3 TL çıkardım → 12 TL"

**Soru:**
"Kumbara bilgiyi nasıl saklıyor?"

**Cevap:**
Kumbara = Değişken!

### 2. KONU ANLATIMI (20 dk)

**Değişken Oluşturma (Projeksiyon):**

1. "Değişkenler" kategorisi (turuncu)
2. "Değişken oluştur" butonu
3. İsim: "Puan"
4. Tüm sprite'lar için / Sadece bu sprite için → Seç
5. Tamam

**Değişken Blokları:**

**Örnek 1: Puan Başlatma**
```
(Yeşil bayrak tıklandığında)
[Puan değişkenini 0 yap]
```

**Örnek 2: Puan Arttırma**
```
(Bu sprite tıklandığında)
[Puan değişkenini 1 arttır]
[Yaşasın! söyle]
```

**Örnek 3: Sayaç**
```
(Yeşil bayrak tıklandığında)
[Sayaç değişkenini 0 yap]
[10 kez tekrarla]
  [Sayaç değişkenini 1 arttır]
  [1 saniye bekle]
```
→ 10'a kadar sayar

**Örnek 4: İsim Sorma**
```
(Yeşil bayrak tıklandığında)
[İsim değişkenini [Adın ne?] sor ve bekle]
[[Merhaba ] ve [İsim] birleştir söyle]
```

### 3. UYGULAMALI ÇALIŞMA (45 dk)

**Görev 1: Tıklama Oyunu (15 dk)**

**Amaç:** Sprite'a tıklayınca puan kazan

```
(Yeşil bayrak tıklandığında)
[Puan değişkenini 0 yap]

(Bu sprite tıklandığında)
[Puan değişkenini 1 arttır]
[Yay! sesi çal]
[rastgele konuma git]
```

**Öğrenciler:**
- Hızlı sprite seç (elma, top...)
- 30 saniye süre koy (zamanlayıcı)
- Kaç puan toplanır?

**Görev 2: Geri Sayım (15 dk)**

**Amaç:** 10'dan 0'a geri sayım

```
(Yeşil bayrak tıklandığında)
[Süre değişkenini 10 yap]
[10 kez tekrarla]
  [Süre göster]
  [1 saniye bekle]
  [Süre değişkenini -1 değiştir]
[SÜRE BİTTİ! söyle]
```

**Bonus:** Roket fırlatma animasyonu

**Görev 3: Basit Hesap Makinesi (15 dk)**

**Amaç:** İki sayıyı topla

```
(Yeşil bayrak tıklandığında)
[Sayı1 değişkenini [Birinci sayı?] sor ve bekle]
[Sayı2 değişkenini [İkinci sayı?] sor ve bekle]
[Sonuç değişkenini <[Sayı1] + [Sayı2]> yap]
[[Sonuç: ] ve [Sonuç] birleştir söyle] (2 saniye)
```

**Öğrenciler:**
- Toplama yap
- Bonus: Çıkarma, çarpma, bölme seçenekleri

### 4. KAPANIŞ (5 dk)

**Gösterim:**
Öğrenciler oyunlarını gösterir

**Soru:**
"Değişken ne işe yarar?"

**Kayıt:**
"Hafta31-Degiskenler"

---

## 🏠 EV ÖDEVİ

**"Kelime Oyunu"**

**Görev:**
Kullanıcıdan 3 kelime al (isim, fiil, sıfat), hikaye oluştur

**Adımlar:**
1. "İsim", "Fiil", "Sıfat" değişkenleri oluştur
2. Kullanıcıdan soruyla al
3. Komik hikaye yaz

**Örnek:**
```
(Yeşil bayrak tıklandığında)
[İsim değişkenini [Bir isim gir (örn: kedi)?] sor ve bekle]
[Fiil değişkenini [Bir fiil gir (örn: koşmak)?] sor ve bekle]
[Sıfat değişkenini [Bir sıfat gir (örn: hızlı)?] sor ve bekle]

[Hikaye değişkenini
  [[İsim] ve [ ] ve [Fiil] ve [iken ] ve [Sıfat] ve [ oldu!] birleştir
yap]

[Hikaye söyle] (5 saniye)
```

**Çıktı:**
"Kedi koşarken hızlı oldu!"

---

## 📊 ÖZ DEĞERLENDİRME

**Kendimi Değerlendiriyorum:**

- ☐ Değişken kavramını anlıyorum
- ☐ Değişken oluşturabiliyorum
- ☐ Değişkenin değerini değiştirebiliyorum
- ☐ Puan sistemi yapabiliyorum
- ☐ Sayaç kullanabiliyorum
- ☐ Metin birleştirebiliyorum

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Değişken Kavramı:**
- 5. sınıf için soyut olabilir
- "Kutu" benzetmesi yapın (içine bir şey koy, çıkar)
- Kumbara, skor tahtası gibi somut örnekler

**Değişken İsimlendirme:**
- Türkçe isim kullanılabilir (Puan, İsim, Hız...)
- Boşluksuz yazın veya "_" kullanın (Toplam_Puan)

**Sık Sorunlar:**
- "Değişken gösteriyor ama değişmiyor!" → "değiştir" bloğunu kullanmamış
- "Değişken ekranda görünmüyor!" → "göster" bloğu
- "Değişken bulamıyorum!" → Değişkenler kategorisinde, altında listelenir

**Tür Karışıklığı:**
- Scratch'te tip yok ama mantıksal hata olabilir
- "Puan" değişkenine "Ahmet" yazmak garip!

**İleri:**
- Liste kavramı gelecek haftalarda

---

## 💡 MERAKLISINA

**Değişkenler Hakkında:**

💾 **Bilgisayar Hafızası:** Milyarlarca değişken saklar (RAM)

🎮 **Oyunlarda:** Her karakter, obje ayrı değişken (konum, can, puan...)

📊 **Veri Bilimi:** Büyük veriler değişkenlerde saklanır

🤖 **AI:** Yapay zeka milyonlarca değişken kullanarak öğrenir

**İlginç:**
En ünlü değişken adı: "x" (matematik ve programlamada)

**Eğlenceli:**
Bazı oyunlarda 10,000+ değişken var!

---

## 🧩 EĞLENCE

**Değişken Bulmacası:**

```
Puan = 0
Puan = Puan + 5
Puan = Puan + 10
Puan = Puan - 3
```

**Soru:** Puan kaç olur?

**Cevap:** 12

---

**Şaka:**

Programcı çocuğuna soruyor:
"Kumbarada ne kadar paran var?"
Çocuk: "Değişken!"
Baba: "Kaç lira?"
Çocuk: "Değişkenin değeri undefined!" 😄

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Bilimde, teknikte, düşüncede, fikirde, eğitimde, ekonomide gerçek yol gösterici bilimdir."
> **- Mustafa Kemal Atatürk**

Atatürk, bilimin önemini vurgulamıştır. Değişkenler, bilgisayar biliminin temel taşlarından biridir. Bugün öğrendiğiniz bu kavram, gelecekteki bilimsel çalışmalarınızın temelidir.

---

## 💎 DEĞERLER EĞİTİMİ

**Düzen ve Organizasyon:**
Değişkenler bilgiyi düzenli saklar.

**Matematiksel Düşünme:**
Değişken matematikten gelir (x, y, z...)

**Problem Çözme:**
Karmaşık problemleri değişkenlerle basitleştiririz.

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta çocuğunuz **değişkenler** kavramını öğrendi. Programlarında bilgi saklayıp değiştirebiliyor artık!

**Öğrendikleri:**
- Değişken kavramı
- Değişken oluşturma
- Değer atama ve değiştirme
- Puan sistemi, sayaç yapma
- Metin birleştirme

**Ev Ödevi:**
"Kelime Oyunu" - Kullanıcıdan kelime alıp hikaye oluşturma

**Günlük Hayat:**
Değişken örnekleri:
- Banka hesabı (para miktarı değişir)
- Araba sayacı (kilometre artar)
- Sınav notu (değişken bir değer)

**Not:** Değişken, programlamanın en temel kavramıdır. Çocuğunuz artık gerçek programlar yazabilir!

---

## 📎 EK KAYNAKLAR

**Scratch Projeler:**
- "Tıklama Oyunu"
- "Geri Sayım"
- "Hesap Makinesi"
- "Quiz Oyunu" (puan tutma)

**Videolar:**
- "Scratch Değişkenler Türkçe"
- "Variable Nedir?"

**Oyunlar:**
- Code.org - Variables (Değişkenler)

**İleri Seviye:**
- Global vs Local değişkenler (Scratch'te basit)
- Liste (array) kavramı (gelecek haftalarda)

**Matematik Bağlantısı:**
- x + 5 = 10 → x nedir? (Değişken!)

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
