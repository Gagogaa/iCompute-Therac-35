from flask import Blueprint, render_template, request, jsonify, url_for, send_file, send_from_directory, stream_with_context, make_response
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
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy import desc
import base64

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
    return render_template('test_modify.html', link=url_for('admin.admin_index'), link1=url_for('admin.admin_test'), link2=url_for('admin.admin_view_test'))


@admin.route('test/test_edit', methods=("GET", "POST"))
@login_required
@required_user_type('Supervisor')
def admin_test():
    questions = []
    question = {}
    testNames = []
    for counter, exam_question in enumerate(database_session.query(Questions.question, Questions.section).distinct(), start=1):
        question['id'] = str(counter)
        question['question'] = exam_question.question
        question['answers'] = []
        question['side'] = "left"
        question['section'] = exam_question.section
        for answer in database_session.query(Questions.answer, Questions.is_correct).filter(Questions.question == exam_question.question):
            question['answers'].append({"answer": escape(answer.answer), "is_correct": escape(answer.is_correct)})
        questions.append(question)
        question = {}

    for test in database_session.query(iComputeTest.test_name).distinct():
        testNames.append(test.test_name)

    if request.method == "POST":
        test_name = request.form['test']
        for exam_question in database_session.query(iComputeTest.question).filter(iComputeTest.test_name == test_name):
            for question in questions:
                if question['question'] == exam_question.question:
                    question['side'] = "right"

        return render_template('test.html', questions=questions, tests=testNames, link=url_for('admin.admin_index'), active_select=test_name)

    return render_template('test.html', questions=questions, tests=testNames, link=url_for('admin.admin_index'), active_select='New Test')


@admin.route('test/add_question', methods=["POST"])
@login_required
@required_user_type('Supervisor')
def test_add_question():
    if ('testId' in request.form) and ('question' in request.form):
        existing_question = iComputeTest.query.filter_by(test_name=request.form['testId'], question=request.form['question']).first()
        question_section = Questions.query.filter_by(question=request.form['question']).first()

        if (not existing_question) and question_section:
            test = iComputeTest.query.filter_by(test_name=request.form['testId']).order_by(desc(iComputeTest.orderId)).first()


            test_question = iComputeTest(orderId=(test.orderId + 1 if test else 1),
                                         question=request.form['question'],
                                         section=question_section.section,
                                         test_name=request.form['testId'],
                                         year=(test.year if test else datetime.now().year),
                                         student_grade='5'  # TODO Figure out what to do with this
                                         )

            database_session.add(test_question)
            database_session.commit()

            return "success"

    return "error"


@admin.route('test/remove_question', methods=["POST"])
@login_required
@required_user_type('Supervisor')
def test_remove_question():
    if ('testId' in request.form) and ('question' in request.form):
        question = database_session.query(iComputeTest).filter_by(test_name=request.form['testId'], question=request.form['question']).first()
        if question:
            database_session.delete(question)
            database_session.commit()
            return "success"

    return "error"


@admin.route('test/test_view', methods=("GET", "POST"))
@login_required
@required_user_type('Supervisor')
def admin_view_test():
    test_names = []
    for test in database_session.query(iComputeTest.test_name).distinct():
        test_names.append(test.test_name)

    if request.method == "POST":
        exam_questions_s1 = []
        question = {}

        for counter, exam_question_s1 in enumerate(database_session.query(iComputeTest.question).filter(iComputeTest.test_name == request.form['test']).order_by(iComputeTest.orderId), start=1):
            question['id'] = str(counter)
            question['question'] = exam_question_s1.question
            question['answers'] = []
            for answer in database_session.query(Questions.answer).filter(Questions.question == exam_question_s1.question):
                question['answers'].append(escape(answer.answer))
            for section in database_session.query(Questions.section).filter(Questions.question == exam_question_s1.question):
                question['section'] = section.section
            exam_questions_s1.append(question)
            question = {}

        test = database_session.query(iComputeTest).filter(iComputeTest.test_name == request.form['test']).first()

        exam_questions_s3 = []
        images=[]
        question = {}
        fileData = {}
        counter = 0
        fileCounter = 0
        # Build Dictionary for questions pulled from the db
        # TODO grab the correct exam for this team!
        for counter, exam_question_s3 in enumerate(database_session.query(iComputeTest.question).filter(iComputeTest.test_name == request.form['test']).order_by(iComputeTest.orderId), start=1):
            question['id'] = counter
            question['question'] = exam_question_s3.question
            for section in database_session.query(Questions.section).filter(Questions.question == exam_question_s3.question):
                question['section'] = section.section
            for data in database_session.query(QuestionsImages.data).filter(QuestionsImages.question == exam_question_s3.question):
                fileData = {}
                fileData['file_id'] = fileCounter
                fileData['file_counter'] = counter
                image = base64.encodestring(data.data)
                image2 = image.decode("UTF8")
                fileData['image'] = image2
                images.append(fileData)
                fileCounter +=1

            exam_questions_s3.append(question)
            counter += 1
            question = {}
        return render_template('test_view.html', name=test.test_name, year=test.year, grade=test.student_grade, is_chosen=True, tests=test_names, exam_questions_s1 = exam_questions_s1, exam_questions_s3 = exam_questions_s3, images = images)

    return render_template('test_view.html', is_chosen=False, tests=test_names)


