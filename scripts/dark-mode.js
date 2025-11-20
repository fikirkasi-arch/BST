// Dark Mode - BST Eğitim Portalı
// Dark mode toggle ve tema yönetimi

const DarkMode = {
    // Dark mode durumunu kontrol et
    isDarkMode() {
        return localStorage.getItem('darkMode') === 'enabled';
    },

    // Dark mode'u aktif et
    enable() {
        document.body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'enabled');
        this.updateToggleButton();
        this.logChange('enabled');
    },

    // Dark mode'u devre dışı bırak
    disable() {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'disabled');
        this.updateToggleButton();
        this.logChange('disabled');
    },

    // Toggle - açık/kapalı değiştir
    toggle() {
        if (this.isDarkMode()) {
            this.disable();
        } else {
            this.enable();
        }
    },

    // Toggle butonunu güncelle
    updateToggleButton() {
        const toggleBtn = document.getElementById('darkModeToggle');
        if (toggleBtn) {
            if (this.isDarkMode()) {
                toggleBtn.innerHTML = '☀️ Light Mode';
                toggleBtn.setAttribute('aria-label', 'Light moda geç');
            } else {
                toggleBtn.innerHTML = '🌙 Dark Mode';
                toggleBtn.setAttribute('aria-label', 'Dark moda geç');
            }
        }
    },

    // Değişikliği logla
    logChange(mode) {
        if (typeof BSTAnalytics !== 'undefined') {
            BSTAnalytics.logActivity('dark_mode', {
                mode: mode,
                timestamp: new Date().toISOString()
            });
        }
    },

    // Dark mode CSS'ini ekle
    injectStyles() {
        const styleId = 'dark-mode-styles';
        if (document.getElementById(styleId)) return;

        const style = document.createElement('style');
        style.id = styleId;
        style.textContent = `
            /* Dark Mode Styles */
            body.dark-mode {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
                color: #e0e0e0 !important;
            }

            body.dark-mode .container {
                background: #0f3460 !important;
                color: #e0e0e0 !important;
            }

            body.dark-mode header {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
            }

            body.dark-mode .tabs {
                background: #16213e !important;
                border-bottom-color: #533483 !important;
            }

            body.dark-mode .tab {
                color: #b0b0b0 !important;
            }

            body.dark-mode .tab:hover {
                background: #1a1a2e !important;
            }

            body.dark-mode .tab.active {
                background: #0f3460 !important;
                color: #bb86fc !important;
                border-bottom-color: #bb86fc !important;
            }

            body.dark-mode .tab-content {
                background: #0f3460 !important;
                color: #e0e0e0 !important;
            }

            body.dark-mode .grade-btn {
                background: linear-gradient(135deg, #533483 0%, #1a1a2e 100%) !important;
                color: #e0e0e0 !important;
                border-color: #bb86fc !important;
            }

            body.dark-mode .grade-btn:hover {
                background: linear-gradient(135deg, #bb86fc 0%, #7b2cbf 100%) !important;
                box-shadow: 0 8px 25px rgba(187, 134, 252, 0.3) !important;
            }

            body.dark-mode .unit-card {
                background: #16213e !important;
                color: #e0e0e0 !important;
                border: 2px solid #533483 !important;
            }

            body.dark-mode .unit-card:hover {
                background: #1a1a2e !important;
                border-color: #bb86fc !important;
                box-shadow: 0 10px 30px rgba(187, 134, 252, 0.3) !important;
            }

            body.dark-mode .unit-title {
                color: #bb86fc !important;
            }

            body.dark-mode .modal-content {
                background: #16213e !important;
                color: #e0e0e0 !important;
            }

            body.dark-mode .close {
                color: #e0e0e0 !important;
            }

            body.dark-mode .close:hover {
                color: #bb86fc !important;
            }

            body.dark-mode h2,
            body.dark-mode h3 {
                color: #bb86fc !important;
            }

            body.dark-mode p {
                color: #b0b0b0 !important;
            }

            body.dark-mode .quiz-container,
            body.dark-mode .game-card,
            body.dark-mode .stat-card,
            body.dark-mode .badge-card {
                background: #16213e !important;
                color: #e0e0e0 !important;
                border: 1px solid #533483 !important;
            }

            body.dark-mode .quiz-container:hover,
            body.dark-mode .game-card:hover,
            body.dark-mode .stat-card:hover {
                box-shadow: 0 10px 30px rgba(187, 134, 252, 0.2) !important;
            }

            body.dark-mode .option {
                background: #0f3460 !important;
                border-color: #533483 !important;
                color: #e0e0e0 !important;
            }

            body.dark-mode .option:hover {
                background: #1a1a2e !important;
                border-color: #bb86fc !important;
            }

            body.dark-mode .btn-primary {
                background: linear-gradient(135deg, #533483 0%, #7b2cbf 100%) !important;
            }

            body.dark-mode .btn-secondary {
                background: #1a1a2e !important;
                color: #e0e0e0 !important;
            }

            body.dark-mode input,
            body.dark-mode textarea,
            body.dark-mode select {
                background: #1a1a2e !important;
                color: #e0e0e0 !important;
                border-color: #533483 !important;
            }

            body.dark-mode input:focus,
            body.dark-mode textarea:focus,
            body.dark-mode select:focus {
                border-color: #bb86fc !important;
                box-shadow: 0 0 10px rgba(187, 134, 252, 0.3) !important;
            }

            /* Header navigation buttons in dark mode */
            body.dark-mode .header-nav-btn {
                background: rgba(187, 134, 252, 0.2) !important;
                border-color: rgba(187, 134, 252, 0.4) !important;
            }

            body.dark-mode .header-nav-btn:hover {
                background: rgba(187, 134, 252, 0.3) !important;
                border-color: rgba(187, 134, 252, 0.6) !important;
            }

            body.dark-mode .header-nav-btn.search-btn {
                background: rgba(255, 215, 0, 0.2) !important;
                border-color: rgba(255, 215, 0, 0.4) !important;
            }

            body.dark-mode .header-nav-btn.search-btn:hover {
                background: rgba(255, 215, 0, 0.3) !important;
            }

            /* Smooth transition */
            body {
                transition: background 0.3s ease, color 0.3s ease;
            }

            .container,
            .tab-content,
            .grade-btn,
            .unit-card {
                transition: background 0.3s ease, color 0.3s ease, border-color 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    },

    // Sayfa yüklendiğinde başlat
    init() {
        // CSS'i ekle
        this.injectStyles();

        // Kaydedilmiş tercihi uygula
        if (this.isDarkMode()) {
            document.body.classList.add('dark-mode');
        }

        // Toggle butonunu güncelle
        this.updateToggleButton();

        // Toggle butonuna event listener ekle
        const toggleBtn = document.getElementById('darkModeToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                this.toggle();
            });
        }

        // Klavye kısayolu (Ctrl+Shift+D)
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'D') {
                e.preventDefault();
                this.toggle();
            }
        });
    }
};

// Sayfa yüklendiğinde dark mode'u başlat
document.addEventListener('DOMContentLoaded', () => {
    DarkMode.init();
});
