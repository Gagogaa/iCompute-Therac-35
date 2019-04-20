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

    return render_template('questionEditUI.html', questions=questions, answers=answers, files=files, home_link='./' )


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
    response.headers['Content-Disposition'] = f'attachment; filename=' + test + '.csv'

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

                else:
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
        if not QuestionsImages.query.filter_by(file_name=file.filename).first():
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

# TODO When altering a question we also need to alter the questions in the Test table
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
    return "success"


# TODO is this used in the project?
def clear_student_answers():
    del_query = database_session.query(StudentAnswers)
    del_query.delete()
    database_session.commit()
