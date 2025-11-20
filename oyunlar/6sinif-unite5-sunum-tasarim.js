
const questions = [
    {
        question: "Hangisi bir sunum programıdır?",
        options: [
            "Microsoft PowerPoint",
            "Paint",
            "Notepad",
            "Calculator"
        ],
        correct: 0
    },
    {
        question: "Sunum hazırlarken hangi kural ÖNEMLİDİR?",
        options: [
            "Slaytları çok fazla yazıyla doldurmak",
            "Okunaksız fontlar kullanmak",
            "Kısa ve öz bilgiler vermek",
            "Karışık renkler kullanmak"
        ],
        correct: 2
    },
    {
        question: "PowerPoint'te yeni bir slayt eklemek için hangi kısayol kullanılır?",
        options: [
            "Ctrl+S",
            "Ctrl+M",
            "Ctrl+P",
            "Ctrl+Z"
        ],
        correct: 1
    },
    {
        question: "Sunum slaytlarına hareketli geçiş efekti eklemek için ne kullanılır?",
        options: [
            "Geçiş (Transition)",
            "Kaydet",
            "Yazdır",
            "Kapat"
        ],
        correct: 0
    },
    {
        question: "Sunum tasarımında hangi yazı tipi boyutu en UYGUN değildir?",
        options: [
            "24-32 punto (başlıklar için)",
            "18-24 punto (metin için)",
            "8-10 punto (çok küçük)",
            "16-20 punto (alt başlıklar için)"
        ],
        correct: 2
    },
    {
        question: "Etkili bir sunumda slayt başına kaç satır metin olmalıdır?",
        options: [
            "50-60 satır",
            "30-40 satır",
            "5-7 satır (madde işareti ile)",
            "100 satır"
        ],
        correct: 2
    },
    {
        question: "Sunum slaytlarına görsel eklemek neden önemlidir?",
        options: [
            "Sadece süsleme için",
            "Anlayışı kolaylaştırmak ve dikkat çekmek için",
            "Zamanı doldurmak için",
            "Hiçbir işe yaramaz"
        ],
        correct: 1
    },
    {
        question: "Sunum sırasında hangi davranış YANLIŞTIR?",
        options: [
            "İzleyicilere bakmak",
            "Açık ve net konuşmak",
            "Sürekli sırt dönüp ekrana bakmak",
            "Güvenli durmak"
        ],
        correct: 2
    },
    {
        question: "PowerPoint'te animasyon eklemek hangi amaca hizmet eder?",
        options: [
            "Sadece gösteriş için",
            "Bilgileri adım adım göstermek ve dikkat çekmek için",
            "Sunumu karmaşıklaştırmak için",
            "Hiçbir işe yaramaz"
        ],
        correct: 1
    },
    {
        question: "İyi bir sunum tasarımında renk kullanımı nasıl olmalıdır?",
        options: [
            "Çok fazla farklı renk kullanılmalı",
            "Sadece siyah beyaz olmalı",
            "Uyumlu ve okunabilir renkler seçilmeli",
            "Hiç renk kullanılmamalı"
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
        message = "Harika! Sunum tasarımında uzman oldun! 🎤✨";
    } else if (percentage >= 60) {
        message = "Güzel! İyi sunumlar hazırlayabilirsin! 👍";
    } else if (percentage >= 40) {
        message = "İyi! Biraz daha pratik yapmalısın! 💪";
    } else {
        message = "Sunum tasarımını tekrar çalışmalısın! 📚";
    }

    document.getElementById('quiz').innerHTML = `
        <div style="text-align:center; padding: 40px 0;">
            <h2 style="color: #667eea; margin-bottom: 20px;">🎉 Quiz Tamamlandı!</h2>
            <p style="font-size: 2em; margin: 20px 0; color: #764ba2;"><strong>${score} / ${questions.length * 10}</strong></p>
            <p style="font-size: 1.3em; color: #666; margin: 15px 0;">Başarı Oranı: <strong>%${percentage}</strong></p>
            <p style="font-size: 1.2em; color: #333; margin: 20px 0;">${message}</p>
            <div style="background: #fce4ec; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left;">
                <h3 style="color: #667eea;">🎨 Etkili Sunum İpuçları:</h3>
                <ul style="line-height: 2; margin-top: 10px;">
                    <li>Kısa ve öz bilgiler kullan</li>
                    <li>Büyük ve okunabilir yazı tipi seç</li>
                    <li>Görseller ekleyerek destekle</li>
                    <li>Uyumlu renkler kullan</li>
                    <li>Slayt başına 5-7 madde yeterli</li>
                    <li>İzleyicilere bakarak sunum yap</li>
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
