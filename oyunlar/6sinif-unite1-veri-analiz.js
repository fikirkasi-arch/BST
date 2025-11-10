
const questions = [
    {
        question: "Veri nedir?",
        options: [
            "Topladığımız bilgi ve sayılar",
            "Sadece harfler",
            "Sadece resimler",
            "Bir oyun"
        ],
        correct: 0
    },
    {
        question: "Verileri görselleştirmek için hangi araç KULLANILMAZ?",
        options: [
            "Grafik",
            "Tablo",
            "Diyagram",
            "Kalem"
        ],
        correct: 3
    },
    {
        question: "Bir sınıfın boy uzunluklarını göstermek için en uygun grafik türü hangisidir?",
        options: [
            "Pasta grafiği",
            "Çubuk grafiği",
            "Harita",
            "Resim"
        ],
        correct: 1
    },
    {
        question: "Pasta grafiği ne zaman kullanılır?",
        options: [
            "Zaman içindeki değişimi göstermek için",
            "Parçaların bütüne oranını göstermek için",
            "Sadece sayıları yazmak için",
            "Resim çizmek için"
        ],
        correct: 1
    },
    {
        question: "Hangi program veri analizi ve grafik oluşturmada kullanılır?",
        options: [
            "Paint",
            "Excel veya Google Sheets",
            "Notepad",
            "Hesap Makinesi"
        ],
        correct: 1
    },
    {
        question: "Verilerin ortalamasını bulmak için ne yapmalıyız?",
        options: [
            "En büyük sayıyı alırız",
            "Tüm sayıları toplar, sayı adedine böleriz",
            "En küçük sayıyı alırız",
            "Rastgele bir sayı seçeriz"
        ],
        correct: 1
    },
    {
        question: "Çizgi grafiği ne zaman kullanılır?",
        options: [
            "Zaman içindeki değişimi göstermek için",
            "Sadece bir değeri göstermek için",
            "Resim çizmek için",
            "Metin yazmak için"
        ],
        correct: 0
    },
    {
        question: "Bir ankette toplanan veriler hangi kategoriye girer?",
        options: [
            "Görsel veri",
            "Anket verisi (birincil veri)",
            "Hatalı veri",
            "Anlamsız veri"
        ],
        correct: 1
    },
    {
        question: "Veri analizi neden önemlidir?",
        options: [
            "Sadece zaman geçirmek için",
            "Karar vermek ve tahmin yapmak için",
            "Hiçbir işe yaramaz",
            "Sadece öğretmenler için"
        ],
        correct: 1
    },
    {
        question: "Hangi grafik türü kıyaslama yapmak için en uygunudur?",
        options: [
            "Pasta grafiği",
            "Çubuk grafiği",
            "Harita",
            "Resim"
        ],
        correct: 1
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
        message = "Mükemmel! Veri analizi konusunda uzman oldun! 📊✨";
    } else if (percentage >= 60) {
        message = "Güzel! Veri analizi yapabiliyorsun! 👍";
    } else if (percentage >= 40) {
        message = "İyi! Biraz daha pratik yapmalısın! 💪";
    } else {
        message = "Veri analizi konusunu tekrar çalışmalısın! 📚";
    }

    document.getElementById('quiz').innerHTML = `
        <div style="text-align:center; padding: 40px 0;">
            <h2 style="color: #667eea; margin-bottom: 20px;">🎉 Quiz Tamamlandı!</h2>
            <p style="font-size: 2em; margin: 20px 0; color: #764ba2;"><strong>${score} / ${questions.length * 10}</strong></p>
            <p style="font-size: 1.3em; color: #666; margin: 15px 0;">Başarı Oranı: <strong>%${percentage}</strong></p>
            <p style="font-size: 1.2em; color: #333; margin: 20px 0;">${message}</p>
            <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left;">
                <h3 style="color: #667eea;">📈 Grafik Türleri:</h3>
                <ul style="line-height: 2; margin-top: 10px;">
                    <li><strong>Çubuk Grafiği:</strong> Karşılaştırma yapmak için</li>
                    <li><strong>Çizgi Grafiği:</strong> Zaman içindeki değişim için</li>
                    <li><strong>Pasta Grafiği:</strong> Parça-bütün ilişkisi için</li>
                    <li><strong>Tablo:</strong> Ham verileri göstermek için</li>
                    <li><strong>Excel/Sheets:</strong> Veri analizi programları</li>
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
