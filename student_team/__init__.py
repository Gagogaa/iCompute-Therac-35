from flask import Blueprint, render_template, request
from database.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

student_team = Blueprint('student_team', __name__, template_folder='templates')

engine = create_engine('sqlite:///iCompute.db', convert_unicode=True)
database_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=engine))
Base = declarative_base()
Base.query = database_session.query_property()

@student_team.route('/', methods=('GET', 'POST'))
def student_team_index():
    # questions = []
    #
    # for question in database_session.query(SectionOneQnA):
    #     questions.append(question)

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

    if request.method == 'POST':
        return request.form['optradio1']

    return render_template('multiple_choice.html', questions=questions)

@student_team.route('/section-b')
def section_b():
    return render_template('short_answer.html')
