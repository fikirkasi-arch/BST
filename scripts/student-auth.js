// Kullanıcı Kimlik Doğrulama Sistemi - BST Eğitim Portalı
// Öğrenci ve Öğretmen desteği

const UserAuth = {
    SESSION_KEY: 'bst_user_session',
    STUDENTS_KEY: 'bstUsers',
    TEACHERS_KEY: 'bstTeachers',

    // Öğrenci Kayıt
    registerStudent(name, studentNumber, grade, email = '') {
        if (!name || !studentNumber || !grade) {
            return { success: false, message: 'Lütfen tüm alanları doldurun!' };
        }

        let students = JSON.parse(localStorage.getItem(this.STUDENTS_KEY) || '[]');

        if (students.find(s => s.number === studentNumber)) {
            return { success: false, message: 'Bu öğrenci numarası zaten kayıtlı!' };
        }

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
            userType: 'student',
            createdAt: new Date().toISOString()
        };

        students.push(newStudent);
        localStorage.setItem(this.STUDENTS_KEY, JSON.stringify(students));
        this.createSession(newStudent, 'student');

        return { success: true, message: 'Kayıt başarılı!', user: newStudent };
    },

    // Öğretmen Kayıt
    registerTeacher(name, email, school = '', branch = '') {
        if (!name || !email) {
            return { success: false, message: 'Lütfen ad ve e-posta alanlarını doldurun!' };
        }

        let teachers = JSON.parse(localStorage.getItem(this.TEACHERS_KEY) || '[]');

        if (teachers.find(t => t.email === email)) {
            return { success: false, message: 'Bu e-posta adresi zaten kayıtlı!' };
        }

        const newTeacher = {
            id: Date.now(),
            name: name.trim(),
            email: email.trim(),
            school: school.trim(),
            branch: branch.trim(),
            lastLogin: new Date().toISOString().split('T')[0],
            status: 'active',
            userType: 'teacher',
            createdAt: new Date().toISOString()
        };

        teachers.push(newTeacher);
        localStorage.setItem(this.TEACHERS_KEY, JSON.stringify(teachers));
        this.createSession(newTeacher, 'teacher');

        return { success: true, message: 'Kayıt başarılı!', user: newTeacher };
    },

    // Öğrenci Giriş
    loginStudent(studentNumber) {
        if (!studentNumber) {
            return { success: false, message: 'Lütfen öğrenci numaranızı girin!' };
        }

        const students = JSON.parse(localStorage.getItem(this.STUDENTS_KEY) || '[]');
        const student = students.find(s => s.number === studentNumber.trim());

        if (!student) {
            return { success: false, message: 'Öğrenci bulunamadı! Lütfen kayıt olun.' };
        }

        student.lastLogin = new Date().toISOString().split('T')[0];
        const index = students.findIndex(s => s.id === student.id);
        students[index] = student;
        localStorage.setItem(this.STUDENTS_KEY, JSON.stringify(students));

        this.createSession(student, 'student');
        return { success: true, message: 'Giriş başarılı!', user: student };
    },

    // Öğretmen Giriş
    loginTeacher(email) {
        if (!email) {
            return { success: false, message: 'Lütfen e-posta adresinizi girin!' };
        }

        const teachers = JSON.parse(localStorage.getItem(this.TEACHERS_KEY) || '[]');
        const teacher = teachers.find(t => t.email === email.trim());

        if (!teacher) {
            return { success: false, message: 'Öğretmen bulunamadı! Lütfen kayıt olun.' };
        }

        teacher.lastLogin = new Date().toISOString().split('T')[0];
        const index = teachers.findIndex(t => t.id === teacher.id);
        teachers[index] = teacher;
        localStorage.setItem(this.TEACHERS_KEY, JSON.stringify(teachers));

        this.createSession(teacher, 'teacher');
        return { success: true, message: 'Giriş başarılı!', user: teacher };
    },

    // Oturum oluştur
    createSession(user, userType) {
        const session = {
            userId: user.id,
            name: user.name,
            userType: userType,
            email: user.email || '',
            number: user.number || '',
            grade: user.grade || '',
            school: user.school || '',
            branch: user.branch || '',
            loginTime: new Date().toISOString()
        };
        localStorage.setItem(this.SESSION_KEY, JSON.stringify(session));
    },

    // Çıkış yap
    logout() {
        localStorage.removeItem(this.SESSION_KEY);
        window.location.href = 'giris.html';
    },

    // Giriş yapılmış mı?
    isLoggedIn() {
        return this.getSession() !== null;
    },

    // Öğretmen mi?
    isTeacher() {
        const session = this.getSession();
        return session && session.userType === 'teacher';
    },

    // Öğrenci mi?
    isStudent() {
        const session = this.getSession();
        return session && session.userType === 'student';
    },

    // Oturum bilgisi al
    getSession() {
        try {
            return JSON.parse(localStorage.getItem(this.SESSION_KEY));
        } catch {
            return null;
        }
    },

    // Mevcut kullanıcı bilgisi al
    getCurrentUser() {
        const session = this.getSession();
        if (!session) return null;

        if (session.userType === 'student') {
            const students = JSON.parse(localStorage.getItem(this.STUDENTS_KEY) || '[]');
            return students.find(s => s.id === session.userId) || null;
        } else {
            const teachers = JSON.parse(localStorage.getItem(this.TEACHERS_KEY) || '[]');
            return teachers.find(t => t.id === session.userId) || null;
        }
    },

    // Profil güncelle
    updateProfile(updates) {
        const session = this.getSession();
        if (!session) return { success: false, message: 'Oturum bulunamadı!' };

        if (session.userType === 'student') {
            const students = JSON.parse(localStorage.getItem(this.STUDENTS_KEY) || '[]');
            const index = students.findIndex(s => s.id === session.userId);
            if (index === -1) return { success: false, message: 'Kullanıcı bulunamadı!' };

            if (updates.name) students[index].name = updates.name.trim();
            if (updates.email) students[index].email = updates.email.trim();
            if (updates.grade) students[index].grade = parseInt(updates.grade);

            localStorage.setItem(this.STUDENTS_KEY, JSON.stringify(students));

            session.name = students[index].name;
            session.grade = students[index].grade;
            localStorage.setItem(this.SESSION_KEY, JSON.stringify(session));

            return { success: true, message: 'Profil güncellendi!', user: students[index] };
        } else {
            const teachers = JSON.parse(localStorage.getItem(this.TEACHERS_KEY) || '[]');
            const index = teachers.findIndex(t => t.id === session.userId);
            if (index === -1) return { success: false, message: 'Kullanıcı bulunamadı!' };

            if (updates.name) teachers[index].name = updates.name.trim();
            if (updates.email) teachers[index].email = updates.email.trim();
            if (updates.school) teachers[index].school = updates.school.trim();
            if (updates.branch) teachers[index].branch = updates.branch.trim();

            localStorage.setItem(this.TEACHERS_KEY, JSON.stringify(teachers));

            session.name = teachers[index].name;
            session.school = teachers[index].school;
            session.branch = teachers[index].branch;
            localStorage.setItem(this.SESSION_KEY, JSON.stringify(session));

            return { success: true, message: 'Profil güncellendi!', user: teachers[index] };
        }
    }
};

// Eski StudentAuth ile uyumluluk
const StudentAuth = {
    isLoggedIn: () => UserAuth.isLoggedIn(),
    getSession: () => UserAuth.getSession(),
    getCurrentStudent: () => UserAuth.getCurrentUser(),
    logout: () => UserAuth.logout(),
    login: (number) => UserAuth.loginStudent(number),
    register: (name, number, grade, email) => UserAuth.registerStudent(name, number, grade, email),
    updateProfile: (updates) => UserAuth.updateProfile(updates)
};

// Global erişim
window.UserAuth = UserAuth;
window.StudentAuth = StudentAuth;

