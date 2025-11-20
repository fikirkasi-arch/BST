// Admin Authentication System - BST Eğitim Portalı

const AdminAuth = {
    // Admin şifresi (hash olarak saklanmalı, şimdilik basit)
    ADMIN_PASSWORD: '877265',
    SESSION_KEY: 'bst_admin_session',
    SESSION_DURATION: 24 * 60 * 60 * 1000, // 24 saat

    // Giriş yap
    login(password) {
        if (password === this.ADMIN_PASSWORD) {
            const session = {
                loggedIn: true,
                loginTime: new Date().toISOString(),
                expiresAt: Date.now() + this.SESSION_DURATION
            };
            localStorage.setItem(this.SESSION_KEY, JSON.stringify(session));
            this.logActivity('Giriş yapıldı');
            return true;
        }
        return false;
    },

    // Çıkış yap
    logout() {
        this.logActivity('Çıkış yapıldı');
        localStorage.removeItem(this.SESSION_KEY);
        window.location.href = 'login.html';
    },

    // Oturum kontrolü
    isLoggedIn() {
        const session = this.getSession();
        if (!session) return false;

        // Oturum süresi kontrolü
        if (Date.now() > session.expiresAt) {
            this.logout();
            return false;
        }

        return session.loggedIn === true;
    },

    // Oturum bilgisi al
    getSession() {
        try {
            return JSON.parse(localStorage.getItem(this.SESSION_KEY));
        } catch {
            return null;
        }
    },

    // Sayfa koruma
    requireAuth() {
        if (!this.isLoggedIn()) {
            window.location.href = 'login.html';
            return false;
        }
        return true;
    },

    // Aktivite günlüğü
    logActivity(action) {
        const logs = JSON.parse(localStorage.getItem('bst_admin_logs') || '[]');
        logs.unshift({
            action,
            timestamp: new Date().toISOString(),
            date: new Date().toLocaleString('tr-TR')
        });
        // Son 100 aktiviteyi sakla
        if (logs.length > 100) logs.pop();
        localStorage.setItem('bst_admin_logs', JSON.stringify(logs));
    },

    // Aktivite günlüğünü al
    getActivityLogs() {
        return JSON.parse(localStorage.getItem('bst_admin_logs') || '[]');
    }
};

// Sayfa yüklendiğinde koruma kontrolü (login sayfası hariç)
document.addEventListener('DOMContentLoaded', () => {
    const isLoginPage = window.location.pathname.includes('login.html');

    if (!isLoginPage) {
        AdminAuth.requireAuth();
    }
});
