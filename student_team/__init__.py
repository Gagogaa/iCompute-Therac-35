from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy

student_team = Blueprint('student_team', __name__, template_folder='templates')

@student_team.route('/')
def student_team_index():
    # fake dictionary for question generation to match info retrieved from DB
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

    # fake dictionary for submition push into database
    from modals import StudentAnswer
    temp = StudentAnswer('__name__', '2019', '1', 'id', 'answer')
    db.session.add(temp)
    db.session.commit()

    return render_template('multiple_choice.html', questions=questions)
