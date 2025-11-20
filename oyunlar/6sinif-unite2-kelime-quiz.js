
const questions = [
    {
        question: "Kelime işlemci programı nedir?",
        options: [
            "Metin yazma ve düzenleme programı",
            "Sadece oyun oynama programı",
            "Sadece resim çizme programı",
            "Video izleme programı"
        ],
        correct: 0
    },
    {
        question: "Hangisi bir kelime işlemci programıdır?",
        options: [
            "Paint",
            "Calculator",
            "Microsoft Word",
            "Media Player"
        ],
        correct: 2
    },
    {
        question: "Kelime işlemcide yazı tipini değiştirmek için hangi özellik kullanılır?",
        options: [
            "Font/Yazı Tipi",
            "Yazdır",
            "Kaydet",
            "Kapat"
        ],
        correct: 0
    },
    {
        question: "Metni kalın (bold) yapmak için hangi kısayol tuşu kullanılır?",
        options: [
            "Ctrl+I",
            "Ctrl+U",
            "Ctrl+B",
            "Ctrl+S"
        ],
        correct: 2
    },
    {
        question: "Metni eğik (italic) yapmak için hangi kısayol tuşu kullanılır?",
        options: [
            "Ctrl+I",
            "Ctrl+B",
            "Ctrl+U",
            "Ctrl+X"
        ],
        correct: 0
    },
    {
        question: "Kelime işlemcide sayfa düzenini (yatay/dikey) değiştirmek için hangi menü kullanılır?",
        options: [
            "Dosya",
            "Düzen (Layout)",
            "Ekle",
            "Görünüm"
        ],
        correct: 1
    },
    {
        question: "Kelime işlemcide tablo eklemek için hangi menü kullanılır?",
        options: [
            "Dosya",
            "Düzenle",
            "Ekle (Insert)",
            "Araçlar"
        ],
        correct: 2
    },
    {
        question: "Metni ortalamak için hangi hizalama seçeneği kullanılır?",
        options: [
            "Sola Hizala",
            "Ortala (Center)",
            "Sağa Hizala",
            "İki Yana Yasla"
        ],
        correct: 1
    },
    {
        question: "Kelime işlemcide yazım hatalarını kontrol etmek için hangi özellik kullanılır?",
        options: [
            "Bul ve Değiştir",
            "Yazım Denetimi (Spell Check)",
            "Kaydet",
            "Yazdır"
        ],
        correct: 1
    },
    {
        question: "Kelime işlemcide madde işareti (bullet) eklemek hangi özelliği kullanır?",
        options: [
            "Tablo",
            "Resim",
            "Madde İşaretleri ve Numaralandırma",
            "Sayfa Numarası"
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
        message = "Harika! Kelime işlemci programlarını mükemmel biliyorsun! 📝✨";
    } else if (percentage >= 60) {
        message = "Güzel! Kelime işlemci kullanabiliyorsun! 👍";
    } else if (percentage >= 40) {
        message = "İyi! Biraz daha pratik yapmalısın! 💪";
    } else {
        message = "Kelime işlemci programlarını tekrar çalışmalısın! 📚";
    }

    document.getElementById('quiz').innerHTML = `
        <div style="text-align:center; padding: 40px 0;">
            <h2 style="color: #667eea; margin-bottom: 20px;">🎉 Quiz Tamamlandı!</h2>
            <p style="font-size: 2em; margin: 20px 0; color: #764ba2;"><strong>${score} / ${questions.length * 10}</strong></p>
            <p style="font-size: 1.3em; color: #666; margin: 15px 0;">Başarı Oranı: <strong>%${percentage}</strong></p>
            <p style="font-size: 1.2em; color: #333; margin: 20px 0;">${message}</p>
            <div style="background: #fff8e1; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left;">
                <h3 style="color: #667eea;">⌨️ Önemli Kısayollar:</h3>
                <ul style="line-height: 2; margin-top: 10px;">
                    <li><strong>Ctrl+B:</strong> Kalın yazı (Bold)</li>
                    <li><strong>Ctrl+I:</strong> Eğik yazı (Italic)</li>
                    <li><strong>Ctrl+U:</strong> Altı çizili (Underline)</li>
                    <li><strong>Ctrl+S:</strong> Kaydet (Save)</li>
                    <li><strong>Ctrl+P:</strong> Yazdır (Print)</li>
                    <li><strong>Ctrl+Z:</strong> Geri al (Undo)</li>
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
