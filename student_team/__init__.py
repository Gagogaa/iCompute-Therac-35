from flask import Blueprint, render_template, request, escape
from database import database_session
from database.models import *
import datetime
from logon import required_user_type
from flask_login import login_required, current_user
from sqlalchemy import func, over


student_team = Blueprint('student_team', __name__, template_folder='student_templates')


@student_team.route('/', methods=('GET', 'POST'))
@login_required
@required_user_type('Student')
def student_team_index():
    exam_questions = []
    question = {}

    # Build Dictionary for questions pulled from the db
    for counter, exam_question in enumerate(database_session.query(iComputeTest.question).order_by(iComputeTest.orderId), start=1):
        question['id'] = str(counter)
        question['question'] = exam_question.question
        question['answers'] = []
        for answer in database_session.query(Questions.answer).filter(Questions.question == exam_question.question):
            question['answers'].append(escape(answer.answer))
        exam_questions.append(question)
        question = {}

    # Grab the Student submitted answers off the form and submit to database
    if request.method == 'POST':
        for question in exam_questions:
            form_response = request.form[question['id']] if question['id'] in request.form else None

            database_session.add(StudentAnswer(
                team_name=current_user.username,
                team_year=datetime.datetime.now().year,
                section=1,
                # TODO since the question was escaped we may need to unescape it here
                question=question['question'],
                answer=form_response))

            database_session.commit()

    return render_template('multiple_choice.html', exam_questions=exam_questions)


@student_team.route('/sectionb')
def section_b():
    return render_template('short_answer.html')
