from flask import Blueprint, render_template, request, escape, redirect, url_for, flash
from database import database_session
from database.models import *
from flask_login import login_required, current_user, logout_user
from logon import required_user_type
import datetime
import random
import base64

student_team = Blueprint('student_team', __name__, template_folder='student_templates')

# Function for grading all students answers to section 1
def grade_section_one(team):
    student_team = StudentTeam.query.filter_by(team_name=team).order_by(StudentTeam.team_year).first()
    total_questions = database_session.query(iComputeTest).filter(iComputeTest.test_name==student_team.test_id).count()
    correct_answers = 0

    for response in StudentAnswer.query.filter_by(team_name=team).all():
        question = Questions.query.filter_by(question=response.question, is_correct=True).first()
        if question:
            if response.answer == question.answer:
                correct_answers += 1

    student_score = StudentScore(team_name=student_team.team_name,
                                 team_year=student_team.team_year,
                                 test_name=student_team.test_id,
                                 total_score=(correct_answers*2),
                                 # WESO Scoring says that each multiple choice question is worth 2 points
                                 section_one_score=(correct_answers*2),
                                 section_two_score=0,
                                 section_three_score=0)

    database_session.add(student_score)
    database_session.commit()


@student_team.route('/', methods=('GET', 'POST'))
@login_required
@required_user_type('Student')
def student_team_index():
    student_team = StudentTeam.query.filter_by(team_name=current_user.username).order_by(StudentTeam.team_year).first()
    exam_questions_s1 = []
    question = {}

    # Build Dictionary for questions pulled from the db
    # TODO grab the correct exam for this team!
    for counter, exam_question_s1 in enumerate(database_session.query(iComputeTest.question).filter(and_(iComputeTest.test_name == student_team.test_id, iComputeTest.section == 1)).order_by(iComputeTest.orderId), start=1):
        question['id'] = str(counter)
        question['question'] = exam_question_s1.question
        question['answers'] = []
        for answer in database_session.query(Questions.answer).filter(Questions.question == exam_question_s1.question):
            question['answers'].append(escape(answer.answer))
            random.shuffle(question['answers'])
        exam_questions_s1.append(question)
        question = {}

    # Grab the Student submitted answers off the form and submit to database
    if request.method == 'POST':
        for question in exam_questions_s1:
            form_response = request.form[question['id']] if question['id'] in request.form else None

            database_session.add(StudentAnswer(
                team_name=current_user.username,
                team_year=student_team.team_year,
                section=1,
                # TODO since the question was escaped we may need to unescape it here
                question=question['question'],
                answer=form_response))

            database_session.commit()
        grade_section_one(current_user.username)

        # For now when the team is done taking the test the application will destroy the password and log the team out.

        return redirect(url_for('student_team.student_s3'))

    return render_template('multiple_choice.html', exam_questions_s1 = exam_questions_s1)


@student_team.route('/sectionb')
@login_required
@required_user_type('Student')
def section_b():
    return render_template('short_answer.html')


@student_team.route('/sectionc', methods=('GET', 'POST'))
@login_required
@required_user_type('Student')
def student_s3():
    student_team = StudentTeam.query.filter_by(team_name=current_user.username).order_by(StudentTeam.team_year).first()
    exam_questions_s3 = []
    images=[]
    question = {}
    fileData = {}
    counter = 0
    fileCounter = 0
    # Build Dictionary for questions pulled from the db
    # TODO grab the correct exam for this team!
    for counter, exam_question_s3 in enumerate(database_session.query(iComputeTest.question).filter(and_(iComputeTest.test_name == student_team.test_id, iComputeTest.section == 3)).order_by(iComputeTest.orderId), start=1):
        question['id'] = counter
        question['question'] = exam_question_s3.question
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

    if request.method == 'POST':
        if ('inputFile' in request.files) and ('hiddenfield_id' in request.form):
            file = request.files['inputFile']
            myQuestion = request.form['hiddenfield_id']
            database_session.add(StudentAnswer(
                    team_name=current_user.username,
                    team_year=student_team.team_year,
                    section=3,
                    # TODO since the question was escaped we may need to unescape it here
                    question=myQuestion,
                    answer=file.filename,
                    scratch_file=file.read()))
        database_session.commit()
        current_user.password = 'Deactivated'
        database_session.commit()
        logout_user()
        flash('Your answers have been submitted. Thank you for participating!', 'info')
        return redirect(url_for('index'))

    return render_template('scratch_submit.html', exam_questions_s3 = exam_questions_s3, images = images)
