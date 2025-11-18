// Öğrenci Kimlik Doğrulama Sistemi - BST Eğitim Portalı

const StudentAuth = {
    SESSION_KEY: 'bst_student_session',
    STUDENTS_KEY: 'bstUsers',

    // Kayıt ol
    register(name, studentNumber, grade, email = '') {
        if (!name || !studentNumber || !grade) {
            return { success: false, message: 'Lütfen tüm alanları doldurun!' };
        }

        // Mevcut öğrencileri al
        let students = JSON.parse(localStorage.getItem(this.STUDENTS_KEY) || '[]');

        // Numara kontrolü
        if (students.find(s => s.number === studentNumber)) {
            return { success: false, message: 'Bu öğrenci numarası zaten kayıtlı!' };
        }

        // Yeni öğrenci ekle
        const newStudent = {
            id: Date.now(),
            name: name.trim(),
            number: studentNumber.trim(),
            grade: parseInt(grade),
            email: email.trim(),
            quizScore: 0,
            gamesPlayed: 0,
            lastLogin: new Date().toISOString().split('T')[0],
            status: 'active',
            createdAt: new Date().toISOString()
        };

        students.push(newStudent);
        localStorage.setItem(this.STUDENTS_KEY, JSON.stringify(students));

        // Otomatik giriş yap
        this.createSession(newStudent);

        return { success: true, message: 'Kayıt başarılı!', student: newStudent };
    },

    // Giriş yap
    login(studentNumber) {
        if (!studentNumber) {
            return { success: false, message: 'Lütfen öğrenci numaranızı girin!' };
        }

        const students = JSON.parse(localStorage.getItem(this.STUDENTS_KEY) || '[]');
        const student = students.find(s => s.number === studentNumber.trim());

        if (!student) {
            return { success: false, message: 'Öğrenci bulunamadı! Lütfen kayıt olun.' };
        }

        // Son giriş tarihini güncelle
        student.lastLogin = new Date().toISOString().split('T')[0];
        const index = students.findIndex(s => s.id === student.id);
        students[index] = student;
        localStorage.setItem(this.STUDENTS_KEY, JSON.stringify(students));

        // Oturum oluştur
        this.createSession(student);

        return { success: true, message: 'Giriş başarılı!', student: student };
    },

    // Oturum oluştur
    createSession(student) {
        const session = {
            studentId: student.id,
            name: student.name,
            number: student.number,
            grade: student.grade,
            loginTime: new Date().toISOString()
        };
        localStorage.setItem(this.SESSION_KEY, JSON.stringify(session));
    },

    // Çıkış yap
    logout() {
        localStorage.removeItem(this.SESSION_KEY);
        window.location.href = 'ogrenci-giris.html';
    },

    // Giriş yapılmış mı?
    isLoggedIn() {
        return this.getSession() !== null;
    },

    // Oturum bilgisi al
    getSession() {
        try {
            return JSON.parse(localStorage.getItem(this.SESSION_KEY));
        } catch {
            return null;
        }
    },

    // Mevcut öğrenci bilgisi al
    getCurrentStudent() {
        const session = this.getSession();
        if (!session) return null;

        const students = JSON.parse(localStorage.getItem(this.STUDENTS_KEY) || '[]');
        return students.find(s => s.id === session.studentId) || null;
    },

    // Profil güncelle
    updateProfile(updates) {
        const session = this.getSession();
        if (!session) return { success: false, message: 'Oturum bulunamadı!' };

        const students = JSON.parse(localStorage.getItem(this.STUDENTS_KEY) || '[]');
        const index = students.findIndex(s => s.id === session.studentId);

        if (index === -1) return { success: false, message: 'Öğrenci bulunamadı!' };

        // Güncellenebilir alanlar
        if (updates.name) students[index].name = updates.name.trim();
        if (updates.email) students[index].email = updates.email.trim();
        if (updates.grade) students[index].grade = parseInt(updates.grade);

        localStorage.setItem(this.STUDENTS_KEY, JSON.stringify(students));

        // Oturumu da güncelle
        session.name = students[index].name;
        session.grade = students[index].grade;
        localStorage.setItem(this.SESSION_KEY, JSON.stringify(session));

        return { success: true, message: 'Profil güncellendi!', student: students[index] };
    },

    // Puan güncelle
    updateScore(quizScore, gamesPlayed) {
        const session = this.getSession();
        if (!session) return;

        const students = JSON.parse(localStorage.getItem(this.STUDENTS_KEY) || '[]');
        const index = students.findIndex(s => s.id === session.studentId);

        if (index !== -1) {
            if (quizScore !== undefined) students[index].quizScore = quizScore;
            if (gamesPlayed !== undefined) students[index].gamesPlayed = gamesPlayed;
            localStorage.setItem(this.STUDENTS_KEY, JSON.stringify(students));
        }
    }
};

// Global erişim için
window.StudentAuth = StudentAuth;