@admin.route('/user')
@login_required
@required_user_type('Supervisor')
def admin_edit_users():
    supervisorArray = []
    data = {}
    counterSupervisor = 1

    # Build Dictionary users
    for supervisor in database_session.query(Users).filter(Users.user_type == 'Supervisor'):
        data['id'] = counterSupervisor
        currentSupervisor = supervisor.username
        data['supervisor'] = currentSupervisor
        supervisorArray.append(data)

        counterSupervisor += 1
        data = {}


    graderArray = []
    data = {}
    counterGrader = 1

        # Build Dictionary users
    for grader in database_session.query(Users).filter(Users.user_type == 'Grader'):
        data['id'] = counterGrader
        currentGrader = grader.username
        data['grader'] = currentGrader
        graderArray.append(data)

        counterGrader += 1
        data = {}



    studentTeamArray = []
    data = {}
    counterStudent = 1

        # Build Dictionary users
    for studentTeam in database_session.query(Users).filter(Users.user_type == 'Student'):
        data['id'] = counterStudent
        currentStudentTeam = studentTeam.username
        data['studentTeam'] = currentStudentTeam
        print(currentStudentTeam)
        studentTeamArray.append(data)

        counterStudent += 1
        data = {}

    tests = []
    data = {}
    counterTests = 1
    for test in database_session.query(iComputeTest.test_name).distinct():
        data['id'] = counterTests
        data['test_name'] = test.test_name
        tests.append(data)

        counterTests +=1
        data={}

    return render_template('userAdd.html', supervisorArray=supervisorArray, graderArray=graderArray, studentTeamArray=studentTeamArray, tests=tests)


@admin.route('/addUser',  methods=['POST'])
@login_required
@required_user_type('Supervisor')
def admin_add_users():
    if 'user_type' in request.form:
        user_type = request.form['user_type']
        if user_type == "Student":
            if 'username' in request.form and 'password' in request.form and 'test_name' in request.form  and 'team_year' in request.form and 'school_name' in request.form:
                username = request.form['username']
                password = request.form['password']
                test_name = request.form['test_name']
                team_year = request.form['team_year']
                school_name = request.form['school_name']
                userData = [Users(username = username,
                                   password = generate_password_hash(password),
                                   user_type = user_type),

                            StudentTeam(team_name = username,
                                        team_year = team_year,
                                        school_name = school_name,
                                        test_id = test_name)
                                   ]
                database_session.add_all(userData)
                database_session.commit()
        elif user_type == "Grader":
            if 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                userData = [Users(username = username,
                                   password = generate_password_hash(password),
                                   user_type = user_type)
                                   ]
                database_session.add_all(userData)
                database_session.commit()
        else:
            if 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                userData = [Users(username = username,
                                   password = generate_password_hash(password),
                                   user_type = user_type)
                                   ]

                database_session.add_all(userData)
                database_session.commit()
    return 'success'


@admin.route('/question')
@login_required
@required_user_type('Supervisor')
def admin_edit_questions():
    questions = []
    answers = []
    files = []
    ansData = {}
    data = {}
    counter = 1
    ansNum = 1
    fileCounter = 1

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

        for file in database_session.query(QuestionsImages.file_name).filter(QuestionsImages.question == question.question):
            fileData = {}
            fileData['file_id'] = fileCounter
            fileData['file_counter'] = counter
            file_name = file.file_name
            fileData['file'] = file_name
            files.append(fileData)
            fileCounter +=1
        questions.append(data)
        ansNum = 1
        counter += 1
        data = {}

    response = make_response(render_template('questionEditUI.html', questions=questions, answers=answers, files=files, home_link='./' ))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies.

    return response


