# BST Eğitim Portalı - Proje Tanıtımı (AI için)

## 📋 Proje Özeti

**Proje Adı:** Bilişim Teknolojileri Eğitim Portalı
**Hedef Kitle:** 5. ve 6. Sınıf öğrencileri
**Eğitim Yılı:** 2025-2026
**Teknoloji Stack:** HTML, CSS, Vanilla JavaScript, LocalStorage, Chart.js
**Durum:** Aktif geliştirme aşamasında

---

## 🎯 Projenin Amacı

Türkiye Milli Eğitim Bakanlığı müfredatına uygun, 5. ve 6. sınıf öğrencileri için kapsamlı bir dijital eğitim platformu. Öğrencilerin bilişim teknolojileri dersini eğlenceli, interaktif ve etkili bir şekilde öğrenmelerini sağlamak.

---

## 📚 Müfredat Yapısı

### **5. Sınıf (36 Hafta - 6 Ünite)**
1. **Bilişim Temelleri** (9 hafta)
   - Donanım, yazılım, işletim sistemleri
   - Dosya ve klasör yönetimi
   - Veri birimleri (bit, byte, KB, MB, GB)

2. **Dijital Ürün Tasarımı** (6 hafta)
   - Microsoft Word (belge hazırlama)
   - Paint (dijital çizim)
   - PowerPoint (sunum hazırlama)

3. **Ağlar ve İletişim** (3 hafta)
   - İnternet ve ağ kavramları (LAN, WAN)
   - E-posta ve dijital iletişim
   - İşbirliği araçları (Google Docs, Zoom)

4. **Etik ve Güvenlik** (2 hafta)
   - Dijital etik ve siber zorbalık
   - Şifre güvenliği
   - Kişisel bilgi koruması

5. **Yapay Zeka** (4 hafta)
   - Yapay zeka kavramı
   - Kullanım alanları
   - Avantajlar ve dezavantajlar

6. **Scratch Programlama** (14 hafta)
   - Blok tabanlı programlama
   - Döngüler, koşullar, değişkenler
   - Oyun ve animasyon projesi oluşturma

### **6. Sınıf (31 Hafta - 5 Ünite)**
1. **Bilişim Teknolojileri** (4 hafta)
   - Bilişim tarihçesi
   - İkili sayı sistemi (bit, byte)
   - Güncel teknolojiler (IoT, AR, bulut)

2. **Etik ve Güvenlik** (5 hafta)
   - KVKK (Kişisel Verilerin Korunması Kanunu)
   - Phishing ve siber saldırılar
   - İki faktörlü kimlik doğrulama (2FA)

3. **İletişim ve İşbirliği** (2 hafta)
   - Bulut tabanlı işbirliği
   - Video konferans araçları
   - Ortak belge hazırlama

4. **Ürün Oluşturma** (7 hafta)
   - Grafik tasarım (Canva, GIMP)
   - Video düzenleme
   - Animasyon ve podcast

5. **Problem Çözme ve Programlama** (21 hafta)
   - Algoritmik düşünme
   - Python programlamaya giriş
   - Koşullar, döngüler, listeler

---

## 🗂️ Proje Dosya Yapısı

