
const questions = [
    {
        question: "Yapay Zeka (AI) nedir?",
        options: [
            "Bilgisayarların insan gibi düşünmesini ve öğrenmesini sağlayan teknoloji",
            "Sadece oyun oynamak için kullanılan program",
            "Robot yapımında kullanılan bir metal",
            "İnternet bağlantısı sağlayan cihaz"
        ],
        correct: 0
    },
    {
        question: "Hangisi yapay zeka kullanan bir uygulamadır?",
        options: [
            "Kağıt ve kalem",
            "Siri veya Google Asistan gibi sesli asistanlar",
            "Cetvel",
            "Silgi"
        ],
        correct: 1
    },
    {
        question: "Netflix'in size film önermesi hangi yapay zeka özelliğini kullanır?",
        options: [
            "Rastgele seçim",
            "Alfabetik sıralama",
            "Makine öğrenmesi ve tahmin sistemleri",
            "Manuel seçim"
        ],
        correct: 2
    },
    {
        question: "Yapay zekanın öğrenmesi için neye ihtiyacı vardır?",
        options: [
            "Elektrik",
            "Veri (Data)",
            "Kağıt",
            "Müzik"
        ],
        correct: 1
    },
    {
        question: "Hangisi yapay zeka kullanım alanlarından DEĞİLDİR?",
        options: [
            "Hastalık teşhisi",
            "Otonom araçlar (sürücüsüz arabalar)",
            "Yüz tanıma sistemleri",
            "Kalem üretimi"
        ],
        correct: 3
    },
    {
        question: "Chatbot (Sohbet robotu) ne işe yarar?",
        options: [
            "Yemek pişirir",
            "İnsanlarla metin üzerinden otomatik konuşur",
            "Ev temizler",
            "Araba sürer"
        ],
        correct: 1
    },
    {
        question: "Yapay zeka hangi durumda yanlış karar verebilir?",
        options: [
            "Yeterli ve doğru veriyle eğitildiğinde",
            "Yanlış veya önyargılı verilerle eğitildiğinde",
            "İnsan gözetiminde çalıştığında",
            "Düzenli güncellendiğinde"
        ],
        correct: 1
    },
    {
        question: "Hangi oyun yapay zeka ile bilgisayara karşı oynanır?",
        options: [
            "Saklambaç",
            "Satranç (bilgisayara karşı)",
            "Körebe",
            "İp atlama"
        ],
        correct: 1
    },
    {
        question: "Yapay zekanın etik kullanımı için hangisi ÖNEMLİ DEĞİLDİR?",
        options: [
            "İnsanların mahremiyetine saygı",
            "Adil ve önyargısız olması",
            "Sadece kar amacı gütmesi",
            "Güvenli ve kontrollü kullanım"
        ],
        correct: 2
    },
    {
        question: "Yapay zeka geleceğimizde nasıl bir rol oynayabilir?",
        options: [
            "Hayatımızı hiç etkilemez",
            "Sadece oyunlarda kullanılır",
            "Sağlık, eğitim, ulaşım gibi birçok alanda yardımcı olabilir",
            "Teknoloji ortadan kaldırır"
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
        message = "Mükemmel! Yapay zeka konusunda uzman oldun! 🤖✨";
    } else if (percentage >= 60) {
        message = "Güzel! Yapay zekayı iyi anlıyorsun! 👍";
    } else if (percentage >= 40) {
        message = "Fena değil! Biraz daha çalışarak gelişebilirsin! 💪";
    } else {
        message = "Yapay zeka konusunu tekrar çalışmalısın! 📚";
    }

    document.getElementById('quiz').innerHTML = `
        <div style="text-align:center; padding: 40px 0;">
            <h2 style="color: #667eea; margin-bottom: 20px;">🎉 Quiz Tamamlandı!</h2>
            <p style="font-size: 2em; margin: 20px 0; color: #764ba2;"><strong>${score} / ${questions.length * 10}</strong></p>
            <p style="font-size: 1.3em; color: #666; margin: 15px 0;">Başarı Oranı: <strong>%${percentage}</strong></p>
            <p style="font-size: 1.2em; color: #333; margin: 20px 0;">${message}</p>
            <div style="background: #f0f4ff; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left;">
                <h3 style="color: #667eea;">🤖 Yapay Zeka Hakkında:</h3>
                <ul style="line-height: 2; margin-top: 10px;">
                    <li>AI öğrenmek için veri kullanır</li>
                    <li>Sesli asistanlar (Siri, Alexa) AI kullanır</li>
                    <li>Netflix ve YouTube AI ile öneri yapar</li>
                    <li>Otonom araçlar AI ile çalışır</li>
                    <li>AI etik kullanılmalıdır</li>
                    <li>Geleceğin teknolojisidir!</li>
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
