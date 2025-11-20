# TABLOLAMA PROJESİ: SINIF NOT SİSTEMİ

## 🎯 PROJE AMACI

Öğrencilerin Excel/Google Sheets kullanarak:
- Düzenli tablo oluşturmayı öğrenmeleri
- Formül ve fonksiyonları kullanmaları
- Veri analizi yapmalar

ı
- Grafik oluşturmalarını öğrenmeleri

**Hedef Sınıf:** 6. Sınıf
**Tahmini Süre:** 3 ders saati (120 dakika)
**Zorluk Seviyesi:** Orta

---

## 📋 GEREKLİ MATERYALLER

- Bilgisayar (Excel veya Google Sheets yüklü)
- İnternet bağlantısı (Google Sheets için)
- Projeksiyon
- Örnek veri seti
- Çalışma kağıdı

---

## 📚 ÖN BİLGİLER

Öğrencilerin bilmesi gerekenler:
- Temel bilgisayar kullanımı
- Dosya kaydetme/açma
- Tablolama programının temel arayüzü

---

## 🎮 PROJE: "S

INIF NOT TAKİP SİSTEMİ"

### Proje Özeti
Hayali bir sınıfın ders notlarını içeren bir tablo oluşturup, ortalama hesaplama, başarı durumu belirleme ve grafik oluşturma.

---

## 📝 ADIM ADIM UYGULAMA

### 🔷 BÖLÜM 1: TABLO OLUŞTURMA (30 dk)

#### ADIM 1: Yeni Dosya Açma

**Excel için:**
1. Excel'i açın
2. **Boş Çalışma Kitabı** seçin
3. Dosya > Farklı Kaydet > "Sinif_Notlari_AdSoyad"

**Google Sheets için:**
1. Google Drive'a gidin
2. Yeni > Google E-Tablolar
3. Üstten isim verin: "Sinif_Notlari_AdSoyad"

---

#### ADIM 2: Başlıkları Oluşturma

**A1 hücresine** başlık yazın: **6-A SINIFI NOT TABLOSU**

Bu hücreyi **birleştirin ve ortala** (A1:G1)

**A3'ten başlayarak sütun başlıkları:**
| A3 | B3 | C3 | D3 | E3 | F3 | G3 |
|----|----|----|----|----|----|----|
| No | Ad Soyad | Matematik | Fen | Türkçe | Ortalama | Durum |

**Biçimlendirme:**
- Başlık satırını **kalın** yapın
- Arka plan rengi: **Mavi**
- Yazı rengi: **Beyaz**
- Hizalama: **Ortala**

---

#### ADIM 3: Veri Girişi

**A4'ten başlayarak örnek veriler girin:**

```
No  Ad Soyad        Matematik  Fen  Türkçe
1   Ahmet Yılmaz    85         90   75
2   Ayşe Demir      92         88   95
3   Mehmet Kaya     70         65   72
4   Zeynep Çelik    88         92   90
5   Can Öztürk      76         80   78
6   Elif Arslan     95         93   97
7   Burak Şahin     68         70   69
8   Selin Yıldız    91         89   92
9   Emre Koç        73         75   71
10  Deniz Aydın     87         85   88
```

**İpucu:** Kendi arkadaşlarınızın isimlerini kullanabilirsiniz!

---

### 🔷 BÖLÜM 2: FORMÜL VE FONKSİYONLAR (40 dk)

#### ADIM 4: Ortalama Hesaplama

