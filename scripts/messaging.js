/**
 * BST Eğitim Portalı - Mesajlaşma Sistemi
 * Kullanıcıların admin'e mesaj göndermesini sağlar
 * Küfür filtresi ve güvenlik kontrolleri içerir
 */

const Messaging = {
    // Konfigürasyon
    MAX_MESSAGE_LENGTH: 1000,
    MIN_MESSAGE_LENGTH: 10,
    MAX_SUBJECT_LENGTH: 100,
    COOLDOWN_MINUTES: 5, // Mesajlar arası minimum süre

    // Küfür listesi (Türkçe yaygın küfürler)
    PROFANITY_WORDS: [
        'amk', 'amq', 'aq', 'mk', 'mq',
        's.ktir', 's.k', 'sik',
        'orospu', 'o.rospu', 'orsp',
        'pezeveng', 'p.zeveng',
        'salak', 'aptal', 'gerizekalı',
        'mal', 'dangalak', 'ahmak'
    ],

    // Tehlikeli pattern'ler (XSS, SQL Injection vb.)
    DANGEROUS_PATTERNS: [
        /<script/i,
        /javascript:/i,
        /on\w+=/i, // onclick, onload vb.
        /<iframe/i,
        /eval\(/i,
        /expression\(/i,
        /vbscript:/i,
        /drop\s+table/i,
        /insert\s+into/i,
        /delete\s+from/i,
        /update\s+\w+\s+set/i,
        /union\s+select/i,
        /--/,
        /;--/,
        /\/\*/
    ],

    /**
     * Metni temizle (sanitize)
     */
    sanitizeText(text) {
        if (!text) return '';

        // HTML karakterlerini escape et
        const div = document.createElement('div');
        div.textContent = text;
        let sanitized = div.innerHTML;

        // Fazla boşlukları temizle
        sanitized = sanitized.trim().replace(/\s+/g, ' ');

        return sanitized;
    },

    /**
     * Küfür kontrolü
     */
    containsProfanity(text) {
        if (!text) return false;

        const lowerText = text.toLowerCase();

        // Noktalama işaretlerini ve boşlukları kaldır
        const cleanText = lowerText.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()\s]/g, '');

        // Küfür kelimelerini kontrol et
        for (const word of this.PROFANITY_WORDS) {
            if (cleanText.includes(word)) {
                return true;
            }
        }

        return false;
    },

    /**
     * Güvenlik tehditlerini kontrol et
     */
    containsSecurityThreat(text) {
        if (!text) return false;

        for (const pattern of this.DANGEROUS_PATTERNS) {
            if (pattern.test(text)) {
                return true;
            }
        }

        return false;
    },

    /**
     * Spam kontrolü (aynı mesajı kısa sürede tekrar gönderme)
     */
    isSpam(userId, messageContent) {
        const messages = this.getUserMessages(userId);

        // Son 5 dakikadaki mesajları kontrol et
        const fiveMinutesAgo = Date.now() - (this.COOLDOWN_MINUTES * 60 * 1000);
        const recentMessages = messages.filter(m => m.timestamp > fiveMinutesAgo);

        // Aynı içerik var mı?
        const duplicate = recentMessages.find(m => m.content === messageContent);
        if (duplicate) {
            return true;
        }

        // Çok fazla mesaj gönderilmiş mi? (5 dakikada 3'ten fazla)
        if (recentMessages.length >= 3) {
            return true;
        }

        return false;
    },

    /**
     * Mesaj validasyonu
     */
    validateMessage(messageData) {
        const errors = [];

        // Konu kontrolü
        if (!messageData.subject || messageData.subject.trim().length === 0) {
            errors.push('Konu başlığı boş bırakılamaz!');
        } else if (messageData.subject.length > this.MAX_SUBJECT_LENGTH) {
            errors.push(`Konu başlığı en fazla ${this.MAX_SUBJECT_LENGTH} karakter olabilir!`);
        }

        // İçerik kontrolü
        if (!messageData.content || messageData.content.trim().length === 0) {
            errors.push('Mesaj içeriği boş bırakılamaz!');
        } else if (messageData.content.length < this.MIN_MESSAGE_LENGTH) {
            errors.push(`Mesaj en az ${this.MIN_MESSAGE_LENGTH} karakter olmalıdır!`);
        } else if (messageData.content.length > this.MAX_MESSAGE_LENGTH) {
            errors.push(`Mesaj en fazla ${this.MAX_MESSAGE_LENGTH} karakter olabilir!`);
        }

        // Küfür kontrolü
        if (this.containsProfanity(messageData.subject) || this.containsProfanity(messageData.content)) {
            errors.push('Mesajınız uygunsuz içerik barındırıyor!');
        }

        // Güvenlik tehdidi kontrolü
        if (this.containsSecurityThreat(messageData.subject) || this.containsSecurityThreat(messageData.content)) {
            errors.push('Mesajınız güvenlik kurallarına uygun değil!');
        }

        // Spam kontrolü
        if (messageData.userId && this.isSpam(messageData.userId, messageData.content)) {
            errors.push(`Lütfen mesajlar arasında en az ${this.COOLDOWN_MINUTES} dakika bekleyin!`);
        }

        return {
            isValid: errors.length === 0,
            errors: errors
        };
    },

    /**
     * Mesaj gönder
     */
    sendMessage(messageData) {
        try {
            const session = Auth.getSession();
            if (!session) {
                return {
                    success: false,
                    message: 'Mesaj göndermek için giriş yapmalısınız!'
                };
            }

            // Mesajı temizle
            const cleanMessage = {
                subject: this.sanitizeText(messageData.subject),
                content: this.sanitizeText(messageData.content),
                userId: session.userId,
                userName: session.name,
                userEmail: session.email || session.number,
                userRole: session.role
            };

            // Validate
            const validation = this.validateMessage(cleanMessage);
            if (!validation.isValid) {
                return {
                    success: false,
                    message: validation.errors.join('\n')
                };
            }

            // Mesajı kaydet
            const messages = JSON.parse(localStorage.getItem('bst_messages') || '[]');

            const newMessage = {
                id: this.generateMessageId(),
                ...cleanMessage,
                timestamp: Date.now(),
                read: false,
                replied: false,
                reply: null
            };

            messages.push(newMessage);
            localStorage.setItem('bst_messages', JSON.stringify(messages));

            // Admin'e bildirim gönder
            this.notifyAdmin(newMessage);

            return {
                success: true,
                message: 'Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapılacaktır.'
            };

        } catch (error) {
            console.error('Send message error:', error);
            return {
                success: false,
                message: 'Mesaj gönderilirken hata oluştu!'
            };
        }
    },

    /**
     * Kullanıcının mesajlarını al
     */
    getUserMessages(userId) {
        const messages = JSON.parse(localStorage.getItem('bst_messages') || '[]');
        return messages.filter(m => m.userId === userId).sort((a, b) => b.timestamp - a.timestamp);
    },

    /**
     * Tüm mesajları al (Admin için)
     */
    getAllMessages() {
        const messages = JSON.parse(localStorage.getItem('bst_messages') || '[]');
        return messages.sort((a, b) => b.timestamp - a.timestamp);
    },

    /**
     * Okunmamış mesaj sayısı (Admin için)
     */
    getUnreadCount() {
        const messages = JSON.parse(localStorage.getItem('bst_messages') || '[]');
        return messages.filter(m => !m.read).length;
    },

    /**
     * Mesajı okundu olarak işaretle
     */
    markAsRead(messageId) {
        const messages = JSON.parse(localStorage.getItem('bst_messages') || '[]');
        const message = messages.find(m => m.id === messageId);

        if (message) {
            message.read = true;
            localStorage.setItem('bst_messages', JSON.stringify(messages));
        }
    },

    /**
     * Mesaja cevap ver (Admin için)
     */
    replyToMessage(messageId, replyContent) {
        try {
            const session = Auth.getSession();
            if (!session || session.role !== 'admin') {
                return {
                    success: false,
                    message: 'Bu işlem için admin yetkisi gereklidir!'
                };
            }

            const messages = JSON.parse(localStorage.getItem('bst_messages') || '[]');
            const message = messages.find(m => m.id === messageId);

            if (!message) {
                return {
                    success: false,
                    message: 'Mesaj bulunamadı!'
                };
            }

            // Cevabı temizle
            const cleanReply = this.sanitizeText(replyContent);

            if (cleanReply.length < 5) {
                return {
                    success: false,
                    message: 'Cevap en az 5 karakter olmalıdır!'
                };
            }

            message.reply = {
                content: cleanReply,
                adminName: session.name,
                timestamp: Date.now()
            };
            message.replied = true;
            message.read = true;

            localStorage.setItem('bst_messages', JSON.stringify(messages));

            return {
                success: true,
                message: 'Cevap başarıyla gönderildi!'
            };

        } catch (error) {
            console.error('Reply error:', error);
            return {
                success: false,
                message: 'Cevap gönderilirken hata oluştu!'
            };
        }
    },

    /**
     * Mesajı sil (Admin için)
     */
    deleteMessage(messageId) {
        const session = Auth.getSession();
        if (!session || session.role !== 'admin') {
            return {
                success: false,
                message: 'Bu işlem için admin yetkisi gereklidir!'
            };
        }

        let messages = JSON.parse(localStorage.getItem('bst_messages') || '[]');
        messages = messages.filter(m => m.id !== messageId);
        localStorage.setItem('bst_messages', JSON.stringify(messages));

        return {
            success: true,
            message: 'Mesaj silindi!'
        };
    },

    /**
     * Mesaj ID oluştur
     */
    generateMessageId() {
        return 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    },

    /**
     * Admin'e bildirim gönder
     */
    notifyAdmin(message) {
        const notifications = JSON.parse(localStorage.getItem('bst_admin_notifications') || '[]');

        notifications.push({
            type: 'message',
            messageId: message.id,
            title: 'Yeni Mesaj',
            content: `${message.userName} bir mesaj gönderdi: ${message.subject}`,
            timestamp: Date.now(),
            read: false
        });

        localStorage.setItem('bst_admin_notifications', JSON.stringify(notifications));
    },

    /**
     * Mesaj formatla (görüntüleme için)
     */
    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);

        if (days > 0) {
            return `${days} gün önce`;
        } else if (hours > 0) {
            return `${hours} saat önce`;
        } else if (minutes > 0) {
            return `${minutes} dakika önce`;
        } else {
            return 'Az önce';
        }
    }
};

// Global erişim için
if (typeof window !== 'undefined') {
    window.Messaging = Messaging;
}
