// Konu Haritası (Mind Map) Sistemi
const BSTTopicMap = {
    // Konu haritası verisi
    topicData: {
        '5': {
            name: '5. Sınıf Bilişim',
            children: [
                {
                    name: 'Bilişim Temelleri',
                    children: [
                        { name: 'Donanım', emoji: '💻' },
                        { name: 'Yazılım', emoji: '📱' },
                        { name: 'İşletim Sistemi', emoji: '🖥️' },
                        { name: 'Dosya Yönetimi', emoji: '📁' }
                    ],
                    color: '#f5576c',
                    emoji: '📱'
                },
                {
                    name: 'Dijital Ürün Tasarımı',
                    children: [
                        { name: 'Word', emoji: '📝' },
                        { name: 'Paint', emoji: '🎨' },
                        { name: 'PowerPoint', emoji: '📊' }
                    ],
                    color: '#fccb90',
                    emoji: '🎨'
                },
                {
                    name: 'Ağlar ve İletişim',
                    children: [
                        { name: 'İnternet', emoji: '🌐' },
                        { name: 'E-posta', emoji: '📧' },
                        { name: 'Tarayıcı', emoji: '🔍' }
                    ],
                    color: '#4facfe',
                    emoji: '🌐'
                },
                {
                    name: 'Etik ve Güvenlik',
                    children: [
                        { name: 'Dijital Etik', emoji: '⚖️' },
                        { name: 'Şifre Güvenliği', emoji: '🔐' },
                        { name: 'Siber Zorbalık', emoji: '🛡️' }
                    ],
                    color: '#667eea',
                    emoji: '🛡️'
                },
                {
                    name: 'Yapay Zeka',
                    children: [
                        { name: 'AI Kavramı', emoji: '🤖' },
                        { name: 'Makine Öğrenmesi', emoji: '🧠' },
                        { name: 'Otomasyon', emoji: '⚙️' }
                    ],
                    color: '#43e97b',
                    emoji: '🤖'
                },
                {
                    name: 'Scratch Programlama',
                    children: [
                        { name: 'Blok Kodlama', emoji: '🧩' },
                        { name: 'Döngüler', emoji: '🔄' },
                        { name: 'Koşullar', emoji: '❓' },
                        { name: 'Oyun Yapımı', emoji: '🎮' }
                    ],
                    color: '#764ba2',
                    emoji: '💻'
                }
            ]
        },
        '6': {
            name: '6. Sınıf Bilişim',
            children: [
                {
                    name: 'Bilişim Teknolojileri',
                    children: [
                        { name: 'Tarihçe', emoji: '📜' },
                        { name: 'İkili Sayı', emoji: '01' },
                        { name: 'Bulut Bilişim', emoji: '☁️' }
                    ],
                    color: '#4facfe',
                    emoji: '💾'
                },
                {
                    name: 'Etik ve Güvenlik',
                    children: [
                        { name: 'KVKK', emoji: '📜' },
                        { name: 'Phishing', emoji: '🎣' },
                        { name: '2FA', emoji: '🔐' }
                    ],
                    color: '#43e97b',
                    emoji: '🛡️'
                },
                {
                    name: 'İletişim ve İşbirliği',
                    children: [
                        { name: 'Video Konferans', emoji: '📹' },
                        { name: 'Bulut Depolama', emoji: '💾' },
                        { name: 'Ortak Belgeler', emoji: '📄' }
                    ],
                    color: '#764ba2',
                    emoji: '📡'
                },
                {
                    name: 'Ürün Oluşturma',
                    children: [
                        { name: 'Grafik Tasarım', emoji: '🎨' },
                        { name: 'Video Düzenleme', emoji: '🎬' },
                        { name: 'Podcast', emoji: '🎙️' }
                    ],
                    color: '#d57eeb',
                    emoji: '🎬'
                },
                {
                    name: 'Problem Çözme',
                    children: [
                        { name: 'Python', emoji: '🐍' },
                        { name: 'Algoritma', emoji: '📊' },
                        { name: 'Fonksiyonlar', emoji: '⚙️' }
                    ],
                    color: '#f5576c',
                    emoji: '🧩'
                }
            ]
        }
    },

    // Konu haritası modal'ını göster
    showTopicMap(gradeLevel) {
        const data = this.topicData[gradeLevel];

        if (!data) {
            console.error('Konu haritası bulunamadı:', gradeLevel);
            return;
        }

        const modal = document.createElement('div');
        modal.id = 'topic-map-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        `;

        const content = this.generateMapHTML(data, gradeLevel);

        modal.innerHTML = `
            <div style="background: white; border-radius: 20px; max-width: 1200px; width: 100%; max-height: 85vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.4);">
                <div style="position: sticky; top: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 20px 20px 0 0; z-index: 1; display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="margin: 0; color: white;">🗺️ ${data.name} Konu Haritası</h2>
                    <button onclick="this.closest('#topic-map-modal').remove()" style="background: rgba(255,255,255,0.2); border: none; color: white; font-size: 1.5em; cursor: pointer; width: 40px; height: 40px; border-radius: 50%;">✖</button>
                </div>
                <div style="padding: 40px;">
                    ${content}
                </div>
            </div>
        `;

        // Modal dışına tıklanınca kapat
        modal.onclick = (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        };

        document.body.appendChild(modal);
    },

    // Harita HTML'ini oluştur
    generateMapHTML(data, gradeLevel) {
        let html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px;">';

        data.children.forEach((unit, index) => {
            html += `
                <div style="background: linear-gradient(135deg, ${unit.color}15, ${unit.color}30); border: 3px solid ${unit.color}; border-radius: 15px; padding: 25px; position: relative; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    <div style="font-size: 3em; text-align: center; margin-bottom: 15px;">${unit.emoji}</div>
                    <h3 style="text-align: center; color: ${unit.color}; margin-bottom: 20px; font-size: 1.2em;">Ünite ${index + 1}: ${unit.name}</h3>

                    <div style="display: flex; flex-direction: column; gap: 12px;">
                        ${unit.children.map(subtopic => `
                            <div style="background: white; padding: 12px 15px; border-radius: 10px; display: flex; align-items: center; gap: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                                <span style="font-size: 1.5em;">${subtopic.emoji}</span>
                                <span style="font-weight: 500; color: #333;">${subtopic.name}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        });

        html += '</div>';

        return html;
    }
};
