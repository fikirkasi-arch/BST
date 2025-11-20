
const questions = [
    {
        question: "Scratch'te programı başlatmak için hangi blok kullanılır?",
        options: [
            "Yeşil bayrak tıklandığında",
            "Dur",
            "Bekle",
            "Gizlen"
        ],
        correct: 0
    },
    {
        question: "Scratch'te karakteri (sprite) hareket ettirmek için hangi blok kategorisi kullanılır?",
        options: [
            "Görünümler",
            "Sesler",
            "Hareket",
            "Olaylar"
        ],
        correct: 2
    },
    {
        question: "Scratch'te karakterin bir şey söylemesi için hangi blok kullanılır?",
        options: [
            "10 adım git",
            "2 saniye 'Merhaba' de",
            "Sahneyi değiştir",
            "Müziği başlat"
        ],
        correct: 1
    },
    {
        question: "Scratch'te bir işlemi tekrar tekrar yapmak için hangi blok kullanılır?",
        options: [
            "Eğer ... ise",
            "10 kere tekrarla",
            "Bekle",
            "Durdur"
        ],
        correct: 1
    },
    {
        question: "Scratch'te karakterin kostümünü değiştirmek hangi kategoriye aittir?",
        options: [
            "Hareket",
            "Görünümler",
            "Olaylar",
            "Algılama"
        ],
        correct: 1
    },
    {
        question: "Scratch'te ses çalmak için hangi blok kategorisi kullanılır?",
        options: [
            "Hareket",
            "Görünümler",
            "Sesler",
            "Kontrol"
        ],
        correct: 2
    },
    {
        question: "Scratch'te karakterin başka bir karaktere değip değmediğini kontrol etmek için hangi blok kategorisi kullanılır?",
        options: [
            "Algılama",
            "Hareket",
            "Görünümler",
            "Sesler"
        ],
        correct: 0
    },
    {
        question: "Scratch'te programı durdurmak için hangi blok kullanılır?",
        options: [
            "Başla",
            "10 adım git",
            "Hepsini durdur",
            "Bekle"
        ],
        correct: 2
    },
    {
        question: "Scratch'te bir değişken oluşturmak için hangi blok kategorisi kullanılır?",
        options: [
            "Değişkenler",
            "Hareket",
            "Görünümler",
            "Sesler"
        ],
        correct: 0
    },
    {
        question: "Scratch'te karakterin x ve y koordinatlarını değiştirmek hangi kategoriye aittir?",
        options: [
            "Görünümler",
            "Sesler",
            "Hareket",
            "Kontrol"
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
        message = "Harika! Scratch programlamada ustalaştın! 🎮✨";
    } else if (percentage >= 60) {
        message = "Güzel! Scratch bloklarını iyi biliyorsun! 👍";
    } else if (percentage >= 40) {
        message = "İyi! Biraz daha pratik yapmalısın! 💪";
    } else {
        message = "Scratch'i tekrar çalışmalısın! 📚";
    }

    document.getElementById('quiz').innerHTML = `
        <div style="text-align:center; padding: 40px 0;">
            <h2 style="color: #667eea; margin-bottom: 20px;">🎉 Quiz Tamamlandı!</h2>
            <p style="font-size: 2em; margin: 20px 0; color: #764ba2;"><strong>${score} / ${questions.length * 10}</strong></p>
            <p style="font-size: 1.3em; color: #666; margin: 15px 0;">Başarı Oranı: <strong>%${percentage}</strong></p>
            <p style="font-size: 1.2em; color: #333; margin: 20px 0;">${message}</p>
            <div style="background: #fff3e0; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left;">
                <h3 style="color: #667eea;">🎨 Scratch Blok Kategorileri:</h3>
                <ul style="line-height: 2; margin-top: 10px;">
                    <li><strong>Hareket:</strong> Karakteri hareket ettir</li>
                    <li><strong>Görünümler:</strong> Görünüm ve kostüm değiştir</li>
                    <li><strong>Sesler:</strong> Müzik ve ses çal</li>
                    <li><strong>Olaylar:</strong> Programı başlat/kontrol et</li>
                    <li><strong>Kontrol:</strong> Döngü ve koşullar</li>
                    <li><strong>Algılama:</strong> Dokunma ve mesafe kontrol</li>
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
