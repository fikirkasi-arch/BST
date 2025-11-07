import express from 'express';
import { body } from 'express-validator';
import * as templateController from '../controllers/templateController';
import { authenticate, authorize } from '../middleware/auth';
import { validate } from '../middleware/validation';

const router = express.Router();

/**
 * @route   GET /api/templates
 * @desc    Tüm mesaj şablonlarını getir
 * @access  Private
 */
router.get('/', authenticate, templateController.getTemplates);

/**
 * @route   GET /api/templates/categories
 * @desc    Şablon kategorilerini getir
 * @access  Private
 */
router.get('/categories', authenticate, templateController.getTemplateCategories);

/**
 * @route   GET /api/templates/:id
 * @desc    Belirli bir şablonu getir
 * @access  Private
 */
router.get('/:id', authenticate, templateController.getTemplateById);

/**
 * @route   POST /api/templates
 * @desc    Yeni şablon oluştur
 * @access  Private (Admin, Manager)
 */
router.post(
  '/',
  authenticate,
  authorize('admin', 'manager'),
  validate([
    body('name').trim().notEmpty().withMessage('Şablon adı gerekli'),
    body('content').trim().notEmpty().withMessage('Şablon içeriği gerekli'),
    body('message_type').isIn(['sms', 'whatsapp', 'email']).withMessage('Geçersiz mesaj tipi'),
  ]),
  templateController.createTemplate
);

/**
 * @route   PUT /api/templates/:id
 * @desc    Şablonu güncelle
 * @access  Private (Admin, Manager)
 */
router.put(
  '/:id',
  authenticate,
  authorize('admin', 'manager'),
  validate([
    body('name').trim().notEmpty().withMessage('Şablon adı gerekli'),
    body('content').trim().notEmpty().withMessage('Şablon içeriği gerekli'),
    body('message_type').isIn(['sms', 'whatsapp', 'email']).withMessage('Geçersiz mesaj tipi'),
  ]),
  templateController.updateTemplate
);

/**
 * @route   DELETE /api/templates/:id
 * @desc    Şablonu sil
 * @access  Private (Admin)
 */
router.delete(
  '/:id',
  authenticate,
  authorize('admin'),
  templateController.deleteTemplate
);

export default router;
