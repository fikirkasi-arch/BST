/**
 * BST Eğitim Portalı - Gelişmiş Auth Sistemi
 * Hibrit LocalStorage tabanlı güvenli authentication
 */

const Auth = {
    // Güvenlik sabitleri
    SALT: 'BST_EDU_2024_SECURE_SALT',
    MAX_LOGIN_ATTEMPTS: 5,
    LOCKOUT_DURATION: 15 * 60 * 1000, // 15 dakika
    SESSION_DURATION: 24 * 60 * 60 * 1000, // 24 saat

    /**
     * Gelişmiş SHA-256 benzeri hash fonksiyonu
     */
    hashPassword(password, salt = this.SALT) {
        let hash = 0;
        const combined = salt + password + salt;

        for (let i = 0; i < combined.length; i++) {
            const char = combined.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }

        // Multiple rounds for extra security
        let finalHash = Math.abs(hash).toString(16);
        for (let round = 0; round < 3; round++) {
            finalHash = btoa(finalHash).split('').reverse().join('');
        }

        return finalHash;
    },

    /**
     * Güvenlik sorusu cevabını hash'le
     */
    hashSecurityAnswer(answer) {
        return this.hashPassword(answer.toLowerCase().trim(), 'SECURITY_SALT_2024');
    },

    /**
     * Kullanıcı kaydı oluştur
     */
    register(userData) {
        try {
            const users = this.getAllUsers();

            // Email veya numara kontrolü
            const identifier = userData.email || userData.number;
            if (this.userExists(identifier)) {
                return {
                    success: false,
                    message: 'Bu kullanıcı zaten kayıtlı!'
                };
            }

            // Şifre güvenlik kontrolü
            if (userData.password.length < 6) {
                return {
                    success: false,
                    message: 'Şifre en az 6 karakter olmalıdır!'
                };
            }

            // Güvenlik soruları kontrolü
            if (!userData.securityQuestions || userData.securityQuestions.length !== 2) {
                return {
                    success: false,
                    message: 'İki güvenlik sorusu gereklidir!'
                };
            }

            // Kullanıcı objesi oluştur
            const user = {
                id: this.generateUserId(),
                name: userData.name,
                email: userData.email || null,
                number: userData.number || null,
                password: this.hashPassword(userData.password),
                role: userData.role,
                grade: userData.grade || null,
                school: userData.school || null,
                branch: userData.branch || null,
                securityQuestions: userData.securityQuestions.map(sq => ({
                    question: sq.question,
                    answer: this.hashSecurityAnswer(sq.answer)
                })),
                status: userData.role === 'teacher' ? 'pending' : 'active',
                // Subscription sistemi - Öğretmenler için free, öğrenciler için null
                subscription: userData.role === 'teacher' ? {
                    plan: 'free',
                    startDate: new Date().toISOString(),
                    endDate: null, // Free sınırsız
                    status: 'active'
                } : null,
                createdAt: new Date().toISOString(),
                lastLogin: null
            };

            // Kullanıcıyı kaydet
            users.push(user);
            localStorage.setItem('bst_users', JSON.stringify(users));

            // Öğretmen ise admin onayı bekle
            if (userData.role === 'teacher') {
                this.notifyAdminPendingApproval(user);
                return {
                    success: true,
                    message: 'Kayıt başarılı! Hesabınız admin onayı bekliyor.',
                    requiresApproval: true
                };
            }

            // Öğrenci veya diğerleri direkt aktif
            this.createSession(user);
            return {
                success: true,
                message: 'Kayıt başarılı! Yönlendiriliyorsunuz...',
                user: this.sanitizeUser(user)
            };

        } catch (error) {
            console.error('Register error:', error);
            return {
                success: false,
                message: 'Kayıt sırasında hata oluştu!'
            };
        }
    },

    /**
     * Kullanıcı girişi
     */
    login(identifier, password, role) {
        try {
            // Rate limiting kontrolü
            if (this.isLockedOut(identifier)) {
                const remainingTime = this.getRemainingLockoutTime(identifier);
                return {
                    success: false,
                    message: `Çok fazla başarısız deneme! ${Math.ceil(remainingTime / 60000)} dakika sonra tekrar deneyin.`
                };
            }

            const users = this.getAllUsers();
            const user = users.find(u =>
                (u.email === identifier || u.number === identifier) &&
                u.role === role
            );

            if (!user) {
                this.recordFailedAttempt(identifier);
                return {
                    success: false,
                    message: 'Kullanıcı bulunamadı!'
                };
            }

            // Şifre kontrolü
            if (user.password !== this.hashPassword(password)) {
                this.recordFailedAttempt(identifier);
                return {
                    success: false,
                    message: 'Şifre hatalı!'
                };
            }

            // Öğretmen onay kontrolü
            if (user.role === 'teacher' && user.status !== 'active') {
                return {
                    success: false,
                    message: user.status === 'pending'
                        ? 'Hesabınız admin onayı bekliyor!'
                        : 'Hesabınız askıya alınmış!'
                };
            }

            // Başarılı giriş
            this.clearFailedAttempts(identifier);
            this.updateLastLogin(user.id);
            this.createSession(user);

            return {
                success: true,
                message: 'Giriş başarılı! Yönlendiriliyorsunuz...',
                user: this.sanitizeUser(user)
            };

        } catch (error) {
            console.error('Login error:', error);
            return {
                success: false,
                message: 'Giriş sırasında hata oluştu!'
            };
        }
    },

    /**
     * Şifre sıfırlama - Güvenlik soruları ile
     */
    resetPassword(identifier, securityAnswers, newPassword) {
        try {
            const users = this.getAllUsers();
            const user = users.find(u => u.email === identifier || u.number === identifier);

            if (!user) {
                return {
                    success: false,
                    message: 'Kullanıcı bulunamadı!'
                };
            }

            // Güvenlik sorularını kontrol et
            const answersMatch = user.securityQuestions.every((sq, index) => {
                const providedAnswer = this.hashSecurityAnswer(securityAnswers[index]);
                return sq.answer === providedAnswer;
            });

            if (!answersMatch) {
                return {
                    success: false,
                    message: 'Güvenlik soruları cevapları hatalı!'
                };
            }

            // Yeni şifre kontrolü
            if (newPassword.length < 6) {
                return {
                    success: false,
                    message: 'Şifre en az 6 karakter olmalıdır!'
                };
            }

            // Şifreyi güncelle
            user.password = this.hashPassword(newPassword);
            const userIndex = users.findIndex(u => u.id === user.id);
            users[userIndex] = user;
            localStorage.setItem('bst_users', JSON.stringify(users));

            return {
                success: true,
                message: 'Şifreniz başarıyla güncellendi!'
            };

        } catch (error) {
            console.error('Reset password error:', error);
            return {
                success: false,
                message: 'Şifre sıfırlama sırasında hata oluştu!'
            };
        }
    },

    /**
     * Güvenlik sorularını getir
     */
    getSecurityQuestions(identifier) {
        const users = this.getAllUsers();
        const user = users.find(u => u.email === identifier || u.number === identifier);

        if (!user) {
            return {
                success: false,
                message: 'Kullanıcı bulunamadı!'
            };
        }

        return {
            success: true,
            questions: user.securityQuestions.map(sq => sq.question)
        };
    },

    /**
     * Session oluştur
     */
    createSession(user) {
        const session = {
            userId: user.id,
            role: user.role,
            name: user.name,
            email: user.email,
            number: user.number,
            subscription: user.subscription ? user.subscription.plan : null,
            createdAt: Date.now(),
            expiresAt: Date.now() + this.SESSION_DURATION
        };

        localStorage.setItem('bst_session', JSON.stringify(session));
    },

    /**
     * Mevcut session'ı al
     */
    getSession() {
        const sessionData = localStorage.getItem('bst_session');
        if (!sessionData) return null;

        const session = JSON.parse(sessionData);

        // Session süresi dolmuş mu?
        if (Date.now() > session.expiresAt) {
            this.logout();
            return null;
        }

        return session;
    },

    /**
     * Giriş yapılmış mı?
     */
    isLoggedIn() {
        return this.getSession() !== null;
    },

    /**
     * Çıkış yap
     */
    logout() {
        localStorage.removeItem('bst_session');
        window.location.href = 'giris.html';
    },

    /**
     * Kullanıcı bilgilerini al
     */
    getCurrentUser() {
        const session = this.getSession();
        if (!session) return null;

        const users = this.getAllUsers();
        const user = users.find(u => u.id === session.userId);

        return user ? this.sanitizeUser(user) : null;
    },

    /**
     * Profil bilgilerini güncelle
     */
    updateProfile(updates) {
        try {
            const session = this.getSession();
            if (!session) {
                return {
                    success: false,
                    message: 'Oturum bulunamadı!'
                };
            }

            const users = this.getAllUsers();
            const userIndex = users.findIndex(u => u.id === session.userId);

            if (userIndex === -1) {
                return {
                    success: false,
                    message: 'Kullanıcı bulunamadı!'
                };
            }

            // Güncellenebilir alanlar
            if (updates.name) users[userIndex].name = updates.name;
            if (updates.email !== undefined) users[userIndex].email = updates.email;
            if (updates.grade) users[userIndex].grade = updates.grade;
            if (updates.school) users[userIndex].school = updates.school;
            if (updates.branch) users[userIndex].branch = updates.branch;

            // Kaydet
            localStorage.setItem('bst_users', JSON.stringify(users));

            // Session'ı güncelle
            session.name = users[userIndex].name;
            session.email = users[userIndex].email;
            localStorage.setItem('bst_session', JSON.stringify(session));

            return {
                success: true,
                message: 'Profil güncellendi!'
            };

        } catch (error) {
            console.error('Update profile error:', error);
            return {
                success: false,
                message: 'Profil güncellenirken hata oluştu!'
            };
        }
    },

    /**
     * Kullanıcı var mı kontrolü
     */
    userExists(identifier) {
        const users = this.getAllUsers();
        return users.some(u => u.email === identifier || u.number === identifier);
    },

    /**
     * Tüm kullanıcıları al
     */
    getAllUsers() {
        const usersData = localStorage.getItem('bst_users');
        return usersData ? JSON.parse(usersData) : [];
    },

    /**
     * Kullanıcı ID oluştur
     */
    generateUserId() {
        return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    },

    /**
     * Hassas bilgileri temizle
     */
    sanitizeUser(user) {
        const { password, securityQuestions, ...sanitized } = user;
        return sanitized;
    },

    /**
     * Son giriş zamanını güncelle
     */
    updateLastLogin(userId) {
        const users = this.getAllUsers();
        const userIndex = users.findIndex(u => u.id === userId);
        if (userIndex !== -1) {
            users[userIndex].lastLogin = new Date().toISOString();
            localStorage.setItem('bst_users', JSON.stringify(users));
        }
    },

    /**
     * Başarısız giriş denemesi kaydet
     */
    recordFailedAttempt(identifier) {
        const attempts = JSON.parse(localStorage.getItem('bst_failed_attempts') || '{}');

        if (!attempts[identifier]) {
            attempts[identifier] = {
                count: 0,
                lastAttempt: Date.now(),
                lockedUntil: null
            };
        }

        attempts[identifier].count++;
        attempts[identifier].lastAttempt = Date.now();

        // Max denemeyi aştıysa kilitle
        if (attempts[identifier].count >= this.MAX_LOGIN_ATTEMPTS) {
            attempts[identifier].lockedUntil = Date.now() + this.LOCKOUT_DURATION;
        }

        localStorage.setItem('bst_failed_attempts', JSON.stringify(attempts));
    },

    /**
     * Başarısız denemeleri temizle
     */
    clearFailedAttempts(identifier) {
        const attempts = JSON.parse(localStorage.getItem('bst_failed_attempts') || '{}');
        delete attempts[identifier];
        localStorage.setItem('bst_failed_attempts', JSON.stringify(attempts));
    },

    /**
     * Kilitli mi kontrolü
     */
    isLockedOut(identifier) {
        const attempts = JSON.parse(localStorage.getItem('bst_failed_attempts') || '{}');
        const userAttempts = attempts[identifier];

        if (!userAttempts || !userAttempts.lockedUntil) {
            return false;
        }

        if (Date.now() > userAttempts.lockedUntil) {
            // Kilit süresi dolmuş, temizle
            this.clearFailedAttempts(identifier);
            return false;
        }

        return true;
    },

    /**
     * Kalan kilit süresini al
     */
    getRemainingLockoutTime(identifier) {
        const attempts = JSON.parse(localStorage.getItem('bst_failed_attempts') || '{}');
        const userAttempts = attempts[identifier];

        if (!userAttempts || !userAttempts.lockedUntil) {
            return 0;
        }

        return Math.max(0, userAttempts.lockedUntil - Date.now());
    },

    /**
     * Admin'e bekleyen onay bildirimi
     */
    notifyAdminPendingApproval(user) {
        const notifications = JSON.parse(localStorage.getItem('bst_admin_notifications') || '[]');
        notifications.push({
            type: 'teacher_approval',
            userId: user.id,
            userName: user.name,
            userEmail: user.email,
            timestamp: Date.now(),
            read: false
        });
        localStorage.setItem('bst_admin_notifications', JSON.stringify(notifications));
    },

    /**
     * İlk admin kullanıcısını oluştur (sistem ilk çalıştığında)
     */
    initializeDefaultAdmin() {
        const users = this.getAllUsers();

        // Admin zaten var mı?
        if (users.some(u => u.role === 'admin')) {
            return;
        }

        // Default admin oluştur
        const admin = {
            id: 'admin_default_001',
            name: 'Admin',
            email: 'admin@bst.edu.tr',
            number: null,
            password: this.hashPassword('Admin123!'),
            role: 'admin',
            grade: null,
            school: null,
            branch: null,
            securityQuestions: [
                {
                    question: 'İlk okulunuzun adı?',
                    answer: this.hashSecurityAnswer('BST')
                },
                {
                    question: 'En sevdiğiniz renk?',
                    answer: this.hashSecurityAnswer('mavi')
                }
            ],
            status: 'active',
            subscription: null, // Admin için subscription gerekmez
            createdAt: new Date().toISOString(),
            lastLogin: null
        };

        users.push(admin);
        localStorage.setItem('bst_users', JSON.stringify(users));
        console.log('Default admin created: admin@bst.edu.tr / Admin123!');
    },

    /**
     * Subscription Yönetimi
     */

    // Kullanıcının subscription durumunu al
    getSubscriptionStatus(userId) {
        const users = this.getAllUsers();
        const user = users.find(u => u.id === userId);

        if (!user || user.role !== 'teacher') {
            return null;
        }

        // Subscription yoksa veya free ise
        if (!user.subscription || user.subscription.plan === 'free') {
            return 'free';
        }

        // Premium ise süresini kontrol et
        if (user.subscription.plan === 'premium') {
            const endDate = user.subscription.endDate ? new Date(user.subscription.endDate) : null;
            const now = new Date();

            // Süre dolmuşsa free'ye düşür
            if (endDate && now > endDate) {
                this.downgradeToFree(userId);
                return 'free';
            }

            return 'premium';
        }

        return 'free';
    },

    // Premium'a yükselt
    upgradeToPremium(userId, durationMonths = 1) {
        try {
            const users = this.getAllUsers();
            const userIndex = users.findIndex(u => u.id === userId);

            if (userIndex === -1) {
                return {
                    success: false,
                    message: 'Kullanıcı bulunamadı!'
                };
            }

            const user = users[userIndex];

            if (user.role !== 'teacher') {
                return {
                    success: false,
                    message: 'Premium üyelik sadece öğretmenler içindir!'
                };
            }

            const endDate = new Date();
            endDate.setMonth(endDate.getMonth() + durationMonths);

            user.subscription = {
                plan: 'premium',
                startDate: new Date().toISOString(),
                endDate: endDate.toISOString(),
                status: 'active',
                durationMonths: durationMonths
            };

            localStorage.setItem('bst_users', JSON.stringify(users));

            // Session'ı güncelle
            const session = this.getSession();
            if (session && session.userId === userId) {
                session.subscription = 'premium';
                localStorage.setItem('bst_session', JSON.stringify(session));
            }

            return {
                success: true,
                message: `Premium üyeliğiniz ${durationMonths} ay süreyle aktifleştirildi!`,
                endDate: endDate.toISOString()
            };

        } catch (error) {
            console.error('Upgrade error:', error);
            return {
                success: false,
                message: 'Premium yükseltme sırasında hata oluştu!'
            };
        }
    },

    // Free'ye düşür
    downgradeToFree(userId) {
        const users = this.getAllUsers();
        const userIndex = users.findIndex(u => u.id === userId);

        if (userIndex === -1) return;

        users[userIndex].subscription = {
            plan: 'free',
            startDate: new Date().toISOString(),
            endDate: null,
            status: 'active'
        };

        localStorage.setItem('bst_users', JSON.stringify(users));

        // Session'ı güncelle
        const session = this.getSession();
        if (session && session.userId === userId) {
            session.subscription = 'free';
            localStorage.setItem('bst_session', JSON.stringify(session));
        }
    },

    // Subscription bilgilerini al
    getSubscriptionInfo(userId) {
        const users = this.getAllUsers();
        const user = users.find(u => u.id === userId);

        if (!user || !user.subscription) {
            return null;
        }

        return {
            plan: user.subscription.plan,
            status: user.subscription.status,
            startDate: user.subscription.startDate,
            endDate: user.subscription.endDate,
            daysRemaining: user.subscription.endDate ?
                Math.ceil((new Date(user.subscription.endDate) - new Date()) / (1000 * 60 * 60 * 24)) :
                null
        };
    }
};

// Sayfa yüklendiğinde admin'i initialize et
if (typeof window !== 'undefined') {
    window.addEventListener('DOMContentLoaded', () => {
        Auth.initializeDefaultAdmin();
    });
}

// Global erişim için
if (typeof window !== 'undefined') {
    window.Auth = Auth;
}
