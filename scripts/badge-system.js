// Rozet Sistemi - BST Eğitim Portalı

const BadgeSystem = {
    // Tüm rozetler
    badges: [
        { id: 'first-quiz', name: 'İlk Adım', icon: '🌟', desc: 'İlk quiz\'ini tamamladın!', requirement: 'quiz', value: 1 },
        { id: 'quiz-master', name: 'Quiz Tutkunu', icon: '🎯', desc: '10 quiz tamamladın!', requirement: 'quiz', value: 10 },
        { id: 'perfect-score', name: 'Mükemmel', icon: '💯', desc: 'Bir quiz\'den %100 aldın!', requirement: 'perfect', value: 100 },
        { id: 'streak-7', name: 'Ateşli', icon: '🔥', desc: '7 gün üst üste çalıştın!', requirement: 'streak', value: 7 },
        { id: 'streak-30', name: 'Kararlı', icon: '💪', desc: '30 gün üst üste çalıştın!', requirement: 'streak', value: 30 },
        { id: 'game-master', name: 'Oyun Ustası', icon: '🎮', desc: '10 farklı oyun oynadın!', requirement: 'games', value: 10 },
        { id: 'unit-complete', name: 'Ünite Şampiyonu', icon: '📚', desc: 'Bir üniteyi tamamen bitirdin!', requirement: 'unit', value: 1 },
        { id: 'all-units', name: 'Tüm Üniteler', icon: '🏆', desc: 'Tüm üniteleri tamamladın!', requirement: 'unit', value: 11 },
        { id: 'speed-master', name: 'Hız Rekoru', icon: '⚡', desc: 'Quiz\'i 2 dakikada bitir!', requirement: 'speed', value: 120 },
        { id: 'helping-hand', name: 'Yardımsever', icon: '🤝', desc: 'Arkadaşına yardım et!', requirement: 'social', value: 1 },
        { id: 'early-bird', name: 'Erken Kuş', icon: '🐦', desc: 'Sabah 7\'den önce çalış!', requirement: 'time', value: 7 },
        { id: 'night-owl', name: 'Gece Kuşu', icon: '🦉', desc: 'Gece 10\'dan sonra çalış!', requirement: 'time', value: 22 },
        { id: 'curious', name: 'Meraklı', icon: '🔍', desc: 'Sözlüğü 50 kez kullan!', requirement: 'dictionary', value: 50 },
        { id: 'flashcard-fan', name: 'Kart Ustası', icon: '🎴', desc: '100 flashcard çalış!', requirement: 'flashcards', value: 100 },
        { id: 'video-watcher', name: 'Video İzleyici', icon: '📺', desc: '20 eğitim videosu izle!', requirement: 'videos', value: 20 },
        { id: 'collector', name: 'Koleksiyoncu', icon: '🌈', desc: 'Her kategoriden rozet kazan!', requirement: 'variety', value: 5 },
        { id: 'graduation', name: 'Mezuniyet', icon: '🎓', desc: 'Tüm rozetleri topla!', requirement: 'all', value: 25 }
    ],

    // Kullanıcının rozetlerini al
    getUserBadges() {
        const userData = BSTStorage.getUserData();
        return userData.badges || [];
    },

    // Rozet kazanıldı mı kontrol et
    hasBadge(badgeId) {
        return this.getUserBadges().includes(badgeId);
    },

    // Rozet kazan
    earnBadge(badgeId) {
        if (this.hasBadge(badgeId)) return false;

        const userData = BSTStorage.getUserData();
        userData.badges.push(badgeId);
        userData.earnedBadges = userData.badges.length;
        BSTStorage.saveUserData(userData);

        // Rozet bildirimi göster
        this.showBadgeNotification(badgeId);
        return true;
    },

    // Rozet bildirimi
    showBadgeNotification(badgeId) {
        const badge = this.badges.find(b => b.id === badgeId);
        if (!badge) return;

        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 10000;
            animation: slideIn 0.5s ease-out;
            font-family: 'Segoe UI', sans-serif;
        `;
        notification.innerHTML = `
            <div style="font-size: 3em; text-align: center; margin-bottom: 10px;">${badge.icon}</div>
            <div style="font-size: 1.3em; font-weight: bold; text-align: center;">Yeni Rozet!</div>
            <div style="font-size: 1.1em; text-align: center; margin-top: 5px;">${badge.name}</div>
            <div style="font-size: 0.9em; text-align: center; margin-top: 5px; opacity: 0.9;">${badge.desc}</div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.5s ease-in';
            setTimeout(() => notification.remove(), 500);
        }, 4000);
    },

    // Rozet ilerleme yüzdesi
    getBadgeProgress() {
        const total = this.badges.length;
        const earned = this.getUserBadges().length;
        return Math.round((earned / total) * 100);
    },

    // Kategoriye göre rozetler
    getBadgesByCategory() {
        const categories = {
            'Quiz': this.badges.filter(b => b.requirement === 'quiz'),
            'Streak': this.badges.filter(b => b.requirement === 'streak'),
            'Oyun': this.badges.filter(b => b.requirement === 'games'),
            'Ünite': this.badges.filter(b => b.requirement === 'unit'),
            'Özel': this.badges.filter(b => !['quiz', 'streak', 'games', 'unit'].includes(b.requirement))
        };
        return categories;
    }
};

// CSS animasyonları ekle
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);
