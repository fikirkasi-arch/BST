import express from 'express';
import { body } from 'express-validator';
import * as studentController from '../controllers/studentController';
import { authenticate, authorize } from '../middleware/auth';
import { validate } from '../middleware/validation';

const router = express.Router();

/**
 * @route   GET /api/students
 * @desc    Öğrenci listesini getir
 * @access  Private
 */
router.get('/', authenticate, studentController.getStudents);

/**
 * @route   GET /api/students/:id
 * @desc    Öğrenci detayını getir
 * @access  Private
 */
router.get('/:id', authenticate, studentController.getStudentById);

/**
 * @route   POST /api/students
 * @desc    Yeni öğrenci ekle
 * @access  Private (Admin, Manager)
 */
router.post(
  '/',
  authenticate,
  authorize('admin', 'manager'),
  validate([
    body('student_number').trim().notEmpty().withMessage('Öğrenci numarası gerekli'),
    body('first_name').trim().notEmpty().withMessage('Ad gerekli'),
    body('last_name').trim().notEmpty().withMessage('Soyad gerekli'),
  ]),
  studentController.createStudent
);

/**
 * @route   PUT /api/students/:id
 * @desc    Öğrenci güncelle
 * @access  Private (Admin, Manager)
 */
router.put(
  '/:id',
  authenticate,
  authorize('admin', 'manager'),
  validate([
    body('student_number').trim().notEmpty().withMessage('Öğrenci numarası gerekli'),
    body('first_name').trim().notEmpty().withMessage('Ad gerekli'),
    body('last_name').trim().notEmpty().withMessage('Soyad gerekli'),
  ]),
  studentController.updateStudent
);

/**
 * @route   DELETE /api/students/:id
 * @desc    Öğrenci sil
 * @access  Private (Admin)
 */
router.delete(
  '/:id',
  authenticate,
  authorize('admin'),
  studentController.deleteStudent
);

/**
 * @route   POST /api/students/parents
 * @desc    Öğrenciye veli ekle
 * @access  Private (Admin, Manager)
 */
router.post(
  '/parents',
  authenticate,
  authorize('admin', 'manager'),
  validate([
    body('student_id').isInt().withMessage('Geçerli öğrenci ID gerekli'),
    body('parent_id').isInt().withMessage('Geçerli veli ID gerekli'),
  ]),
  studentController.addParentToStudent
);

export default router;
