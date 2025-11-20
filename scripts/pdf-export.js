// PDF Yazdırma/İndirme Sistemi
const BSTPDFExport = {
    // Ders anlatımını PDF olarak indir
    exportLessonToPDF(lessonId, lessonTitle) {
        // Modal içeriğini al
        const modalContent = document.getElementById('modalBody');

        if (!modalContent) {
            console.error('İçerik bulunamadı');
            return;
        }

        // Yazdırma için optimize edilmiş pencere aç
        const printWindow = window.open('', '_blank', 'width=800,height=600');

        if (!printWindow) {
            if (typeof BSTNotification !== 'undefined') {
                BSTNotification.show('Pop-up engelleyicinizi devre dışı bırakın', 'error');
            }
            return;
        }

        // HTML içeriği hazırla
        const htmlContent = `
            <!DOCTYPE html>
            <html lang="tr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>${lessonTitle} - BST Eğitim</title>
                <style>
                    @media print {
                        @page {
                            margin: 2cm;
                            size: A4;
                        }
                    }

                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        line-height: 1.8;
                        color: #333;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background: white;
                    }

                    h1, h2, h3, h4 {
                        color: #667eea;
                        margin-top: 1.5em;
                        margin-bottom: 0.5em;
                        page-break-after: avoid;
                    }

                    h1 {
                        font-size: 2em;
                        text-align: center;
                        border-bottom: 3px solid #667eea;
                        padding-bottom: 10px;
                    }

                    h2 {
                        font-size: 1.6em;
                        color: #f5576c;
                    }

                    h3 {
                        font-size: 1.3em;
                        color: #4facfe;
                    }

                    h4 {
                        font-size: 1.1em;
                    }

                    p {
                        margin: 1em 0;
                        text-align: justify;
                    }

                    ul, ol {
                        margin: 1em 0;
                        padding-left: 2em;
                    }

                    li {
                        margin: 0.5em 0;
                    }

                    strong {
                        color: #667eea;
                        font-weight: 600;
                    }

                    code, pre {
                        background: #f5f5f5;
                        padding: 2px 6px;
                        border-radius: 4px;
                        font-family: 'Courier New', monospace;
                    }

                    pre {
                        padding: 15px;
                        overflow-x: auto;
                        page-break-inside: avoid;
                    }

                    .header {
                        text-align: center;
                        margin-bottom: 30px;
                        padding-bottom: 20px;
                        border-bottom: 2px solid #e0e0e0;
                    }

                    .logo {
                        font-size: 2.5em;
                        margin-bottom: 10px;
                    }

                    .footer {
                        margin-top: 50px;
                        padding-top: 20px;
                        border-top: 2px solid #e0e0e0;
                        text-align: center;
                        color: #999;
                        font-size: 0.9em;
                        page-break-before: avoid;
                    }

                    .page-break {
                        page-break-before: always;
                    }

                    .no-print {
                        display: none;
                    }

                    @media print {
                        .no-print {
                            display: none !important;
                        }

                        body {
                            background: white;
                        }

                        h1, h2, h3, h4 {
                            page-break-after: avoid;
                        }

                        ul, ol {
                            page-break-inside: avoid;
                        }

                        img {
                            max-width: 100%;
                            page-break-inside: avoid;
                        }
                    }

                    .print-button {
                        position: fixed;
                        top: 20px;
                        right: 20px;
                        padding: 12px 24px;
                        background: #667eea;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 1em;
                        cursor: pointer;
                        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                        z-index: 1000;
                    }

                    .print-button:hover {
                        background: #764ba2;
                    }

                    @media print {
                        .print-button {
                            display: none;
                        }
                    }
                </style>
            </head>
            <body>
                <button class="print-button no-print" onclick="window.print()">🖨️ Yazdır / PDF Olarak Kaydet</button>

                <div class="header">
                    <div class="logo">📚</div>
                    <h1>BST Eğitim Portalı</h1>
                    <p style="color: #666; margin: 10px 0;">Bilişim Teknolojileri ve Yazılım Dersi</p>
                </div>

                <div class="content">
                    ${modalContent.innerHTML}
                </div>

                <div class="footer">
                    <p><strong>BST Eğitim Portalı</strong></p>
                    <p>2025-2026 Eğitim Yılı</p>
                    <p style="margin-top: 10px;">Bu belge BST Eğitim Portalı tarafından oluşturulmuştur.</p>
                    <p style="margin-top: 5px; font-size: 0.85em;">Yazdırma Tarihi: ${new Date().toLocaleDateString('tr-TR', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    })}</p>
                </div>

                <script>
                    // Sayfa yüklendiğinde otomatik yazdırma dialogunu aç (isteğe bağlı)
                    // window.onload = () => setTimeout(() => window.print(), 500);
                </script>
            </body>
            </html>
        `;

        printWindow.document.write(htmlContent);
        printWindow.document.close();

        // Bildirim göster
        if (typeof BSTNotification !== 'undefined') {
            BSTNotification.show('PDF hazırlandı! Yazdır butonuna basın.', 'success', 3000);
        }
    },

    // Tüm ünitenin içeriğini PDF olarak indir
    exportFullUnitToPDF(gradeLevel, unitNumber) {
        // Bu fonksiyon tüm ünite içeriğini birleştirip PDF oluşturur
        // Şimdilik basit bir uyarı göster
        if (typeof BSTNotification !== 'undefined') {
            BSTNotification.show('Tam ünite PDF özelliği yakında aktif olacak!', 'info', 3000);
        }
    }
};
