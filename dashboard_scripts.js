// ==================== PROGRESS TRACKING SYSTEM ====================
// LocalStorage için anahtarlar
const STORAGE_KEYS = {
    completedWeeks: 'bty_completed_weeks',
    completedGames: 'bty_completed_games',
    completedWorksheets: 'bty_completed_worksheets',
    activities: 'bty_activities',
    badges: 'bty_badges',
    currentWeek: 'bty_current_week'
};

// İlerleme verilerini yükleme
function loadProgress() {
    return {
        weeks: JSON.parse(localStorage.getItem(STORAGE_KEYS.completedWeeks) || '[]'),
        games: JSON.parse(localStorage.getItem(STORAGE_KEYS.completedGames) || '[]'),
        worksheets: JSON.parse(localStorage.getItem(STORAGE_KEYS.completedWorksheets) || '[]'),
        activities: JSON.parse(localStorage.getItem(STORAGE_KEYS.activities) || '[]'),
        badges: JSON.parse(localStorage.getItem(STORAGE_KEYS.badges) || '[]'),
        currentWeek: parseInt(localStorage.getItem(STORAGE_KEYS.currentWeek) || '1')
    };
}

// İlerleme verilerini kaydetme
function saveProgress(type, value) {
    const progress = loadProgress();

    if (type === 'week' && !progress.weeks.includes(value)) {
        progress.weeks.push(value);
        localStorage.setItem(STORAGE_KEYS.completedWeeks, JSON.stringify(progress.weeks));
        addActivity(`Hafta ${value} tamamlandı! 🎉`);
    } else if (type === 'game' && !progress.games.includes(value)) {
        progress.games.push(value);
        localStorage.setItem(STORAGE_KEYS.completedGames, JSON.stringify(progress.games));
        addActivity(`${value} oyunu oynandı 🎮`);
    } else if (type === 'worksheet' && !progress.worksheets.includes(value)) {
        progress.worksheets.push(value);
        localStorage.setItem(STORAGE_KEYS.completedWorksheets, JSON.stringify(progress.worksheets));
        addActivity(`${value} çalışma sayfası tamamlandı 📝`);
    }

    updateDashboard();
    checkBadges();
}

// Aktivite ekleme
function addActivity(text) {
    const progress = loadProgress();
    const activity = {
        text: text,
        time: new Date().toLocaleDateString('tr-TR') + ' ' + new Date().toLocaleTimeString('tr-TR', {hour: '2-digit', minute: '2-digit'})
    };
    progress.activities.unshift(activity);
    if (progress.activities.length > 10) progress.activities = progress.activities.slice(0, 10);
    localStorage.setItem(STORAGE_KEYS.activities, JSON.stringify(progress.activities));
}

// Dashboard güncelleme
function updateDashboard() {
    const progress = loadProgress();

    // Element kontrolü
    const weeksEl = document.getElementById('completedWeeks');
    if (!weeksEl) return; // Dashboard açık değilse çık

    // İstatistikleri güncelle
    weeksEl.textContent = progress.weeks.length;
    document.getElementById('completedGames').textContent = progress.games.length;
    document.getElementById('completedWorksheets').textContent = progress.worksheets.length;

    // İlerleme çubuklarını güncelle
    const weeksPercent = (progress.weeks.length / 67) * 100;
    const gamesPercent = (progress.games.length / 67) * 100;
    const worksheetsPercent = (progress.worksheets.length / 67) * 100;
    const totalPercent = ((progress.weeks.length + progress.games.length + progress.worksheets.length) / 201) * 100;

    document.getElementById('weeksProgress').style.width = weeksPercent + '%';
    document.getElementById('gamesProgress').style.width = gamesPercent + '%';
    document.getElementById('worksheetsProgress').style.width = worksheetsPercent + '%';
    document.getElementById('totalProgress').textContent = Math.round(totalPercent) + '%';
    document.getElementById('totalProgressBar').style.width = totalPercent + '%';

    // Aktiviteleri güncelle
    updateActivities();
}

// Aktivite listesini güncelleme
function updateActivities() {
    const progress = loadProgress();
    const listDiv = document.getElementById('activityList');
    if (!listDiv) return;

    if (progress.activities.length === 0) {
        listDiv.innerHTML = '<div style="text-align: center; padding: 30px; color: #999;"><p>Henüz hiç aktivite yok. Öğrenmeye başla!</p></div>';
        return;
    }

    listDiv.innerHTML = progress.activities.map(activity => `
        <div class="activity-item">
            <strong>${activity.text}</strong>
            <div class="time">${activity.time}</div>
        </div>
    `).join('');
}

// Rozet kontrolleri
function checkBadges() {
    const progress = loadProgress();
    const badgeConditions = {
        badge1: progress.weeks.length >= 1,    // İlk hafta
        badge2: progress.games.length >= 5,    // 5 oyun
        badge3: progress.worksheets.length >= 10,  // 10 çalışma
        badge4: ((progress.weeks.length + progress.games.length + progress.worksheets.length) / 201) >= 0.5,  // %50
        badge5: progress.weeks.length >= 67 && progress.games.length >= 67 && progress.worksheets.length >= 67  // Tam
    };

    Object.keys(badgeConditions).forEach(badgeId => {
        const badge = document.getElementById(badgeId);
        if (badge && badgeConditions[badgeId] && badge.classList.contains('locked')) {
            badge.classList.remove('locked');
            badge.querySelector('span').textContent = '🏆';
            addActivity(`Yeni rozet kazanıldı: ${badge.textContent.split('-')[1].trim()} 🏅`);
        }
    });
}

