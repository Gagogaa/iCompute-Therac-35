import click
import database
import datetime
from flask import current_app, g
from flask.cli import with_appcontext
from database.models import *
from database.__init__ import *
from werkzeug.security import generate_password_hash


def init_app(app):
    #app.teardown_appcontext(close_db)
    app.cli.add_command(testing_data)


@click.command('add-testing-data')
@with_appcontext
def testing_data():
    AddData = [
        Questions(question = 'This provides a step-by-step procedure for performing a task.',
                  answer = 'Keyboard',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'This provides a step-by-step procedure for performing a task.',
                  answer = 'Algorithm',
                  is_correct = True,
                  section = 1
                  ),
        Questions(question = 'This provides a step-by-step procedure for performing a task.',
                  answer = 'Internet',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'This provides a step-by-step procedure for performing a task.',
                  answer = 'Windows',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'Which one of the following is not a programming language?',
                  answer = 'Java',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'Which one of the following is not a programming language?',
                  answer = 'HTML',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'Which one of the following is not a programming language?',
                  answer = 'C++',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'Which one of the following is not a programming language?',
                  answer = 'Binary',
                  is_correct = True,
                  section = 1
                  ),
        Questions(question = 'This is a third test question.',
                  answer = 'Wrong',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'This is a third test question.',
                  answer = 'Correct',
                  is_correct = True,
                  section = 1
                  ),
        Questions(question = 'This is a third test question.',
                  answer = 'Double Wrong',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'This is a third test question.',
                  answer = 'Triple Wrong',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'This is a fourth test question.',
                  answer = 'Wrong',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'This is a fourth test question.',
                  answer = 'Double wrong',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'This is a fourth test question.',
                  answer = 'Correct',
                  is_correct = True,
                  section = 1
                  ),
        Questions(question = 'This is a fourth test question.',
                  answer = 'Triple Wrong',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'This is a fifth test question.',
                  answer = 'Correct',
                  is_correct = True,
                  section = 1
                  ),
        Questions(question = 'This is a fourth test question.',
                  answer = 'Wrong',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'This is a fourth test question.',
                  answer = 'Double wrong',
                  is_correct = False,
                  section = 1
                  ),
        Questions(question = 'This is a fourth test question.',
                  answer = 'Triple Wrong',
                  is_correct = False,
                  section = 1
                  ),
        StudentTeam(name = 'TeamM8s',
                    year = datetime.datetime.now(),
                    school_name= 'School of Rock'
                    ),
        StudentTeam(name = 'TeamL8',
                    year = datetime.datetime.now(),
                    school_name = 'School of Hard Knocks'
                    ),
        StudentAnswer(team_name = 'teamM8s',
                      team_year = datetime.datetime.now(),
                      section = 1,
                      question = 'This provides a step-by-step procedure for performing a task.',
                      answer = 'Algorithm'
                      ),
        StudentAnswer(team_name = 'teamM8s',
                      team_year = datetime.datetime.now(),
                      section = 1,
                      question = 'Which one of the following is not a programming language?',
                      answer = 'Binary'
                      ),
        StudentAnswer(team_name = 'teamL8',
                      team_year = datetime.datetime.now(),
                      section = 1,
                      question = 'This provides a step-by-step procedure for performing a task.',
                      answer = 'Keyboard'
                      ),
        StudentAnswer(team_name = 'teamL8',
                      team_year = datetime.datetime.now(),
                      section = 1,
                      question = 'Which one of the following is not a programming language?',
                      answer = 'C++'
                      ),
        iComputeTest(orderId = 1,
                     question = 'This provides a step-by-step procedure for performing a task.',
                     section = 1,
                     year = datetime.datetime.now(),
                     student_grade = 'Fourth'
                     ),
        iComputeTest(orderId = 2,
                     question = 'Which one of the following is not a programming language?',
                     section = 1,
                     year = datetime.datetime.now(),
                     student_grade = 'Fourth'
                     ),
        Users(username = 'teamM8s',
              password = generate_password_hash('password'),
              user_type = 'Student'
              ),
        Users(username = 'teamL8',
              password = generate_password_hash('password'),
              user_type = 'Student'
              ),
        Users(username = 'supervisor123',
              password = generate_password_hash('password'),
              user_type = 'Supervisor'
              ),
        Users(username = 'grader456',
              password = generate_password_hash('password'),
              user_type = 'Grader'
              ),
        StudentScore(team_name = 'teamM8s',
                     team_year = '2019',
                     score = 100
                     ),
        StudentScore(team_name = 'teamL8',
                     team_year = '2019',
                     score = 0
                     )
    ]

    database_session.add_all(AddData)
    database_session.commit()
