// Analytics ve İstatistikler - BST Eğitim Portalı

const BSTAnalytics = {
    // Sayfa görüntüleme kaydı
    trackPageView(pageName) {
        const views = this.getPageViews();
        views[pageName] = (views[pageName] || 0) + 1;
        localStorage.setItem('bstPageViews', JSON.stringify(views));
    },

    getPageViews() {
        const data = localStorage.getItem('bstPageViews');
        return data ? JSON.parse(data) : {};
    },

    // Aktivite kaydı
    logActivity(activityType, details = {}) {
        const activities = this.getActivities();
        activities.push({
            type: activityType,
            details: details,
            timestamp: new Date().toISOString()
        });

        // Son 100 aktiviteyi tut
        if (activities.length > 100) {
            activities.shift();
        }

        localStorage.setItem('bstActivities', JSON.stringify(activities));
    },

    getActivities() {
        const data = localStorage.getItem('bstActivities');
        return data ? JSON.parse(data) : [];
    },

    // Haftalık aktivite özeti
    getWeeklyActivity() {
        const activities = this.getActivities();
        const oneWeekAgo = new Date();
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

        return activities.filter(a => new Date(a.timestamp) >= oneWeekAgo);
    },

    // En popüler sayfalar
    getPopularPages(limit = 5) {
        const views = this.getPageViews();
        return Object.entries(views)
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit);
    },

    // Çalışma süresi tahmini (dakika)
    getEstimatedStudyTime() {
        const activities = this.getWeeklyActivity();
        // Her aktivite ortalama 5 dakika varsayımı
        return activities.length * 5;
    },

    // Günlük aktivite dağılımı
    getDailyActivityDistribution() {
        const activities = this.getActivities();
        const distribution = {
            'Pazartesi': 0,
            'Salı': 0,
            'Çarşamba': 0,
            'Perşembe': 0,
            'Cuma': 0,
            'Cumartesi': 0,
            'Pazar': 0
        };

        const dayNames = ['Pazar', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'];

        activities.forEach(a => {
            const date = new Date(a.timestamp);
            const dayName = dayNames[date.getDay()];
            distribution[dayName]++;
        });

        return distribution;
    }
};

// Sayfa yüklendiğinde takip et
document.addEventListener('DOMContentLoaded', () => {
    const pageName = document.title || 'Unknown Page';
    BSTAnalytics.trackPageView(pageName);
});
