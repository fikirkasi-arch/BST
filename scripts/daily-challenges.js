// Daily Challenges - BST Eğitim Portalı
// Günlük görev sistemi

const DailyChallenges = {
    // Tüm challenge türleri
    challengeTemplates: [
        {
            id: 'quiz-3',
            type: 'quiz',
            title: '3 Quiz Tamamla',
            description: 'Bugün 3 farklı quiz çöz',
            target: 3,
            reward: 50,
            icon: '📝'
        },
        {
            id: 'quiz-perfect',
            type: 'quiz',
            title: 'Mükemmel Skor',
            description: 'Bir quiz\'den %100 al',
            target: 100,
            reward: 100,
            icon: '💯'
        },
        {
            id: 'games-5',
            type: 'game',
            title: '5 Oyun Oyna',
            description: 'Bugün 5 farklı oyun oyna',
            target: 5,
            reward: 30,
            icon: '🎮'
        },
        {
            id: 'flashcards-20',
            type: 'flashcard',
            title: '20 Flashcard Çalış',
            description: '20 flashcard ile pratik yap',
            target: 20,
            reward: 40,
            icon: '🗂️'
        },
        {
            id: 'study-30min',
            type: 'time',
            title: '30 Dakika Çalış',
            description: 'Bugün toplam 30 dakika çalış',
            target: 30,
            reward: 60,
            icon: '⏱️'
        },
        {
            id: 'sozluk-visit',
            type: 'visit',
            title: 'Sözlük Ziyareti',
            description: 'Sözlük sayfasını ziyaret et',
            target: 1,
            reward: 20,
            icon: '📖'
        },
        {
            id: 'streak-maintain',
            type: 'streak',
            title: 'Streak Devam',
            description: 'Günlük streak\'ini koru',
            target: 1,
            reward: 25,
            icon: '🔥'
        }
    ],

    // Bugünün challenge'larını al
    getTodayChallenges() {
        const today = new Date().toDateString();
        const saved = localStorage.getItem('dailyChallenges');

        if (saved) {
            const data = JSON.parse(saved);
            // Aynı gün mü kontrol et
            if (data.date === today) {
                return data.challenges;
            }
        }

        // Yeni günlük challenge'lar oluştur
        return this.generateNewChallenges();
    },

    // Yeni challenge'lar oluştur (günde 3 rastgele)
    generateNewChallenges() {
        const today = new Date().toDateString();
        const shuffled = [...this.challengeTemplates].sort(() => Math.random() - 0.5);
        const selected = shuffled.slice(0, 3);

        const challenges = selected.map(template => ({
            ...template,
            progress: 0,
            completed: false,
            claimed: false
        }));

        // Kaydet
        localStorage.setItem('dailyChallenges', JSON.stringify({
            date: today,
            challenges: challenges
        }));

        return challenges;
    },

    // Challenge ilerlemesini güncelle
    updateProgress(challengeType, value = 1) {
        const challenges = this.getTodayChallenges();
        let updated = false;

        challenges.forEach(challenge => {
            if (challenge.type === challengeType && !challenge.completed) {
                // İlerlemeyi güncelle
                if (challengeType === 'quiz' && challenge.id === 'quiz-perfect') {
                    // Mükemmel skor challenge'ı
                    if (value === 100) {
                        challenge.progress = 100;
                        challenge.completed = true;
                        updated = true;
                    }
                } else {
                    challenge.progress += value;
                    if (challenge.progress >= challenge.target) {
                        challenge.progress = challenge.target;
                        challenge.completed = true;
                        updated = true;
                    }
                }
            }
        });

        if (updated) {
            // Kaydet
            const today = new Date().toDateString();
            localStorage.setItem('dailyChallenges', JSON.stringify({
                date: today,
                challenges: challenges
            }));

            // Bildirim göster
            this.showCompletionNotification(challenges.filter(c => c.completed && !c.claimed));
        }

        return challenges;
    },

    // Ödül al
    claimReward(challengeId) {
        const challenges = this.getTodayChallenges();
        const challenge = challenges.find(c => c.id === challengeId);

        if (challenge && challenge.completed && !challenge.claimed) {
            challenge.claimed = true;

            // Ödülü ver
            if (typeof BSTStorage !== 'undefined') {
                const userData = BSTStorage.getUserData();
                userData.totalPoints = (userData.totalPoints || 0) + challenge.reward;
                BSTStorage.saveUserData(userData);
            }

            // Kaydet
            const today = new Date().toDateString();
            localStorage.setItem('dailyChallenges', JSON.stringify({
                date: today,
                challenges: challenges
            }));

            // Badge kontrol et
            if (typeof BadgeSystem !== 'undefined') {
                const completed = challenges.filter(c => c.claimed).length;
                if (completed === 3) {
                    BadgeSystem.earnBadge('daily-master');
                }
            }

            // Bildirim
            this.showRewardNotification(challenge);

            return true;
        }

        return false;
    },

    // Tamamlama bildirimi
    showCompletionNotification(completedChallenges) {
        if (completedChallenges.length === 0) return;

        completedChallenges.forEach(challenge => {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 80px;
                right: 20px;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 20px 25px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                z-index: 10001;
                animation: slideInRight 0.5s ease-out;
                max-width: 350px;
            `;

            notification.innerHTML = `
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="font-size: 2.5em;">${challenge.icon}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold; font-size: 1.1em; margin-bottom: 5px;">
                            Challenge Tamamlandı!
                        </div>
                        <div style="font-size: 0.9em; opacity: 0.9;">
                            ${challenge.title}
                        </div>
                        <div style="font-size: 0.85em; opacity: 0.8; margin-top: 5px;">
                            🎁 +${challenge.reward} puan kazandın!
                        </div>
                    </div>
                    <button onclick="this.parentElement.parentElement.remove()"
                            style="background: rgba(255,255,255,0.2); border: none; color: white; width: 30px; height: 30px; border-radius: 50%; cursor: pointer; font-size: 1.2em;">
                        ✖
                    </button>
                </div>
            `;

            document.body.appendChild(notification);

            // 5 saniye sonra otomatik kapat
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.style.animation = 'slideOutRight 0.5s ease-out';
                    setTimeout(() => notification.remove(), 500);
                }
            }, 5000);
        });

        // Animasyon ekle
        if (!document.getElementById('challenge-notification-animation')) {
            const style = document.createElement('style');
            style.id = 'challenge-notification-animation';
            style.textContent = `
                @keyframes slideInRight {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                @keyframes slideOutRight {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    },

    // Ödül bildirimi
    showRewardNotification(challenge) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            z-index: 10002;
            text-align: center;
            animation: popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        `;

        notification.innerHTML = `
            <div style="font-size: 4em; margin-bottom: 15px;">🎉</div>
            <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 10px;">
                Ödül Alındı!
            </div>
            <div style="font-size: 3em; font-weight: bold; margin: 20px 0;">
                +${challenge.reward} Puan
            </div>
            <button onclick="this.parentElement.remove()"
                    style="background: rgba(255,255,255,0.3); border: 2px solid white; color: white; padding: 12px 30px; border-radius: 25px; cursor: pointer; font-size: 1em; font-weight: bold; margin-top: 15px;">
                Harika! 🎯
            </button>
        `;

        document.body.appendChild(notification);

        // 3 saniye sonra otomatik kapat
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'popOut 0.3s ease-out';
                setTimeout(() => notification.remove(), 300);
            }
        }, 3000);

        // Animasyon ekle
        if (!document.getElementById('reward-notification-animation')) {
            const style = document.createElement('style');
            style.id = 'reward-notification-animation';
            style.textContent = `
                @keyframes popIn {
                    0% {
                        transform: translate(-50%, -50%) scale(0);
                        opacity: 0;
                    }
                    100% {
                        transform: translate(-50%, -50%) scale(1);
                        opacity: 1;
                    }
                }
                @keyframes popOut {
                    0% {
                        transform: translate(-50%, -50%) scale(1);
                        opacity: 1;
                    }
                    100% {
                        transform: translate(-50%, -50%) scale(0);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    },

    // Challenge widget'ı göster (dashboard için)
    renderWidget(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const challenges = this.getTodayChallenges();

        container.innerHTML = `
            <div style="background: white; border-radius: 15px; padding: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                <h3 style="color: #667eea; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">🎯</span>
                    Günlük Görevler
                </h3>
                ${challenges.map(challenge => `
                    <div style="background: ${challenge.completed ? '#e8f5e9' : '#f5f5f5'}; padding: 15px; border-radius: 10px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="font-size: 1.5em;">${challenge.icon}</span>
                                <div>
                                    <div style="font-weight: bold; color: #333;">${challenge.title}</div>
                                    <div style="font-size: 0.85em; color: #666;">${challenge.description}</div>
                                </div>
                            </div>
                            ${challenge.completed && !challenge.claimed ?
                                `<button onclick="DailyChallenges.claimReward('${challenge.id}')"
                                         style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: bold;">
                                    🎁 Al
                                </button>` :
                                challenge.claimed ?
                                `<span style="color: #4caf50; font-weight: bold;">✓ Alındı</span>` :
                                `<span style="color: #999; font-size: 0.9em;">${challenge.reward} puan</span>`
                            }
                        </div>
                        <div style="background: #e0e0e0; height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); height: 100%; width: ${(challenge.progress / challenge.target) * 100}%; transition: width 0.3s;"></div>
                        </div>
                        <div style="font-size: 0.8em; color: #666; margin-top: 5px; text-align: right;">
                            ${challenge.progress}/${challenge.target}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
};

// Sayfa yüklendiğinde challenge'ları başlat
document.addEventListener('DOMContentLoaded', () => {
    // Günlük challenge'ları oluştur/yükle
    DailyChallenges.getTodayChallenges();

    // Analytics ile entegre et
    if (typeof BSTAnalytics !== 'undefined') {
        const originalLogActivity = BSTAnalytics.logActivity;
        BSTAnalytics.logActivity = function(activityType, details) {
            // Orijinal fonksiyonu çağır
            originalLogActivity.call(this, activityType, details);

            // Challenge ilerlemesini güncelle
            if (activityType === 'quiz_completed') {
                DailyChallenges.updateProgress('quiz', 1);
                if (details.percentage === 100) {
                    DailyChallenges.updateProgress('quiz', 100);
                }
            } else if (activityType === 'game_played') {
                DailyChallenges.updateProgress('game', 1);
            } else if (activityType === 'flashcard_studied') {
                DailyChallenges.updateProgress('flashcard', details.count || 1);
            } else if (activityType === 'page_view' && details.pageName && details.pageName.includes('Sözlük')) {
                DailyChallenges.updateProgress('visit', 1);
            }
        };
    }
});
