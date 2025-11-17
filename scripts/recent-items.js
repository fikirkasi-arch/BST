// Hızlı Erişim ve Favoriler Sistemi
const BSTRecent = {
    RECENT_KEY: 'bst_recent_items',
    FAVORITES_KEY: 'bst_favorites',
    MAX_RECENT: 5,

    // Son görüntülenen öğeyi kaydet
    addRecentItem(item) {
        let recent = this.getRecentItems();

        // Aynı öğe varsa çıkar (en üste eklemek için)
        recent = recent.filter(r => r.url !== item.url);

        // Başa ekle
        recent.unshift({
            title: item.title,
            url: item.url,
            emoji: item.emoji || '📄',
            category: item.category || 'page',
            timestamp: Date.now()
        });

        // Maksimum sayıda tut
        if (recent.length > this.MAX_RECENT) {
            recent = recent.slice(0, this.MAX_RECENT);
        }

        localStorage.setItem(this.RECENT_KEY, JSON.stringify(recent));
        this.updateRecentDisplay();
    },

    // Son görüntülenenleri getir
    getRecentItems() {
        const data = localStorage.getItem(this.RECENT_KEY);
        return data ? JSON.parse(data) : [];
    },

    // Favorilere ekle/çıkar
    toggleFavorite(item) {
        let favorites = this.getFavorites();
        const exists = favorites.find(f => f.url === item.url);

        if (exists) {
            // Çıkar
            favorites = favorites.filter(f => f.url !== item.url);
        } else {
            // Ekle
            favorites.push({
                title: item.title,
                url: item.url,
                emoji: item.emoji || '📄',
                category: item.category || 'page',
                timestamp: Date.now()
            });
        }

        localStorage.setItem(this.FAVORITES_KEY, JSON.stringify(favorites));
        this.updateFavoritesDisplay();
        return !exists; // true = eklendi, false = çıkarıldı
    },

    // Favorileri getir
    getFavorites() {
        const data = localStorage.getItem(this.FAVORITES_KEY);
        return data ? JSON.parse(data) : [];
    },

    // Favori mi kontrol et
    isFavorite(url) {
        const favorites = this.getFavorites();
        return favorites.some(f => f.url === url);
    },

    // Ana sayfada son açtıkların görüntüsünü güncelle
    updateRecentDisplay() {
        const container = document.getElementById('recent-items-container');
        if (!container) return;

        const recent = this.getRecentItems();

        if (recent.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">Henüz görüntülenen içerik yok</p>';
            return;
        }

        const categoryColors = {
            quiz: '#4facfe',
            game: '#f093fb',
            page: '#43e97b',
            lesson: '#667eea'
        };

        container.innerHTML = recent.map(item => `
            <a href="${item.url}" style="text-decoration: none;" onclick="BSTRecent.addRecentItem({title: '${item.title}', url: '${item.url}', emoji: '${item.emoji}', category: '${item.category}'})">
                <div style="background: white; border-left: 4px solid ${categoryColors[item.category] || '#667eea'}; padding: 15px; border-radius: 8px; margin-bottom: 10px; cursor: pointer; transition: all 0.3s; box-shadow: 0 2px 5px rgba(0,0,0,0.05);"
                     onmouseover="this.style.transform='translateX(5px)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'"
                     onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='0 2px 5px rgba(0,0,0,0.05)'">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">${item.emoji}</span>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; color: #333; margin-bottom: 3px;">${item.title}</div>
                            <div style="font-size: 0.85em; color: #999;">${this.getTimeAgo(item.timestamp)}</div>
                        </div>
                    </div>
                </div>
            </a>
        `).join('');
    },

    // Favoriler görüntüsünü güncelle
    updateFavoritesDisplay() {
        const container = document.getElementById('favorites-container');
        if (!container) return;

        const favorites = this.getFavorites();

        if (favorites.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">Henüz favori eklenmemiş</p>';
            return;
        }

        const categoryColors = {
            quiz: '#4facfe',
            game: '#f093fb',
            page: '#43e97b',
            lesson: '#667eea'
        };

        container.innerHTML = favorites.map(item => `
            <div style="background: white; border-left: 4px solid ${categoryColors[item.category] || '#667eea'}; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); position: relative;">
                <a href="${item.url}" style="text-decoration: none; display: flex; align-items: center; gap: 12px;" onclick="BSTRecent.addRecentItem({title: '${item.title}', url: '${item.url}', emoji: '${item.emoji}', category: '${item.category}'})">
                    <span style="font-size: 1.8em;">${item.emoji}</span>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #333;">${item.title}</div>
                    </div>
                </a>
                <button onclick="event.preventDefault(); BSTRecent.toggleFavorite({title: '${item.title}', url: '${item.url}', emoji: '${item.emoji}', category: '${item.category}'}); BSTNotification.show('Favorilerden çıkarıldı', 'info');"
                        style="position: absolute; top: 10px; right: 10px; background: #ff4757; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 0.85em;">
                    ❌
                </button>
            </div>
        `).join('');
    },

    // Zaman farkını hesapla
    getTimeAgo(timestamp) {
        const seconds = Math.floor((Date.now() - timestamp) / 1000);

        if (seconds < 60) return 'Az önce';
        if (seconds < 3600) return Math.floor(seconds / 60) + ' dakika önce';
        if (seconds < 86400) return Math.floor(seconds / 3600) + ' saat önce';
        if (seconds < 604800) return Math.floor(seconds / 86400) + ' gün önce';
        return new Date(timestamp).toLocaleDateString('tr-TR');
    },

    // Sayfa yüklendiğinde çalıştır
    init() {
        this.updateRecentDisplay();
        this.updateFavoritesDisplay();
    }
};

// Sayfa yüklendiğinde başlat
document.addEventListener('DOMContentLoaded', () => {
    BSTRecent.init();
});
