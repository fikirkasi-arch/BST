// İlerleme Takip Sistemi
const BSTProgress = {
    PROGRESS_KEY: 'bst_progress_data',

    // İlerleme verisini getir
    getProgress() {
        const data = localStorage.getItem(this.PROGRESS_KEY);
        return data ? JSON.parse(data) : {
            completed: {
                quizzes: [],
                games: [],
                lessons: [],
                videos: []
            },
            scores: {}
        };
    },

    // İlerlemeyi kaydet
    saveProgress(progress) {
        localStorage.setItem(this.PROGRESS_KEY, JSON.stringify(progress));
    },

    // Quiz tamamlandı olarak işaretle
    markQuizCompleted(quizId, score, totalQuestions) {
        const progress = this.getProgress();

        if (!progress.completed.quizzes.includes(quizId)) {
            progress.completed.quizzes.push(quizId);
        }

        progress.scores[quizId] = {
            score: score,
            total: totalQuestions,
            percentage: Math.round((score / totalQuestions) * 100),
            date: new Date().toISOString()
        };

        this.saveProgress(progress);
        this.updateAllProgressDisplays();
    },

    // Oyun tamamlandı
    markGameCompleted(gameId) {
        const progress = this.getProgress();

        if (!progress.completed.games.includes(gameId)) {
            progress.completed.games.push(gameId);
        }

        this.saveProgress(progress);
        this.updateAllProgressDisplays();
    },

    // Ders tamamlandı
    markLessonCompleted(lessonId) {
        const progress = this.getProgress();

        if (!progress.completed.lessons.includes(lessonId)) {
            progress.completed.lessons.push(lessonId);
        }

        this.saveProgress(progress);
        this.updateAllProgressDisplays();
    },

    // Video izlendi
    markVideoCompleted(videoId) {
        const progress = this.getProgress();

        if (!progress.completed.videos.includes(videoId)) {
            progress.completed.videos.push(videoId);
        }

        this.saveProgress(progress);
        this.updateAllProgressDisplays();
    },

    // Ünite ilerleme yüzdesi hesapla
    calculateUnitProgress(gradeLevel, unitNumber) {
        const progress = this.getProgress();

        // Her ünite için beklenen içerik sayıları
        const unitContent = {
            '5-1': { quizzes: 1, games: 2, lessons: 3 },
            '5-2': { quizzes: 1, games: 2, lessons: 3 },
            '5-3': { quizzes: 1, games: 1, lessons: 3 },
            '5-4': { quizzes: 1, games: 1, lessons: 2 },
            '5-5': { quizzes: 1, games: 0, lessons: 2 },
            '5-6': { quizzes: 1, games: 3, lessons: 4 },
            '6-1': { quizzes: 1, games: 2, lessons: 3 },
            '6-2': { quizzes: 1, games: 1, lessons: 3 },
            '6-3': { quizzes: 1, games: 1, lessons: 2 },
            '6-4': { quizzes: 1, games: 0, lessons: 3 },
            '6-5': { quizzes: 1, games: 2, lessons: 4 }
        };

        const unitKey = `${gradeLevel}-${unitNumber}`;
        const expected = unitContent[unitKey];

        if (!expected) return 0;

        // Tamamlanan içerikleri say
        let completed = 0;
        let total = expected.quizzes + expected.games + expected.lessons;

        // Quiz'leri kontrol et
        const quizId = `quiz-${gradeLevel}-unite${unitNumber}`;
        if (progress.completed.quizzes.includes(quizId)) {
            completed += expected.quizzes;
        }

        // Oyunları kontrol et (basitleştirilmiş)
        const completedGamesForUnit = progress.completed.games.filter(g =>
            g.includes(`${gradeLevel}sinif-unite${unitNumber}`)
        ).length;
        completed += Math.min(completedGamesForUnit, expected.games);

        // Dersleri kontrol et
        const lessonId = `lesson-${gradeLevel}-unite${unitNumber}`;
        if (progress.completed.lessons.includes(lessonId)) {
            completed += expected.lessons;
        }

        return Math.round((completed / total) * 100);
    },

    // Genel ilerleme yüzdesi (sınıf bazında)
    calculateOverallProgress(gradeLevel) {
        const unitCounts = {
            '5': 6,
            '6': 5
        };

        const unitCount = unitCounts[gradeLevel];
        let totalProgress = 0;

        for (let i = 1; i <= unitCount; i++) {
            totalProgress += this.calculateUnitProgress(gradeLevel, i);
        }

        return Math.round(totalProgress / unitCount);
    },

    // Tüm ilerleme göstergelerini güncelle
    updateAllProgressDisplays() {
        // Ana sayfadaki ünite kartlarını güncelle
        this.updateUnitCards();

        // Profil sayfasındaki genel ilerlemeyi güncelle
        this.updateOverallProgress();
    },

    // Ünite kartlarına ilerleme göstergesi ekle
    updateUnitCards() {
        // 5. sınıf üniteleri
        const grade5Units = document.querySelectorAll('#grade-5-content .unit-card');
        grade5Units.forEach((card, index) => {
            const unitNumber = index + 1;
            const progress = this.calculateUnitProgress('5', unitNumber);
            this.addProgressBadge(card, progress);
        });

        // 6. sınıf üniteleri
        const grade6Units = document.querySelectorAll('#grade-6-content .unit-card');
        grade6Units.forEach((card, index) => {
            const unitNumber = index + 1;
            const progress = this.calculateUnitProgress('6', unitNumber);
            this.addProgressBadge(card, progress);
        });
    },

    // İlerleme badge'i ekle
    addProgressBadge(card, percentage) {
        // Mevcut badge'i kaldır
        const existingBadge = card.querySelector('.progress-badge');
        if (existingBadge) {
            existingBadge.remove();
        }

        // Yeni badge oluştur
        const badge = document.createElement('div');
        badge.className = 'progress-badge';

        let color = '#ff4757'; // Kırmızı (düşük)
        let icon = '🔴';

        if (percentage >= 75) {
            color = '#10ac84'; // Yeşil (yüksek)
            icon = '✅';
        } else if (percentage >= 50) {
            color = '#feca57'; // Sarı (orta)
            icon = '🟡';
        } else if (percentage >= 25) {
            color = '#ff9800'; // Turuncu (başlangıç)
            icon = '🟠';
        }

        badge.innerHTML = `
            <div style="position: absolute; top: 15px; right: 15px; background: white; padding: 8px 15px; border-radius: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); font-weight: bold; font-size: 0.9em; z-index: 1;">
                <span style="margin-right: 5px;">${icon}</span>
                <span style="color: ${color};">${percentage}%</span>
            </div>
        `;

        card.style.position = 'relative';
        card.appendChild(badge);
    },

    // Genel ilerleme güncelle
    updateOverallProgress() {
        const progress5 = this.calculateOverallProgress('5');
        const progress6 = this.calculateOverallProgress('6');

        // Profil sayfasında göster
        const profilimSection = document.getElementById('profilim');
        if (profilimSection) {
            let progressContainer = profilimSection.querySelector('.overall-progress-container');

            if (!progressContainer) {
                progressContainer = document.createElement('div');
                progressContainer.className = 'overall-progress-container';
                profilimSection.insertBefore(progressContainer, profilimSection.firstChild.nextSibling);
            }

            progressContainer.innerHTML = `
                <div style="background: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
                    <h3 style="margin-bottom: 25px; text-align: center;">📊 Genel İlerleme</h3>

                    <div style="margin-bottom: 25px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span style="font-weight: 600;">📘 5. Sınıf</span>
                            <span style="font-weight: bold; color: ${progress5 >= 70 ? '#10ac84' : '#667eea'};">${progress5}%</span>
                        </div>
                        <div style="background: #e0e0e0; height: 12px; border-radius: 6px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; width: ${progress5}%; transition: width 1s;"></div>
                        </div>
                    </div>

                    <div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span style="font-weight: 600;">📗 6. Sınıf</span>
                            <span style="font-weight: bold; color: ${progress6 >= 70 ? '#10ac84' : '#667eea'};">${progress6}%</span>
                        </div>
                        <div style="background: #e0e0e0; height: 12px; border-radius: 6px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #43e97b, #38f9d7); height: 100%; width: ${progress6}%; transition: width 1s;"></div>
                        </div>
                    </div>
                </div>
            `;
        }
    },

    // Test için örnek veri ekle
    addSampleProgress() {
        const progress = this.getProgress();

        // Örnek quiz'ler
        progress.completed.quizzes = ['quiz-5-unite1', 'quiz-5-unite2'];
        progress.scores['quiz-5-unite1'] = { score: 9, total: 10, percentage: 90 };
        progress.scores['quiz-5-unite2'] = { score: 7, total: 10, percentage: 70 };

        // Örnek oyunlar
        progress.completed.games = ['5sinif-unite1-memorygame', '5sinif-unite1-donanimoyunu'];

        // Örnek dersler
        progress.completed.lessons = ['lesson-5-unite1'];

        this.saveProgress(progress);
        this.updateAllProgressDisplays();

        if (typeof BSTNotification !== 'undefined') {
            BSTNotification.show('Örnek ilerleme verisi eklendi!', 'success');
        }
    }
};

// Sayfa yüklendiğinde ilerlemeyi göster
document.addEventListener('DOMContentLoaded', () => {
    // Küçük bir gecikme ile kartların yüklenmesini bekle
    setTimeout(() => {
        BSTProgress.updateAllProgressDisplays();
    }, 500);
});
