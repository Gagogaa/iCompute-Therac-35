from flask import Blueprint, render_template, request
from database.models import *
from flask_login import login_required
from logon import required_user_type
from database import database_session


grader = Blueprint('grader', __name__, template_folder='grader_templates')


# Function for grading all students answers to section 1
def grade_section_one(team):
    # If the student answers are already graded don't try to regrade them
    student_team = StudentScore.query.filter_by(team_name=team).first()

    if student_team:
        return student_team.section_one_score

    correct_answers = 0
    # TODO make sure we are only getting the number of questions from this test
    # right now we have no way to actually do that...
    # so I think that we should add a field to student team for the test that they are suppose to take
    total_questions = database_session.query(iComputeTest).count()

    # TODO look at the grading break down to see what score really needs to be added to the database
    for answer in StudentAnswer.query.filter_by(team_name=team).all():
        correct_answer = Questions.query.filter_by(question=answer.question, is_correct=True).first()
        if correct_answer:
            if correct_answer.answer == answer.answer:
                correct_answers += 1

    student_team = StudentTeam.query.filter_by(team_name=team).order_by(StudentTeam.team_year).first()

    student_score = StudentScore(team_name=student_team.team_name,
                                 team_year=student_team.team_year,
                                 test_name=None,  # right now we have no idea what test the students were taking
                                 total_score=0,  # This should probably be nullable but for now they get a 0 until the grader grades the exam
                                 section_one_score=correct_answers,
                                 section_two_score=0,
                                 section_three_score=0)

    database_session.add(student_score)
    database_session.commit()

    return correct_answers


@grader.route('/', methods=('GET', 'POST'))
@login_required
@required_user_type('Grader')
def grader_index():
    teams = []
    for team in database_session.query(StudentTeam.team_name):
        teams.append(team.team_name)

    # If the grader chose a team, display team info
    if request.method == 'POST':
        if 'team_name' in request.form:
            team = request.form['team_name']
            sec_a_score = grade_section_one(team)
            return render_template('grader_home.html', teams=teams, sec_a_score=sec_a_score)

    return render_template('grader_home.html', teams=teams, sec_a_score=None)
