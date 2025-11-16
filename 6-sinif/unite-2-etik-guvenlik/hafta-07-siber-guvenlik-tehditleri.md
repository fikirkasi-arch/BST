# HAFTA 7: SİBER GÜVENLİK TEHDİTLERİ
**Sınıf:** 6
**Ünite:** 2 - Etik ve Güvenlik
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Siber Tehditler, Zararlı Yazılımlar, Kimlik Avı, Sosyal Mühendislik

---

## 🎯 ÖĞRENME KAZANIMLARI

- Siber tehdit türlerini tanır
- Zararlı yazılımları ayırt eder
- Kimlik avı (phishing) girişimlerini fark eder
- Sosyal mühendislik taktiklerini bilir
- Siber tehditlerden korunma yollarını uygular

---

## 📚 KONU ÖZETİ

### Zararlı Yazılımlar (Malware)

**1. Virüs:**
- Kendini kopyalar, diğer dosyalara bulaşır
- Zarar verir (dosya silme, yavaşlatma)
- Örnek: ILOVEYOU virüsü (2000)

**2. Truva Atı (Trojan):**
- Yararlı gibi görünür ama zararlıdır
- Örnek: "Bedava oyun" indirirsin, bilgisayarını kontrol ederler

**3. Solucan (Worm):**
- Ağ üzerinden yayılır
- Kendi kendine çoğalır
- İnternet trafiğini tıkar

**4. Casus Yazılım (Spyware):**
- Seni gizlice izler
- Şifreleri, bilgileri çalar
- Tuş kaydedici (keylogger)

**5. Fidye Yazılımı (Ransomware):**
- Dosyalarını şifreler
- Para istenir (fidye)
- Ödesen bile dosyalar gelmeyebilir!

**6. Reklam Yazılımı (Adware):**
- Sürekli reklam gösterir
- Yavaşlatır
- Genelde ücretsiz programlarda

### Kimlik Avı (Phishing)

**Tanım:** Sahte e-posta/mesajla bilgi çalma

**Nasıl Çalışır:**
1. Sahte e-posta/SMS gelir (bankadan, sosyal medyadan...)
2. "Hesabınız bloke oldu! Tıklayın!" der
3. Sahte siteye yönlendirir
4. Şifre/kart bilgisi isterler
5. Bilgileri çalarlar

**Nasıl Anlaşılır:**
- ✉️ Yazım hataları
- ⚠️ Acil eylem tehdidi ("Hemen!", "Bugün!")
- 🔗 Şüpheli link (tıklama!)
- 📧 Bilinmeyen gönderici
- 💰 Para/hediye vaadi

**Örnekler:**
- "Netflix aboneliğiniz iptal! Hemen ödeyin!"
- "1 Milyon TL kazandınız! Bilgilerinizi girin!"
- "Hesabınız çalındı! Şifrenizi gönderin!"

### Sosyal Mühendislik

**Tanım:** İnsanları kandırarak bilgi çalma

**Taktikler:**
1. **Güven Sağlama:** "Ben bankanızdan arıyorum..."
2. **Korku:** "Hesabınız tehlikede!"
3. **Aciliyet:** "5 dakika içinde yapın!"
4. **Merak:** "Bunu görmek zorundasın!"
5. **Yardımseverlik:** "Yardım eder misiniz?"

**Örnekler:**
- Telefonda kendini banka çalışanı olarak tanıtıp şifre istemek
- Sahte teknik destek
- Sahte arkadaşlık kurma

### Diğer Tehditler

**1. DDoS Saldırısı:**
- Siteyi trafikle boğma
- Site çöker

**2. Ortadaki Adam (Man-in-the-Middle):**
- Açık Wi-Fi'da verilerinizi dinleme

**3. SQL Injection:**
- Web sitesi veritabanını hacklemek

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ (10 dk)

