import { Request, Response } from 'express';
import { query, getClient } from '../config/database';
import { AppError } from '../middleware/errorHandler';
import smsService from '../services/smsService';
import whatsappService from '../services/whatsappService';
import { BulkMessageRequest } from '../types';

/**
 * Toplu mesaj gönder
 */
export const sendBulkMessage = async (
  req: Request,
  res: Response
): Promise<void> => {
  const client = await getClient();

  try {
    const userId = (req as any).user.userId;
    const {
      message_type,
      content,
      recipients,
      scheduled_at,
      template_id,
    }: BulkMessageRequest = req.body;

    // Alıcıları topla
    const recipientList = await collectRecipients(recipients);

    if (recipientList.length === 0) {
      throw new AppError('Alıcı bulunamadı', 400);
    }

    await client.query('BEGIN');

    // Mesajı veritabanına kaydet
    const messageResult = await client.query(
      `INSERT INTO messages (sender_id, message_type, recipient_type, content, recipient_count, status, scheduled_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7)
       RETURNING *`,
      [
        userId,
        message_type,
        recipients.type,
        content,
        recipientList.length,
        scheduled_at ? 'scheduled' : 'pending',
        scheduled_at || null,
      ]
    );

    const message = messageResult.rows[0];

    // Her alıcı için kişiselleştirilmiş mesaj oluştur ve kaydet
    const recipientInserts = recipientList.map((recipient) => {
      const personalizedContent = smsService.personalizeMessage(content, {
        ad: recipient.first_name || '',
        soyad: recipient.last_name || '',
        tam_ad: recipient.full_name || '',
        telefon: recipient.phone,
      });

      return client.query(
        `INSERT INTO message_recipients (message_id, recipient_name, phone, personalized_content, status)
         VALUES ($1, $2, $3, $4, $5)`,
        [
          message.id,
          recipient.full_name,
          recipient.phone,
          personalizedContent,
          'pending',
        ]
      );
    });

    await Promise.all(recipientInserts);

    // Eğer zamanlanmamışsa hemen gönder
    if (!scheduled_at) {
      await sendMessageNow(client, message.id, message_type, recipientList, content);
    }

    await client.query('COMMIT');

    res.status(201).json({
      success: true,
      message: scheduled_at
        ? 'Mesaj zamanlandı'
        : 'Mesaj gönderiliyor',
      data: {
        message_id: message.id,
        recipient_count: recipientList.length,
        status: message.status,
      },
    });
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
};

/**
 * Alıcıları topla
 */
async function collectRecipients(recipientsConfig: any): Promise<any[]> {
  const recipients: any[] = [];

  // Sınıflara göre
  if (recipientsConfig.class_ids && recipientsConfig.class_ids.length > 0) {
    const classRecipients = await query(
      `SELECT DISTINCT p.first_name, p.last_name, p.phone,
              CONCAT(p.first_name, ' ', p.last_name) as full_name
       FROM parents p
       JOIN student_parents sp ON p.id = sp.parent_id
       JOIN students s ON sp.student_id = s.id
       WHERE s.class_id = ANY($1)
       AND p.is_active = true
       AND s.is_active = true`,
      [recipientsConfig.class_ids]
    );
    recipients.push(...classRecipients.rows);
  }

  // Öğrenci numaralarına göre
  if (
    recipientsConfig.student_numbers &&
    recipientsConfig.student_numbers.length > 0
  ) {
    const studentRecipients = await query(
      `SELECT DISTINCT p.first_name, p.last_name, p.phone,
              CONCAT(p.first_name, ' ', p.last_name) as full_name
       FROM parents p
       JOIN student_parents sp ON p.id = sp.parent_id
       JOIN students s ON sp.student_id = s.id
       WHERE s.student_number = ANY($1)
       AND p.is_active = true
       AND s.is_active = true`,
      [recipientsConfig.student_numbers]
    );
    recipients.push(...studentRecipients.rows);
  }

  // Tüm veliler
  if (recipientsConfig.type === 'parents') {
    const allParents = await query(
      `SELECT first_name, last_name, phone,
              CONCAT(first_name, ' ', last_name) as full_name
       FROM parents
       WHERE is_active = true`
    );
    recipients.push(...allParents.rows);
  }

  // Personel
  if (recipientsConfig.staff_ids && recipientsConfig.staff_ids.length > 0) {
    const staffRecipients = await query(
      `SELECT first_name, last_name, phone,
              CONCAT(first_name, ' ', last_name) as full_name
       FROM staff
       WHERE id = ANY($1)
       AND is_active = true`,
      [recipientsConfig.staff_ids]
    );
    recipients.push(...staffRecipients.rows);
  }

  // Elle girilen numaralar
  if (
    recipientsConfig.phone_numbers &&
    recipientsConfig.phone_numbers.length > 0
  ) {
    const customRecipients = recipientsConfig.phone_numbers.map(
      (phone: string) => ({
        first_name: '',
        last_name: '',
        phone,
        full_name: phone,
      })
    );
    recipients.push(...customRecipients);
  }

  // Tekrarları kaldır (telefon numarasına göre)
  const uniqueRecipients = recipients.reduce((acc: any[], current: any) => {
    const exists = acc.find((item) => item.phone === current.phone);
    if (!exists) {
      acc.push(current);
    }
    return acc;
  }, []);

  return uniqueRecipients;
}

/**
 * Mesajı hemen gönder
 */
async function sendMessageNow(
  client: any,
  messageId: number,
  messageType: string,
  recipients: any[],
  content: string
): Promise<void> {
  // Durumu 'sending' yap
  await client.query(
    'UPDATE messages SET status = $1, updated_at = NOW() WHERE id = $2',
    ['sending', messageId]
  );

  // Arka planda gönder (async)
  setImmediate(async () => {
    try {
      let sentCount = 0;
      let failedCount = 0;

      for (const recipient of recipients) {
        const personalizedContent = smsService.personalizeMessage(content, {
          ad: recipient.first_name || '',
          soyad: recipient.last_name || '',
          tam_ad: recipient.full_name || '',
        });

        let result;

        if (messageType === 'SMS') {
          result = await smsService.sendSMS(recipient.phone, personalizedContent);
        } else if (messageType === 'WhatsApp') {
          result = await whatsappService.sendMessage(
            recipient.phone,
            personalizedContent
          );
        }

        // Sonucu kaydet
        if (result && result.success) {
          sentCount++;
          await query(
            `UPDATE message_recipients
             SET status = $1, sent_at = NOW(), provider_message_id = $2
             WHERE message_id = $3 AND phone = $4`,
            ['sent', result.messageId, messageId, recipient.phone]
          );
        } else {
          failedCount++;
          await query(
            `UPDATE message_recipients
             SET status = $1, error_message = $2
             WHERE message_id = $3 AND phone = $4`,
            ['failed', result?.error || 'Bilinmeyen hata', messageId, recipient.phone]
          );
        }
      }

      // Mesaj durumunu güncelle
      await query(
        `UPDATE messages
         SET status = $1, sent_count = $2, failed_count = $3, sent_at = NOW()
         WHERE id = $4`,
        ['sent', sentCount, failedCount, messageId]
      );
    } catch (error) {
      console.error('Mesaj gönderme hatası:', error);
      await query(
        'UPDATE messages SET status = $1 WHERE id = $2',
        ['failed', messageId]
      );
    }
  });
}

/**
 * Mesaj listesi
 */
export const getMessages = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { page = 1, limit = 20, status } = req.query;
    const offset = (Number(page) - 1) * Number(limit);

    let queryText = `
      SELECT m.*, u.full_name as sender_name
      FROM messages m
      JOIN users u ON m.sender_id = u.id
    `;

    const params: any[] = [];
    if (status) {
      queryText += ' WHERE m.status = $1';
      params.push(status);
    }

    queryText += ` ORDER BY m.created_at DESC LIMIT $${params.length + 1} OFFSET $${params.length + 2}`;
    params.push(Number(limit), offset);

    const result = await query(queryText, params);

    // Toplam sayfa sayısı
    const countResult = await query('SELECT COUNT(*) FROM messages');
    const total = parseInt(countResult.rows[0].count);

    res.json({
      success: true,
      data: result.rows,
      pagination: {
        total,
        page: Number(page),
        limit: Number(limit),
        totalPages: Math.ceil(total / Number(limit)),
      },
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Mesaj detayı
 */
export const getMessageById = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { id } = req.params;

    const messageResult = await query(
      `SELECT m.*, u.full_name as sender_name
       FROM messages m
       JOIN users u ON m.sender_id = u.id
       WHERE m.id = $1`,
      [id]
    );

    if (messageResult.rows.length === 0) {
      throw new AppError('Mesaj bulunamadı', 404);
    }

    const message = messageResult.rows[0];

    // Alıcıları al
    const recipientsResult = await query(
      'SELECT * FROM message_recipients WHERE message_id = $1 ORDER BY created_at',
      [id]
    );

    res.json({
      success: true,
      data: {
        ...message,
        recipients: recipientsResult.rows,
      },
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Zamanlanmış mesajı iptal et
 */
export const cancelScheduledMessage = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { id } = req.params;

    const result = await query(
      `UPDATE messages
       SET status = 'cancelled', updated_at = NOW()
       WHERE id = $1 AND status = 'scheduled'
       RETURNING *`,
      [id]
    );

    if (result.rows.length === 0) {
      throw new AppError('Zamanlanmış mesaj bulunamadı', 404);
    }

    res.json({
      success: true,
      message: 'Mesaj iptal edildi',
      data: result.rows[0],
    });
  } catch (error) {
    throw error;
  }
};
