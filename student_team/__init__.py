from flask import Blueprint

student_team = Blueprint('student_team', __name__)

@student_team.route('/')
def student_team_index():
    return 'Hello student team'

