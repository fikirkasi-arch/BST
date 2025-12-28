import { Request, Response } from 'express';
import { query } from '../config/database';
import { AppError } from '../middleware/errorHandler';
import xlsx from 'xlsx';
import multer from 'multer';
import path from 'path';

/**
 * Tüm öğrencileri getir
 */
export const getStudents = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { page = 1, limit = 50, class_id, search } = req.query;
    const offset = (Number(page) - 1) * Number(limit);

    let queryText = `
      SELECT s.*, c.name as class_name, c.grade_level
      FROM students s
      LEFT JOIN classes c ON s.class_id = c.id
      WHERE s.is_active = true
    `;

    const params: any[] = [];

    if (class_id) {
      params.push(class_id);
      queryText += ` AND s.class_id = $${params.length}`;
    }

    if (search) {
      params.push(`%${search}%`);
      queryText += ` AND (s.first_name ILIKE $${params.length} OR s.last_name ILIKE $${params.length} OR s.student_number ILIKE $${params.length})`;
    }

    queryText += ` ORDER BY s.student_number LIMIT $${params.length + 1} OFFSET $${params.length + 2}`;
    params.push(Number(limit), offset);

    const result = await query(queryText, params);

    // Toplam kayıt sayısı
    const countResult = await query(
      'SELECT COUNT(*) FROM students WHERE is_active = true'
    );
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
 * Öğrenci detayı
 */
