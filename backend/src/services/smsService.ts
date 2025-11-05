import axios from 'axios';
import twilio from 'twilio';
import { ProviderSettings } from '../types';

export interface SMSResult {
  success: boolean;
  messageId?: string;
  error?: string;
}

class SMSService {
  private twilioClient: any;

  constructor() {
    // Twilio istemcisini başlat
    if (process.env.TWILIO_ACCOUNT_SID && process.env.TWILIO_AUTH_TOKEN) {
      this.twilioClient = twilio(
        process.env.TWILIO_ACCOUNT_SID,
        process.env.TWILIO_AUTH_TOKEN
      );
    }
  }

  /**
   * Twilio ile SMS gönder
   */
  async sendViaTwilio(to: string, message: string): Promise<SMSResult> {
    try {
      if (!this.twilioClient) {
        return {
          success: false,
          error: 'Twilio yapılandırılmamış',
        };
      }

      const result = await this.twilioClient.messages.create({
        body: message,
        from: process.env.TWILIO_PHONE_NUMBER,
        to: to,
      });

      return {
        success: true,
        messageId: result.sid,
      };
    } catch (error: any) {
      console.error('Twilio SMS hatası:', error);
      return {
        success: false,
        error: error.message,
      };
    }
  }

  /**
   * NetGSM (Türkiye) ile SMS gönder
   */
  async sendViaNetGSM(to: string, message: string): Promise<SMSResult> {
    try {
      const username = process.env.NETGSM_USERNAME;
      const password = process.env.NETGSM_PASSWORD;
      const header = process.env.NETGSM_HEADER;

      if (!username || !password || !header) {
        return {
          success: false,
          error: 'NetGSM yapılandırılmamış',
        };
      }

      // Telefon numarasını temizle (sadece rakamlar)
      const cleanPhone = to.replace(/\D/g, '');

      // NetGSM API URL'i
      const url = 'https://api.netgsm.com.tr/sms/send/get';

      const params = {
        usercode: username,
        password: password,
        gsmno: cleanPhone,
        message: message,
        msgheader: header,
        filter: '0',
      };

      const response = await axios.get(url, { params });

      // NetGSM yanıt kodu kontrolü
      // 00: Başarılı, 01: Hatalı kullanıcı adı/şifre, vb.
      const resultCode = response.data.split(' ')[0];

      if (resultCode === '00' || resultCode.includes('00')) {
        return {
          success: true,
          messageId: response.data,
        };
      } else {
        return {
          success: false,
          error: `NetGSM hata kodu: ${resultCode}`,
        };
      }
    } catch (error: any) {
      console.error('NetGSM SMS hatası:', error);
      return {
        success: false,
        error: error.message,
      };
    }
  }

  /**
   * Genel SMS gönderme metodu (sağlayıcı seçimi ile)
   */
  async sendSMS(
    to: string,
    message: string,
    provider: 'twilio' | 'netgsm' = 'netgsm'
  ): Promise<SMSResult> {
    // Telefon numarası kontrolü
    if (!to || to.trim() === '') {
      return {
        success: false,
        error: 'Geçersiz telefon numarası',
      };
    }

    // Mesaj kontrolü
    if (!message || message.trim() === '') {
      return {
        success: false,
        error: 'Mesaj boş olamaz',
      };
    }

    // Sağlayıcıya göre gönderim
    switch (provider) {
      case 'twilio':
        return await this.sendViaTwilio(to, message);
      case 'netgsm':
        return await this.sendViaNetGSM(to, message);
      default:
        return {
          success: false,
          error: 'Geçersiz SMS sağlayıcısı',
        };
    }
  }

  /**
   * Toplu SMS gönderimi
   */
  async sendBulkSMS(
    recipients: Array<{ phone: string; message: string }>,
    provider: 'twilio' | 'netgsm' = 'netgsm'
  ): Promise<Array<{ phone: string; result: SMSResult }>> {
    const results = [];

    for (const recipient of recipients) {
      const result = await this.sendSMS(
        recipient.phone,
        recipient.message,
        provider
      );

      results.push({
        phone: recipient.phone,
        result,
      });

      // Rate limiting - her SMS arasında 100ms bekle
      await this.delay(100);
    }

    return results;
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

  /**
   * Telefon numarasını formatla
   */
  formatPhoneNumber(phone: string, countryCode: string = '90'): string {
    // Sadece rakamları al
    let cleaned = phone.replace(/\D/g, '');

    // Eğer ülke kodu yoksa ekle
    if (!cleaned.startsWith(countryCode)) {
      // Baştaki 0'ı kaldır
      if (cleaned.startsWith('0')) {
        cleaned = cleaned.substring(1);
      }
      cleaned = countryCode + cleaned;
    }

    return '+' + cleaned;
  }

  /**
   * Gecikme fonksiyonu
   */
  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

export default new SMSService();