```
BST/
│
├── index.html                          # Ana sayfa (tüm ünitelerin hub'ı)
│
├── sozluk.html                         # Bilişim Sözlüğü (100+ terim, videolar)
├── flashcards.html                     # Hafıza kartları (çalışma sistemi)
│
├── quiz-5-unite1.html                  # 5. Sınıf Ünite 1 Quiz (10 soru)
├── quiz-5-unite2.html                  # 5. Sınıf Ünite 2 Quiz (10 soru)
├── quiz-6-unite2.html                  # 6. Sınıf Ünite 2 Quiz (10 soru)
├── [... 10 quiz dosyası daha]
│
├── student-dashboard.html              # Öğrenci paneli (ilerleme, istatistikler)
├── leaderboard.html                    # Lider tablosu (sıralama sistemi)
├── badges.html                         # Rozet koleksiyonu (17 başarı rozeti)
├── games-hub.html                      # Oyun merkezi (11 eğitici oyun)
├── video-library.html                  # Video kütüphanesi
├── progress-report.html                # İlerleme raporu
├── exam-creator.html                   # Sınav oluşturucu (öğretmen aracı)
│
├── oyunlar/                            # 11 eğitici oyun
│   ├── 5sinif-unite1-donanimoyunu.html
│   ├── 5sinif-unite1-bilisimquiz.html
│   ├── 5sinif-unite2-harfavi.html
│   ├── 5sinif-unite2-officequiz.html
│   ├── 5sinif-unite2-wordexcelmatch.html
│   ├── 5sinif-unite3-wordsimulation.html
│   ├── 6sinif-unite1-programmingquiz.html
│   ├── 6sinif-unite1-algoritmapuzzle.html
│   ├── 6sinif-unite2-scratchproject.html
│   ├── 6sinif-unite2-codeblocks.html
│   └── 6sinif-unite3-internetquiz.html
│
├── scripts/                            # JavaScript modülleri
│   ├── storage.js                      # LocalStorage yönetimi (veri kalıcılığı)
│   ├── analytics.js                    # Kullanıcı istatistikleri ve takip
│   ├── badge-system.js                 # Rozet/başarı sistemi (17 rozet)
│   ├── quiz-engine.js                  # Ortak quiz motoru
│   ├── search.js                       # Global arama (Ctrl+K)
│   ├── dark-mode.js                    # Dark mode toggle ve CSS
│   └── daily-challenges.js             # Günlük görev sistemi (7 görev türü)
│
└── sunumlar/                           # PowerPoint sunumları (her ünite için)
```

---

## ⚙️ Sistem Mimarisi

### **Frontend Teknolojileri**
- **HTML5** - Semantik ve erişilebilir yapı
- **CSS3** - Gradient tasarımlar, animasyonlar, responsive
- **Vanilla JavaScript** - Modüler yapı, ES6+
- **Chart.js 4.4.0** - Veri görselleştirme (grafikler)

### **Veri Yönetimi**
- **LocalStorage API** - Tüm kullanıcı verisi client-side
  - Quiz sonuçları
  - Rozet durumları
  - Streak takibi
  - Daily challenges
  - Kullanıcı tercihleri (dark mode)
  - Analytics verileri

### **Modüler Yapı**
```javascript
// Her modül namespace pattern kullanıyor
const BSTStorage = { /* veri yönetimi */ }
const BSTAnalytics = { /* takip ve analiz */ }
const BadgeSystem = { /* rozet sistemi */ }
const QuizEngine = { /* quiz motoru */ }
const BSTSearch = { /* arama motoru */ }
const DarkMode = { /* tema yönetimi */ }
const DailyChallenges = { /* görev sistemi */ }
```

---

## 🎮 Temel Özellikler

### **1. Quiz Sistemi** 📝
- **Quiz Engine:** Ortak motor, tüm quizler için
- **Özellikler:**
  - İlerleme çubuğu (Soru X/Y)
  - Animasyonlu cevap kontrolü
  - Sonuç ekranı (emoji, puan, yüzde)
  - LocalStorage'a otomatik kayıt
  - Badge tetikleme
  - Analytics entegrasyonu
- **Toplam:** 13 quiz (5. ve 6. sınıf için)

### **2. Oyun Sistemi** 🎮
- **11 Eğitici Oyun:**
  - Donanım Eşleştirme
  - Bilişim Quiz
  - Harf Avı
  - Office Quiz
  - Word-Excel Eşleştirme
  - Word Simülasyonu
  - Programlama Quiz
  - Algoritma Bulmaca
  - Scratch Projesi
  - Kod Blokları
  - İnternet Güvenliği Quiz

### **3. Bilişim Sözlüğü** 📖
- **100+ Terim:**
  - Türkçe ve İngilizce
  - Detaylı açıklamalar
  - İlgili YouTube video linkleri
  - Kategorilere göre filtreleme
  - Arama özelliği
  - Telaffuz bilgisi

