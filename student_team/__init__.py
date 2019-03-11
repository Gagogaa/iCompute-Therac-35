from flask import Blueprint, render_template
from database.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

student_team = Blueprint('student_team', __name__, template_folder='templates')

engine = create_engine('sqlite:///iCompute.db', convert_unicode=True)
database_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=engine))
Base = declarative_base()
Base.query = database_session.query_property()

@student_team.route('/')
def student_team_index():
    questions = []

    for question in database_session.query(SectionOneQnA):
        questions.append(question)

    return render_template('multiple_choice.html', questions=questions)

@student_team.route('/section-b')
def section_b():
    

    return render_template('short_answer.html')
