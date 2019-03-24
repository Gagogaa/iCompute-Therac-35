from flask import Blueprint, render_template, request
from database.models import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

grader = Blueprint('grader', __name__, template_folder='grader_templates')

engine = create_engine('sqlite:///iCompute.db', convert_unicode=True)
Session = sessionmaker(bind=engine)
session = Session()

def grade_section_one(team):
    correct_answers = 0
    for answer in session.query.filter(StudentAnswer.team_name == team):
        correct_answer = session.query.filter(_and(Questions.question == answer.question, Questions.is_correct == True))
        if correct_answer.answer == answer.answer:
            correct_answers += 1



@grader.route('/')
def grader_index():
    teams = []
    for team in session.query(StudentTeam.name):
        teams.append(team.name)

    if request.method == 'POST':
        team = request.form['team_name']
        score = grade_section_one(team)


    return render_template('grader_home.html', teams=teams)
