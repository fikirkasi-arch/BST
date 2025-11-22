/**
 * BST Eğitim Portalı - Kullanım Limiti Takip Sistemi
 * Free ve Premium öğretmenler için kullanım limitlerini yönetir
 */

const UsageLimits = {
    // Limitler
    LIMITS: {
        free: {
            examsPerMonth: 10,
            activitiesPerMonth: 5,
            studentsPerClass: 30
        },
        premium: {
            examsPerMonth: -1, // unlimited
            activitiesPerMonth: -1, // unlimited
            studentsPerClass: -1 // unlimited
        }
    },

    /**
     * Kullanıcının mevcut ay kullanımını al
     */
    getCurrentMonthUsage(userId) {
        const usage = JSON.parse(localStorage.getItem('bst_usage') || '{}');
        const currentMonth = new Date().toISOString().slice(0, 7); // "2025-11"

        if (!usage[userId]) {
            usage[userId] = {};
        }

        if (!usage[userId][currentMonth]) {
            usage[userId][currentMonth] = {
                exams: 0,
                activities: 0,
                students: 0
            };
        }

        return usage[userId][currentMonth];
    },

    /**
     * Kullanıcının limiti var mı kontrol et
     */
    checkLimit(userId, featureType) {
        const session = Auth.getSession();

        if (!session) {
            return { allowed: false, reason: 'Giriş yapılmamış' };
        }

        // Admin veya premium ise sınırsız
        if (session.role === 'admin' || session.subscription === 'premium') {
            return { allowed: true, remaining: -1 };
        }

        // Öğretmen değilse izin yok
        if (session.role !== 'teacher') {
            return { allowed: false, reason: 'Sadece öğretmenler için' };
        }

        // Free kullanıcı için limit kontrolü
        const usage = this.getCurrentMonthUsage(userId);
        const limits = this.LIMITS.free;

        let limit, current;
        switch (featureType) {
            case 'exam':
                limit = limits.examsPerMonth;
                current = usage.exams || 0;
                break;
            case 'activity':
                limit = limits.activitiesPerMonth;
                current = usage.activities || 0;
                break;
            case 'student':
                limit = limits.studentsPerClass;
                current = usage.students || 0;
                break;
            default:
                return { allowed: false, reason: 'Geçersiz özellik tipi' };
        }

        if (current >= limit) {
            return {
                allowed: false,
                reason: 'Aylık limit doldu',
                limit: limit,
                current: current,
                remaining: 0
            };
        }

        return {
            allowed: true,
            limit: limit,
            current: current,
            remaining: limit - current
        };
    },

    /**
     * Kullanımı artır
     */
    incrementUsage(userId, featureType) {
        const usage = JSON.parse(localStorage.getItem('bst_usage') || '{}');
        const currentMonth = new Date().toISOString().slice(0, 7);

        if (!usage[userId]) {
            usage[userId] = {};
        }

        if (!usage[userId][currentMonth]) {
            usage[userId][currentMonth] = {
                exams: 0,
                activities: 0,
                students: 0
            };
        }

        switch (featureType) {
            case 'exam':
                usage[userId][currentMonth].exams++;
                break;
            case 'activity':
                usage[userId][currentMonth].activities++;
                break;
            case 'student':
                usage[userId][currentMonth].students++;
                break;
        }

        localStorage.setItem('bst_usage', JSON.stringify(usage));

        return usage[userId][currentMonth];
    },

    /**
     * Kullanım istatistiklerini al
     */
    getUsageStats(userId) {
        const session = Auth.getSession();
        if (!session) return null;

        const usage = this.getCurrentMonthUsage(userId);
        const subscription = session.subscription || 'free';
        const limits = this.LIMITS[subscription];

        return {
            subscription: subscription,
            exams: {
                used: usage.exams || 0,
                limit: limits.examsPerMonth,
                remaining: limits.examsPerMonth === -1 ? -1 : limits.examsPerMonth - (usage.exams || 0),
                percentage: limits.examsPerMonth === -1 ? 0 : ((usage.exams || 0) / limits.examsPerMonth) * 100
            },
            activities: {
                used: usage.activities || 0,
                limit: limits.activitiesPerMonth,
                remaining: limits.activitiesPerMonth === -1 ? -1 : limits.activitiesPerMonth - (usage.activities || 0),
                percentage: limits.activitiesPerMonth === -1 ? 0 : ((usage.activities || 0) / limits.activitiesPerMonth) * 100
            },
            students: {
                used: usage.students || 0,
                limit: limits.studentsPerClass,
                remaining: limits.studentsPerClass === -1 ? -1 : limits.studentsPerClass - (usage.students || 0),
                percentage: limits.studentsPerClass === -1 ? 0 : ((usage.students || 0) / limits.studentsPerClass) * 100
            }
        };
    },

    /**
     * Limit uyarı mesajı oluştur
     */
    getLimitWarningHTML(featureType) {
        const session = Auth.getSession();
        if (!session) return '';

        const check = this.checkLimit(session.userId, featureType);

        if (check.allowed && check.remaining <= 2 && check.remaining > 0) {
            // Limite yaklaşılıyor uyarısı
            return `
                <div class="limit-warning" style="margin: 20px 0;">
                    <div class="icon">⚠️</div>
                    <div class="content">
                        <h4>Limite Yaklaşıyorsunuz!</h4>
                        <p>Bu ay ${check.limit} ${featureType === 'exam' ? 'sınav' : 'etkinlik'} oluşturabilirsiniz. ${check.remaining} hakkınız kaldı.</p>
                    </div>
                    <button onclick="showPremiumModal()">Premium'a Geç</button>
                </div>
            `;
        } else if (!check.allowed) {
            // Limit doldu uyarısı
            return `
                <div class="limit-warning" style="margin: 20px 0; border-color: #dc3545;">
                    <div class="icon">🔒</div>
                    <div class="content">
                        <h4>Aylık Limitiniz Doldu!</h4>
                        <p>Ücretsiz üyelikle ayda ${check.limit} ${featureType === 'exam' ? 'sınav' : 'etkinlik'} oluşturabilirsiniz. Premium üyelikle sınırsız kullanım!</p>
                    </div>
                    <button onclick="showPremiumModal()">Premium'a Geç</button>
                </div>
            `;
        }

        return '';
    },

    /**
     * Kullanım dashboard'u için HTML
     */
    getUsageDashboardHTML(userId) {
        const stats = this.getUsageStats(userId);
        if (!stats) return '';

        const isPremium = stats.subscription === 'premium';

        return `
            <div style="background: white; padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                    📊 Kullanım İstatistikleri
                    ${isPremium ? '<span class="premium-badge">⭐ Premium</span>' : '<span style="color: #28a745; font-size: 0.85em;">(Ücretsiz)</span>'}
                </h3>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <!-- Sınav Kullanımı -->
                    <div style="padding: 15px; background: #f8f9fa; border-radius: 10px;">
                        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">Sınav Oluşturma</div>
                        <div style="font-size: 1.5em; font-weight: 600; color: #667eea;">
                            ${stats.exams.used}${stats.exams.limit === -1 ? '' : ` / ${stats.exams.limit}`}
                        </div>
                        ${stats.exams.limit !== -1 ? `
                            <div style="margin-top: 8px; background: #e0e0e0; height: 6px; border-radius: 3px; overflow: hidden;">
                                <div style="width: ${Math.min(stats.exams.percentage, 100)}%; height: 100%; background: ${stats.exams.percentage > 80 ? '#dc3545' : '#28a745'}; transition: width 0.3s;"></div>
                            </div>
                        ` : '<div style="margin-top: 8px; color: #28a745; font-weight: 600;">✓ Sınırsız</div>'}
                    </div>

                    <!-- Etkinlik Kullanımı -->
                    <div style="padding: 15px; background: #f8f9fa; border-radius: 10px;">
                        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">Etkinlik Oluşturma</div>
                        <div style="font-size: 1.5em; font-weight: 600; color: #f093fb;">
                            ${stats.activities.used}${stats.activities.limit === -1 ? '' : ` / ${stats.activities.limit}`}
                        </div>
                        ${stats.activities.limit !== -1 ? `
                            <div style="margin-top: 8px; background: #e0e0e0; height: 6px; border-radius: 3px; overflow: hidden;">
                                <div style="width: ${Math.min(stats.activities.percentage, 100)}%; height: 100%; background: ${stats.activities.percentage > 80 ? '#dc3545' : '#28a745'}; transition: width 0.3s;"></div>
                            </div>
                        ` : '<div style="margin-top: 8px; color: #28a745; font-weight: 600;">✓ Sınırsız</div>'}
                    </div>
                </div>

                ${!isPremium ? `
                    <div style="margin-top: 15px; padding: 15px; background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%); border-radius: 10px; text-align: center;">
                        <p style="margin: 0 0 10px 0; color: #856404; font-weight: 600;">⭐ Premium ile Sınırsız Kullanım!</p>
                        <button onclick="showPremiumModal()" style="padding: 10px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">
                            Premium'a Geç
                        </button>
                    </div>
                ` : ''}
            </div>
        `;
    }
};

// Global erişim için
if (typeof window !== 'undefined') {
    window.UsageLimits = UsageLimits;
}
