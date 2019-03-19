import click
import database
import datetime
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
    AddData =[
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
                                section = 1),
    Questions(question = 'What is the name of the unit that helps store data in a computer?',
                                answer = 'CPU',
                                is_Correct = True,
                                section = 1),
    Questions(question = 'What is the name of the unit that helps store data in a computer?',
                                answer = 'Input',
                                is_Correct = False,
                                section = 1),
    Questions(question = 'What is the name of the unit that helps store data in a computer?',
                                answer = 'Memory',
                                is_Correct = False,
                                section = 1),
    Questions(question = 'What is the name of the unit that helps store data in a computer?',
                                answer = 'Output',
                                is_Correct = False,
                                section = 1),
    StudentTeam(name = 'TeamM8s',
                               year = datetime.datetime.now(),
                               first_student = 'Anthony',
                               second_student = 'Greg'
                               ),
    StudentTeam(name = 'TeamL8',
                              year = datetime.datetime.now(),
                              first_student = 'Jake',
                              second_student = 'Zane'
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
                            studentGrade = 'Fourth'
                            ),
    iComputeTest(orderId = 2,
                            question = 'Which one of the following is not a programming language?',
                            section = 1,
                            year = datetime.datetime.now(),
                            studentGrade = 'Fourth'
                            ),
    Users(Username = 'teamM8s',
                            Password = 'password',
                            UserType = 'Student'
                            ),
    Users(Username = 'teamL8',
                            Password = 'password',
                            UserType = 'Student'
                            ),
    Users(Username = 'supervisor123',
                            Password = 'password',
                            UserType = 'Supervisor'
                            ),
    Users(Username = 'grader456',
                            Password = 'password',
                            UserType = 'Grader'
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
    database_session.flush()
