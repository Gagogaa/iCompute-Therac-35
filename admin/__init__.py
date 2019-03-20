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
    if section=1:
        print("add section 1")
    elif section=2:
        question = [ Questions(question = request.form['question'],
                                   answer = 'This is a section 2 question',
                                   is_Correct = True,
                                   section = 2),
                                   ]
        database_session.add(question)
        database_session.commit()
        database_session.flush()
    elif section=3:
        question = [ Questions(question = request.form['question'],
                                           answer = 'This is a section 3 question',
                                           is_Correct = True,
                                           section = 3),
                                           ]
        database_session.add(question)
        database_session.commit()
        database_session.flush()

def del_question():
    del_st = Questions.query.filter_by(question=request.form['question']).all()
    database_session.delete(del_st)
