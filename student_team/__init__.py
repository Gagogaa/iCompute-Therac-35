from flask import Blueprint, render_template, request
from database import database_session
from database.models import *
import datetime
from logon import required_user_type
from flask_login import login_required


student_team = Blueprint('student_team', __name__, template_folder='student_templates')


@student_team.route('/', methods=('GET', 'POST'))
@login_required
@required_user_type('Student')
def student_team_index():

    questions = []
    data = {}
    counter = 1
    ansNum = 1

    # Build Dictionary for questions pulled from the db
    for question in database_session.query(iComputeTest.question):
        data['id'] = counter
        data['question'] = question.question
        for answer in database_session.query(Questions.answer).filter(Questions.question == question.question):
            ans = 'answer' + str(ansNum)
            data[ans] = answer.answer
            ansNum += 1
        questions.append(data)
        ansNum = 1
        counter += 1
        data = {}


    #grab the Student submitted answers off the form and submit to database
    if request.method == 'POST':
        #checking to make sure an empty form isn't being submitted so it doesn't break the app
        is_validated = True
        if 'team_name' not in request.form:
            is_validated = False

        for i in range(1, (len(questions)+1)):
            questionName = "question" + str(i)
            valueName = "optradio" + str(i)
            if questionName not in request.form or valueName not in request.form:
                is_validated = False

        if is_validated == True:
            year = '2019'
            for i in range(1, (len(questions)+1)):
                questionName = "question" + str(i)
                valueName =  "optradio" + str(i)
                if request.form[valueName] == 'not_answered':
                    temp = StudentAnswer(team_name=request.form['team_name'],
                                         team_year=datetime.datetime.now().year,
                                         section=1,
                                         question=request.form[questionName],
                                         answer=None)
                else:
                    temp = StudentAnswer(team_name=request.form['team_name'],
                                         team_year=datetime.datetime.now().year,
                                         section=1,
                                         question=request.form[questionName],
                                         answer=request.form[valueName])
                database_session.add(temp)
                database_session.commit()
        else:
            return render_template('multiple_choice.html', questions=questions)

    return render_template('multiple_choice.html', questions=questions)

@student_team.route('/sectionb')
def section_b():
    return render_template('short_answer.html')
