from flask import Blueprint, render_template

grader = Blueprint('grader', __name__, template_folder='templates')

@grader.route('/')
def grader_index():
    return render_template('index.html')
