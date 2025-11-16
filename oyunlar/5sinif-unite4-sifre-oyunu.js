
const questions = [
    {
        question: "Güçlü bir şifrede hangi özellikler bulunmalıdır?",
        options: [
            "Büyük-küçük harf, rakam ve özel karakter",
            "Sadece rakamlar",
            "Sadece harfler",
            "Sadece isminiz"
        ],
        correct: 0
    },
    {
        question: "Hangisi ZAYIF bir şifredir?",
        options: [
            "Tr@p45*mK!",
            "123456",
            "Gx9#kLm2$pR",
            "aB7!xY3@zQ"
        ],
        correct: 1
    },
    {
        question: "Şifreniz kaç karakterden az olmamalıdır?",
        options: ["4 karakter", "6 karakter", "8 karakter", "10 karakter"],
        correct: 2
    },
    {
        question: "Şifrenizi kiminle paylaşmalısınız?",
        options: [
            "En yakın arkadaşınızla",
            "Öğretmeninizle",
            "Hiç kimseyle paylaşmamalısınız",
            "Sınıf arkadaşlarınızla"
        ],
        correct: 2
    },
    {
        question: "Hangi şifre daha güçlüdür?",
        options: [
            "adı123",
            "Ankara",
            "Benim@S1fr3m!",
            "123456789"
        ],
        correct: 2
    },
    {
        question: "Şifrenizi ne sıklıkta değiştirmelisiniz?",
        options: [
            "Hiç değiştirmemeliyim",
            "Düzenli aralıklarla (3-6 ayda bir)",
            "Her gün",
            "Yılda bir kere"
        ],
        correct: 1
    },
    {
        question: "Şifrenizi hangi yerde saklamamalısınız?",
        options: [
            "Aklınızda",
            "Bilgisayarınızın ekranına yapıştırılan not kağıdında",
            "Şifreli not defterinde",
            "Güvenli şifre yöneticisinde"
        ],
        correct: 1
    },
    {
        question: "Hangisi güvenli bir şifre oluşturma yöntemidir?",
        options: [
            "Doğum tarihini kullanmak",
            "İsminizi yazmak",
            "Anlamlı bir cümlenin baş harflerini almak ve rakam eklemek",
            "123456 yazmak"
        ],
        correct: 2
    },
    {
        question: "Farklı sitelerde aynı şifreyi kullanmalı mıyız?",
        options: [
            "Evet, hatırlaması kolay olsun",
            "Hayır, her site için farklı şifre kullanmalıyız",
            "Sadece önemli sitelerde farklı şifre",
            "Fark etmez"
        ],
        correct: 1
    },
    {
        question: "Şifrenizi unutursanız ne yapmalısınız?",
        options: [
            "Yeni hesap açmalısınız",
            "Vazgeçmelisiniz",
            "'Şifremi Unuttum' seçeneğini kullanmalısınız",
            "Rastgele şifreler denemelisiniz"
        ],
        correct: 2
    }
];

let currentQuestion = 0;
let score = 0;

function loadQuestion() {
    if (currentQuestion >= questions.length) {
        showResult();
        return;
    }

    const q = questions[currentQuestion];
    document.getElementById('question').textContent = `Soru ${currentQuestion + 1}/${questions.length}: ${q.question}`;

    const optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = '';

    q.options.forEach((option, index) => {
        const div = document.createElement('div');
        div.className = 'option';
        div.textContent = option;
        div.onclick = () => checkAnswer(index);
        optionsDiv.appendChild(div);
    });

    document.getElementById('nextBtn').style.display = 'none';
}

function checkAnswer(selected) {
    const q = questions[currentQuestion];
    const options = document.querySelectorAll('.option');

    options.forEach((opt, i) => {
        opt.style.pointerEvents = 'none';
        if (i === q.correct) {
            opt.classList.add('correct');
        } else if (i === selected && selected !== q.correct) {
            opt.classList.add('wrong');
        }
    });

    if (selected === q.correct) {
        score += 10;
        document.getElementById('score').textContent = score;
    }

    document.getElementById('nextBtn').style.display = 'block';
}

function nextQuestion() {
    currentQuestion++;
    loadQuestion();
}

function showResult() {
    const percentage = Math.round((score / (questions.length * 10)) * 100);
    let message;

    if (percentage >= 80) {
        message = "Harika! Şifre güvenliği konusunda uzman oldun! 🔐";
    } else if (percentage >= 60) {
        message = "İyi! Şifre güvenliğini anlıyorsun! 👍";
    } else if (percentage >= 40) {
        message = "Fena değil! Biraz daha çalışmalısın! 💪";
    } else {
        message = "Şifre güvenliği konusunu tekrar çalışmalısın! 📚";
    }

    document.getElementById('quiz').innerHTML = `
        <div style="text-align:center; padding: 40px 0;">
            <h2 style="color: #667eea; margin-bottom: 20px;">🎉 Quiz Tamamlandı!</h2>
            <p style="font-size: 2em; margin: 20px 0; color: #764ba2;"><strong>${score} / ${questions.length * 10}</strong></p>
            <p style="font-size: 1.3em; color: #666; margin: 15px 0;">Başarı Oranı: <strong>%${percentage}</strong></p>
            <p style="font-size: 1.2em; color: #333; margin: 20px 0;">${message}</p>
            <div style="background: #e7f3ff; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left;">
                <h3 style="color: #667eea;">🔒 Güçlü Şifre İpuçları:</h3>
                <ul style="line-height: 2; margin-top: 10px;">
                    <li>En az 8 karakter kullan</li>
                    <li>Büyük-küçük harf karıştır</li>
                    <li>Rakam ve özel karakter ekle (!@#$%)</li>
                    <li>Kişisel bilgi kullanma</li>
                    <li>Her site için farklı şifre</li>
                    <li>Düzenli olarak değiştir</li>
                </ul>
            </div>
        </div>
    `;
    document.getElementById('resetBtn').style.display = 'block';
}

function resetQuiz() {
    currentQuestion = 0;
    score = 0;
    document.getElementById('score').textContent = score;
    document.getElementById('resetBtn').style.display = 'none';
    loadQuestion();
}

loadQuestion();