### **4. Flashcards** 🗂️
- Çalışma kartları
- İki yönlü çevirme (TR ↔ EN)
- İlerleme takibi
- Rastgele sıralama

### **5. Rozet Sistemi** 🏆
- **17 Farklı Rozet:**
  1. 🌟 İlk Adım - İlk quiz'i tamamla
  2. 💯 Mükemmel - %100 puan al
  3. 🔥 Ateşli - 7 gün streak
  4. 💪 Kararlı - 30 gün streak
  5. 🎮 Oyun Ustası - 10 oyun oyna
  6. 📚 Kitap Kurdu - 50 quiz tamamla
  7. 🏆 Şampiyon - Tüm quizlerde %90+
  8. ⚡ Hız Rekoru - Quiz'i 2 dakikada bitir
  9. 🎯 Hedef Odaklı - 5 günlük streak
  10. 🌍 Kaşif - Tüm sayfaları ziyaret et
  11. 💎 Elmas - 1000 puan kazan
  12. 🔮 Bilge - Sözlükte 50 kelime ara
  13. 🎨 Yaratıcı - 5 flashcard çalış
  14. 🚀 Roket - Tüm üniteleri tamamla
  15. 🎓 Bilgin - 100 quiz tamamla
  16. 🌟 Süper Yıldız - 10000 puan kazan
  17. 👑 Kral - Tüm rozetleri kazan

- **Özellikler:**
  - Otomatik kazanma (event-driven)
  - Animasyonlu bildirimler (popup)
  - Kilitli/açık rozetler
  - İlerleme gösterimi

### **6. Dashboard** 📊
- **İstatistik Kartları:**
  - Tamamlanan quizler
  - Oynanan oyunlar
  - Ortalama başarı
  - Kazanılan rozetler
  - Streak günleri
  - Toplam puan

- **Grafikler (Chart.js):**
  - Haftalık aktivite (line chart)
  - Quiz performansı (bar chart)

- **Ünite İlerlemesi:**
  - 6 ünite için progress bar
  - Yüzdelik gösterim

- **Günlük Görevler Widget:**
  - 3 günlük görev
  - İlerleme takibi
  - Ödül alma sistemi

### **7. Daily Challenges** 🎯
- **7 Görev Türü:**
  - 📝 3 Quiz Tamamla (+50 puan)
  - 💯 Mükemmel Skor (+100 puan)
  - 🎮 5 Oyun Oyna (+30 puan)
  - 🗂️ 20 Flashcard Çalış (+40 puan)
  - ⏱️ 30 Dakika Çalış (+60 puan)
  - 📖 Sözlük Ziyareti (+20 puan)
  - 🔥 Streak Devam (+25 puan)

- **Özellikler:**
  - Her gün 3 rastgele görev
  - Otomatik ilerleme takibi
  - Ödül alma sistemi
  - Animasyonlu bildirimler
  - Analytics entegrasyonu

### **8. Analytics Sistemi** 📈
- **Takip Edilen Metrikler:**
  - Sayfa görüntüleme
  - Quiz tamamlama
  - Oyun oynama
  - Flashcard çalışma
  - Arama sorguları
  - Harcanan süre

- **Raporlama:**
  - Haftalık aktivite özeti
  - Popüler sayfalar
  - Günlük aktivite dağılımı
  - Tahmini çalışma süresi

### **9. Dark Mode** 🌙
- Toggle butonu (header)
- Klavye kısayolu (Ctrl+Shift+D)
- LocalStorage'da tercih
- Smooth transitions
- Tüm renkler için dark theme

### **10. Global Arama** 🔍
- **Özellikler:**
  - Klavye kısayolu (Ctrl+K)
  - Modal popup
  - Tüm içerikte arama (quiz, oyun, sayfa)
  - İlgililik skoru
  - Kategori etiketleri
  - Türkçe karakter desteği

- **Arama Kapsamı:**
  - 13 quiz
  - 11 oyun
  - 9 sayfa
  - Anahtar kelimeler

---

## 💾 LocalStorage Veri Yapısı

