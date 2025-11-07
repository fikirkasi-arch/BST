import express from 'express';
import { body } from 'express-validator';
import multer from 'multer';
import path from 'path';
import * as studentController from '../controllers/studentController';
import { authenticate, authorize } from '../middleware/auth';
import { validate } from '../middleware/validation';

const router = express.Router();

// Multer configuration for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, 'students-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['.xlsx', '.xls', '.csv'];
    const ext = path.extname(file.originalname).toLowerCase();
    if (allowedTypes.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Sadece Excel (.xlsx, .xls) ve CSV dosyaları yüklenebilir'));
    }
  },
  limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
});

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

/**
 * @route   POST /api/students/import
 * @desc    Excel/CSV dosyasından toplu öğrenci içe aktar
 * @access  Private (Admin, Manager)
 */
router.post(
  '/import',
  authenticate,
  authorize('admin', 'manager'),
  upload.single('file'),
  studentController.importStudentsFromExcel
);

/**
 * @route   GET /api/students/template/download
 * @desc    Örnek Excel şablonunu indir
 * @access  Private
 */
router.get(
  '/template/download',
  authenticate,
  studentController.downloadExcelTemplate
);

export default router;
