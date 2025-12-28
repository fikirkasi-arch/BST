import { Request, Response } from 'express';
import { query } from '../config/database';

/**
 * Genel istatistikleri getir
 */
export const getGeneralStats = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    // Toplam öğrenci sayısı
    const studentsResult = await query(
      'SELECT COUNT(*) as count FROM students WHERE is_active = true'
    );

    // Toplam veli sayısı
    const parentsResult = await query(
      'SELECT COUNT(*) as count FROM parents WHERE is_active = true'
    );

    // Toplam gönderilen mesaj sayısı
    const messagesResult = await query(
      'SELECT COUNT(*) as count FROM messages WHERE status = $1',
      ['sent']
    );

    // Bu ayki mesaj sayısı
    const monthlyMessagesResult = await query(
      `SELECT COUNT(*) as count FROM messages
       WHERE status = $1 AND created_at >= DATE_TRUNC('month', CURRENT_DATE)`,
      ['sent']
    );

    // Bugünkü mesaj sayısı
    const todayMessagesResult = await query(
      `SELECT COUNT(*) as count FROM messages
       WHERE status = $1 AND created_at >= CURRENT_DATE`,
      ['sent']
    );

    // Başarısız mesaj sayısı
    const failedMessagesResult = await query(
      'SELECT COUNT(*) as count FROM message_recipients WHERE status = $1',
      ['failed']
    );

    res.json({
      success: true,
      data: {
        totalStudents: parseInt(studentsResult.rows[0].count),
        totalParents: parseInt(parentsResult.rows[0].count),
        totalMessages: parseInt(messagesResult.rows[0].count),
        monthlyMessages: parseInt(monthlyMessagesResult.rows[0].count),
        todayMessages: parseInt(todayMessagesResult.rows[0].count),
        failedMessages: parseInt(failedMessagesResult.rows[0].count),
      },
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Mesaj istatistiklerini getir (grafik için)
 */
export const getMessageStats = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { period = '7days' } = req.query;

    let dateFilter = '';
    if (period === '7days') {
      dateFilter = `AND m.created_at >= CURRENT_DATE - INTERVAL '7 days'`;
    } else if (period === '30days') {
      dateFilter = `AND m.created_at >= CURRENT_DATE - INTERVAL '30 days'`;
    } else if (period === '12months') {
      dateFilter = `AND m.created_at >= CURRENT_DATE - INTERVAL '12 months'`;
    }

    // Günlük/aylık mesaj sayıları
    let groupBy = '';
    if (period === '12months') {
      groupBy = `TO_CHAR(m.created_at, 'YYYY-MM')`;
    } else {
      groupBy = `TO_CHAR(m.created_at, 'YYYY-MM-DD')`;
    }

    const statsResult = await query(
      `SELECT ${groupBy} as date,
              message_type,
              COUNT(*) as count,
              SUM(CASE WHEN status = 'sent' THEN 1 ELSE 0 END) as sent,
              SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
              SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending
       FROM messages m
       WHERE 1=1 ${dateFilter}
       GROUP BY ${groupBy}, message_type
       ORDER BY date DESC`
    );

    res.json({
      success: true,
      data: statsResult.rows,
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Sınıf bazında istatistikler
 */
export const getClassStats = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const result = await query(
      `SELECT c.id, c.name, c.grade_level, c.section,
              COUNT(DISTINCT s.id) as student_count,
              COUNT(DISTINCT sp.parent_id) as parent_count,
              COUNT(DISTINCT CASE WHEN a.status = 'present' THEN a.id END) as present_count,
              COUNT(DISTINCT CASE WHEN a.status = 'absent' THEN a.id END) as absent_count
       FROM classes c
       LEFT JOIN students s ON c.id = s.class_id AND s.is_active = true
       LEFT JOIN student_parents sp ON s.id = sp.student_id
       LEFT JOIN attendance a ON s.id = a.student_id AND a.date >= CURRENT_DATE - INTERVAL '30 days'
       WHERE c.is_active = true
       GROUP BY c.id, c.name, c.grade_level, c.section
       ORDER BY c.grade_level, c.section`
    );

    res.json({
      success: true,
      data: result.rows,
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Devamsızlık istatistikleri
 */
export const getAttendanceStats = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { start_date, end_date, class_id } = req.query;

    let queryText = `
      SELECT
        TO_CHAR(a.date, 'YYYY-MM-DD') as date,
        COUNT(DISTINCT CASE WHEN a.status = 'present' THEN a.student_id END) as present,
        COUNT(DISTINCT CASE WHEN a.status = 'absent' THEN a.student_id END) as absent,
        COUNT(DISTINCT CASE WHEN a.status = 'late' THEN a.student_id END) as late,
        COUNT(DISTINCT CASE WHEN a.status = 'excused' THEN a.student_id END) as excused
      FROM attendance a
      INNER JOIN students s ON a.student_id = s.id
      WHERE a.date >= COALESCE($1::date, CURRENT_DATE - INTERVAL '30 days')
        AND a.date <= COALESCE($2::date, CURRENT_DATE)
    `;

    const params: any[] = [start_date || null, end_date || null];

    if (class_id) {
      params.push(class_id);
      queryText += ` AND s.class_id = $${params.length}`;
    }

    queryText += ` GROUP BY a.date ORDER BY a.date DESC`;

    const result = await query(queryText, params);

    res.json({
      success: true,
      data: result.rows,
    });
  } catch (error) {
    throw error;
  }
};

/**
 * En çok devamsızlık yapan öğrenciler
 */
export const getTopAbsentStudents = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { limit = 10, days = 30 } = req.query;

    const result = await query(
      `SELECT
        s.id, s.student_number, s.first_name, s.last_name,
        c.name as class_name,
        COUNT(a.id) as absent_count
      FROM students s
      LEFT JOIN classes c ON s.class_id = c.id
      LEFT JOIN attendance a ON s.id = a.student_id
        AND a.status = 'absent'
        AND a.date >= CURRENT_DATE - INTERVAL '${parseInt(days as string)} days'
      WHERE s.is_active = true
      GROUP BY s.id, s.student_number, s.first_name, s.last_name, c.name
      HAVING COUNT(a.id) > 0
      ORDER BY absent_count DESC
      LIMIT $1`,
      [parseInt(limit as string)]
    );

    res.json({
      success: true,
      data: result.rows,
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Mesaj maliyeti raporu
 */
export const getMessageCostReport = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { start_date, end_date } = req.query;

    const result = await query(
      `SELECT
        message_type,
        COUNT(*) as total_messages,
        SUM(CASE WHEN status = 'sent' THEN 1 ELSE 0 END) as sent_messages,
        SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_messages,
        COUNT(DISTINCT user_id) as users_sent
      FROM messages
      WHERE created_at >= COALESCE($1::date, CURRENT_DATE - INTERVAL '30 days')
        AND created_at <= COALESCE($2::date, CURRENT_DATE)
      GROUP BY message_type
      ORDER BY total_messages DESC`,
      [start_date || null, end_date || null]
    );

    res.json({
      success: true,
      data: result.rows,
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Mesaj teslimat oranı
 */
export const getDeliveryRate = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const result = await query(
      `SELECT
        message_type,
        COUNT(*) as total,
        SUM(CASE WHEN mr.status = 'delivered' THEN 1 ELSE 0 END) as delivered,
        SUM(CASE WHEN mr.status = 'failed' THEN 1 ELSE 0 END) as failed,
        SUM(CASE WHEN mr.status = 'pending' THEN 1 ELSE 0 END) as pending,
        ROUND(AVG(CASE WHEN mr.status = 'delivered' THEN 100.0 ELSE 0 END), 2) as delivery_rate
      FROM messages m
      LEFT JOIN message_recipients mr ON m.id = mr.message_id
      WHERE m.created_at >= CURRENT_DATE - INTERVAL '30 days'
      GROUP BY message_type`
    );

    res.json({
      success: true,
      data: result.rows,
    });
  } catch (error) {
    throw error;
  }
};