```javascript
// bstUserData
{
  completedQuizzes: 5,           // Tamamlanan quiz sayısı
  playedGames: 12,               // Oynanan oyun sayısı
  avgScore: 85,                  // Ortalama başarı yüzdesi
  earnedBadges: 7,               // Kazanılan rozet sayısı
  streakDays: 15,                // Üst üste gün sayısı
  totalPoints: 1250,             // Toplam puan
  lastVisit: "2025-01-15",       // Son ziyaret tarihi

  quizScores: [                  // Quiz sonuçları
    { name: "5. Sınıf Ünite 1", score: 8, total: 10, date: "2025-01-10" },
    { name: "6. Sınıf Ünite 2", score: 9, total: 10, date: "2025-01-12" }
  ],

  badges: [                      // Kazanılan rozetler
    "first-quiz",
    "perfect-score",
    "week-streak"
  ],

  unitProgress: {                // Ünite ilerlemeleri
    "5-unite-1": 100,
    "5-unite-2": 85,
    "6-unite-1": 60
  }
}

// bstAnalytics
{
  activities: [                  // Tüm aktiviteler
    { type: "quiz_completed", timestamp: "2025-01-10T10:30:00Z", details: {...} },
    { type: "page_view", timestamp: "2025-01-10T10:25:00Z", details: {...} }
  ],
  pageViews: {                   // Sayfa görüntüleme sayıları
    "Ana Sayfa": 45,
    "Sözlük": 23,
    "Quiz": 18
  }
}

// dailyChallenges
{
  date: "Mon Jan 15 2025",       // Günün tarihi
  challenges: [                  // Günün görevleri
    {
      id: "quiz-3",
      title: "3 Quiz Tamamla",
      progress: 2,
      target: 3,
      completed: false,
      claimed: false,
      reward: 50
    }
  ]
}

// darkMode
"enabled" veya "disabled"
```

---

## 🎨 Tasarım Sistemi

### **Renk Paleti**
```css
/* Primary Gradients */
--gradient-purple: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--gradient-pink: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
--gradient-orange: linear-gradient(135deg, #fccb90 0%, #d57eeb 100%);
--gradient-blue: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
--gradient-green: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);

/* Dark Mode */
--dark-bg: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
--dark-container: #0f3460;
--dark-accent: #bb86fc;
--dark-text: #e0e0e0;
```

### **Tipografi**
- **Font:** Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Başlıklar:** 2em - 2.5em, bold
- **Metin:** 1em - 1.2em, normal
- **Küçük Metin:** 0.8em - 0.9em

### **Spacing**
- **Card Padding:** 20px - 40px
- **Gap:** 15px - 30px
- **Border Radius:** 10px - 20px
- **Box Shadow:** 0 10px 30px rgba(0,0,0,0.2)

