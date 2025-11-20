// Başarı Bildirimleri ve Toast Sistemi
const BSTNotification = {
    // Bildirim göster
    show(message, type = 'success', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = 'bst-notification';

        const icons = {
            success: '✅',
            error: '❌',
            info: 'ℹ️',
            warning: '⚠️',
            achievement: '🏆'
        };

        const colors = {
            success: '#10ac84',
            error: '#ee5a6f',
            info: '#4facfe',
            warning: '#feca57',
            achievement: '#f093fb'
        };

        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.5em;">${icons[type] || icons.info}</span>
                <span style="flex: 1; font-weight: 500;">${message}</span>
            </div>
        `;

        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: white;
            color: #333;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
            z-index: 10000;
            min-width: 300px;
            max-width: 400px;
            border-left: 4px solid ${colors[type] || colors.info};
            animation: slideInRight 0.3s ease-out;
            font-size: 0.95em;
        `;

        document.body.appendChild(notification);

        // Otomatik kapat
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, duration);
    },

    // Quiz tamamlama bildirimi
    showQuizComplete(quizName, score, totalQuestions) {
        const percentage = Math.round((score / totalQuestions) * 100);
        let emoji = '🎉';
        let message = '';

        if (percentage >= 90) {
            emoji = '🏆';
            message = `Mükemmel! ${quizName} quiz'ini %${percentage} başarı ile tamamladın!`;
        } else if (percentage >= 70) {
            emoji = '⭐';
            message = `Harika! ${quizName} quiz'ini %${percentage} başarı ile tamamladın!`;
        } else if (percentage >= 50) {
            emoji = '👍';
            message = `İyi! ${quizName} quiz'ini %${percentage} başarı ile tamamladın!`;
        } else {
            emoji = '💪';
            message = `${quizName} quiz'ini tamamladın. Tekrar deneyerek gelişebilirsin!`;
        }

        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            z-index: 10001;
            text-align: center;
            animation: popIn 0.5s ease-out;
            max-width: 500px;
        `;

        notification.innerHTML = `
            <div style="font-size: 4em; margin-bottom: 20px;">${emoji}</div>
            <h2 style="color: white; margin-bottom: 15px; font-size: 1.8em;">Tebrikler!</h2>
            <p style="font-size: 1.2em; margin-bottom: 20px; opacity: 0.95;">${message}</p>
            <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 12px; margin-bottom: 20px;">
                <div style="font-size: 2.5em; font-weight: bold;">${score}/${totalQuestions}</div>
                <div style="opacity: 0.9;">Doğru Cevap</div>
            </div>
            <button onclick="this.parentElement.remove()" style="background: white; color: #667eea; border: none; padding: 12px 30px; border-radius: 25px; font-size: 1.1em; font-weight: 600; cursor: pointer;">
                Kapat
            </button>
        `;

        // Backdrop ekle
        const backdrop = document.createElement('div');
        backdrop.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 10000;
            animation: fadeIn 0.3s;
        `;
        backdrop.onclick = () => {
            backdrop.remove();
            notification.remove();
        };

        document.body.appendChild(backdrop);
        document.body.appendChild(notification);

        // Günlük hedefleri güncelle
        if (typeof BSTDailyGoals !== 'undefined') {
            BSTDailyGoals.completeQuiz();
        }
    },

    // Rozet kazanma bildirimi
    showBadgeUnlocked(badgeName, badgeEmoji) {
        this.show(`${badgeEmoji} Yeni rozet kazandın: ${badgeName}!`, 'achievement', 5000);
    },

    // Streak bildirimi
    showStreakUpdate(days) {
        this.show(`🔥 ${days} gün üst üste giriş yaptın! Harika!`, 'achievement', 4000);
    }
};

// CSS animasyonları ekle
if (!document.getElementById('bst-notification-styles')) {
    const style = document.createElement('style');
    style.id = 'bst-notification-styles';
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

        @keyframes popIn {
            0% {
                transform: translate(-50%, -50%) scale(0.5);
                opacity: 0;
            }
            70% {
                transform: translate(-50%, -50%) scale(1.05);
            }
            100% {
                transform: translate(-50%, -50%) scale(1);
                opacity: 1;
            }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}
