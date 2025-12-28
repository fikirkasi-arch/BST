import { Request, Response } from 'express';
import { query } from '../config/database';
import { AppError } from '../middleware/errorHandler';

/**
 * Tüm mesaj şablonlarını getir
 */
export const getTemplates = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { message_type, category, search } = req.query;

    let queryText = `
      SELECT mt.*, u.full_name as creator_name
      FROM message_templates mt
      LEFT JOIN users u ON mt.created_by = u.id
      WHERE mt.is_active = true
    `;

    const params: any[] = [];

    if (message_type) {
      params.push(message_type);
      queryText += ` AND mt.message_type = $${params.length}`;
    }

    if (category) {
      params.push(category);
      queryText += ` AND mt.category = $${params.length}`;
    }

    if (search) {
      params.push(`%${search}%`);
      queryText += ` AND (mt.name ILIKE $${params.length} OR mt.content ILIKE $${params.length})`;
    }

    queryText += ` ORDER BY mt.created_at DESC`;

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
 * Belirli bir şablonu getir
 */
export const getTemplateById = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { id } = req.params;

    const result = await query(
      `SELECT mt.*, u.full_name as creator_name
       FROM message_templates mt
       LEFT JOIN users u ON mt.created_by = u.id
       WHERE mt.id = $1`,
      [id]
    );

    if (result.rows.length === 0) {
      throw new AppError('Şablon bulunamadı', 404);
    }

    res.json({
      success: true,
      data: result.rows[0],
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Yeni şablon oluştur
 */
export const createTemplate = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { name, content, message_type, category, variables } = req.body;
    const userId = (req as any).user.id;

    const result = await query(
      `INSERT INTO message_templates (name, content, message_type, category, variables, created_by)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [name, content, message_type, category || null, variables || [], userId]
    );

    res.status(201).json({
      success: true,
      message: 'Şablon başarıyla oluşturuldu',
      data: result.rows[0],
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Şablonu güncelle
 */
export const updateTemplate = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { id } = req.params;
    const { name, content, message_type, category, variables, is_active } = req.body;

    const result = await query(
      `UPDATE message_templates
       SET name = $1, content = $2, message_type = $3, category = $4,
           variables = $5, is_active = $6, updated_at = CURRENT_TIMESTAMP
       WHERE id = $7
       RETURNING *`,
      [name, content, message_type, category, variables || [], is_active !== undefined ? is_active : true, id]
    );

    if (result.rows.length === 0) {
      throw new AppError('Şablon bulunamadı', 404);
    }

    res.json({
      success: true,
      message: 'Şablon başarıyla güncellendi',
      data: result.rows[0],
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Şablonu sil
 */
export const deleteTemplate = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { id } = req.params;

    const result = await query(
      `UPDATE message_templates
       SET is_active = false, updated_at = CURRENT_TIMESTAMP
       WHERE id = $1
       RETURNING *`,
      [id]
    );

    if (result.rows.length === 0) {
      throw new AppError('Şablon bulunamadı', 404);
    }

    res.json({
      success: true,
      message: 'Şablon başarıyla silindi',
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Şablon kategorilerini getir
 */
export const getTemplateCategories = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const result = await query(
      `SELECT DISTINCT category
       FROM message_templates
       WHERE category IS NOT NULL AND is_active = true
       ORDER BY category`
    );

    const categories = result.rows.map(row => row.category);

    res.json({
      success: true,
      data: categories,
    });
  } catch (error) {
    throw error;
  }
};
