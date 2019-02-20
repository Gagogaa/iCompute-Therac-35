from flask import Blueprint

grader = Blueprint('grader', __name__)

@grader.route('/')
def grader_index():
    return 'Hello grader'

