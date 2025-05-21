from flask import Flask, render_template, request, redirect, url_for, session
from quiz_engine import QuizEngine

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
quiz = QuizEngine('generated_30_questions.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        return redirect(url_for('quiz_question', qid=0))
    return render_template('welcome.html')

@app.route('/quiz/<int:qid>', methods=['GET', 'POST'])
def quiz_question(qid):
    if request.method == 'POST':
        selected_option = request.form.get('option')
        if quiz.check_answer(qid, selected_option):
            quiz.score += 1

        if qid + 1 < quiz.total_questions:
            return redirect(url_for('quiz_question', qid=qid + 1))
        else:
            return redirect(url_for('result'))

    question_data = quiz.get_question(qid)
    return render_template('quiz.html', qid=qid, question=question_data)

@app.route('/result')
def result():
    username = session.get('username', 'Guest')
    return render_template('result.html', name=username, score=quiz.score, total=quiz.total_questions)

if __name__ == '__main__':
    print("✅ Flask app is starting...")
    app.run(debug=True)