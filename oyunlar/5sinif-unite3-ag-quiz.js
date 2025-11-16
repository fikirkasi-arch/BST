
const questions = [
    {
        question: "İnternet nedir?",
        options: [
            "Dünya çapında birbirine bağlı bilgisayarlar ağı",
            "Sadece bir ülkedeki bilgisayarlar",
            "Sadece okullardaki bilgisayarlar",
            "Tek bir büyük bilgisayar"
        ],
        correct: 0
    },
    {
        question: "Yerel Alan Ağının kısaltması nedir?",
        options: ["WAN", "LAN", "MAN", "PAN"],
        correct: 1
    },
    {
        question: "Evdeki internet bağlantısını sağlayan cihaz hangisidir?",
        options: ["Yazıcı", "Tarayıcı", "Modem", "Hoparlör"],
        correct: 2
    },
    {
        question: "www.meb.gov.tr adresindeki 'www' ne anlama gelir?",
        options: [
            "World Wide Web (Dünya Çapında Ağ)",
            "Windows Web Writer",
            "Wireless Web World",
            "World Writing Web"
        ],
        correct: 0
    },
    {
        question: "Hangi cihaz farklı ağları birbirine bağlar?",
        options: ["Klavye", "Mouse", "Router (Yönlendirici)", "Monitör"],
        correct: 2
    },
    {
        question: "İnternet sitelerine girmek için kullandığımız program hangisidir?",
        options: [
            "Web Tarayıcı (Chrome, Firefox, Edge)",
            "Word",
            "Paint",
            "Excel"
        ],
        correct: 0
    },
    {
        question: "Her bilgisayarın internetteki benzersiz adresi ne adıyla bilinir?",
        options: ["E-posta adresi", "IP Adresi", "Ev adresi", "Web adresi"],
        correct: 1
    },
    {
        question: "E-posta adresi hangi işaretle yazılır?",
        options: ["@ işareti ile", "# işareti ile", "$ işareti ile", "& işareti ile"],
        correct: 0
    },
    {
        question: "Geniş Alan Ağı'nın kısaltması nedir?",
        options: ["LAN", "MAN", "WAN", "PAN"],
        correct: 2
    },
    {
        question: "İnternette güvenli olmak için ne yapmalıyız?",
        options: [
            "Herkese şifremizi söylemeliyiz",
            "Tanımadığımız kişilerle kişisel bilgilerimizi paylaşmamalıyız",
            "Tüm sitelere üye olmalıyız",
            "Bilgisayarı hep açık bırakmalıyız"
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
        message = "Mükemmel! Ağlar konusunu harika öğrenmişsin! 🌟";
    } else if (percentage >= 60) {
        message = "Güzel! İyi bir performans gösterdin! 👍";
    } else if (percentage >= 40) {
        message = "Fena değil! Biraz daha çalışarak gelişebilirsin! 💪";
    } else {
        message = "Ağlar konusunu tekrar çalışmalısın! 📚";
    }

    document.getElementById('quiz').innerHTML = `
        <div style="text-align:center; padding: 40px 0;">
            <h2 style="color: #667eea; margin-bottom: 20px;">🎉 Quiz Tamamlandı!</h2>
            <p style="font-size: 2em; margin: 20px 0; color: #764ba2;"><strong>${score} / ${questions.length * 10}</strong></p>
            <p style="font-size: 1.3em; color: #666; margin: 15px 0;">Başarı Oranı: <strong>%${percentage}</strong></p>
            <p style="font-size: 1.2em; color: #333; margin: 20px 0;">${message}</p>
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