**Haber Paylaşımı:**
Güncel siber saldırı haberi (Türkiye'den veya dünyadan)

**Tartışma:**
- Ne oldu?
- Nasıl oldu?
- Nasıl önlenebilirdi?

### 2. KONU ANLATIMI (30 dk)

**Zararlı Yazılımlar:**
- Her tür için açıklama + örnek
- Görsel: Zararlı yazılım türleri tablosu
- Video: "Virüs Nasıl Çalışır?" (5 dk)

**Kimlik Avı:**
- Sahte e-posta örneği gösterimi (projeksiyon)
- Gerçek vs Sahte karşılaştırma

**Gerçek E-posta:**
```
Gönderici: netflix@netflix.com
Konu: Aylık faturanız
İçerik: Merhaba, bu ay faturanız $9.99
[Temiz tasarım, logo doğru]
```

**Sahte E-posta:**
```
Gönderici: netflx-support@gmail.com (!)
Konu: ACİL! HESABINIZ BLOKLANDİ!!!
İçerik: hEmen tiklayin yoksa hESabinız kapanacak!!! (yazım hataları!)
[Link: http://netfliix-login-fake.com]
```

**Sosyal Mühendislik:**
- Gerçek vakalar
- Taktikleri tanıma
- Savunma yöntemleri

### 3. ETKİNLİK (35 dk)

**Aktivite 1: Phishing Dedektifleri (15 dk)**

**10 e-posta/mesaj gösterilir, gerçek mi sahte mi?**

**Örnek 1:**
"Sayın müşterimiz, kredi kartınız bloke edilmiştir. Aşağıdaki linke tıklayıp bilgilerinizi güncelleyin. Bankamız."

**Cevap:** SAHTE
- Genel hitap ("Sayın müşterimiz")
- Aciliyet
- Link istiyor

**Örnek 2:**
"Merhaba Ahmet, bu ay internet faturan 150 TL. Otomatik ödeme 25 Mayıs'ta çekilecek. Türk Telekom"

**Cevap:** GEREKLİ KONTROLBİLGİSİ (İsim var, detay var, ama yine de şüpheli link olup olmadığını kontrol et)

**Aktivite 2: Zararlı Yazılım Eşleştirme (10 dk)**

| Durum | Hangi Zararlı? |
|-------|----------------|
| Dosyalarım şifrelenmiş, para istiyorlar | Fidye Yazılımı |
| Sürekli reklam çıkıyor | Reklam Yazılımı |
| Şifrelerimi çalmışlar | Casus Yazılım |
| Bilgisayar çok yavaş, her yere bulaşmış | Virüs |
| "Bedava oyun" indirdim, şimdi kontrol edemiyorum | Truva Atı |

**Aktivite 3: Güvenlik Senaryoları (10 dk)**

Gruplar halinde durumları analiz et:

**Senaryo 1:**
"Bilinmeyen numaradan SMS: 'Hediye kazandınız! Linke tıklayın!'"
- Ne yapmalı?

**Cevap:** Tıklama! Sil, engelle.

**Senaryo 2:**
"E-posta: Netflix'ten gelmiş gibi, şifre güncellemesi istiyor."
- Gerçek mi?

**Cevap:** Muhtemelen sahte. Netflix asla e-postayla şifre istemez. Netflix.com'a kendin git, kontrol et.

### 4. KAPANIŞ (5 dk)

**Siber Güvenlik Kuralları:**
1. ❌ Şüpheli linke TIKLAMA
2. 🔒 Antivirüs kullan
3. 📧 E-postaları dikkatli kontrol et
4. 🔑 Şifreni kimseyle paylaşma
5. 🚫 Bilinmeyen kaynaklardan indirme

---

## 🏠 EV ÖDEVİ

**"Phishing Simülasyonu Raporu"**

**Görev:**
Ailenden birinin e-posta kutusunu kontrol et (izinle!)

**Adımlar:**
1. Spam/gereksiz klasörünü incele
2. 3 şüpheli e-posta bul
3. Her biri için analiz yap:
   - Gönderici kim?
   - Ne istiyor?
   - Şüpheli işaretler? (yazım hatası, aciliyet, link...)
   - Gerçek mi sahte mi?

**Rapor:**
Her e-posta için 1 paragraf analiz

**DİKKAT:** Şüpheli linklere TIKLAMA! Sadece gözlemle!

---

## 📊 ÖZ DEĞERLENDİRME

- ☐ Zararlı yazılım türlerini biliyorum
- ☐ Phishing'i tanıyabiliyorum
- ☐ Sosyal mühendislik taktiklerini fark edebiliyorum
- ☐ Şüpheli e-postaları ayırt edebiliyorum
- ☐ Siber tehditlerden korunabilirim

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Gerçekçi Örnekler:**
- Güncel phishing örnekleri kullanın (internetten bulabilirsiniz)
- Türkiye'den örnekler daha etkili

**Korkutmadan Bilinçlendirme:**
- Amaç korku değil, farkındalık
- "Dikkatli olursan güvendesin" mesajı

**Teknik Detay:**
- Fazla teknik girmeyin (SQL injection vb. sadece bahsedin)
- Pratik korunma yöntemlerine odaklanın

**Antivirüs:**
- Okul bilgisayarlarında antivirüs olmalı
- Ücretsiz seçenekler: Windows Defender, Avast Free

**Gerçek Vaka:**
Mümkünse Türkiye'den gerçek siber saldırı vakası paylaşın (haberlerden)

---

## 💡 MERAKLISINA

**Ünlü Siber Saldırılar:**

🐛 **ILOVEYOU Virüsü (2000):** 10 milyon bilgisayar etkilendi, $10 milyar zarar

🔐 **WannaCry (2017):** 150 ülkede 200,000+ bilgisayar, fidye yazılımı

🏥 **SolarWinds (2020):** Devlet kuruluşlarına saldırı

💰 **Fidye Rekorları:** Bazı şirketler milyonlarca dolar fidye ödedi

**İstatistik:**
Her gün 560,000 yeni zararlı yazılım tespit ediliyor!

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Güvenlik her şeyin temelidir."
> **- Mustafa Kemal Atatürk ruhu**

Atatürk güvenliğin önemini vurgulamıştır. Siber güvenlik de modern dünyanın güvenliğidir.

**Not:** Türkiye'nin siber güvenlik ekipleri var (USOM - Ulusal Siber Olaylara Müdahale Merkezi)

---

## 💎 DEĞERLER EĞİTİMİ

**Dikkat ve Özen:** Dijital dünyada dikkatli olmalıyız
**Eleştirel Düşünme:** Her şeye körü körüne inanmamalıyız
**Sorumluluk:** Güvenliğimizi sağlamak bizim sorumluluğumuz

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta **Siber Güvenlik Tehditleri** konusunu işledik. Çocuğunuz zararlı yazılımlar, phishing ve sosyal mühendislik hakkında bilgilendi.

**Ev Ödevi:**
E-posta kutusunda phishing örnekleri arama (ailenizin izniyle)

**UYARILAR:**
- Çocuğunuza asla e-postalardaki linklere tıklamamasını öğretin
- Bilinmeyen gönderenleri açmamalı
- Şüpheli SMS/e-posta gelirse size göstermeli

**Korunma:**
- Antivirüs kullanın (Windows Defender yeterli)
- Güncellemeleri yapın
- Bilinmeyen kaynaklardan dosya indirmeyin

**Acil Durum:**
Eğer çocuğunuz veya siz phishing'e maruz kaldıysanız:
1. Şifreleri hemen değiştirin
2. Bankayı arayın (kart bilgisi verilmişse)
3. Okulu bilgilendirin

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