// Bugünün görevini tamamlama
function markTaskComplete() {
    const progress = loadProgress();
    const currentWeek = progress.currentWeek;

    saveProgress('week', currentWeek);

    // Butonu güncelle
    const btn = document.getElementById('markCompleteBtn');
    btn.textContent = '✓ Tamamlandı!';
    btn.classList.add('completed');
    btn.disabled = true;

    // Bir sonraki haftaya geç
    const nextWeek = currentWeek + 1;
    if (nextWeek <= 67) {
        localStorage.setItem(STORAGE_KEYS.currentWeek, nextWeek);
        setTimeout(() => {
            updateTodayTask(nextWeek);
            btn.textContent = '✓ Tamamlandı Olarak İşaretle';
            btn.classList.remove('completed');
            btn.disabled = false;
        }, 2000);
    }
}

// Bugünün görevini güncelleme
function updateTodayTask(week) {
    const taskDesc = document.getElementById('taskDescription');
    if (!taskDesc) return;

    const weekTopics = {
        1: 'Bilişim Temelleri: Bilgisayar Bileşenleri',
        2: 'Bilişim Temelleri: İşletim Sistemleri',
        3: 'Bilişim Temelleri: Dosya Yönetimi',
        4: 'Bilişim Temelleri: Donanım',
        5: 'Dijital Ürün Tasarımı',
        // Daha fazla hafta ekleyebilirsiniz
    };
    taskDesc.textContent = `Hafta ${week} - ${weekTopics[week] || 'Yeni Konu'}`;
}

// İlerlemeyi sıfırlama
function resetProgress() {
    if (confirm('Tüm ilerlemenizi silmek istediğinizden emin misiniz? Bu işlem geri alınamaz!')) {
        Object.values(STORAGE_KEYS).forEach(key => localStorage.removeItem(key));
        location.reload();
    }
}

// İlerlemeyi dışa aktarma
function exportProgress() {
    const progress = loadProgress();
    const data = JSON.stringify(progress, null, 2);
    const blob = new Blob([data], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'bty_ilerleme_' + new Date().toISOString().split('T')[0] + '.json';
    a.click();
}

// ==================== SEARCH AND FILTER SYSTEM ====================
let currentFilter = 'all';

// Arama fonksiyonu
function performSearch() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    const searchTerm = searchInput.value.toLowerCase().trim();
    const allCards = document.querySelectorAll('#calisma .resource-card, #calisma .accordion');
    const resultsDiv = document.getElementById('searchResults');

    let matchCount = 0;

    allCards.forEach(card => {
        const cardText = card.textContent.toLowerCase();
        const matchesSearch = searchTerm === '' || cardText.includes(searchTerm);
        const matchesFilter = currentFilter === 'all' || checkFilter(card, currentFilter);

        if (matchesSearch && matchesFilter) {
            card.style.display = '';
            matchCount++;
        } else {
            card.style.display = 'none';
        }
    });

    if (resultsDiv) {
        if (searchTerm !== '' || currentFilter !== 'all') {
            resultsDiv.textContent = `📊 ${matchCount} sonuç bulundu`;
        } else {
            resultsDiv.textContent = '';
        }
    }
}

// Filtreleme kontrolü
function checkFilter(element, filter) {
    const text = element.textContent.toLowerCase();

    switch(filter) {
        case '5-sinif':
            return text.includes('5') || text.includes('5.sınıf') || text.includes('5. sınıf');
        case '6-sinif':
            return text.includes('6') || text.includes('6.sınıf') || text.includes('6. sınıf');
        case 'oyun':
            return text.includes('oyun') || text.includes('game') || element.querySelector('a[href*="oyun"]');
        case 'calisma':
            return text.includes('çalışma') || text.includes('worksheet') || element.querySelector('a[href*="calisma"]');
        case 'quiz':
            return text.includes('quiz') || element.querySelector('a[href*="quiz"]');
        default:
            return true;
    }
}

// Filtre uygulama
function filterContent(filter) {
    currentFilter = filter;

    // Filtre butonlarını güncelle
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    // event global değişken olarak erişilebilir
    if (window.event && window.event.target) {
        window.event.target.classList.add('active');
    }

    performSearch();
}

// ==================== INITIALIZATION ====================
// Sayfa yüklendiğinde dashboard'u güncelle
window.addEventListener('DOMContentLoaded', function() {
    updateDashboard();
    checkBadges();

    const progress = loadProgress();
    updateTodayTask(progress.currentWeek);

    // Accordion başlatma
    var firstAccordions = document.querySelectorAll('.accordion');
    if (firstAccordions.length > 0) {
        // İlk accordion'ı otomatik açabilirsiniz (opsiyonel)
        // firstAccordions[0].click();
    }
});
