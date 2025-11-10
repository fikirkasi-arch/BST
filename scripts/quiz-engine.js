// Quiz Engine - BST Eğitim Portalı
// Ortak quiz motoru - tüm quizlerde kullanılabilir

const QuizEngine = {
    currentQuiz: null,
    currentQuestion: 0,
    score: 0,
    startTime: null,
    timerInterval: null,
    userAnswers: [],

    // Quiz'i başlat
    initQuiz(quizData) {
        this.currentQuiz = quizData;
        this.currentQuestion = 0;
        this.score = 0;
        this.startTime = new Date();
        this.userAnswers = [];

        // Soruları karıştır (isteğe bağlı)
        if (quizData.shuffle) {
            this.shuffleQuestions();
        }

        this.renderQuestion();
        if (quizData.timerEnabled) {
            this.startTimer(quizData.timerDuration);
        }

        // Analytics kaydı
        if (typeof BSTAnalytics !== 'undefined') {
            BSTAnalytics.logActivity('quiz_started', {
                quizName: quizData.title,
                questionCount: quizData.questions.length
            });
        }
    },

    // Soruları karıştır
    shuffleQuestions() {
        const questions = this.currentQuiz.questions;
        for (let i = questions.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [questions[i], questions[j]] = [questions[j], questions[i]];
        }
    },

    // Soruyu göster
    renderQuestion() {
        const question = this.currentQuiz.questions[this.currentQuestion];
        const container = document.getElementById('quiz-container');

        if (!container) {
            console.error('Quiz container bulunamadı!');
            return;
        }

        const progressPercent = ((this.currentQuestion / this.currentQuiz.questions.length) * 100).toFixed(0);

        container.innerHTML = `
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: #667eea;">Soru ${this.currentQuestion + 1} / ${this.currentQuiz.questions.length}</span>
                    <span style="font-weight: bold; color: #764ba2;">Puan: ${this.score}</span>
                </div>
                <div style="background: #e0e0e0; border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); height: 100%; width: ${progressPercent}%; transition: width 0.3s;"></div>
                </div>
            </div>

            <div style="background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <h3 style="color: #333; margin-bottom: 25px; font-size: 1.3em;">${question.question}</h3>

                <div id="options-container" style="display: grid; gap: 15px;">
                    ${question.options.map((option, index) => `
                        <button class="quiz-option" onclick="QuizEngine.selectAnswer(${index})"
                                style="padding: 15px 20px; border: 2px solid #e0e0e0; background: white; border-radius: 12px; cursor: pointer; text-align: left; font-size: 1em; transition: all 0.3s;">
                            ${String.fromCharCode(65 + index)}) ${option}
                        </button>
                    `).join('')}
                </div>
            </div>

            <div style="text-align: center;">
                <button onclick="QuizEngine.skipQuestion()"
                        style="padding: 12px 30px; background: #95a5a6; color: white; border: none; border-radius: 10px; cursor: pointer; font-size: 1em;">
                    ⏭️ Atla
                </button>
            </div>
        `;

        // Hover efektleri için CSS ekle
        this.addOptionStyles();
    },

    // Şık stilleri ekle
    addOptionStyles() {
        const styleId = 'quiz-option-styles';
        if (!document.getElementById(styleId)) {
            const style = document.createElement('style');
            style.id = styleId;
            style.textContent = `
                .quiz-option:hover {
                    border-color: #667eea !important;
                    background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%) !important;
                    transform: translateX(5px);
                }
                .quiz-option.selected {
                    border-color: #667eea !important;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                    color: white !important;
                }
                .quiz-option.correct {
                    border-color: #27ae60 !important;
                    background: #27ae60 !important;
                    color: white !important;
                }
                .quiz-option.wrong {
                    border-color: #e74c3c !important;
                    background: #e74c3c !important;
                    color: white !important;
                }
            `;
            document.head.appendChild(style);
        }
    },

    // Cevap seç
    selectAnswer(optionIndex) {
        const question = this.currentQuiz.questions[this.currentQuestion];
        const options = document.querySelectorAll('.quiz-option');

        // Tüm şıkları devre dışı bırak
        options.forEach(opt => opt.style.pointerEvents = 'none');

        // Seçilen şığı işaretle
        options[optionIndex].classList.add('selected');

        // Doğru cevabı göster
        const correctIndex = question.correct;

        setTimeout(() => {
            if (optionIndex === correctIndex) {
                options[optionIndex].classList.remove('selected');
                options[optionIndex].classList.add('correct');
                this.score += this.currentQuiz.pointsPerQuestion || 10;
                this.userAnswers.push({ question: this.currentQuestion, correct: true });
            } else {
                options[optionIndex].classList.remove('selected');
                options[optionIndex].classList.add('wrong');
                options[correctIndex].classList.add('correct');
                this.userAnswers.push({ question: this.currentQuestion, correct: false });
            }

            // Sonraki soruya geç
            setTimeout(() => {
                this.nextQuestion();
            }, 1500);
        }, 300);
    },

    // Soruyu atla
    skipQuestion() {
        this.userAnswers.push({ question: this.currentQuestion, correct: false, skipped: true });
        this.nextQuestion();
    },

    // Sonraki soru
    nextQuestion() {
        this.currentQuestion++;

        if (this.currentQuestion < this.currentQuiz.questions.length) {
            this.renderQuestion();
        } else {
            this.finishQuiz();
        }
    },

    // Quiz'i bitir
    finishQuiz() {
        const endTime = new Date();
        const duration = Math.round((endTime - this.startTime) / 1000); // saniye
        const totalQuestions = this.currentQuiz.questions.length;
        const correctAnswers = this.userAnswers.filter(a => a.correct).length;
        const percentage = Math.round((correctAnswers / totalQuestions) * 100);

        // Sonuçları kaydet
        if (typeof BSTStorage !== 'undefined') {
            BSTStorage.saveQuizResult(this.currentQuiz.title, correctAnswers, totalQuestions);
        }

        // Rozet kontrolü
        if (typeof BadgeSystem !== 'undefined') {
            // Mükemmel skor rozeti
            if (percentage === 100) {
                BadgeSystem.earnBadge('perfect-score');
            }
            // Hız rozeti (2 dakikadan kısa)
            if (duration <= 120) {
                BadgeSystem.earnBadge('speed-master');
            }
        }

        // Analytics kaydı
        if (typeof BSTAnalytics !== 'undefined') {
            BSTAnalytics.logActivity('quiz_completed', {
                quizName: this.currentQuiz.title,
                score: correctAnswers,
                total: totalQuestions,
                percentage: percentage,
                duration: duration
            });
        }

        // Sonuç ekranını göster
        this.showResults(correctAnswers, totalQuestions, percentage, duration);
    },

    // Sonuçları göster
    showResults(correct, total, percentage, duration) {
        const container = document.getElementById('quiz-container');

        let emoji = '🎉';
        let message = 'Harika!';
        let color = '#27ae60';

        if (percentage === 100) {
            emoji = '🏆';
            message = 'Mükemmel!';
            color = '#f39c12';
        } else if (percentage >= 80) {
            emoji = '⭐';
            message = 'Çok İyi!';
            color = '#3498db';
        } else if (percentage >= 60) {
            emoji = '👍';
            message = 'İyi!';
            color = '#9b59b6';
        } else {
            emoji = '📚';
            message = 'Çalışmaya devam!';
            color = '#e74c3c';
        }

        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        const timeStr = minutes > 0 ? `${minutes} dakika ${seconds} saniye` : `${seconds} saniye`;

        container.innerHTML = `
            <div style="text-align: center; background: white; padding: 50px 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                <div style="font-size: 5em; margin-bottom: 20px;">${emoji}</div>
                <h2 style="color: ${color}; font-size: 2.5em; margin-bottom: 15px;">${message}</h2>
                <p style="font-size: 1.5em; color: #666; margin-bottom: 30px;">Quiz Tamamlandı!</p>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin-bottom: 30px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 15px;">
                        <div style="font-size: 2em; font-weight: bold;">${correct}/${total}</div>
                        <div style="font-size: 0.9em; opacity: 0.9;">Doğru Cevap</div>
                    </div>
                    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 15px;">
                        <div style="font-size: 2em; font-weight: bold;">%${percentage}</div>
                        <div style="font-size: 0.9em; opacity: 0.9;">Başarı Oranı</div>
                    </div>
                    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 15px;">
                        <div style="font-size: 2em; font-weight: bold;">${timeStr}</div>
                        <div style="font-size: 0.9em; opacity: 0.9;">Süre</div>
                    </div>
                </div>

                <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
                    <button onclick="location.reload()"
                            style="padding: 15px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 12px; cursor: pointer; font-size: 1em; font-weight: bold;">
                        🔄 Tekrar Dene
                    </button>
                    <button onclick="window.location.href='index.html'"
                            style="padding: 15px 30px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; border: none; border-radius: 12px; cursor: pointer; font-size: 1em; font-weight: bold;">
                        🏠 Ana Sayfa
                    </button>
                    <button onclick="window.location.href='student-dashboard.html'"
                            style="padding: 15px 30px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; border: none; border-radius: 12px; cursor: pointer; font-size: 1em; font-weight: bold;">
                        📊 Dashboard
                    </button>
                </div>
            </div>
        `;

        // Timer'ı durdur
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }
    },

    // Timer başlat
    startTimer(duration) {
        let timeLeft = duration;
        const timerDisplay = document.createElement('div');
        timerDisplay.id = 'quiz-timer';
        timerDisplay.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 12px;
            font-size: 1.2em;
            font-weight: bold;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            z-index: 1000;
        `;
        document.body.appendChild(timerDisplay);

        this.timerInterval = setInterval(() => {
            timeLeft--;
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerDisplay.innerHTML = `⏱️ ${minutes}:${seconds.toString().padStart(2, '0')}`;

            if (timeLeft <= 10) {
                timerDisplay.style.background = 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)';
                timerDisplay.style.animation = 'pulse 1s infinite';
            }

            if (timeLeft <= 0) {
                clearInterval(this.timerInterval);
                this.finishQuiz();
            }
        }, 1000);

        // Pulse animasyonu ekle
        if (!document.getElementById('timer-pulse-style')) {
            const style = document.createElement('style');
            style.id = 'timer-pulse-style';
            style.textContent = `
                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                }
            `;
            document.head.appendChild(style);
        }
    },

    // Quiz verilerini doğrula
    validateQuizData(quizData) {
        if (!quizData || !quizData.questions || !Array.isArray(quizData.questions)) {
            console.error('Geçersiz quiz verisi!');
            return false;
        }

        for (let i = 0; i < quizData.questions.length; i++) {
            const q = quizData.questions[i];
            if (!q.question || !q.options || !Array.isArray(q.options) || q.correct === undefined) {
                console.error(`Soru ${i + 1} geçersiz!`);
                return false;
            }
        }

        return true;
    }
};
