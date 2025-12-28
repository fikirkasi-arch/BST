import nodemailer from 'nodemailer';

class EmailService {
  private transporter: nodemailer.Transporter | null = null;

  constructor() {
    this.initialize();
  }

  private async initialize() {
    try {
      if (!process.env.SMTP_HOST || !process.env.SMTP_USER) {
        console.log('⚠️  Email servisi yapılandırılmadı (SMTP ayarları eksik)');
        return;
      }

      this.transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST,
        port: parseInt(process.env.SMTP_PORT || '587'),
        secure: process.env.SMTP_SECURE === 'true',
        auth: {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASSWORD,
        },
      });

      // Test connection
      await this.transporter.verify();
      console.log('✅ Email servisi başarıyla yapılandırıldı');
    } catch (error) {
      console.error('❌ Email servisi başlatılamadı:', error);
      this.transporter = null;
    }
  }

  /**
   * Email gönder
   */
  async sendEmail(to: string, subject: string, content: string): Promise<boolean> {
    try {
      if (!this.transporter) {
        console.error('Email servisi yapılandırılmadı');
        return false;
      }

      const info = await this.transporter.sendMail({
        from: `"${process.env.SMTP_FROM_NAME || 'Okul SMS Sistemi'}" <${process.env.SMTP_USER}>`,
        to,
        subject,
        text: content,
        html: this.formatHtmlEmail(content),
      });

      console.log('✅ Email gönderildi:', info.messageId);
      return true;
    } catch (error: any) {
      console.error('❌ Email gönderme hatası:', error.message);
      return false;
    }
  }

  /**
   * Toplu email gönder
   */
  async sendBulkEmail(recipients: string[], subject: string, content: string): Promise<{
    sent: number;
    failed: number;
    results: { email: string; success: boolean; error?: string }[];
  }> {
    const results: { email: string; success: boolean; error?: string }[] = [];
    let sent = 0;
    let failed = 0;

    for (const email of recipients) {
      try {
        // Değişkenleri değiştir (basit örnek)
        let personalizedContent = content;

        const success = await this.sendEmail(email, subject, personalizedContent);

        if (success) {
          sent++;
          results.push({ email, success: true });
        } else {
          failed++;
          results.push({ email, success: false, error: 'Send failed' });
        }

        // Rate limiting (saniyede 2 email)
        await new Promise(resolve => setTimeout(resolve, 500));
      } catch (error: any) {
        failed++;
        results.push({ email, success: false, error: error.message });
      }
    }

    return { sent, failed, results };
  }

  /**
   * HTML email formatla
   */
  private formatHtmlEmail(content: string): string {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <style>
          body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
          }
          .header {
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
          }
          .content {
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
          }
          .footer {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            font-size: 12px;
            color: #666;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h2>Okul SMS Sistemi</h2>
        </div>
        <div class="content">
          ${content.replace(/\n/g, '<br>')}
        </div>
        <div class="footer">
          <p>Bu email otomatik olarak gönderilmiştir.</p>
        </div>
      </body>
      </html>
    `;
  }

  /**
   * Servisi test et
   */
  async testConnection(): Promise<boolean> {
    try {
      if (!this.transporter) {
        return false;
      }
      await this.transporter.verify();
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * Servis durumunu kontrol et
   */
  isConfigured(): boolean {
    return this.transporter !== null;
  }
}

export default new EmailService();
