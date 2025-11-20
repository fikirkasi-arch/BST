# HAFTA 8: GÜVENLİ İNTERNET KULLANIMI
**Sınıf:** 6
**Ünite:** 2 - Etik ve Güvenlik
**Süre:** 2 Ders Saati (80 dakika)
**Konu:** Güçlü Şifre, İki Faktörlü Doğrulama, Güvenli Tarayıcı, VPN

---

## 🎯 ÖĞRENME KAZANIMLARI

- Güçlü şifre oluşturur
- İki faktörlü doğrulamayı kullanır
- Güvenli web sitelerini tanır (HTTPS)
- Açık Wi-Fi risklerini bilir
- Güvenli internet alışkanlıkları edinir

---

## 📚 KONU ÖZETİ

### Güçlü Şifre

**Zayıf Şifre:**
- 123456
- password
- Adınız
- Doğum tarihiniz
- qwerty

**Güçlü Şifre Kuralları:**
1. **Uzunluk:** En az 12 karakter
2. **Karmaşıklık:**
   - Büyük harf (A-Z)
   - Küçük harf (a-z)
   - Rakam (0-9)
   - Sembol (!@#$%^&*)
3. **Benzersizlik:** Her site için farklı şifre
4. **Tahmin Edilemezlik:** Kelime yok, rastgele

**Örnekler:**
- ❌ Zayıf: ahmet2010
- ✅ Güçlü: Aj#9mK2!pL7x

**Şifre Oluşturma Teknikleri:**

**1. Cümle Yöntemi:**
"Benim en sevdiğim renk mavidir 2024"
→ BeSeReM!2024

**2. Rastgele:**
Şifre yöneticisi kullan (LastPass, 1Password)

**Şifre Yöneticisi:**
- Tüm şifreleri saklar
- Otomatik güçlü şifre üretir
- Tek ana şifre (çok güçlü olmalı!)

### İki Faktörlü Doğrulama (2FA)

**Tanım:** Şifre + ikinci bir doğrulama

**Nasıl Çalışır:**
1. Şifreni gir
2. Telefonuna kod gelir (SMS/Uygulama)
3. Kodu gir
4. Giriş başarılı

**Türleri:**
- **SMS:** Telefona kod
- **Authenticator App:** Google Authenticator, Microsoft Authenticator
- **Biyometrik:** Parmak izi, yüz tanıma
- **Donanım:** Fiziksel anahtar (YubiKey)

**Neden Önemli:**
Şifren çalınsa bile, telefon olmadan giremezler!

### HTTPS ve Güvenli Web

**HTTP vs HTTPS:**
- **HTTP:** Güvensiz (şifrelenmemiş)
- **HTTPS:** Güvenli (şifrelenmiş) 🔒

**Nasıl Anlaşılır:**
- Adres çubuğunda kilit simgesi 🔒
- URL: https://...

**Güvenli Site Özellikleri:**
- ✅ HTTPS
- ✅ Kilit simgesi
- ✅ Tanınmış site
- ❌ "Güvenli değil" uyarısı

**SSL Sertifikası:**
HTTPS'in çalışması için gerekli

### Açık Wi-Fi Riskleri

**Tehlikeler:**
1. **Ortadaki Adam:** Verilerinizi görebilirler
2. **Sahte Hotspot:** "Starbucks WiFi" gibi sahte ağ
3. **Şifresiz Ağ:** Herkes görebilir

**Korunma:**
- Açık Wi-Fi'da bankacılık yapma
- VPN kullan
- HTTPS sitelerinde gezin
- Otomatik bağlanma kapat

### VPN (Virtual Private Network)

**Tanım:** İnterneti şifreleyerek güvenli hale getirir

**Nasıl Çalışır:**
Bilgisayar → VPN Sunucu (şifreli) → İnternet

**Faydaları:**
- Verilerinizi şifreler
- IP adresinizi gizler
- Konum değiştirme

**Ücretsiz/Ücretli:**
- Ücretsiz: ProtonVPN, Windscribe (sınırlı)
- Ücretli: NordVPN, ExpressVPN

**Not:** Okul ağında VPN kullanımı için izin gerekebilir

---

## 📖 DERS AKIŞI (80 DAKİKA)

### 1. GİRİŞ (10 dk)

**Test:**
"Şifreniz ne kadar güçlü?"

Öğrenciler (gerçek şifrelerini değil!) örnek bir şifre düşünür:
- ahmet123 → Zayıf (4/10)
- Ahmet!2024 → Orta (7/10)
- Aj#9mK2!pL → Güçlü (10/10)

**Online Tool (Projeksiyon):**
https://howsecureismypassword.net (İngilizce ama görsel)

### 2. KONU ANLATIMI (30 dk)

**Güçlü Şifre:**
- Kurallar
- Örnekler
- Şifre yöneticisi tanıtımı

**İki Faktörlü Doğrulama:**
- Gösterim: Öğretmen Google hesabında 2FA aktifleştir (projeksiyon)
- Adım adım nasıl yapılır
- Authenticator uygulaması gösterimi

**HTTPS:**
- Tarayıcıda örnekler
- Güvenli vs güvensiz site
- Sertifika kontrolü

**Açık Wi-Fi:**
- Riskler
- Gerçek vaka örnekleri
- Korunma yöntemleri

**VPN:**
- Basit animasyon/diyagram
- Ne işe yarar
- Kullanım örneği (varsa)

### 3. UYGULAMALI ETKİNLİK (35 dk)

**Aktivite 1: Şifre Oluşturma Atölyesi (15 dk)**

**Görev:** Her öğrenci 3 güçlü şifre oluştursun (hayali hesaplar için)

**Yöntemler:**
1. Cümle yöntemi: "Annem bugün 5 elma aldı!" → AbU5eA!
2. Rastgele (zarla): Harf + sayı + sembol
3. Şifre yöneticisi simülasyonu

**Kontrol:** Öğretmen kontrol eder (güçlü mü?)

**Aktivite 2: HTTPS Dedektifleri (10 dk)**

**10 web sitesi gösterilir (projeksiyon), güvenli mi?**

| Site | HTTPS? | Güvenli mi? |
|------|---------|-------------|
| https://google.com | ✅ | Evet |
| http://bankaornek.com | ❌ | Hayır! |
| https://youtube.com | ✅ | Evet |
| http://sahtesite.tk | ❌ | Hayır! |

**Aktivite 3: Güvenlik Senaryoları (10 dk)**

**Senaryo 1:**
"Cafe'de açık WiFi var. Bankacılık yapmalı mıyım?"
- Cevap: Hayır! Evde yap veya VPN kullan.

**Senaryo 2:**
"E-posta şifremi heryerde aynı kullanıyorum. Sorun var mı?"
- Cevap: EVET! Büyük risk. Her site için farklı şifre.

**Senaryo 3:**
"Bir site 2FA istiyor. Zahmetli, atlayayım mı?"
- Cevap: Hayır! 2FA ekstra güvenlik, aktifleştir.

### 4. KAPANIŞ (5 dk)

**Güvenli İnternet Taahhütü:**

"Ben, [İsim], bundan sonra:
- ✅ Güçlü şifreler kullanacağım
- ✅ Her site için farklı şifre yapacağım
- ✅ 2FA aktifleştirecek
- ✅ HTTPS kontrolü yapacağım
- ✅ Açık WiFi'da dikkatli olacağım"

---

## 🏠 EV ÖDEVİ

**"Dijital Güvenlik Yükseltmesi"**

**Görev:**
Ailenle birlikte güvenlik yükseltmesi yap

**Adımlar:**

**1. Şifre Kontrolü:**
- Kaç farklı şifre kullanıyorsun?
- Güçlü mü zayıf mı?
- Ailenle birlikte yeni güçlü şifreler oluştur

**2. İki Faktörlü Doğrulama:**
- Hangi hesaplarında 2FA var?
- Ailenle birlikte en az 1 hesapta (Google, Instagram...) 2FA aktifleştirin

**Adım adım:**
- Ayarlar → Güvenlik → 2FA/İki Adımlı Doğrulama
- Telefon numarası ekle
- Doğrulama kodu al
- Aktif!

**3. HTTPS Kontrolü:**
- 5 sık kullandığın siteyi kontrol et
- HTTPS mi?

**Rapor:**
- Kaç şifre değiştirdin?
- 2FA aktifleştirdin mi? Hangi hesapta?
- HTTPS olmayan site buldun mu?

---

## 📊 ÖZ DEĞERLENDİRME

- ☐ Güçlü şifre oluşturabiliyorum
- ☐ 2FA'nın ne olduğunu biliyorum
- ☐ HTTPS'i tanıyabiliyorum
- ☐ Açık Wi-Fi risklerini biliyorum
- ☐ Güvenli internet kullanabilirim

---

## 🎓 CAN ALICI HUSUSLAR

**Öğretmen İçin:**

**Şifre Güvenliği:**
- Öğrencilerin GERÇEK şifrelerini paylaşmasını istemeyin
- Sadece örnek şifreler

**2FA Gösterimi:**
- Kendi hesabınızda gösterin (kişisel bilgiler gizli)
- Adım adım anlatın

**VPN:**
- Karmaşık gelebilir, basit tutun
- "Şifreleme tüneli" benzetmesi

**Pratik Uygulama:**
- Mümkünse bilgisayar lab'ında:
  - 2FA aktifleştirme (Google hesap)
  - HTTPS kontrol

**Veli İletişimi:**
- Ev ödevi aile katılımlı
- Velilere de faydalı olacak

---

## 💡 MERAKLISINA

**Şifre İstatistikleri:**

🔑 **En Yaygın Şifre:** 123456 (milyonlarca kişi!)

⏱️ **Kırılma Süresi:**
- 123456 → 1 saniyeden az
- Ahmet123 → Birkaç saat
- Aj#9mK2!pL7x → Milyonlarca yıl!

📊 **Veri İhlalleri:**
2021'de 22 milyar şifre sızdı!

🔐 **2FA Etkisi:**
2FA kullanıldığında hesap hırsızlığı %99.9 azalıyor!

---

## 🇹🇷 ATATÜRKÇÜLÜK

> "Güvenlik temelsiz olmaz, temelli olmalıdır."
> **- Mustafa Kemal Atatürk**

Atatürk, güvenliğin temel olduğunu vurgulamıştır. Dijital güvenlik de modern çağın temelidir.

---

## 💎 DEĞERLER EĞİTİMİ

**Sorumluluk:** Kendi güvenliğimizi sağlamak bizim sorumluluğumuz
**Özen:** Şifrelerde dikkatli olmalıyız
**Öğrenme:** Sürekli yeni güvenlik yöntemlerini öğrenmeliyiz

---

## 📞 VELİ BİLGİLENDİRME

**Sayın Velimiz,**

Bu hafta **Güvenli İnternet Kullanımı** konusunu işledik. Çocuğunuz şifre güvenliği, 2FA ve HTTPS öğrendi.

**ÖNEMLİ EV ÖDEVİ:**
Ailecek yapılacak güvenlik yükseltmesi. Lütfen çocuğunuza yardımcı olun:

**1. Şifre Kontrolü:**
- Aile içi şifreleri kontrol edin
- Zayıf şifreler güçlendirilsin
- Her hesap için farklı şifre

**2. İki Faktörlü Doğrulama (2FA):**
- En az 1 önemli hesapta 2FA aktifleştirin (Google, banka, sosyal medya)
- Nasıl yapılır: Ayarlar → Güvenlik → 2FA
- Telefon numaranızı ekleyin

**TAVSİYE:**
- Şifre yöneticisi kullanabilirsiniz (LastPass, 1Password - ücretsiz seçenekler var)
- Banka/mail gibi kritik hesaplarda mutlaka 2FA
- Çocuğunuzun şifrelerini bilmeniz güvenlik için iyi olabilir (yaşa göre)

**AÇIK Wİ-Fİ:**
- Cafe, AVM gibi yerlerde açık WiFi'da bankacılık/alışveriş yapmayın
- Gerekirse VPN kullanın (ProtonVPN ücretsiz)

---

**Hazırlayan:** Bilişim Teknolojileri Öğretmeni
**Tarih:** 2025-2026
**Sürüm:** 1.0
