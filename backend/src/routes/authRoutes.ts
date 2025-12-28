import express from 'express';
import { body } from 'express-validator';
import * as authController from '../controllers/authController';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';

const router = express.Router();

/**
 * @route   POST /api/auth/register
 * @desc    Yeni kullanıcı kaydı
 * @access  Public
 */
router.post(
  '/register',
  validate([
    body('username').trim().isLength({ min: 3 }).withMessage('Kullanıcı adı en az 3 karakter olmalı'),
    body('email').isEmail().withMessage('Geçerli bir email adresi girin'),
    body('password').isLength({ min: 6 }).withMessage('Şifre en az 6 karakter olmalı'),
    body('full_name').trim().notEmpty().withMessage('Ad soyad gerekli'),
    body('role').optional().isIn(['admin', 'manager', 'teacher']).withMessage('Geçersiz rol'),
  ]),
  authController.register
);

/**
 * @route   POST /api/auth/login
 * @desc    Kullanıcı girişi
 * @access  Public
 */
router.post(
  '/login',
  validate([
    body('username').trim().notEmpty().withMessage('Kullanıcı adı gerekli'),
    body('password').notEmpty().withMessage('Şifre gerekli'),
  ]),
  authController.login
);

/**
 * @route   GET /api/auth/me
 * @desc    Mevcut kullanıcı bilgilerini getir
 * @access  Private
 */
router.get('/me', authenticate, authController.getCurrentUser);

/**
 * @route   PUT /api/auth/password
 * @desc    Şifre güncelle
 * @access  Private
 */
router.put(
  '/password',
  authenticate,
  validate([
    body('currentPassword').notEmpty().withMessage('Mevcut şifre gerekli'),
    body('newPassword').isLength({ min: 6 }).withMessage('Yeni şifre en az 6 karakter olmalı'),
  ]),
  authController.updatePassword
);

export default router;
