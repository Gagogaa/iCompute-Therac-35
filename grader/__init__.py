from flask import Blueprint, render_template, request
from database.models import *
from flask_login import login_required
from logon import required_user_type
from database import database_session
from sqlalchemy import and_


grader = Blueprint('grader', __name__, template_folder='grader_templates')


# Function for grading all students answers to section 1
def grade_section_one(team):
    # to display the results of the first part of the test
    results = {}
    correct_answers = 0
    # TODO I don't think this is doing what we want it to because this will count all of the questions from all of the tests
    # we just want the count from the current test
    total_questions = database_session.query(iComputeTest).count()
    # grab all student answers that were for the chosen team
    # TODO we also need to grab team year (this is just in case schools have teams with the same name consecutive years)
    for answer in database_session.query(StudentAnswer).filter(StudentAnswer.team_name == team):
        results[answer.question] = answer.answer
        # grab the correct answer for the given question
        correct_answer = database_session.query(Questions).filter(and_(Questions.question == answer.question, Questions.is_correct == True))
        # if they got it right, increment the number of correct answers
        if correct_answer.answer == answer.answer:
            correct_answers += 1

    # return both the test score and the results of the test
    return (correct_answers/total_questions), results


@grader.route('/', methods=('GET', 'POST'))
@login_required
@required_user_type('Grader')
def grader_index():
    teams = []
    for team in database_session.query(StudentTeam.team_name):
        teams.append(team.team_name)

    # If the grader chose a team, display team info
    if request.method == 'POST':
        team = request.form['team_name']
        sec_a_score, results = grade_section_one(team)
        return render_template('grader_home.html', teams=teams, sec_a_score=sec_a_score, results=results)

    return render_template('grader_home.html', teams=teams, sec_a_score=None, results=None)
