from flask import Blueprint, render_template, request, escape, redirect, url_for, flash
from database import database_session
from database.models import *
from flask_login import login_required, current_user, logout_user
from logon import required_user_type
import datetime
import random


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
                                 total_score=0,  # This should probably be nullable but for now they get a 0 until the grader grades the exam
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
    for counter, exam_question_s1 in enumerate(database_session.query(iComputeTest.question).filter(iComputeTest.test_name == student_team.test_id).order_by(iComputeTest.orderId), start=1):
        question['id'] = str(counter)
        question['question'] = exam_question_s1.question
        question['answers'] = []
        for answer in database_session.query(Questions.answer).filter(Questions.question == exam_question_s1.question):
            question['answers'].append(escape(answer.answer))
            random.shuffle(question['answers'])
        for section in database_session.query(Questions.section).filter(Questions.question == exam_question_s1.question):
            question['section'] = section.section
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
        current_user.password = 'Deactivated'
        database_session.commit()
        logout_user()
        flash('Your answers have been submitted. Thank you for participating!', 'info')
        return redirect(url_for('index'))

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
    question = {}

    # Build Dictionary for questions pulled from the db
    # TODO grab the correct exam for this team!
    for counter, exam_question_s3 in enumerate(database_session.query(iComputeTest.question).filter(iComputeTest.test_name == student_team.test_id).order_by(iComputeTest.orderId), start=1):
        question['id'] = str(counter)
        question['question'] = exam_question_s3.question
        question['answers'] = []
        for answer in database_session.query(Questions.answer).filter(Questions.question == exam_question_s3.question):
            question['answers'].append(escape(answer.answer))
            random.shuffle(question['answers'])
        for section in database_session.query(Questions.section).filter(Questions.question == exam_question_s3.question):
            question['section'] = section.section
        exam_questions_s3.append(question)
        question = {}

        #sectionCQuestion = database_session.query(QuestionsImages.question)
    #    sectionCImage = database_session.query(QuestionsImages.file_name)

    #student_team = StudentTeam.query.filter_by(team_name=current_user.username).order_by(StudentTeam.team_year).first()
    #    if 'team_name' in request.form and 'team_year' in request.form and 'section' in request.form and 'question' in request.form and 'answer' in request.form:

# filename to answer
        #filename = $('scratch_file').val().replace(/.*(\/|\\)/, '');
        #filename = request.form['answer']



        return render_template('scratch_submit.html')
