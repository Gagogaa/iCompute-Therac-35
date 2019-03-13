from flask import Blueprint, render_template, request
from database.models import *
from flask_sqlalchemy import SQLAlchemy

student_team = Blueprint('student_team', __name__, template_folder='templates')

@student_team.route('/', methods=('GET', 'POST'))
def student_team_index():
    # Build Dictionary for questions pulled from the db
    questions = [
        {
            "id": 1,
            "question": "What is the name of the unit that helps store data in a computer?",
            "answer1": "CPU",
            "answer2": "Input",
            "answer3": "Memory",
            "answer4": "Output"
        },
        {
            "id": 2,
            "question": "This provides a step-by-step procedure for performing a task.",
            "answer1": "Keyboard",
            "answer2": "Algorithm",
            "answer3": "Internet",
            "answer4": "Windows"
        },
        {
            "id": 3,
            "question": "Which one of the following is not a programming language?",
            "answer1": "Java",
            "answer2": "HTML",
            "answer3": "C++",
            "answer4": "Binary"
        }
    ]

    #grab the Student submitted answers off the form and submit to database
    if request.method == 'POST':
        year = '2019'
        for i in range(1, len(questions)):
            questionName = "question" + str(i)
            valueName =  "optradio" + str(i)
            temp = StudentAnswer(request.form['team_name'], '2019', '1', request.form[question], request.form[valueName])
            db.session.add(temp)
            db.session.commit()

    return render_template('multiple_choice.html', questions=questions)