@admin.route('/individual-results/<test>')
@login_required
@required_user_type('Supervisor')
def individual_results_csv(test):
    all_scores = []

    student_teams = StudentTeam.query.filter_by(test_id=test).all()

    for team in student_teams:
        all_scores = all_scores + list(StudentAnswer.query.filter_by(team_name=team.team_name, team_year=team.team_year).all())

    individual_csv = render_template('individual_scores.csv', student_scores=all_scores)
    response = make_response(individual_csv)

    response.headers['Cache-Control'] = 'must-revalidate'
    response.headers['Pragma'] = 'must-revalidate'
    response.headers['Content-type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename="{test}.csv"'

    return response


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
    for exam_result in exam_results:

        # for each test, grab all team results of that test
        for test_result in database_session.query(StudentScore).filter(StudentScore.test_name == exam_result['test_name']).order_by(StudentScore.total_score.desc()):
            details['team_name'] = test_result.team_name

            for team_info in database_session.query(StudentTeam).filter(StudentTeam.team_name == details['team_name']):
                details['school_name'] = team_info.school_name

            details['team_year'] = test_result.team_year
            details['sectionAScore'] = test_result.section_one_score
            details['sectionBScore'] = test_result.section_two_score
            details['sectionCScore'] = test_result.section_three_score
            details['totalScore'] = test_result.total_score

            exam_result['student_teams'].append(details)
            details = {}

    if request.method == 'POST':
        theName = request.form["testForm"]
        full_info = []

        for exam_result in exam_results:
            if(exam_result['test_name'] == theName):
                full_info = full_info + list(exam_result['student_teams'])

        full_csv = render_template('full_scores.csv', all_scores=full_info)
        response = make_response(full_csv)
        response.headers['Cache-Control'] = 'must-revalidate'
        response.headers['Pragma'] = 'must-revalidate'
        response.headers['Content-type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=' + theName +'.csv'

        return response

    return render_template('testResults.html', link="./", exam_results=exam_results, home_link='./')


@admin.route('/addQuestion', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def add_question():
    if request.method == 'POST':
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
                return redirect(url_for('admin.admin_edit_questions'))
            elif mySection == "short-answer":
                if 'question' in request.form and 'file' in request.form:
                    myQuestion = request.form['question']
                    question = [Questions(question = myQuestion,
                                    answer = "this is a section 2 question",
                                    is_correct = True,
                                    section = 2)]
                    database_session.add_all(question)
                    database_session.commit()
                return redirect(url_for('admin.admin_edit_questions'))


            elif mySection == "scratch-answer":
                if 'question' in request.form:
                    myQuestion = request.form['question']
                    question = [Questions(question = myQuestion,
                                    answer = "this is a section 3 question",
                                    is_correct = True,
                                    section = 3),
                            ]
                    database_session.add_all(question)
                    database_session.commit()
                return redirect(url_for('admin.admin_edit_questions'))

        return 'success'

@admin.route('/addImage', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def add_image():
    if ('inputFile' in request.files) and ('hiddenfield_id' in request.form):
        file = request.files['inputFile']
        myQuestion = request.form['hiddenfield_id']
        if not QuestionsImages.query.filter_by(file_name=file.filename,question=myQuestion).first():
            questionImage = [QuestionsImages(question = myQuestion,
                                             file_name = file.filename,
                                             data = file.read()),
                                             ]
            database_session.add_all(questionImage)
            database_session.commit()

    return redirect(url_for('admin.admin_edit_questions'))


@admin.route('/addAnswer', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def add_answer():
    if 'question' in request.form and 'answer' in request.form:
        question_text = request.form['question'];
        answer_text = request.form['answer'];

        # Check to see if the answer is already associated with this question
        if Questions.query.filter_by(question=question_text, answer=answer_text).count() > 0:
            return "error"

        new_answer = Questions(question=question_text,
                                answer=answer_text,
                                is_correct=False,
                                section=1)
        database_session.add(new_answer);
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

        del_query = database_session.query(iComputeTest).filter(iComputeTest.question==request.form['question'])
        del_query.delete()
        database_session.commit()

        del_query = database_session.query(QuestionsImages).filter(QuestionsImages.question==request.form['question'])
        del_query.delete()
        database_session.commit()
    return "success"


@admin.route('/delAnswer', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def delete_answer():
    if 'question' in request.form and 'answer' in request.form:
        del_query = database_session.query(Questions.answer).filter(and_(Questions.question==request.form['question'], Questions.answer==request.form['answer']))
        del_query.delete()
        database_session.commit()
    return"success"

@admin.route('/delImage', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def delete_image():
    if 'question' in request.form and 'file_name' in request.form:
        del_query = database_session.query(QuestionsImages.file_name).filter(and_(QuestionsImages.question==request.form['question'], QuestionsImages.file_name==request.form['file_name']))
        del_query.delete()
        database_session.commit()
    return"success"


@admin.route('/editQuestion', methods=['POST'])
@login_required
@required_user_type('Supervisor')
def edit_question():
    if 'question' in request.form and 'new_question' in request.form:
        rows_to_update = database_session.query(Questions).filter(Questions.question == request.form['question'])
        test_rows_to_update = database_session.query(iComputeTest).filter(iComputeTest.question == request.form['question'])
        for row in rows_to_update:
            row.question = request.form['new_question']

        for row in test_rows_to_update:
            row.question = request.form['new_question']
        database_session.commit()

        rows_to_update = database_session.query(QuestionsImages).filter(QuestionsImages.question == request.form['question'])
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
    return redirect(url_for('admin.admin_edit_questions'))


# TODO is this used in the project?
def clear_student_answers():
    del_query = database_session.query(StudentAnswers)
    del_query.delete()
    database_session.commit()
