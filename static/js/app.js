let currentQuiz = null;
let currentQuestionIndex = 0;
let score = 0;
function showScreen(screenId) {
    document.getElementById('start-screen').style.display = 'none';
    document.getElementById('loading-screen').style.display = 'none';
    document.getElementById('quiz-screen').style.display = 'none';
    document.getElementById('end-screen').style.display = 'none';
    document.getElementById(screenId).style.display = 'flex';
}
async function generateQuiz() {
    const sport = document.getElementById('sport-select').value;
    const difficulty = document.getElementById('difficulty-select').value;
    const numQuestions = parseInt(document.getElementById('num-questions').value);
    showScreen('loading-screen');
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sport, difficulty, num_questions: numQuestions })
        });
        const data = await response.json();
        if (data.success && data.quiz && data.quiz.questions.length > 0) {
            currentQuiz = data.quiz;
            currentQuestionIndex = 0;
            score = 0;
            renderQuestion();
            showScreen('quiz-screen');
        } else {
            alert('Failed to generate quiz. Please try again.');
            showScreen('start-screen');
        }
    } catch (error) {
        alert('An error occurred. Make sure the backend is running.');
        showScreen('start-screen');
    }
}
function renderQuestion() {
    const question = currentQuiz.questions[currentQuestionIndex];
    document.getElementById('question-indicator').textContent = `Question ${currentQuestionIndex + 1}/${currentQuiz.questions.length}`;
    document.getElementById('quiz-topic-subtitle').textContent = `Contextualize your topic with a subtitle`;
    document.getElementById('question-text').textContent = question.question;
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';
    question.options.forEach(option => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = option;
        btn.onclick = () => selectAnswer(btn, option, question.correct_answer, question.explanation);
        optionsContainer.appendChild(btn);
    });
    document.getElementById('feedback-text').textContent = '';
    document.getElementById('feedback-text').className = 'feedback-text';
    document.getElementById('next-btn').style.display = 'none';
}
function selectAnswer(btn, selected, correct, explanation) {
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach(b => b.disabled = true);
    const feedback = document.getElementById('feedback-text');
    if (selected === correct) {
        btn.classList.add('correct');
        feedback.textContent = 'Correct!';
        feedback.className = 'feedback-text correct';
        score++;
    } else {
        btn.classList.add('wrong');
        feedback.textContent = `Oops, that's wrong.`;
        feedback.className = 'feedback-text wrong';
        buttons.forEach(b => {
            if (b.textContent === correct) b.classList.add('correct');
        });
    }
    document.getElementById('next-btn').style.display = 'block';
    if (currentQuestionIndex === currentQuiz.questions.length - 1) {
        document.getElementById('next-btn').textContent = 'Finish';
    } else {
        document.getElementById('next-btn').textContent = 'Next';
    }
}
function nextQuestion() {
    if (currentQuestionIndex < currentQuiz.questions.length - 1) {
        currentQuestionIndex++;
        renderQuestion();
    } else {
        finishQuiz();
    }
}
function finishQuiz() {
    showScreen('end-screen');
    document.getElementById('final-score-text').textContent = `Here you can include a text to congratulate and wish your audience luck at the end of the quiz. You scored ${score} out of ${currentQuiz.questions.length}!`;
}
function resetQuiz() {
    currentQuiz = null;
    currentQuestionIndex = 0;
    score = 0;
    showScreen('start-screen');
}
