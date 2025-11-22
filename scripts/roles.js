/**
 * BST Eğitim Portalı - Rol Bazlı Erişim Kontrolü
 */

const Roles = {
    // Rol tanımları
    GUEST: 'guest',
    STUDENT: 'student',
    TEACHER: 'teacher',
    ADMIN: 'admin',

    /**
     * Sayfa yüklendiğinde rol kontrolü yap
     */
    checkPageAccess() {
        const session = Auth.getSession();
        const currentPage = window.location.pathname.split('/').pop();

        // Giriş sayfasındaysa ve giriş yapılmışsa ana sayfaya yönlendir
        if (currentPage === 'giris.html' && session) {
            window.location.href = 'index.html';
            return;
        }

        // Admin sayfasındaysa ve admin değilse ana sayfaya yönlendir
        if (currentPage.includes('admin') && (!session || session.role !== this.ADMIN)) {
            window.location.href = '../index.html';
            return;
        }

        return true;
    },

    /**
     * Kullanıcı rolünü al
     */
    getUserRole() {
        const session = Auth.getSession();
        return session ? session.role : this.GUEST;
    },

    /**
     * Kullanıcının subscription durumunu al
     */
    getSubscriptionStatus() {
        const session = Auth.getSession();
        if (!session || session.role !== 'teacher') {
            return null;
        }
        return session.subscription || 'free';
    },

    /**
     * Belirli role sahip mi?
     */
    hasRole(role) {
        return this.getUserRole() === role;
    },

    /**
     * Birden fazla rolden birine sahip mi?
     */
    hasAnyRole(roles) {
        const userRole = this.getUserRole();
        return roles.includes(userRole);
    },

    /**
     * Öğretmen veya üstü mü?
     */
    isTeacherOrAbove() {
        return this.hasAnyRole([this.TEACHER, this.ADMIN]);
    },

    /**
     * Admin mi?
     */
    isAdmin() {
        return this.hasRole(this.ADMIN);
    },

    /**
     * Giriş yapmış mı?
     */
    isAuthenticated() {
        return this.getUserRole() !== this.GUEST;
    },

    /**
     * Sayfa elementlerini rol bazlı göster/gizle
     */
    applyRoleBasedVisibility() {
        const role = this.getUserRole();
        const subscription = this.getSubscriptionStatus();

        // Teacher-only elementler
        document.querySelectorAll('.teacher-only').forEach(el => {
            if (role === this.TEACHER || role === this.ADMIN) {
                el.style.display = el.dataset.originalDisplay || '';
            } else {
                // Original display değerini sakla
                if (!el.dataset.originalDisplay) {
                    const computed = window.getComputedStyle(el).display;
                    el.dataset.originalDisplay = computed !== 'none' ? computed : 'block';
                }
                el.style.display = 'none';
            }
        });

        // Admin-only elementler
        document.querySelectorAll('.admin-only').forEach(el => {
            if (role === this.ADMIN) {
                el.style.display = el.dataset.originalDisplay || '';
            } else {
                if (!el.dataset.originalDisplay) {
                    const computed = window.getComputedStyle(el).display;
                    el.dataset.originalDisplay = computed !== 'none' ? computed : 'block';
                }
                el.style.display = 'none';
            }
        });

        // Student-only elementler
        document.querySelectorAll('.student-only').forEach(el => {
            if (role === this.STUDENT) {
                el.style.display = el.dataset.originalDisplay || '';
            } else {
                if (!el.dataset.originalDisplay) {
                    const computed = window.getComputedStyle(el).display;
                    el.dataset.originalDisplay = computed !== 'none' ? computed : 'block';
                }
                el.style.display = 'none';
            }
        });

        // Auth-only (sadece giriş yapmış kullanıcılar)
        document.querySelectorAll('.auth-only').forEach(el => {
            if (this.isAuthenticated()) {
                el.style.display = el.dataset.originalDisplay || '';
            } else {
                if (!el.dataset.originalDisplay) {
                    const computed = window.getComputedStyle(el).display;
                    el.dataset.originalDisplay = computed !== 'none' ? computed : 'block';
                }
                el.style.display = 'none';
            }
        });

        // Guest-only (sadece misafirler)
        document.querySelectorAll('.guest-only').forEach(el => {
            if (!this.isAuthenticated()) {
                el.style.display = el.dataset.originalDisplay || '';
            } else {
                if (!el.dataset.originalDisplay) {
                    const computed = window.getComputedStyle(el).display;
                    el.dataset.originalDisplay = computed !== 'none' ? computed : 'block';
                }
                el.style.display = 'none';
            }
        });

        // Teacher-free-only (sadece ücretsiz öğretmenler)
        document.querySelectorAll('.teacher-free-only').forEach(el => {
            if (role === this.TEACHER && subscription === 'free') {
                el.style.display = el.dataset.originalDisplay || '';
            } else {
                if (!el.dataset.originalDisplay) {
                    const computed = window.getComputedStyle(el).display;
                    el.dataset.originalDisplay = computed !== 'none' ? computed : 'block';
                }
                el.style.display = 'none';
            }
        });

        // Teacher-premium-only (sadece premium öğretmenler)
        document.querySelectorAll('.teacher-premium-only').forEach(el => {
            if ((role === this.TEACHER && subscription === 'premium') || role === this.ADMIN) {
                el.style.display = el.dataset.originalDisplay || '';
            } else {
                if (!el.dataset.originalDisplay) {
                    const computed = window.getComputedStyle(el).display;
                    el.dataset.originalDisplay = computed !== 'none' ? computed : 'block';
                }
                el.style.display = 'none';
            }
        });
    },

    /**
     * Kullanıcı bilgilerini header'da göster
     */
    updateUserInfo() {
        const session = Auth.getSession();
        const userInfoEl = document.getElementById('userInfo');

        if (!userInfoEl) return;

        if (session) {
            const roleIcon = {
                'student': '👨‍🎓',
                'teacher': '👨‍🏫',
                'admin': '👑'
            }[session.role] || '👤';

            const roleName = {
                'student': 'Öğrenci',
                'teacher': 'Öğretmen',
                'admin': 'Admin'
            }[session.role] || 'Kullanıcı';

            userInfoEl.innerHTML = `
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-size: 0.9em;">
                        ${roleIcon} <strong>${session.name}</strong> (${roleName})
                    </span>
                    <button onclick="Auth.logout()" style="padding: 8px 16px; background: #dc3545; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em;">
                        🚪 Çıkış
                    </button>
                </div>
            `;
        } else {
            userInfoEl.innerHTML = `
                <a href="giris.html" style="padding: 8px 16px; background: #667eea; color: white; text-decoration: none; border-radius: 6px; font-size: 0.85em;">
                    🔐 Giriş Yap
                </a>
            `;
        }
    },

    /**
     * Tüm rol kontrollerini uygula
     */
    initialize() {
        this.checkPageAccess();
        this.applyRoleBasedVisibility();
        this.updateUserInfo();

        // Dinamik içerik değişikliklerini izle
        const observer = new MutationObserver(() => {
            this.applyRoleBasedVisibility();
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
};

// Sayfa yüklendiğinde rol kontrollerini uygula
if (typeof window !== 'undefined') {
    window.addEventListener('DOMContentLoaded', () => {
        Roles.initialize();
    });
}

// Global erişim
if (typeof window !== 'undefined') {
    window.Roles = Roles;
}
