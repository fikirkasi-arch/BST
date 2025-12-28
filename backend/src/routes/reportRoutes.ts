import express from 'express';
import * as reportController from '../controllers/reportController';
import { authenticate, authorize } from '../middleware/auth';

const router = express.Router();

/**
 * @route   GET /api/reports/general
 * @desc    Genel istatistikleri getir
 * @access  Private
 */
router.get('/general', authenticate, reportController.getGeneralStats);

/**
 * @route   GET /api/reports/messages
 * @desc    Mesaj istatistiklerini getir
 * @access  Private
 */
router.get('/messages', authenticate, reportController.getMessageStats);

/**
 * @route   GET /api/reports/classes
 * @desc    Sınıf bazında istatistikler
 * @access  Private
 */
router.get('/classes', authenticate, reportController.getClassStats);

/**
 * @route   GET /api/reports/attendance
 * @desc    Devamsızlık istatistikleri
 * @access  Private
 */
router.get('/attendance', authenticate, reportController.getAttendanceStats);

/**
 * @route   GET /api/reports/top-absent
 * @desc    En çok devamsızlık yapan öğrenciler
 * @access  Private (Admin, Manager)
 */
router.get(
  '/top-absent',
  authenticate,
  authorize('admin', 'manager'),
  reportController.getTopAbsentStudents
);

/**
 * @route   GET /api/reports/message-cost
 * @desc    Mesaj maliyeti raporu
 * @access  Private (Admin)
 */
router.get(
  '/message-cost',
  authenticate,
  authorize('admin'),
  reportController.getMessageCostReport
);

/**
 * @route   GET /api/reports/delivery-rate
 * @desc    Mesaj teslimat oranı
 * @access  Private
 */
router.get('/delivery-rate', authenticate, reportController.getDeliveryRate);

export default router;