**F4 hücresine (Ahmet'in ortalaması):**

```excel
=ORTALAMA(C4:E4)
```

veya

```excel
=(C4+D4+E4)/3
```

**İki yöntem de çalışır!**

**Formülü kopyalama:**
1. F4 hücresini seçin
2. Sağ alt köşedeki küçük kareyi tutup aşağı sürükleyin
3. F13'e kadar kopyalayın

---

#### ADIM 5: Durum Belirleme (IF Fonksiyonu)

**G4 hücresine:**

```excel
=EĞER(F4>=70;"Geçti";"Kaldı")
```

**Google Sheets için:**
```excel
=IF(F4>=70,"Geçti","Kaldı")
```

**Açıklama:**
- Eğer ortalama 70 veya üstüyse "Geçti"
- Değilse "Kaldı"

**Formülü G13'e kadar kopyalayın**

---

#### ADIM 6: Durum Renklendir

me (Koşullu Biçimlendirme)

**G4:G13 aralığını seçin:**

**Excel için:**
1. Giriş > Koşullu Biçimlendirme
2. Hücre Kuralları > Eşittir
3. "Geçti" için **Yeşil** arka plan
4. Tekrarlayın: "Kaldı" için **Kırmızı** arka plan

**Google Sheets için:**
1. Biçim > Koşullu biçimlendirme
2. Biçimlendirme kuralları: "Metin içeriyor" > "Geçti"
3. Biçimlendirme stili: Yeşil arka plan
4. Başka kural ekle: "Kaldı" için kırmızı

---

#### ADIM 7: İstatistikler Ekleme

**A15'ten başlayarak:**

| Açıklama | Formül |
|----------|--------|
| A15: **SINIF İSTATİSTİKLERİ** (birleştirilmiş hücre) | |
| A17: En Yüksek Not (Mat) | B17: `=MAKS(C4:C13)` |
| A18: En Düşük Not (Mat) | B18: `=MİN(C4:C13)` |
| A19: Sınıf Ortalaması (Mat) | B19: `=ORTALAMA(C4:C13)` |
| A20: Geçen Öğrenci Sayısı | B20: `=SAYTAŞI.EĞER(G4:G13;"Geçti")` |
| A21: Kalan Öğrenci Sayısı | B21: `=SAYTAŞI.EĞER(G4:G13;"Kaldı")` |

**Google Sheets için:**
- MAKS → MAX
- MİN → MIN
- ORTALAMA → AVERAGE
- SAYTAŞI.EĞER → COUNTIF

---

### 🔷 BÖLÜM 3: GRAFİK OLUŞTURMA (30 dk)

#### ADIM 8: Öğrenci Başarı Grafiği

**B3:B13 ve F3:F13 hücrelerini seçin** (Ctrl tuşuyla)

**Grafik Ekleme:**
1. Ekle > Grafik
2. Grafik türü: **Sütun Grafiği**
3. Grafik Başlığı: "Öğrenci Ortalamaları"
4. Yatay eksen: "Öğrenciler"
5. Dikey eksen: "Ortalama"

**Grafik özelleştirme:**
- Renk teması seçin
- Veri etiketlerini gösterin
- Grafik stilini değiştirin

---

#### ADIM 9: Ders Karşılaştırma Grafiği

**Yeni bir grafik için:**

**C3:E3 başlıklarını ve C17:E17 sınıf ortalamalarını seçin**

**Grafik türü:** Çubuk veya Pasta grafiği

**Başlık:** "Derslere Göre Sınıf Ortalaması"

---

#### ADIM 10: Geçen-Kalan Pasta Grafiği

**A20:B21 aralığını seçin**

**Grafik türü:** Pasta Grafiği

**Başlık:** "Başarı Dağılımı"

**Renk:**
- Geçen: Yeşil
- Kalan: Kırmızı

---

### 🔷 BÖLÜM 4: FİLTRELEME VE SIRALAMA (20 dk)

#### ADIM 11: Filtre Ekleme

**A3:G13 aralığını seçin**

**Veri > Filtre** butonuna tıklayın

**Sütun başlıklarında ok simgeleri görünecek**

**Denemeler:**
1. Duruma göre filtrele: Sadece "Geçti" olanları göster
2. Matematik notuna göre filtrele: 80'in üstündekiler
3. Filtreyi temizle

---

#### ADIM 12: Sıralama

**A3:G13 aralığını seçin**

**Veri > Sırala**

**Sıralama kriterleri:**
- **Sıralama ölçütü 1:** Ortalama, Büyükten küçüğe
- Uygula

**Sonuç:** En başarılı öğrenci en üstte!

---

## ✅ DEĞERLENDİRME KONTROL LİSTESİ

| Kriter | Puan | Tamamlandı |
|--------|------|------------|
| Tablo düzgün oluşturuldu | 10 | ☐ |
| Başlıklar doğru biçimlendirildi | 5 | ☐ |
| Ortalama formülü doğru | 15 | ☐ |
| IF formülü doğru | 15 | ☐ |
| Koşullu biçimlendirme yapıldı | 10 | ☐ |
| İstatistik formülleri doğru | 15 | ☐ |
| En az 2 grafik oluşturuldu | 20 | ☐ |
| Filtreleme ve sıralama yapıldı | 10 | ☐ |
| **TOPLAM** | **100** | |

---

## 🎨 GELİŞTİRME FİKİRLERİ

### Kolay Seviye:
- ✨ Daha fazla öğrenci ekleyin (20 öğrenci)
- 🎨 Farklı renk temaları deneyin
- 📊 Daha fazla grafik türü ekleyin

### Orta Seviye:
- 📚 Daha fazla ders ekleyin (İngilizce, Sosyal)
- 💯 Harf notu sistemi ekleyin (A, B, C...)
- 📈 Dönemsel karşılaştırma yapın (1. dönem vs 2. dönem)

### İleri Seviye:
- 🏆 En başarılı öğrenciyi otomatik bulun (ENBOY fonksiyonu)
- 📊 Pivot tablo oluşturun
- 🎯 Başarı yüzdesi hesaplayın
- 💼 Öğretmen raporlama sayfası ekleyin

---

## 🐛 SORUN GİDERME

### Problem: Formül çalışmıyor, yazı olarak görünüyor
**Çözüm:** = işaretiyle başladığından emin olun. Hücre formatını "Genel" yapın.

### Problem: #DEĞER! hatası
**Çözüm:** Formüldeki hücre referanslarını kontrol edin. Sayısal olmayan veri var mı?

### Problem: Grafik yanlış veri gösteriyor
**Çözüm:** Grafik veri aralığını kontrol edin. Veri kaynağını düzenleyin.

### Problem: Koşullu biçimlendirme çalışmıyor
**Çözüm:** Doğru hücre aralığını seçtiğinizden ve kuralın doğru olduğundan emin olun.

---

## 🏠 EV ÖDEVİ

**"Aile Bütçesi Tablosu"**

Evinizin aylık gelir-gider tablosunu oluşturun:

**Sütunlar:**
- Kategori (Gıda, Fatura, Eğlence vb.)
- Planlanan Tutar
- Gerçekleşen Tutar
- Fark (Formül ile)

**Ekstra:**
- Toplam gelir/gider
- Kalan para
- Pasta grafiği (Giderlerin dağılımı)

**Dikkat:** Gerçek veriler kullanmak zorunda değilsiniz, tahmin edebilirsiniz!

---

## 👨‍🏫 ÖĞRETMEN NOTLARI

### Ders Öncesi Hazırlık:
- [ ] Bilgisayarlarda Excel/Sheets açık
- [ ] Örnek dosya hazır (gösterim için)
- [ ] Projeksiyon test edildi
- [ ] Yedek plan (internet kesilmesi için Excel)

### Önemli Noktalar:
- İlk kez formül kullanan öğrencilere sabırlı olun
- = işaretinin önemini vurgulayın
- Formül kopyalama kolaylığını gösterin
- Her öğrencinin çalışan bir proje oluşturduğundan emin olun

### Farklılaştırma:
- **İleri öğrenciler:** Karmaşık formüller (VLO

OKUP, EŞLEŞ vb.)
- **Desteklenmesi gerekenler:** Basit formüllerle başlayın
- **Görsel öğrenenler:** Adım adım ekran görüntüleri
- **Kinestetik öğrenenler:** Ellerinde yapmalarını sağlayın

### Zaman Yönetimi:
- **1. Ders (40 dk):** Tablo oluşturma ve veri girişi
- **2. Ders (40 dk):** Formüller ve istatistikler
- **3. Ders (40 dk):** Grafikler ve son rötuşlar

---

## 📸 PORTFOLYO İÇİN

Bu projeden eklenecekler:
- Tamamlanmış tablo ekran görüntüsü
- Grafiklerin ekran görüntüsü
- Kullanılan formüllerin listesi
- Öz değerlendirme formu

---

## 🔗 KAYNAKLAR

**Video Dersler:**
- YouTube: "Excel Formüller"
- YouTube: "Google Sheets Dersleri"
- EBA: Tablolama videoları

**Pratik Siteleri:**
- Excel Easy (Türkçe)
- Google Sheets Eğitim Merkezi
- BTK Akademi Excel Kursu

---

## 🌟 BAŞARI HİKAYESİ

Projenizi tamamladığınızda:
- Gerçek hayatta not takibi yapabileceksiniz
- Veri analizi becerileri kazanacaksınız
- İlerideki projelerde bu bilgileri kullanabileceksiniz
- Matematiksel düşünme geliştirdiniz!

**Tebrikler! 🎉**

---

## 💡 GERÇEKLİF TEMSİL VE ETİK

**Önemli Hatırlatma:**
- Bu projede kullanılan notlar **hayali**dir
- Gerçek öğrenci bilgileri **paylaşılmamalıdır**
- Veri gizliliği önemlidir
- Başkalarının notlarını izinsiz görmek etik değildir

**Ders:** Teknolojiyi kullanırken **gizlilik** ve **etik** her zaman ön planda!

---

**Mutlu çalışmalar! 📊**

*Veri analizi geleceğin en önemli becerilerinden! Bu proje sizin için bir başlangıç.*
