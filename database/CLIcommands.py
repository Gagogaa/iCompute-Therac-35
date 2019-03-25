import click
import database
from flask import current_app, g
from flask.cli import with_appcontext
from database.models import *
from database.__init__ import *
from sqlalchemy import *

def init_app(app):
    #app.teardown_appcontext(close_db)
    app.cli.add_command(testing_data)
    app.cli.add_command(deletion_test)
    app.cli.add_command(update_testing)

@click.command('add-testing-data')
@with_appcontext
def testing_data():
    data =[

    #  Here is the format to use to add Data
    #  TableName(columnName = Data to add,
    #             colName2 = more data,
    #             colName3 =final data,) put comma at end and repeat to add more data


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

    database_session.add_all(data)
    database_session.commit()
    database_session.flush()


@click.command('delete-test')
@with_appcontext
def deletion_test():
    del_query = database_session.query(Questions).filter(Questions.question=='Which one of the following is not a programming language?')
    del_query.delete()
    database_session.commit()

@click.command('update-test')
@with_appcontext
def update_testing():
    rows_to_update = database_session.query(Questions).filter(Questions.question == 'This provides a step-by-step procedure for performing a task.')
    for row in rows_to_update:
        row.question = "this is a new question"
    database_session.commit()