export const getStudentById = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { id } = req.params;

    const studentResult = await query(
      `SELECT s.*, c.name as class_name, c.grade_level
       FROM students s
       LEFT JOIN classes c ON s.class_id = c.id
       WHERE s.id = $1`,
      [id]
    );

    if (studentResult.rows.length === 0) {
      throw new AppError('Öğrenci bulunamadı', 404);
    }

    const student = studentResult.rows[0];

    // Velileri getir
    const parentsResult = await query(
      `SELECT p.*, sp.is_primary
       FROM parents p
       JOIN student_parents sp ON p.id = sp.parent_id
       WHERE sp.student_id = $1`,
      [id]
    );

    res.json({
      success: true,
      data: {
        ...student,
        parents: parentsResult.rows,
      },
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Yeni öğrenci ekle
 */
export const createStudent = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const {
      student_number,
      first_name,
      last_name,
      class_id,
      date_of_birth,
    } = req.body;

    // Öğrenci numarası kontrolü
    const existing = await query(
      'SELECT * FROM students WHERE student_number = $1',
      [student_number]
    );

    if (existing.rows.length > 0) {
      throw new AppError('Bu öğrenci numarası zaten kullanılıyor', 400);
    }

    const result = await query(
      `INSERT INTO students (student_number, first_name, last_name, class_id, date_of_birth)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING *`,
      [student_number, first_name, last_name, class_id || null, date_of_birth || null]
    );

    res.status(201).json({
      success: true,
      message: 'Öğrenci başarıyla eklendi',
      data: result.rows[0],
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Öğrenci güncelle
 */
export const updateStudent = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { id } = req.params;
    const { student_number, first_name, last_name, class_id, date_of_birth } =
      req.body;

    const result = await query(
      `UPDATE students
       SET student_number = $1, first_name = $2, last_name = $3,
           class_id = $4, date_of_birth = $5, updated_at = NOW()
       WHERE id = $6
       RETURNING *`,
      [student_number, first_name, last_name, class_id, date_of_birth, id]
    );

    if (result.rows.length === 0) {
      throw new AppError('Öğrenci bulunamadı', 404);
    }

    res.json({
      success: true,
      message: 'Öğrenci başarıyla güncellendi',
      data: result.rows[0],
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Öğrenci sil (soft delete)
 */
export const deleteStudent = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { id } = req.params;

    const result = await query(
      'UPDATE students SET is_active = false, updated_at = NOW() WHERE id = $1 RETURNING *',
      [id]
    );

    if (result.rows.length === 0) {
      throw new AppError('Öğrenci bulunamadı', 404);
    }

    res.json({
      success: true,
      message: 'Öğrenci başarıyla silindi',
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Öğrenciye veli ekle
 */
export const addParentToStudent = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { student_id, parent_id, is_primary } = req.body;

    // İlişki kontrolü
    const existing = await query(
      'SELECT * FROM student_parents WHERE student_id = $1 AND parent_id = $2',
      [student_id, parent_id]
    );

    if (existing.rows.length > 0) {
      throw new AppError('Bu ilişki zaten mevcut', 400);
    }

    const result = await query(
      `INSERT INTO student_parents (student_id, parent_id, is_primary)
       VALUES ($1, $2, $3)
       RETURNING *`,
      [student_id, parent_id, is_primary || false]
    );

    res.status(201).json({
      success: true,
      message: 'Veli öğrenciye başarıyla eklendi',
      data: result.rows[0],
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Excel/CSV dosyasından toplu öğrenci ekleme
 */
export const importStudentsFromExcel = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    if (!req.file) {
      throw new AppError('Dosya yüklenmedi', 400);
    }

    const filePath = req.file.path;
    const workbook = xlsx.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const data = xlsx.utils.sheet_to_json(worksheet);

    let successCount = 0;
    let errorCount = 0;
    const errors: any[] = [];

    for (const row of data as any[]) {
      try {
        // Öğrenci bilgilerini al
        const studentNumber = row['Öğrenci No'] || row['student_number'];
        const firstName = row['Ad'] || row['first_name'];
        const lastName = row['Soyad'] || row['last_name'];
        const classId = row['Sınıf ID'] || row['class_id'];
        const dateOfBirth = row['Doğum Tarihi'] || row['date_of_birth'];

        // Veli bilgilerini al
        const parentFirstName = row['Veli Ad'] || row['parent_first_name'];
        const parentLastName = row['Veli Soyad'] || row['parent_last_name'];
        const parentPhone = row['Veli Telefon'] || row['parent_phone'];
        const parentEmail = row['Veli Email'] || row['parent_email'];
        const relationship = row['Yakınlık'] || row['relationship'] || 'veli';

        if (!studentNumber || !firstName || !lastName) {
          errors.push({ row, error: 'Öğrenci no, ad ve soyad zorunludur' });
          errorCount++;
          continue;
        }

        // Öğrenciyi ekle
        const studentResult = await query(
          `INSERT INTO students (student_number, first_name, last_name, class_id, date_of_birth)
           VALUES ($1, $2, $3, $4, $5)
           ON CONFLICT (student_number)
           DO UPDATE SET first_name = $2, last_name = $3, class_id = $4, date_of_birth = $5
           RETURNING id`,
          [studentNumber, firstName, lastName, classId || null, dateOfBirth || null]
        );

        const studentId = studentResult.rows[0].id;

        // Veli bilgisi varsa veli ekle
        if (parentPhone) {
          await query(
            `INSERT INTO parents (first_name, last_name, phone, email, relationship)
             VALUES ($1, $2, $3, $4, $5)
             ON CONFLICT (phone)
             DO UPDATE SET first_name = $1, last_name = $2, email = $4
             RETURNING id`,
            [parentFirstName || '', parentLastName || '', parentPhone, parentEmail || null, relationship]
          );

          // Öğrenci-veli ilişkisini ekle
          const parentResult = await query(
            'SELECT id FROM parents WHERE phone = $1',
            [parentPhone]
          );

          if (parentResult.rows.length > 0) {
            await query(
              `INSERT INTO student_parents (student_id, parent_id)
               VALUES ($1, $2)
               ON CONFLICT (student_id, parent_id) DO NOTHING`,
              [studentId, parentResult.rows[0].id]
            );
          }
        }

        successCount++;
      } catch (error: any) {
        errors.push({ row, error: error.message });
        errorCount++;
      }
    }

    res.json({
      success: true,
      message: 'Import işlemi tamamlandı',
      data: {
        total: data.length,
        success: successCount,
        failed: errorCount,
        errors: errors.slice(0, 10), // İlk 10 hatayı göster
      },
    });
  } catch (error) {
    throw error;
  }
};

/**
 * Örnek Excel şablonunu indir
 */
export const downloadExcelTemplate = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const template = [
      {
        'Öğrenci No': '12345',
        'Ad': 'Ahmet',
        'Soyad': 'Yılmaz',
        'Sınıf ID': '1',
        'Doğum Tarihi': '2010-01-15',
        'Veli Ad': 'Mehmet',
        'Veli Soyad': 'Yılmaz',
        'Veli Telefon': '5551234567',
        'Veli Email': 'mehmet@example.com',
        'Yakınlık': 'baba',
      },
      {
        'Öğrenci No': '12346',
        'Ad': 'Ayşe',
        'Soyad': 'Kaya',
        'Sınıf ID': '1',
        'Doğum Tarihi': '2010-03-20',
        'Veli Ad': 'Fatma',
        'Veli Soyad': 'Kaya',
        'Veli Telefon': '5559876543',
        'Veli Email': 'fatma@example.com',
        'Yakınlık': 'anne',
      },
    ];

    const worksheet = xlsx.utils.json_to_sheet(template);
    const workbook = xlsx.utils.book_new();
    xlsx.utils.book_append_sheet(workbook, worksheet, 'Öğrenciler');

    const buffer = xlsx.write(workbook, { type: 'buffer', bookType: 'xlsx' });

    res.setHeader('Content-Disposition', 'attachment; filename=ogrenci-sablonu.xlsx');
    res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    res.send(buffer);
  } catch (error) {
    throw error;
  }
};
