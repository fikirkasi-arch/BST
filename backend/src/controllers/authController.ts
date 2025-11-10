import { Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { query } from '../config/database';
import { AppError } from '../middleware/errorHandler';
import { LoginCredentials, LoginResponse } from '../types';

export const register = async (req: Request, res: Response): Promise<void> => {
  try {
    const { username, email, password, full_name, role, phone } = req.body;

    // Kullanıcı adı kontrolü
    const existingUser = await query(
      'SELECT * FROM users WHERE username = $1 OR email = $2',
      [username, email]
    );

    if (existingUser.rows.length > 0) {
      throw new AppError('Kullanıcı adı veya email zaten kullanılıyor', 400);
    }

    // Şifreyi hashle
    const salt = await bcrypt.genSalt(10);
    const password_hash = await bcrypt.hash(password, salt);

    // Kullanıcıyı oluştur
    const result = await query(
      `INSERT INTO users (username, email, password_hash, full_name, role, phone)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING id, username, email, full_name, role, phone, is_active, created_at`,
      [username, email, password_hash, full_name, role || 'teacher', phone]
    );

    const user = result.rows[0];

    res.status(201).json({
      success: true,
      message: 'Kullanıcı başarıyla oluşturuldu',
      data: user,
    });
  } catch (error) {
    throw error;
  }
};

export const login = async (req: Request, res: Response): Promise<void> => {
  try {
    const { username, password }: LoginCredentials = req.body;

    // Kullanıcıyı bul
    const result = await query(
      'SELECT * FROM users WHERE username = $1 AND is_active = true',
      [username]
    );

    if (result.rows.length === 0) {
      throw new AppError('Geçersiz kullanıcı adı veya şifre', 401);
    }

    const user = result.rows[0];

    // Şifreyi kontrol et
    const isPasswordValid = await bcrypt.compare(password, user.password_hash);

    if (!isPasswordValid) {
      throw new AppError('Geçersiz kullanıcı adı veya şifre', 401);
    }

    // JWT token oluştur
    const secret = process.env.JWT_SECRET || 'your_jwt_secret';
    const expiresIn = process.env.JWT_EXPIRES_IN || '7d';

    const token = jwt.sign(
      {
        userId: user.id,
        username: user.username,
        role: user.role,
      },
      secret,
      { expiresIn: expiresIn as string }
    );

    const response: LoginResponse = {
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        role: user.role,
      },
    };

    res.json({
      success: true,
      message: 'Giriş başarılı',
      data: response,
    });
  } catch (error) {
    throw error;
  }
};

export const getCurrentUser = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const userId = (req as any).user.userId;

    const result = await query(
      'SELECT id, username, email, full_name, role, phone, is_active FROM users WHERE id = $1',
      [userId]
    );

    if (result.rows.length === 0) {
      throw new AppError('Kullanıcı bulunamadı', 404);
    }

    res.json({
      success: true,
      data: result.rows[0],
    });
  } catch (error) {
    throw error;
  }
};

export const updatePassword = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const userId = (req as any).user.userId;
    const { currentPassword, newPassword } = req.body;

    // Mevcut kullanıcıyı al
    const result = await query('SELECT * FROM users WHERE id = $1', [userId]);

    if (result.rows.length === 0) {
      throw new AppError('Kullanıcı bulunamadı', 404);
    }

    const user = result.rows[0];

    // Mevcut şifreyi kontrol et
    const isPasswordValid = await bcrypt.compare(
      currentPassword,
      user.password_hash
    );

    if (!isPasswordValid) {
      throw new AppError('Mevcut şifre yanlış', 401);
    }

    // Yeni şifreyi hashle
    const salt = await bcrypt.genSalt(10);
    const newPasswordHash = await bcrypt.hash(newPassword, salt);

    // Şifreyi güncelle
    await query(
      'UPDATE users SET password_hash = $1, updated_at = NOW() WHERE id = $2',
      [newPasswordHash, userId]
    );

    res.json({
      success: true,
      message: 'Şifre başarıyla güncellendi',
    });
  } catch (error) {
    throw error;
  }
};
