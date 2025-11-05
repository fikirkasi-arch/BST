import express from 'express';
import { body } from 'express-validator';
import * as messageController from '../controllers/messageController';
import { authenticate, authorize } from '../middleware/auth';
import { validate } from '../middleware/validation';

const router = express.Router();

/**
 * @route   POST /api/messages/bulk
 * @desc    Toplu mesaj gönder
 * @access  Private (Admin, Manager, Teacher)
 */
router.post(
  '/bulk',
  authenticate,
  validate([
    body('message_type').isIn(['SMS', 'WhatsApp']).withMessage('Geçersiz mesaj tipi'),
    body('content').trim().notEmpty().withMessage('Mesaj içeriği gerekli'),
    body('recipients.type').isIn(['class', 'student_numbers', 'parents', 'staff', 'custom']).withMessage('Geçersiz alıcı tipi'),
  ]),
  messageController.sendBulkMessage
);

/**
 * @route   GET /api/messages
 * @desc    Mesaj listesini getir
 * @access  Private
 */
router.get('/', authenticate, messageController.getMessages);

/**
 * @route   GET /api/messages/:id
 * @desc    Mesaj detayını getir
 * @access  Private
 */
router.get('/:id', authenticate, messageController.getMessageById);

/**
 * @route   DELETE /api/messages/:id/cancel
 * @desc    Zamanlanmış mesajı iptal et
 * @access  Private (Admin, Manager)
 */
router.delete(
  '/:id/cancel',
  authenticate,
  authorize('admin', 'manager'),
  messageController.cancelScheduledMessage
);

export default router;
