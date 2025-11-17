// Günlük Hedefler ve Streak Sistemi
const BSTDailyGoals = {
    GOALS_KEY: 'bst_daily_goals',
    STREAK_KEY: 'bst_login_streak',

    // Günlük hedefleri getir
    getTodayGoals() {
        const today = new Date().toDateString();
        const data = localStorage.getItem(this.GOALS_KEY);
        const goals = data ? JSON.parse(data) : null;

        // Bugünün hedefleri yoksa veya tarih geçmişse yeni oluştur
        if (!goals || goals.date !== today) {
            const newGoals = {
                date: today,
                quizCompleted: 0,
                quizTarget: 1,
                gameCompleted: 0,
                gameTarget: 1,
                minutesStudied: 0,
                minutesTarget: 20
            };
            localStorage.setItem(this.GOALS_KEY, JSON.stringify(newGoals));
            return newGoals;
        }

        return goals;
    },

    // Quiz tamamlandı
    completeQuiz() {
        const goals = this.getTodayGoals();
        goals.quizCompleted++;
        localStorage.setItem(this.GOALS_KEY, JSON.stringify(goals));
        this.updateDisplay();
        this.checkAllGoalsComplete();
    },

    // Oyun tamamlandı
    completeGame() {
        const goals = this.getTodayGoals();
        goals.gameCompleted++;
        localStorage.setItem(this.GOALS_KEY, JSON.stringify(goals));
        this.updateDisplay();
        this.checkAllGoalsComplete();
    },

    // Çalışma dakikası ekle
    addStudyMinutes(minutes) {
        const goals = this.getTodayGoals();
        goals.minutesStudied += minutes;
        localStorage.setItem(this.GOALS_KEY, JSON.stringify(goals));
        this.updateDisplay();
    },

    // Tüm hedefler tamamlandı mı kontrol et
    checkAllGoalsComplete() {
        const goals = this.getTodayGoals();
        const allComplete =
            goals.quizCompleted >= goals.quizTarget &&
            goals.gameCompleted >= goals.gameTarget;

        if (allComplete) {
            setTimeout(() => {
                if (typeof BSTNotification !== 'undefined') {
                    BSTNotification.show('🎉 Bugünün tüm hedeflerini tamamladın! Harikasın!', 'achievement', 5000);
                }
            }, 500);
        }
    },

    // Streak hesapla
    updateStreak() {
        const data = localStorage.getItem(this.STREAK_KEY);
        const streak = data ? JSON.parse(data) : { days: 0, lastVisit: null };

        const today = new Date().toDateString();
        const yesterday = new Date(Date.now() - 86400000).toDateString();

        if (streak.lastVisit === today) {
            // Bugün zaten sayıldı
            return streak.days;
        } else if (streak.lastVisit === yesterday) {
            // Dün de giriş yapılmış, streak devam ediyor
            streak.days++;
            streak.lastVisit = today;
        } else {
            // Streak kırıldı veya ilk giriş
            streak.days = 1;
            streak.lastVisit = today;
        }

        localStorage.setItem(this.STREAK_KEY, JSON.stringify(streak));

        // Streak bildirimi (3 günden fazlaysa)
        if (streak.days >= 3 && typeof BSTNotification !== 'undefined') {
            BSTNotification.showStreakUpdate(streak.days);
        }

        return streak.days;
    },

    // Streak bilgisini getir
    getStreak() {
        const data = localStorage.getItem(this.STREAK_KEY);
        const streak = data ? JSON.parse(data) : { days: 0, lastVisit: null };

        const today = new Date().toDateString();
        const yesterday = new Date(Date.now() - 86400000).toDateString();

        // Eğer bugün veya dün giriş yapılmamışsa streak 0
        if (streak.lastVisit !== today && streak.lastVisit !== yesterday) {
            return 0;
        }

        return streak.days;
    },

    // Görüntüyü güncelle
    updateDisplay() {
        const container = document.getElementById('daily-goals-container');
        if (!container) return;

        const goals = this.getTodayGoals();
        const streak = this.getStreak();

        const quizProgress = Math.min((goals.quizCompleted / goals.quizTarget) * 100, 100);
        const gameProgress = Math.min((goals.gameCompleted / goals.gameTarget) * 100, 100);

        container.innerHTML = `
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                    <h2 style="color: white; margin: 0;">📅 Bugünün Hedefleri</h2>
                    ${streak > 0 ? `<div style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-weight: bold;">🔥 ${streak} Gün</div>` : ''}
                </div>

                <!-- Quiz Hedefi -->
                <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 12px; margin-bottom: 15px; backdrop-filter: blur(10px);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.5em;">📝</span>
                            <span style="font-weight: 500;">Quiz Çöz</span>
                        </div>
                        <span style="font-weight: bold; font-size: 1.1em;">${goals.quizCompleted}/${goals.quizTarget}</span>
                    </div>
                    <div style="background: rgba(0,0,0,0.2); height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: #10ac84; height: 100%; width: ${quizProgress}%; transition: width 0.5s;"></div>
                    </div>
                </div>

                <!-- Oyun Hedefi -->
                <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 12px; backdrop-filter: blur(10px);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.5em;">🎮</span>
                            <span style="font-weight: 500;">Oyun Oyna</span>
                        </div>
                        <span style="font-weight: bold; font-size: 1.1em;">${goals.gameCompleted}/${goals.gameTarget}</span>
                    </div>
                    <div style="background: rgba(0,0,0,0.2); height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: #f093fb; height: 100%; width: ${gameProgress}%; transition: width 0.5s;"></div>
                    </div>
                </div>

                ${quizProgress === 100 && gameProgress === 100 ?
                    '<div style="margin-top: 20px; text-align: center; font-size: 1.2em; font-weight: bold; animation: pulse 2s infinite;">🎉 Tüm hedefler tamamlandı! 🎉</div>' :
                    '<div style="margin-top: 15px; text-align: center; opacity: 0.9; font-size: 0.9em;">Hedeflerini tamamlayarak streak kazanmaya devam et!</div>'
                }
            </div>
        `;
    },

    // Başlat
    init() {
        this.updateStreak();
        this.updateDisplay();
    }
};

// Sayfa yüklendiğinde başlat
document.addEventListener('DOMContentLoaded', () => {
    BSTDailyGoals.init();
});

// Pulse animasyonu ekle
if (!document.getElementById('bst-goals-styles')) {
    const style = document.createElement('style');
    style.id = 'bst-goals-styles';
    style.textContent = `
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
    `;
    document.head.appendChild(style);
}
