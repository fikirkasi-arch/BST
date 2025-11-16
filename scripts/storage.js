// LocalStorage Yönetimi - BST Eğitim Portalı

const BSTStorage = {
    // Kullanıcı verisini kaydet
    saveUserData(data) {
        const existingData = this.getUserData();
        const merged = { ...existingData, ...data };
        localStorage.setItem('bstUserData', JSON.stringify(merged));
    },

    // Kullanıcı verisini al
    getUserData() {
        const data = localStorage.getItem('bstUserData');
        return data ? JSON.parse(data) : this.getDefaultUserData();
    },

    // Varsayılan kullanıcı verisi
    getDefaultUserData() {
        return {
            completedQuizzes: 0,
            playedGames: 0,
            avgScore: 0,
            earnedBadges: 0,
            streakDays: 0,
            totalPoints: 0,
            lastVisit: null,
            quizScores: [],
            badges: [],
            unitProgress: {}
        };
    },

    // Quiz sonucunu kaydet
    saveQuizResult(quizName, score, totalQuestions) {
        const userData = this.getUserData();
        userData.quizScores.push({
            name: quizName,
            score: score,
            total: totalQuestions,
            percentage: Math.round((score / totalQuestions) * 100),
            date: new Date().toISOString()
        });
        userData.completedQuizzes++;

        // Ortalama skoru güncelle
        const allScores = userData.quizScores.map(q => q.percentage);
        userData.avgScore = Math.round(allScores.reduce((a, b) => a + b, 0) / allScores.length);

        // Puan ekle
        userData.totalPoints += score * 10;

        this.saveUserData(userData);
        this.checkBadges();
    },

    // Rozet kontrolü
    checkBadges() {
        const userData = this.getUserData();
        const badges = [];

        // İlk quiz rozeti
        if (userData.completedQuizzes >= 1 && !userData.badges.includes('first-quiz')) {
            badges.push('first-quiz');
        }

        // 10 quiz rozeti
        if (userData.completedQuizzes >= 10 && !userData.badges.includes('quiz-master')) {
            badges.push('quiz-master');
        }

        // Mükemmel skor rozeti
        if (userData.quizScores.some(q => q.percentage === 100) && !userData.badges.includes('perfect-score')) {
            badges.push('perfect-score');
        }

        // Yeni rozetleri ekle
        if (badges.length > 0) {
            userData.badges = [...new Set([...userData.badges, ...badges])];
            userData.earnedBadges = userData.badges.length;
            this.saveUserData(userData);
            return badges;
        }

        return [];
    },

    // Streak günlerini güncelle
    updateStreak() {
        const userData = this.getUserData();
        const today = new Date().toDateString();
        const lastVisit = userData.lastVisit ? new Date(userData.lastVisit).toDateString() : null;

        if (lastVisit !== today) {
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            const yesterdayStr = yesterday.toDateString();

            if (lastVisit === yesterdayStr) {
                // Streak devam ediyor
                userData.streakDays++;
            } else if (lastVisit === null || lastVisit !== today) {
                // Yeni streak veya streak kırıldı
                userData.streakDays = 1;
            }

            userData.lastVisit = new Date().toISOString();
            this.saveUserData(userData);
        }
    },

    // Tüm verileri sıfırla
    resetAllData() {
        if (confirm('Tüm ilerleme verileriniz silinecek. Emin misiniz?')) {
            localStorage.removeItem('bstUserData');
            location.reload();
        }
    }
};

// Sayfa yüklendiğinde streak'i güncelle
document.addEventListener('DOMContentLoaded', () => {
    BSTStorage.updateStreak();
});
