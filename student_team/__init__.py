from flask import Blueprint, render_template

student_team = Blueprint('student_team', __name__)

@student_team.route('/')
def student_team_index():
    return render_template('student/multiple_choice.html')
