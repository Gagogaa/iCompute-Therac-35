from flask import Blueprint, render_template, request, jsonify, url_for, send_file, send_from_directory, stream_with_context
from io import StringIO
from flask_login import login_required
from logon import required_user_type
from database import database_session
from database.models import *
from database.__init__ import *
from flask import *
from pprint import pprint
import csv
import os
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
import re


admin = Blueprint('admin', __name__, template_folder='admin_templates')


@admin.route('/')
@login_required
@required_user_type('Supervisor')
def admin_index():
    return render_template('index.html', link="#", link2="./test", link3="./question", link4="./user", link5="./results")


@admin.route('/test')
@login_required
@required_user_type('Supervisor')
def admin_modify_test():
    return render_template('test_modify.html', link=url_for('admin.admin_create_test'), link2=url_for('admin.admin_edit_test'), link3=url_for('admin.admin_view_test'))


@admin.route('test/test_create', methods=("GET", "POST"))
@login_required
@required_user_type('Supervisor')
def admin_create_test():
    questions = []
    for question in database_session.query(Questions.question).distinct():
        questions.append(question.question)

    if request.method == 'POST':
        is_validated = True
        if ('test_name' not in request.form) or ('year' not in request.form) or ('grade' not in request.form):
            is_validated = False

        if is_validated:
            if request.form['test_name'] not in database_session.query(iComputeTest.test_name).distinct():
                # database_session.query(iComputeTest).delete()
                database_session.commit()
                for i in range(1, len(request.form)-2):
                    temp = iComputeTest(orderId=i,
                                        question=request.form['question' + str(i)],
                                        section=1,
                                        test_name=request.form['test_name'],
                                        year=int(request.form['year']),
                                        student_grade=request.form['grade'])
                    database_session.add(temp)
                database_session.commit()
                return redirect(url_for('admin.admin_view_test'))
            else:
                flash('A test with this test name already exists. Please try again with a different name or edit a pre-existing test.')
                return redirect(url_for('admin.admin_create_test'))
        else:
            flash('Something went wrong with the data you tried to submit.')
            return redirect(url_for('admin.admin_create_test'))

    return render_template('test_create.html', questions=questions)


@admin.route('test/test_edit', methods=("GET", "POST"))
@login_required
@required_user_type('Supervisor')
def admin_edit_test():
    tests = []
    for test in database_session.query(iComputeTest.test_name).distinct():
        tests.append(test.test_name)

    if request.method == 'POST':
        if "question1" in request.form:
            database_session.query(iComputeTest).delete()
            for i in range(1, len(request.form)-2):
                temp = iComputeTest(orderId=i,
                                    question=request.form['question' + str(i)],
                                    section=1,
                                    test_name=request.form['test_name'],
                                    year=int(request.form['year']),
                                    student_grade=request.form['grade'])
                database_session.add(temp)
            database_session.commit()
            return redirect(url_for('admin.admin_view_test'))
        else:
            testquestions = []
            questions = []

            for question in database_session.query(iComputeTest.question).filter(iComputeTest.test_name == request.form['test_name']):
                testquestions.append(question.question)

            for question in database_session.query(Questions.question).distinct():
                questions.append(question.question)

            test = database_session.query(iComputeTest).filter(iComputeTest.test_name == request.form['test_name']).first()
            return render_template('test_edit.html', questions=questions, tests=tests, testquestions=testquestions, name=test.test_name, grade=test.student_grade, year=test.year)

    return render_template('test_edit.html', tests=tests)


@admin.route('test/test_view')
@login_required
@required_user_type('Supervisor')
def admin_view_test():
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
        test = database_session.query(iComputeTest).first()
    return render_template('test_view.html', questions=questions, name=test.test_name, year=test.year, grade=test.student_grade)


@admin.route('/user')
@login_required
@required_user_type('Supervisor')
def admin_edit_users():
    return render_template('userAdd.html', link="./")


@admin.route('/question')
@login_required
@required_user_type('Supervisor')
def admin_edit_questions():
    questions = []
    answers = []
    ansData = {}
    data = {}
    counter = 1
    ansNum = 1

    # Build Dictionary for questions pulled from the db
    for question in database_session.query(Questions.question, Questions.section).distinct():
        data['id'] = counter
        currentQuestion = question.question
        data['question'] = currentQuestion
        section = question.section
        data['section'] = section

        for answer in database_session.query(Questions.answer, Questions.is_correct).filter(Questions.question == question.question):
            ansData = {}
            if answer.is_correct:
                ansData['is_correct'] = True
            else:
                ansData['is_correct'] = False
            ansData['ansCounter'] = counter
            ansData['ans_id'] = ansNum
            ansData['answer'] = answer.answer
            ansData['is_correct'] = answer.is_correct
            answers.append(ansData)
            ansNum += 1

        questions.append(data)
        ansNum = 1
        counter += 1
        data = {}

    return render_template('questionEditUI.html', questions=questions, answers=answers )



@admin.route('./<path:filename>', methods=('GET', 'POST'))
def theDownload(filepath):
	#uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
	return send_from_directory(directory='/', filename=filepath)


