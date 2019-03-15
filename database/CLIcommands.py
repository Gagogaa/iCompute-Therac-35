import click
import database
from flask.cli import with_appcontext
from database.models import *

@click.command('add-testing-data')
@with_appcontext

def testing_data():
    questions =[
     Questions(question = 'What is the name of the unit that helps store data in a computer',
                                answer = 'CPU',
                                is_correct = False,
                                section = 1),

    Questions(question = 'What is the name of the unit that helps store data in a computer',
                                answer = 'Input',
                                is_correct = False,
                                section = 1),

    Questions(question = 'What is the name of the unit that helps store data in a computer',
                                answer = 'Memory',
                                is_correct = True,
                                section = 1),

    Questions(question = 'What is the name of the unit that helps store data in a computer',
                                    answer = 'output',
                                    is_correct = False,
                                    section = 1)
                                ]

    database_session.add_all(questions)
    database_session.commit()
    database_session.flush()
