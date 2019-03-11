from flask import Blueprint, render_template
import database.models
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

student_team = Blueprint('student_team', __name__, template_folder='templates')

@student_team.route('/')
def student_team_index():
    engine = create_engine('sqlite:///iCompute.db', convert_unicode=True)
    database_session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=engine))
    Base = declarative_base()
    Base.query = database_session.query_property()

    for question in database_session.query(SectionOneQnA)

    #Automatically grading the user score


    return render_template('multiple_choice.html', questions=questions)

@student_team.route()