@admin.route('/results', methods=('GET', 'POST'))
@login_required
@required_user_type('Supervisor')
def admin_view_results():
    exam_results = []
    exam_data = {}

    # Build Dictionary for test names pulled from the db
    for counter, test_name in enumerate(database_session.query(StudentScore.test_name).distinct().order_by(StudentScore.test_name), start=1):
        exam_data['id'] = counter
        exam_data['test_name'] = test_name.test_name

        # Set up for different cards on the accordian html section
        exam_data['accord1'] = "#collapse" + str(counter)
        exam_data['accord2'] = "collapse" + str(counter)

        # Set up for the rest of the data needed
        exam_data['student_teams'] = []

        exam_results.append(exam_data)
        exam_data = {}

    # Add the rest of the data in a sub Dictionary of each test
    details = {}
    for i in range(0, counter):

        # for each test, grab all team results of that test
        for test_result in database_session.query(StudentScore).filter(StudentScore.test_name == exam_results[i]['test_name']).order_by(StudentScore.total_score.desc()):
            details['team_name'] = test_result.team_name

            for team_info in database_session.query(StudentTeam).filter(StudentTeam.team_name == details['team_name']):
                details['school_name'] = team_info.school_name

            # TODO Why is team year in details because it's not used on the page?
            details['team_year'] = test_result.team_year
            details['sectionAScore'] = test_result.section_one_score
            details['sectionBScore'] = test_result.section_two_score
            details['sectionCScore'] = test_result.section_three_score
            details['totalScore'] = test_result.total_score

            exam_results[i]['student_teams'].append(details)
            details = {}

    def generate():

        #Generate a csv file to be streamed into a csv file on return
        theName = request.form["testForm"]
        data = StringIO()
        w = csv.writer(data)
        w.writerow([theName])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        for i in range(0, counter):
            if (exam_results[i]['test_name'] == theName):
                for stuff in exam_results[i]['student_teams']:
        	        w.writerows(stuff.items())
        	        yield data.getvalue()
                data.seek(0)
                data.truncate(0)

    #A save button was pressed, time to download a file
    if request.method == 'POST':
        headers = Headers()
        headers.set('Content-Disposition', 'attachment', filename= request.form["testForm"] + '.csv')

        return Response(
            stream_with_context(generate()), mimetype='text/csv', headers=headers
            )
    #not POST method return
    return render_template('testResults.html', link="./", exam_results=exam_results)


@admin.route('/addQuestion', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def add_question():
    if 'section' in request.form:
        mySection = request.form['section']
        if mySection == "multiple-choice":
            if 'question' in request.form and 'answer' in request.form:
                myQuestion = request.form['question']
                myAnswer = request.form['answer']
                question = [Questions(question = myQuestion,
                                   answer = myAnswer,
                                   is_correct = True,
                                   section = 1)
                                   ]
                database_session.add_all(question)
                database_session.commit()
                return render_template('questionEditUI.html')
        elif mySection == "short-answer":
                if 'question' in request.form:
                    myQuestion = request.form['question']
                    question = [Questions(question = myQuestion,
                                    answer = "this is a section 2 question",
                                    is_correct = True,
                                    section = 2)]
                    database_session.add_all(question)
                    database_session.commit()
                    return render_template('questionEditUI.html')
        elif mySection == "scratch-answer":
            if 'question' in request.form:
                myQuestion = request.form['question']
                question = [Questions(question = myQuestion,
                                    answer = "this is a section 3 question",
                                    is_correct = True,
                                    section = 3)]
                database_session.add_all(question)
                database_session.commit()
                return render_template('questionEditUI.html')
    return 'success'


@admin.route('/addAnswer', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def add_answer():
    if 'question' in request.form and 'answer' in request.form:
        currentQuestion = request.form['question'];
        answerToAdd = request.form['answer'];
        new_answer = [Questions(question = currentQuestion,
                                answer = answerToAdd,
                                is_correct = False,
                                section = 1)
                                ]
        database_session.add_all(new_answer);
        database_session.commit();
        return 'success'


# TODO We also need to delete questions in tests
@admin.route('/delQuestion', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def delete_question():
    if 'question' in request.form:
        del_query = database_session.query(Questions).filter(Questions.question==request.form['question'])
        del_query.delete()
        database_session.commit()


@admin.route('/delAnswer', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def delete_answer():
    if 'question' in request.form and 'answer' in request.form:
        del_query = database_session.query(Questions.answer).filter(and_(Questions.question==request.form['question'], Questions.answer==request.form['answer']))
        del_query.delete()
        database_session.commit()
    return"success"


# TODO When altering a question we also need to alter the questions in the Test table
@admin.route('/editQuestion', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def edit_question():
    if 'question' in request.form and 'new_question' in request.form:
        rows_to_update = database_session.query(Questions).filter(Questions.question == request.form['question'])
        for row in rows_to_update:
            row.question = request.form['new_question']
        database_session.commit()
    return "success"


@admin.route('/editAnswer', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def edit_answer():
    if 'question' in request.form and 'answer' in request.form and 'new_answer' in request.form:
        rows_to_update = database_session.query(Questions).filter(Questions.question == request.form['question'], Questions.answer == request.form['answer'])
        for row in rows_to_update:
            row.answer = request.form['new_answer']
        database_session.commit()
    return "success answer"


# TODO is this used in the project?
def clear_student_answers():
    del_query = database_session.query(StudentAnswers)
    del_query.delete()
    database_session.commit()
