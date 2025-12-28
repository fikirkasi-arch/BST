import { Client, LocalAuth } from 'whatsapp-web.js';
import qrcode from 'qrcode-terminal';

export interface WhatsAppResult {
  success: boolean;
  messageId?: string;
  error?: string;
}

class WhatsAppService {
  private client: Client | null = null;
  private isReady: boolean = false;
  private isInitializing: boolean = false;

  /**
   * WhatsApp istemcisini başlat
   */
  async initialize(): Promise<void> {
    if (this.client || this.isInitializing) {
      return;
    }

    this.isInitializing = true;

    try {
      this.client = new Client({
        authStrategy: new LocalAuth({
          dataPath: process.env.WHATSAPP_SESSION_PATH || './whatsapp-session',
        }),
        puppeteer: {
          args: ['--no-sandbox', '--disable-setuid-sandbox'],
          headless: true,
        },
      });

      this.client.on('qr', (qr) => {
        console.log('📱 WhatsApp QR Kodu:');
        qrcode.generate(qr, { small: true });
        console.log('Telefonunuzla bu QR kodunu tarayın.');
      });

      this.client.on('ready', () => {
        console.log('✅ WhatsApp bağlantısı hazır!');
        this.isReady = true;
        this.isInitializing = false;
      });

      this.client.on('authenticated', () => {
        console.log('✅ WhatsApp kimlik doğrulaması başarılı');
      });

      this.client.on('auth_failure', (msg) => {
        console.error('❌ WhatsApp kimlik doğrulama hatası:', msg);
        this.isReady = false;
        this.isInitializing = false;
      });

      this.client.on('disconnected', (reason) => {
        console.log('❌ WhatsApp bağlantısı kesildi:', reason);
        this.isReady = false;
        this.client = null;
      });

      await this.client.initialize();
    } catch (error) {
      console.error('WhatsApp başlatma hatası:', error);
      this.isInitializing = false;
      throw error;
    }
  }

  /**
   * WhatsApp mesajı gönder
   */
  async sendMessage(to: string, message: string): Promise<WhatsAppResult> {
    try {
      if (!this.isReady || !this.client) {
        return {
          success: false,
          error: 'WhatsApp bağlantısı hazır değil',
        };
      }

      // Telefon numarasını formatla
      const formattedNumber = this.formatNumber(to);

      // Mesajı gönder
      const sentMessage = await this.client.sendMessage(
        formattedNumber,
        message
      );

      return {
        success: true,
        messageId: sentMessage.id._serialized,
      };
    } catch (error: any) {
      console.error('WhatsApp mesaj gönderme hatası:', error);
      return {
        success: false,
        error: error.message,
      };
    }
  }

  /**
   * Toplu WhatsApp mesajı gönder
   */
  async sendBulkMessages(
    recipients: Array<{ phone: string; message: string }>
  ): Promise<Array<{ phone: string; result: WhatsAppResult }>> {
    const results = [];

    for (const recipient of recipients) {
      const result = await this.sendMessage(recipient.phone, recipient.message);

      results.push({
        phone: recipient.phone,
        result,
      });

      // Rate limiting - her mesaj arasında 2 saniye bekle
      // WhatsApp spam koruması için
      await this.delay(2000);
    }

    return results;
  }

  /**
   * Telefon numarasını WhatsApp formatına çevir
   */
  private formatNumber(phone: string): string {
    // Sadece rakamları al
    let cleaned = phone.replace(/\D/g, '');

    // Türkiye ülke kodu kontrolü
    if (!cleaned.startsWith('90')) {
      if (cleaned.startsWith('0')) {
        cleaned = cleaned.substring(1);
      }
      cleaned = '90' + cleaned;
    }

    return cleaned + '@c.us';
  }

  /**
   * WhatsApp bağlantı durumunu kontrol et
   */
  isConnected(): boolean {
    return this.isReady;
  }

  /**
   * WhatsApp bağlantısını kapat
   */
  async disconnect(): Promise<void> {
    if (this.client) {
      await this.client.destroy();
      this.client = null;
      this.isReady = false;
    }
  }

  /**
   * Gecikme fonksiyonu
   */
  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /**
   * Mesajı kişiselleştir
   */
  personalizeMessage(
    template: string,
    variables: Record<string, string>
  ): string {
    let message = template;

    for (const [key, value] of Object.entries(variables)) {
      const placeholder = `{${key}}`;
      message = message.replace(new RegExp(placeholder, 'g'), value);
    }

    return message;
  }
}

export default new WhatsAppService();