### **Animasyonlar**
```css
/* Hover Effects */
transform: translateY(-5px);
transition: all 0.3s ease;

/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

---

## 🔧 Geliştirme Detayları

### **Kod Standartları**
- ES6+ JavaScript
- Modüler mimari (namespace pattern)
- Event-driven architecture
- DRY (Don't Repeat Yourself) prensipleri
- Semantic HTML5
- BEM benzeri CSS sınıflandırma

### **Performance Optimizasyonu**
- Lazy loading (gerektiğinde yükleme)
- LocalStorage için efficient data structure
- Debouncing (arama için)
- CSS animations (JS yerine)
- Minimal external dependencies

### **Responsive Tasarım**
```css
/* Mobile First Approach */
@media (max-width: 768px) {
  /* Tablet/Mobile adaptasyonları */
  .tabs { flex-wrap: wrap; }
  .unit-grid { grid-template-columns: 1fr; }
  .header-nav { flex-direction: column; }
}
```

### **Erişilebilirlik**
- Semantic HTML (header, nav, main, section)
- ARIA labels
- Keyboard navigation support
- High contrast colors
- Alt text for images
- Focus indicators

---

## 📈 Kullanım İstatistikleri

### **İçerik Miktarı**
- **13 Quiz** (toplam 130+ soru)
- **11 Oyun** (farklı kategorilerde)
- **100+ Sözlük Terimi** (video linklerle)
- **17 Rozet** (başarı sistemi)
- **7 Günlük Görev Türü**
- **6 Ünite (5. Sınıf)** + **5 Ünite (6. Sınıf)**

### **Kod İstatistikleri**
- **Toplam Satır:** ~5,000+ satır
- **HTML Dosyaları:** 20+
- **JavaScript Modülleri:** 7
- **CSS:** Inline + embedded (~2,000 satır)

---

## 🚀 Gelecek Geliştirmeler

### **Öncelikli (Kısa Vadeli)**
1. ✅ Navigation iyileştirmesi (TAMAMLANDI)
2. ✅ Quiz Engine entegrasyonu (TAMAMLANDI)
3. ✅ Dark Mode (TAMAMLANDI)
4. ✅ Daily Challenges (TAMAMLANDI)
5. ✅ Chart.js visualizations (TAMAMLANDI)

### **Planlananlar (Orta Vadeli)**
- PWA (Progressive Web App) desteği
- Offline çalışma
- Profile/Avatar sistemi
- Study Timer (Pomodoro)
- Export/Share features (PDF rapor)
- Bookmarks/Favorites
- Note-taking system
- Smart Recommendations (AI tabanlı)

### **İleri Seviye (Uzun Vadeli)**
- Backend entegrasyonu (Node.js + MongoDB)
- Gerçek zamanlı multiplayer quiz
- AI Study Assistant (Chatbot)
- Teacher Dashboard (sınıf yönetimi)
- Video chat/tutoring
- Community features (yorum, rating)
- Mobile app (React Native)

---

## 🔐 Güvenlik ve Gizlilik

### **Veri Güvenliği**
- Tüm veri client-side (LocalStorage)
- Şu an backend yok, bu yüzden sunucu güvenliği sorunu yok
- KVKK uyumu (kişisel veri toplamıyoruz)

### **Planlanan Güvenlik (Backend geldiğinde)**
- JWT authentication
- HTTPS zorunlu
- Password hashing (bcrypt)
- Input validation & sanitization
- Rate limiting
- CORS policy

---

## 📱 Responsive Breakpoints

```css
/* Mobile (320px - 767px) */
@media (max-width: 767px) {
  /* Single column layout */
  /* Stack navigation */
  /* Larger touch targets */
}

/* Tablet (768px - 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
  /* 2 column grid */
  /* Side navigation */
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  /* 3+ column grid */
  /* Full navigation */
  /* Hover effects */
}
```

---

## 🎓 Pedagojik Yaklaşım

### **Öğrenme Metodolojisi**
1. **Gamification** - Oyunlaştırma yoluyla motivasyon
2. **Spaced Repetition** - Flashcards ile aralıklı tekrar
3. **Immediate Feedback** - Quiz'lerde anında geri bildirim
4. **Progress Tracking** - İlerleme görselleştirme
5. **Micro-learning** - Küçük parçalarda öğrenme
6. **Self-paced** - Kendi hızında ilerleme

### **Bloom Taksonomisi Entegrasyonu**
- **Hatırlama:** Quiz ve flashcards
- **Anlama:** Sözlük ve video içerikler
- **Uygulama:** Oyunlar ve simülasyonlar
- **Analiz:** Problem çözme aktiviteleri
- **Sentez:** Proje oluşturma (Scratch, Python)
- **Değerlendirme:** Peer assessment (planlanan)

---

## 🐛 Bilinen Sınırlamalar

### **Şu Anki Sınırlar**
1. **Backend yok** - Tüm veri LocalStorage'da (tarayıcı silinirse kaybolur)
2. **Multiplayer yok** - Gerçek zamanlı yarışma yok
3. **AI yok** - Kişiselleştirilmiş öneriler sınırlı
4. **Teacher dashboard sınırlı** - Sadece exam creator var
5. **Video content sınırlı** - Embed YouTube videoları var ama kendi videolarımız yok

### **Tarayıcı Uyumluluğu**
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ⚠️ IE 11 (desteklenmiyor)

---

## 📞 Destek ve Dokümantasyon

### **Dokümantasyon Dosyaları**
- `projetanitimi-ai.md` - Bu dosya (AI'lar için)
- `kullanici-rehberi.md` - Kullanıcılar için rehber
- `README.md` - GitHub açıklaması (varsa)

### **Kod İçi Dokümantasyon**
```javascript
// Her modül JSDoc tarzı yorumlarla
/**
 * Quiz sonucunu kaydeder ve badge kontrolü yapar
 * @param {string} quizName - Quiz adı
 * @param {number} score - Doğru cevap sayısı
 * @param {number} totalQuestions - Toplam soru sayısı
 */
