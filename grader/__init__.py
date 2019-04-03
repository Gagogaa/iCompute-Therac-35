from flask import Blueprint, render_template, request
from database import database_session
from database.models import *
from flask_login import login_required
from logon import required_user_type


grader = Blueprint('grader', __name__, template_folder='grader_templates')


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
            student_scores = StudentScore.query.filter_by(team_name=team).order_by(StudentScore.team_year).first()
            sec_a_score = student_scores.section_one_score
            return render_template('grader_home.html', teams=teams, sec_a_score=sec_a_score)

    return render_template('grader_home.html', teams=teams, sec_a_score=None)
