import click
import database
from flask import Blueprint
from database.models import *
from database.__init__ import *
admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/', methods=('GET', 'POST'))
def admin_index():
    return 'Hello admin'

def add_questions():
    section = 1
    if section=1:
        if 'question' in request.form and 'answer' in request.form :
        question = [Questions(question = request.form['question'],'
                                   answer = request.form['answer'],
                                   is_correct = True,
                                   section = 1)]
        database_session.add(question)
        database_session.commit()
    elif section=2:
        if 'question' in request.form :
        question = [ Questions(question = request.form['question'],
                                   answer = 'This is a section 2 question',
                                   is_Correct = True,
                                   section = 2)
                                   ]
        database_session.add(question)
        database_session.commit()

    elif section=3:
        if 'question' in request.form :
        question = [ Questions(question = request.form['question'],
                                    answer = 'This is a section 3 question',
                                    is_Correct = True,
                                    section = 3),
                                    ]
        database_session.add(question)
        database_session.commit()


def del_question():
    #test in CLI Form
    if 'answer' in request.form and 'question' in request.form :
    del_st = Questions.query.filter_by(question=request.form['question']).all()
        database_session.delete(del_st)
        database_session.commit()


def del_answer():
    #test in CLI form
    if 'answer' in request.form and 'question' in request.form :
    del_st = questions.query.filter(and_(answer=request.form['answer'], question=request.form['question']))
        database_session.delete(del_st)
        database_session.commit()

def update_question():
    #test in CLI form
    if 'question' in request.form and 'new_question' in request.form :
    Questions.update().values(question=request.form ['new_question']).where(
        Questions.c.question==request.form ['question'])
    database_session.commit()


def update_answer():
    #test in CLI form
    if 'question' in request.form and 'answer' in request.form and 'new_answer' in request.form :
    Questions.update().values(answer=request.form ['new_answer']).where(
        Questions.c.question==request.form ['question']).and(Questions.c.answer == request.form ['answer'])
    database_session.commit()
