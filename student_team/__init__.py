from flask import Blueprint, render_template, request
from database.models import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine('sqlite:///iCompute.db', convert_unicode=True)
Session = sessionmaker(bind=engine)
session = Session()

student_team = Blueprint('student_team', __name__, template_folder='student_templates')

@student_team.route('/', methods=('GET', 'POST'))
def student_team_index():

    questions = []
    data = {}
    counter = 1
    ansNum = 1

    # Build Dictionary for questions pulled from the db
    for question in session.query(Questions.question).distinct():
        data['id'] = counter
        data['question'] = question.question
        for answer in session.query(Questions.answer).filter(Questions.question == question.question):
            ans = 'answer' + str(ansNum)
            data[ans] = answer.answer
            ansNum += 1
        questions.append(data)
        ansNum = 1
        counter += 1
        data = {}


    #grab the Student submitted answers off the form and submit to database
    if request.method == 'POST':
        year = '2019'
        for i in range(1, (len(questions)+1)):
            questionName = "question" + str(i)
            valueName =  "optradio" + str(i)
            if request.form[valueName] == 'not_answered':
                temp = StudentAnswer(team_name=request.form['team_name'], team_year=datetime.datetime.now().year, section=1, question=request.form[questionName], answer=None)
            else:
                temp = StudentAnswer(team_name=request.form['team_name'], team_year=datetime.datetime.now().year, section=1, question=request.form[questionName], answer=request.form[valueName])
            database_session.add(temp)
            database_session.commit()

    return render_template('multiple_choice.html', questions=questions)

@student_team.route('/section-b')
def section_b():
    return render_template('short_answer.html')
