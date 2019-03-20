from flask import Blueprint, render_template
from database.models import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

grader = Blueprint('grader', __name__, template_folder='grader_templates')

engine = create_engine('sqlite:///iCompute.db', convert_unicode=True)
Session = sessionmaker(bind=engine)
session = Session()

@grader.route('/')
def grader_index():
    teams = []
    for team in session.query(StudentTeam.name):
        teams.append(team.name)

    return render_template('grader_home.html', teams=teams)
