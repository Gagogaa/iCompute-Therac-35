import click
import database
from flask import current_app, g
from flask.cli import with_appcontext
from database.models import *
from database.__init__ import *

def init_app(app):
    #app.teardown_appcontext(close_db)
    app.cli.add_command(testing_data)



@click.command('add-testing-data')
@with_appcontext
def testing_data():
    questions =[
     Questions(question = 'This provides a step-by-step procedure for performing a task.',
                                answer = 'Keyboard',
                                is_Correct = False,
                                section = 1),

    Questions(question = 'This provides a step-by-step procedure for performing a task.',
                                answer = 'Algorithm',
                                is_Correct = True,
                                section = 1),

    Questions(question = 'This provides a step-by-step procedure for performing a task.',
                                answer = 'Internet',
                                is_Correct = False,
                                section = 1),

    Questions(question = 'This provides a step-by-step procedure for performing a task.',
                                answer = 'Windows',
                                is_Correct = False,
                                section = 1),

    Questions(question = 'Which one of the following is not a programming language?',
                                answer = 'Java',
                                is_Correct = False,
                                section = 1),

    Questions(question = 'Which one of the following is not a programming language?',
                                answer = 'HTML',
                                is_Correct = False,
                                section = 1),

    Questions(question = 'Which one of the following is not a programming language?',
                                answer = 'C++',
                                is_Correct = False,
                                section = 1),

    Questions(question = 'Which one of the following is not a programming language?',
                                answer = 'Binary',
                                is_Correct = True,
                                section = 1)
                                ]

    database_session.add_all(questions)
    database_session.commit()
    database_session.flush()