```

---

## 🌟 Benzersiz Özellikler

### **Bu Projeyi Özel Kılan Şeyler**
1. **Türkçe İçerik** - MEB müfredatına uygun
2. **Gamification** - Rozet, puan, streak sistemi
3. **Dark Mode** - Göz sağlığı
4. **Daily Challenges** - Günlük motivasyon
5. **Analytics** - Detaylı ilerleme takibi
6. **100% Client-Side** - Backend gerektirmez
7. **Modüler Mimari** - Kolay genişletilebilir
8. **Responsive** - Her cihazda çalışır

---

## 🎯 Hedef Kitle Profili

### **Öğrenciler (5-6. Sınıf)**
- **Yaş:** 10-12 yaş
- **Seviye:** Ortaokul başlangıç
- **Bilgisayar Becerisi:** Başlangıç - Orta
- **İhtiyaçlar:**
  - Eğlenceli öğrenme
  - Anında geri bildirim
  - Motivasyon (rozetler, puanlar)
  - Görsel içerik

### **Öğretmenler**
- **İhtiyaçlar:**
  - Ders materyalleri
  - Sınav oluşturma
  - Öğrenci takibi (planlanan)
  - Hazır sunumlar

### **Veliler**
- **İhtiyaçlar:**
  - Çocuk ilerlemesini takip
  - Güvenli içerik
  - Offline çalışabilme (planlanan)

---

## 💡 Kullanım Senaryoları

### **Senaryo 1: Sınıfta Ders**
1. Öğretmen sunumu açar (PowerPoint)
2. Öğrenciler bilgisayarda takip eder
3. Ders sonunda quiz çözerler
4. Sonuçlar otomatik kaydedilir

### **Senaryo 2: Evde Ödevi**
1. Öğrenci dashboard'unu kontrol eder
2. Günlük görevleri görür
3. Eksik quizleri tamamlar
4. Sözlükte terim araştırır
5. Flashcard ile tekrar yapar

### **Senaryo 3: Oyunla Öğrenme**
1. Öğrenci oyun merkezine gider
2. "Donanım Eşleştirme" oyununu oynar
3. Puan kazanır
4. Rozet açılır (bildirim gelir)
5. Lider tablosunda yükselir

---

## 🔄 Güncellemeler ve Versiyon Geçmişi

### **v2.0.0** (Şubat 2025)
- ✅ Navigation iyileştirmesi
- ✅ Quiz Engine entegrasyonu
- ✅ Dark Mode
- ✅ Daily Challenges
- ✅ Chart.js visualizations

### **v1.5.0** (Ocak 2025)
- ✅ Games tab eklendi
- ✅ Student dashboard
- ✅ Badge system (17 rozet)
- ✅ Video library
- ✅ Progress report
- ✅ Exam creator

### **v1.0.0** (Aralık 2024)
- ✅ Quiz improvements
- ✅ Flashcards
- ✅ 6. sınıf ünite 2 quiz

### **v0.5.0** (Kasım 2024)
- ✅ Sözlük genişletmesi (100+ terim)
- ✅ Video linkleri
- ✅ Quiz games

---

## 🏆 En İyi Pratikler

### **Bu Projede Uygulanan**
1. **Modüler JavaScript** - Her modül bağımsız
2. **Semantic HTML** - SEO ve erişilebilirlik
3. **Mobile-First CSS** - Responsive tasarım
4. **Progressive Enhancement** - Temel özellikler herkeste çalışır
5. **LocalStorage Best Practices** - JSON serialization, default values
6. **Event Delegation** - Performans optimizasyonu
7. **Consistent Naming** - Okunabilir kod

---

## 📊 Metrikler ve KPI'lar

### **Ölçülebilir Hedefler**
- **Kullanıcı Bağlılığı:** Ortalama 15 dakika+ oturum
- **Quiz Tamamlama:** %80+ tamamlanma oranı
- **Rozet Kazanma:** Kullanıcı başına ortalama 5+ rozet
- **Daily Active Users:** Hedef %30+ retention
- **Quiz Başarı:** Ortalama %70+ doğru cevap

---

## 🎨 Stil Rehberi

### **UI Components**
- **Butonlar:** Gradient, rounded (12px), shadow
- **Kartlar:** White bg, rounded (20px), shadow
- **Modal:** Center, overlay, fade in
- **Notification:** Top-right/center, slide in, auto-close
- **Progress Bar:** Gradient fill, percentage text

### **İkonlar**
- Emoji kullanımı (evrensel ve renkli)
- Font-size: 1.5em - 4em
- Meaning-based (📝 quiz, 🎮 oyun, 🏆 rozet)

---

## 🔍 SEO ve Erişilebilirlik

### **SEO Optimizasyonu**
```html
<title>Bilişim Teknolojileri Eğitim Portalı - 5. ve 6. Sınıf</title>
<meta name="description" content="MEB müfredatına uygun...">
<meta name="keywords" content="bilişim, teknoloji, eğitim, 5. sınıf, 6. sınıf">
```

### **Accessibility (A11y)**
- Semantic tags (nav, main, article, section)
- Alt text for all images/icons
- Keyboard navigation (Tab, Enter, Esc)
- Focus indicators (:focus styles)
- ARIA labels (aria-label, aria-labelledby)
- Color contrast ratio (WCAG AA)

---

## 🚦 Test Stratejisi

### **Manuel Testing**
- ✅ Browser compatibility
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ LocalStorage operations
- ✅ Feature integration (quiz → badge → analytics)
- ✅ Dark mode transitions

### **Automated Testing (Planlanan)**
- Unit tests (Jest)
- Integration tests
- E2E tests (Cypress)
- Performance tests (Lighthouse)

---

## 📦 Deployment

### **Şu Anki Durum**
- Static HTML files
- GitHub Pages'de host edilebilir
- Herhangi bir static hosting'de çalışır
- Backend gerektirmez

### **Gelecek Deployment**
```bash
# Build process (planlanan)
npm run build
npm run deploy

