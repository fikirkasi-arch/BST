
const questions = [
    {
        question: "Akış diyagramı nedir?",
        options: [
            "Bir sürecin adımlarını görsel olarak gösteren şema",
            "Sadece resimlerin bulunduğu çizim",
            "Sadece yazı yazılan belge",
            "Müzik notası"
        ],
        correct: 0
    },
    {
        question: "Akış diyagramında oval şekil neyi gösterir?",
        options: [
            "İşlem",
            "Karar",
            "Başlangıç ve Bitiş",
            "Veri girişi"
        ],
        correct: 2
    },
    {
        question: "Akış diyagramında dikdörtgen şekil neyi gösterir?",
        options: [
            "Başlangıç",
            "İşlem/Komut",
            "Karar",
            "Bitiş"
        ],
        correct: 1
    },
    {
        question: "Akış diyagramında baklava şekli (◇) neyi gösterir?",
        options: [
            "Başlangıç",
            "İşlem",
            "Karar verme (Evet/Hayır)",
            "Bitiş"
        ],
        correct: 2
    },
    {
        question: "Algoritma nedir?",
        options: [
            "Bir problemi çözmek için izlenen adımlar dizisi",
            "Sadece matematik işlemi",
            "Bilgisayar markası",
            "Oyun türü"
        ],
        correct: 0
    },
    {
        question: "Akış diyagramında paralelkenar şekil neyi gösterir?",
        options: [
            "İşlem",
            "Karar",
            "Veri girişi/çıkışı",
            "Bitiş"
        ],
        correct: 2
    },
    {
        question: "Bir algoritmanın özellikleri nelerdir?",
        options: [
            "Sadece uzun olmalı",
            "Belirsiz ve karmaşık olmalı",
            "Açık, anlaşılır ve sonlu olmalı",
            "Anlamsız olmalı"
        ],
        correct: 2
    },
    {
        question: "Hangi durumda akış diyagramı kullanılır?",
        options: [
            "Sadece oyun oynarken",
            "Bir sürecin adımlarını planlarken",
            "Sadece resim çizerken",
            "Müzik dinlerken"
        ],
        correct: 1
    },
    {
        question: "Akış diyagramında ok işareti neyi gösterir?",
        options: [
            "Bitiş",
            "Başlangıç",
            "Akışın yönünü ve sırasını",
            "Karar"
        ],
        correct: 2
    },
    {
        question: "Hangisi günlük hayatta kullanılan bir algoritma örneğidir?",
        options: [
            "Kahvaltı hazırlama adımları",
            "Rastgele düşünmek",
            "Anlamsız hareketler",
            "Hiçbir şey yapmamak"
        ],
        correct: 0
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
        message = "Mükemmel! Akış diyagramları konusunda uzman oldun! 📊✨";
    } else if (percentage >= 60) {
        message = "Güzel! Akış diyagramlarını anlıyorsun! 👍";
    } else if (percentage >= 40) {
        message = "İyi! Biraz daha çalışmalısın! 💪";
    } else {
        message = "Akış diyagramları konusunu tekrar çalışmalısın! 📚";
    }

    document.getElementById('quiz').innerHTML = `
        <div style="text-align:center; padding: 40px 0;">
            <h2 style="color: #667eea; margin-bottom: 20px;">🎉 Quiz Tamamlandı!</h2>
            <p style="font-size: 2em; margin: 20px 0; color: #764ba2;"><strong>${score} / ${questions.length * 10}</strong></p>
            <p style="font-size: 1.3em; color: #666; margin: 15px 0;">Başarı Oranı: <strong>%${percentage}</strong></p>
            <p style="font-size: 1.2em; color: #333; margin: 20px 0;">${message}</p>
            <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left;">
                <h3 style="color: #667eea;">🔷 Akış Diyagramı Şekilleri:</h3>
                <ul style="line-height: 2; margin-top: 10px;">
                    <li><strong>Oval:</strong> Başlangıç ve Bitiş</li>
                    <li><strong>Dikdörtgen:</strong> İşlem/Komut</li>
                    <li><strong>Baklava (◇):</strong> Karar (Evet/Hayır)</li>
                    <li><strong>Paralelkenar:</strong> Veri Giriş/Çıkış</li>
                    <li><strong>Ok işareti:</strong> Akış yönü</li>
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
