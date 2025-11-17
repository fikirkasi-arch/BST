// Global Search - BST Eğitim Portalı
// Tüm içeriklerde arama yapma modülü

const BSTSearch = {
    // Arama veritabanı
    searchIndex: {
        quizzes: [
            { title: '5. Sınıf - Ünite 1: Bilişim Temelleri Quiz', url: 'quiz-5-unite1.html', category: 'quiz', keywords: ['bilişim', 'teknoloji', 'donanım', 'yazılım', 'işletim sistemi', 'windows', 'linux', 'macos', 'ram', 'cpu', 'hard disk', 'ssd', 'anakart', 'dosya', 'klasör'] },
            { title: '5. Sınıf - Ünite 2: Dijital Ürün Tasarımı Quiz', url: 'quiz-5-unite2.html', category: 'quiz', keywords: ['word', 'powerpoint', 'paint', 'office', 'sunum', 'belge', 'grafik', 'tasarım'] },
            { title: '5. Sınıf - Ünite 3: Ağlar ve İletişim Quiz', url: 'quiz-5-unite3.html', category: 'quiz', keywords: ['internet', 'ağ', 'network', 'e-posta', 'email', 'tarayıcı', 'browser', 'web', 'lan', 'wan'] },
            { title: '5. Sınıf - Ünite 4: Etik ve Güvenlik Quiz', url: 'quiz-5-unite4.html', category: 'quiz', keywords: ['etik', 'güvenlik', 'şifre', 'password', 'dijital vatandaşlık', 'siber zorbalık', 'telif hakkı', 'gizlilik'] },
            { title: '5. Sınıf - Ünite 5: Yapay Zeka Quiz', url: 'quiz-5-unite5.html', category: 'quiz', keywords: ['yapay zeka', 'ai', 'makine öğrenmesi', 'robot', 'otomasyon', 'algoritma'] },
            { title: '5. Sınıf - Ünite 6: Scratch Programlama Quiz', url: 'quiz-5-unite6.html', category: 'quiz', keywords: ['scratch', 'programlama', 'kod', 'blok', 'döngü', 'koşul', 'oyun yapımı', 'animasyon'] },
            { title: '6. Sınıf - Ünite 1: Bilişim Teknolojileri Quiz', url: 'quiz-6-unite1.html', category: 'quiz', keywords: ['bilişim', 'tarihçe', 'ikili sayı', 'bit', 'byte', 'bulut', 'cloud', 'iot', 'nesnelerin interneti'] },
            { title: '6. Sınıf - Ünite 2: Etik ve Güvenlik Quiz', url: 'quiz-6-unite2.html', category: 'quiz', keywords: ['kvkk', 'phishing', '2fa', 'iki faktörlü', 'kimlik doğrulama', 'kişisel veri', 'güvenlik'] },
            { title: '6. Sınıf - Ünite 3: İletişim ve İşbirliği Quiz', url: 'quiz-6-unite3.html', category: 'quiz', keywords: ['bulut depolama', 'google drive', 'onedrive', 'zoom', 'teams', 'video konferans', 'ortak çalışma'] },
            { title: '6. Sınıf - Ünite 4: Ürün Oluşturma Quiz', url: 'quiz-6-unite4.html', category: 'quiz', keywords: ['grafik tasarım', 'canva', 'gimp', 'video düzenleme', 'animasyon', 'podcast'] },
            { title: '6. Sınıf - Ünite 5: Problem Çözme Quiz', url: 'quiz-6-unite5.html', category: 'quiz', keywords: ['programlama', 'python', 'algoritma', 'akış diyagramı', 'döngü', 'koşul', 'değişken', 'fonksiyon'] }
        ],
        games: [
            { title: 'Donanım Eşleştirme Oyunu', url: 'oyunlar/5sinif-unite1-donanimoyunu.html', category: 'game', keywords: ['donanım', 'ram', 'cpu', 'ekran kartı', 'anakart', 'hard disk', 'bilgisayar parçaları'] },
            { title: 'Hafıza Oyunu', url: 'oyunlar/5sinif-unite1-memorygame.html', category: 'game', keywords: ['hafıza', 'memory', 'eşleştirme', 'bilgisayar', 'donanım'] },
            { title: 'Bilişim Quiz', url: 'oyunlar/5sinif-unite1-bilisimquiz.html', category: 'game', keywords: ['bilişim', 'quiz', 'test', 'işletim sistemi', 'donanım'] },
            { title: 'Harf Avı', url: 'oyunlar/5sinif-unite2-harfavi.html', category: 'game', keywords: ['kelime', 'harf', 'oyun', 'bilişim terimleri', 'terim'] },
            { title: 'Kelime Eşleştirme', url: 'kelime-eslestirme.html', category: 'game', keywords: ['kelime', 'eşleştirme', 'terim', 'tanım', 'sözlük'] },
            { title: 'Microsoft Office Quiz', url: 'oyunlar/5sinif-unite2-officequiz.html', category: 'game', keywords: ['office', 'word', 'excel', 'powerpoint', 'microsoft'] },
            { title: 'Word-Excel Eşleştirme', url: 'oyunlar/5sinif-unite2-wordexcelmatch.html', category: 'game', keywords: ['word', 'excel', 'eşleştirme', 'office'] },
            { title: 'Word Simülasyonu', url: 'oyunlar/5sinif-unite3-wordsimulation.html', category: 'game', keywords: ['word', 'simülasyon', 'belge', 'kelime işlemci'] },
            { title: 'Kodlama Parkuru', url: 'oyunlar/coding-parkour.html', category: 'game', keywords: ['kodlama', 'kod', 'parkur', 'engel', 'algoritma', 'programlama'] },
            { title: 'Programlama Quiz', url: 'oyunlar/6sinif-unite1-programmingquiz.html', category: 'game', keywords: ['programlama', 'kod', 'algoritma', 'python'] },
            { title: 'Algoritma Bulmaca', url: 'oyunlar/6sinif-unite1-algoritmapuzzle.html', category: 'game', keywords: ['algoritma', 'bulmaca', 'mantık', 'problem çözme'] },
            { title: 'Scratch Projesi', url: 'oyunlar/6sinif-unite2-scratchproject.html', category: 'game', keywords: ['scratch', 'proje', 'blok', 'programlama', 'oyun yapımı'] },
            { title: 'Kod Blokları', url: 'oyunlar/6sinif-unite2-codeblocks.html', category: 'game', keywords: ['kod', 'blok', 'programlama', 'scratch'] },
            { title: 'İnternet Güvenliği Quiz', url: 'oyunlar/6sinif-unite3-internetquiz.html', category: 'game', keywords: ['internet', 'güvenlik', 'siber', 'phishing', 'şifre'] }
        ],
        pages: [
            { title: 'Bilişim Sözlüğü', url: 'sozluk.html', category: 'page', keywords: ['sözlük', 'terimler', 'kelime', 'tanım', 'kavram', 'açıklama'] },
            { title: 'Flashcards - Hafıza Kartları', url: 'flashcards.html', category: 'page', keywords: ['flashcard', 'kart', 'çalışma', 'tekrar', 'hafıza', 'ezber'] },
            { title: 'Video Kütüphanesi', url: 'video-library.html', category: 'page', keywords: ['video', 'eğitim', 'ders', 'izle', 'anlatım', 'tutorial'] },
            { title: 'Öğrenci Paneli', url: 'student-dashboard.html', category: 'page', keywords: ['panel', 'dashboard', 'ilerleme', 'istatistik', 'gelişim', 'profil'] },
            { title: 'Rozetler', url: 'badges.html', category: 'page', keywords: ['rozet', 'başarı', 'ödül', 'badge', 'kazanım'] },
            { title: 'Lider Tablosu', url: 'leaderboard.html', category: 'page', keywords: ['lider', 'sıralama', 'yarışma', 'puan', 'skor'] },
            { title: 'Oyun Merkezi', url: 'games-hub.html', category: 'page', keywords: ['oyun', 'game', 'eğlence', 'aktivite', 'interaktif'] },
            { title: 'İlerleme Raporu', url: 'progress-report.html', category: 'page', keywords: ['rapor', 'ilerleme', 'başarı', 'analiz', 'değerlendirme'] },
            { title: 'Sınav Oluşturucu', url: 'exam-creator.html', category: 'page', keywords: ['sınav', 'test', 'oluştur', 'öğretmen', 'yazılı'] },
            { title: 'Ana Sayfa', url: 'index.html', category: 'page', keywords: ['anasayfa', 'home', 'başlangıç', 'portal', 'dersler', 'aktiviteler'] }
        ],
        lessons: [
            { title: '5. Sınıf - Ünite 1: Bilişim Temelleri', url: 'index.html#dersler', category: 'lesson', keywords: ['bilişim', 'donanım', 'yazılım', 'işletim sistemi', 'windows', 'linux', 'ram', 'cpu', 'hard disk', 'dosya', 'klasör', 'anakart'] },
            { title: '5. Sınıf - Ünite 2: Dijital Ürün Tasarımı', url: 'index.html#dersler', category: 'lesson', keywords: ['word', 'paint', 'powerpoint', 'belge', 'çizim', 'sunum', 'office', 'tasarım'] },
            { title: '5. Sınıf - Ünite 3: Ağlar ve İletişim', url: 'index.html#dersler', category: 'lesson', keywords: ['internet', 'ağ', 'lan', 'wan', 'e-posta', 'email', 'tarayıcı', 'web', 'iletişim'] },
            { title: '5. Sınıf - Ünite 4: Etik ve Güvenlik', url: 'index.html#dersler', category: 'lesson', keywords: ['etik', 'güvenlik', 'şifre', 'dijital vatandaşlık', 'siber zorbalık', 'telif hakkı', 'gizlilik'] },
            { title: '5. Sınıf - Ünite 5: Yapay Zeka', url: 'index.html#dersler', category: 'lesson', keywords: ['yapay zeka', 'ai', 'makine öğrenmesi', 'robot', 'otomasyon', 'siri', 'alexa'] },
            { title: '5. Sınıf - Ünite 6: Scratch Programlama', url: 'index.html#dersler', category: 'lesson', keywords: ['scratch', 'programlama', 'blok', 'kod', 'döngü', 'koşul', 'oyun yapımı', 'animasyon', 'sprite'] },
            { title: '6. Sınıf - Ünite 1: Bilişim Teknolojileri', url: 'index.html#dersler', category: 'lesson', keywords: ['bilişim tarihçesi', 'ikili sayı', 'bit', 'byte', 'bulut bilişim', 'cloud', 'iot', 'nesnelerin interneti'] },
            { title: '6. Sınıf - Ünite 2: Etik ve Güvenlik', url: 'index.html#dersler', category: 'lesson', keywords: ['kvkk', 'kişisel veri', 'phishing', '2fa', 'iki faktörlü kimlik doğrulama', 'güvenlik'] },
            { title: '6. Sınıf - Ünite 3: İletişim ve İşbirliği', url: 'index.html#dersler', category: 'lesson', keywords: ['bulut depolama', 'google drive', 'onedrive', 'zoom', 'teams', 'video konferans', 'ortak belge'] },
            { title: '6. Sınıf - Ünite 4: Ürün Oluşturma', url: 'index.html#dersler', category: 'lesson', keywords: ['grafik tasarım', 'canva', 'gimp', 'video düzenleme', 'animasyon', 'podcast', 'ses kaydı'] },
            { title: '6. Sınıf - Ünite 5: Problem Çözme ve Programlama', url: 'index.html#dersler', category: 'lesson', keywords: ['python', 'algoritma', 'akış diyagramı', 'programlama', 'döngü', 'koşul', 'değişken', 'fonksiyon', 'liste'] }
        ]
    },

    // Arama yap
    search(query) {
        if (!query || query.length < 2) {
            return [];
        }

        const normalizedQuery = this.normalizeText(query);
        const results = [];

        // Tüm kategorilerde ara
        ['quizzes', 'games', 'pages', 'lessons'].forEach(category => {
            this.searchIndex[category].forEach(item => {
                const score = this.calculateRelevance(normalizedQuery, item);
                if (score > 0) {
                    results.push({
                        ...item,
                        score: score
                    });
                }
            });
        });

        // Skora göre sırala
        results.sort((a, b) => b.score - a.score);

        // Analytics kaydı
        if (typeof BSTAnalytics !== 'undefined') {
            BSTAnalytics.logActivity('search', {
                query: query,
                resultCount: results.length
            });
        }

        return results;
    },

    // İlgililik skorunu hesapla
    calculateRelevance(query, item) {
        let score = 0;
        const normalizedTitle = this.normalizeText(item.title);
        const normalizedKeywords = item.keywords.map(k => this.normalizeText(k));

        // Başlıkta tam eşleşme (en yüksek skor)
        if (normalizedTitle.includes(query)) {
            score += 100;
        }

        // Başlıkta kelime eşleşmesi
        query.split(' ').forEach(word => {
            if (normalizedTitle.includes(word)) {
                score += 50;
            }
        });

        // Anahtar kelimede tam eşleşme
        normalizedKeywords.forEach(keyword => {
            if (keyword.includes(query)) {
                score += 30;
            }
            // Anahtar kelimede kısmi eşleşme
            query.split(' ').forEach(word => {
                if (keyword.includes(word)) {
                    score += 10;
                }
            });
        });

        return score;
    },

    // Metin normalizasyonu (Türkçe karakterler dahil)
    normalizeText(text) {
        return text.toLowerCase()
            .replace(/ı/g, 'i')
            .replace(/ğ/g, 'g')
            .replace(/ü/g, 'u')
            .replace(/ş/g, 's')
            .replace(/ö/g, 'o')
            .replace(/ç/g, 'c')
            .trim();
    },

    // Arama arayüzünü göster
    showSearchModal() {
        // Modal zaten varsa kaldır
        const existingModal = document.getElementById('search-modal');
        if (existingModal) {
            existingModal.remove();
        }

        // Yeni modal oluştur
        const modal = document.createElement('div');
        modal.id = 'search-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 10000;
            display: flex;
            align-items: flex-start;
            justify-content: center;
            padding-top: 100px;
        `;

        modal.innerHTML = `
            <div style="background: white; border-radius: 20px; width: 90%; max-width: 700px; max-height: 80vh; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
                <div style="padding: 25px; border-bottom: 2px solid #e0e0e0;">
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <input type="text" id="search-input" placeholder="Ara... (quiz, oyun, sözlük, vb.)"
                               style="flex: 1; padding: 15px 20px; border: 2px solid #e0e0e0; border-radius: 12px; font-size: 1.1em; outline: none;">
                        <button onclick="BSTSearch.closeSearchModal()"
                                style="padding: 15px 20px; background: #e74c3c; color: white; border: none; border-radius: 12px; cursor: pointer; font-size: 1.1em;">
                            ✖️
                        </button>
                    </div>
                </div>
                <div id="search-results" style="padding: 20px; max-height: calc(80vh - 120px); overflow-y: auto;">
                    <p style="text-align: center; color: #999; font-style: italic;">Aramaya başlamak için yazın...</p>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Input'a focus ver
        const input = document.getElementById('search-input');
        input.focus();

        // Arama olayını dinle
        input.addEventListener('input', (e) => {
            this.performSearch(e.target.value);
        });

        // ESC tuşu ile kapat
        modal.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeSearchModal();
            }
        });

        // Modal dışına tıklanınca kapat
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeSearchModal();
            }
        });
    },

    // Arama işlemini gerçekleştir
    performSearch(query) {
        const resultsContainer = document.getElementById('search-results');

        if (!query || query.length < 2) {
            resultsContainer.innerHTML = '<p style="text-align: center; color: #999; font-style: italic;">En az 2 karakter girin...</p>';
            return;
        }

        const results = this.search(query);

        if (results.length === 0) {
            resultsContainer.innerHTML = '<p style="text-align: center; color: #999;">Sonuç bulunamadı. 😔</p>';
            return;
        }

        const categoryIcons = {
            quiz: '📝',
            game: '🎮',
            page: '📄',
            lesson: '📚'
        };

        const categoryNames = {
            quiz: 'Quiz',
            game: 'Oyun',
            page: 'Sayfa',
            lesson: 'Ders'
        };

        resultsContainer.innerHTML = results.map(result => `
            <a href="${result.url}" style="text-decoration: none; color: inherit;">
                <div style="padding: 15px; border-radius: 12px; border: 2px solid #e0e0e0; margin-bottom: 10px; cursor: pointer; transition: all 0.3s;"
                     onmouseover="this.style.borderColor='#667eea'; this.style.background='#f8f9ff';"
                     onmouseout="this.style.borderColor='#e0e0e0'; this.style.background='white';">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                        <span style="font-size: 1.5em;">${categoryIcons[result.category]}</span>
                        <span style="font-weight: bold; color: #333; flex: 1;">${result.title}</span>
                        <span style="padding: 4px 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; font-size: 0.8em;">
                            ${categoryNames[result.category]}
                        </span>
                    </div>
                    <div style="color: #999; font-size: 0.9em; margin-left: 40px;">
                        ${result.keywords.slice(0, 4).join(' • ')}
                    </div>
                </div>
            </a>
        `).join('');
    },

    // Modalı kapat
    closeSearchModal() {
        const modal = document.getElementById('search-modal');
        if (modal) {
            modal.remove();
        }
    },

    // Klavye kısayolu ekle (Ctrl+K veya Cmd+K)
    initKeyboardShortcut() {
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.showSearchModal();
            }
        });
    }
};

// Sayfa yüklendiğinde klavye kısayolunu aktif et
document.addEventListener('DOMContentLoaded', () => {
    BSTSearch.initKeyboardShortcut();
});