# Environments
- Development: localhost
- Staging: test.bst-edu.com
- Production: bst-edu.com
```

---

## 🤝 Katkıda Bulunma

### **Nasıl Katkı Yapılır**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### **Kod İnceleme Kriterleri**
- Kod standartlarına uygunluk
- Mevcut özellikleri bozmama
- Test coverage
- Dokümantasyon güncellemesi

---

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Ticari kullanım için izin gereklidir.

---

## 👨‍💻 Geliştirici Notları

### **Önemli Dosyalar**
- `index.html` - Ana hub, tüm tab'lar
- `scripts/storage.js` - Veri yönetimi core
- `scripts/analytics.js` - Tracking core
- `scripts/badge-system.js` - Gamification core
- `scripts/quiz-engine.js` - Quiz logic core

### **Debug İpuçları**
```javascript
// LocalStorage'ı temizle
localStorage.clear()

// Tüm veriyi göster
console.log(BSTStorage.getUserData())

// Analytics verisi
console.log(BSTAnalytics.getWeeklyActivity())
```

---

## 📞 İletişim ve Destek

Sorularınız veya önerileriniz için:
- GitHub Issues
- Pull Requests
- Email (belirtilmedi)

---

**Son Güncelleme:** 10 Kasım 2025
**Versiyon:** 2.0.0
**Durum:** Aktif Geliştirme
