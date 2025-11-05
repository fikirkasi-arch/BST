import cron from 'node-cron';
import { query } from '../config/database';
import smsService from './smsService';
import whatsappService from './whatsappService';

class SchedulerService {
  private tasks: Map<string, cron.ScheduledTask> = new Map();

  /**
   * Zamanlanmış mesajları kontrol eden cron job'ı başlat
   */
  startScheduledMessagesCheck(): void {
    // Her dakika zamanlanmış mesajları kontrol et
    const task = cron.schedule('* * * * *', async () => {
      await this.processScheduledMessages();
    });

    this.tasks.set('scheduled-messages', task);
    console.log('✅ Zamanlanmış mesaj kontrolü başlatıldı');
  }

  /**
   * Zamanlanmış mesajları işle
   */
  private async processScheduledMessages(): Promise<void> {
    try {
      // Zamanı gelmiş mesajları al
      const result = await query(
        `SELECT * FROM messages
         WHERE status = 'scheduled'
         AND scheduled_at <= NOW()
         ORDER BY scheduled_at ASC
         LIMIT 10`
      );

      const messages = result.rows;

      if (messages.length === 0) {
        return;
      }

      console.log(
        `📅 ${messages.length} zamanlanmış mesaj işleniyor...`
      );

      for (const message of messages) {
        await this.sendScheduledMessage(message);
      }
    } catch (error) {
      console.error('Zamanlanmış mesaj işleme hatası:', error);
    }
  }

  /**
   * Tek bir zamanlanmış mesajı gönder
   */
  private async sendScheduledMessage(message: any): Promise<void> {
    try {
      // Mesaj durumunu 'sending' yap
      await query(
        'UPDATE messages SET status = $1, updated_at = NOW() WHERE id = $2',
        ['sending', message.id]
      );

      // Alıcıları al
      const recipientsResult = await query(
        'SELECT * FROM message_recipients WHERE message_id = $1 AND status = $2',
        [message.id, 'pending']
      );

      const recipients = recipientsResult.rows;

      let sentCount = 0;
      let failedCount = 0;

      // Her alıcıya mesaj gönder
      for (const recipient of recipients) {
        let result;

        if (message.message_type === 'SMS') {
          result = await smsService.sendSMS(
            recipient.phone,
            recipient.personalized_content
          );
        } else if (message.message_type === 'WhatsApp') {
          result = await whatsappService.sendMessage(
            recipient.phone,
            recipient.personalized_content
          );
        }

        if (result && result.success) {
          sentCount++;
          await query(
            `UPDATE message_recipients
             SET status = $1, sent_at = NOW(), provider_message_id = $2, updated_at = NOW()
             WHERE id = $3`,
            ['sent', result.messageId, recipient.id]
          );
        } else {
          failedCount++;
          await query(
            `UPDATE message_recipients
             SET status = $1, error_message = $2, updated_at = NOW()
             WHERE id = $3`,
            ['failed', result?.error || 'Bilinmeyen hata', recipient.id]
          );
        }

        // Rate limiting
        await this.delay(100);
      }

      // Mesaj durumunu güncelle
      await query(
        `UPDATE messages
         SET status = $1, sent_count = $2, failed_count = $3, sent_at = NOW(), updated_at = NOW()
         WHERE id = $4`,
        ['sent', sentCount, failedCount, message.id]
      );

      console.log(
        `✅ Mesaj gönderildi (ID: ${message.id}): ${sentCount} başarılı, ${failedCount} başarısız`
      );
    } catch (error) {
      console.error('Mesaj gönderme hatası:', error);

      // Mesajı başarısız olarak işaretle
      await query(
        'UPDATE messages SET status = $1, updated_at = NOW() WHERE id = $2',
        ['failed', message.id]
      );
    }
  }

  /**
   * Devamsızlık bildirimi kontrolü (her gün sabah 10'da)
   */
  startAttendanceNotifications(): void {
    const task = cron.schedule('0 10 * * *', async () => {
      await this.processAttendanceNotifications();
    });

    this.tasks.set('attendance-notifications', task);
    console.log('✅ Devamsızlık bildirimi kontrolü başlatıldı');
  }

  /**
   * Devamsızlık bildirimlerini işle
   */
  private async processAttendanceNotifications(): Promise<void> {
    try {
      // Bildirilmemiş devamsızlıkları al
      const result = await query(
        `SELECT a.*, s.first_name, s.last_name, s.student_number,
                p.first_name as parent_first_name, p.last_name as parent_last_name, p.phone
         FROM attendance a
         JOIN students s ON a.student_id = s.id
         JOIN student_parents sp ON s.id = sp.student_id
         JOIN parents p ON sp.parent_id = p.id
         WHERE a.notified = false
         AND a.status = 'absent'
         AND a.date = CURRENT_DATE`
      );

      const absences = result.rows;

      for (const absence of absences) {
        const message = `Sayın ${absence.parent_first_name} ${absence.parent_last_name}, öğrenciniz ${absence.first_name} ${absence.last_name} bugün okula gelmemiştir. Detaylı bilgi için okul idaresi ile iletişime geçiniz.`;

        const smsResult = await smsService.sendSMS(absence.phone, message);

        if (smsResult.success) {
          await query(
            'UPDATE attendance SET notified = true WHERE id = $1',
            [absence.id]
          );
        }
      }

      console.log(
        `✅ ${absences.length} devamsızlık bildirimi gönderildi`
      );
    } catch (error) {
      console.error('Devamsızlık bildirimi hatası:', error);
    }
  }

  /**
   * Tüm cron job'ları durdur
   */
  stopAll(): void {
    this.tasks.forEach((task, name) => {
      task.stop();
      console.log(`❌ ${name} durduruldu`);
    });
    this.tasks.clear();
  }

  /**
   * Gecikme fonksiyonu
   */
  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

export default new SchedulerService();
