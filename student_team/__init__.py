from flask import Blueprint, render_template
import database.models

student_team = Blueprint('student_team', __name__, template_folder='templates')

@student_team.route('/')
def student_team_index():
    

    #Automatically grading the user score


    return render_template('multiple_choice.html', questions=questions)

@student_team.route()
