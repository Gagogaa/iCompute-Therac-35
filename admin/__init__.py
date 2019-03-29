import database
from database.models import *
from database.__init__ import *
from flask import Blueprint, render_template, request
from pprint import pprint

admin = Blueprint('admin', __name__, template_folder='admin_templates')

@admin.route('/')
def admin_index():
    return render_template('index.html', link="#", link2="./test", link3="./question", link4="./user", link5="./results")

@admin.route('/test')
def admin_create_test():
    return render_template('test_create.html', link="./")

@admin.route('/user')
def admin_edit_users():
	return render_template('userAdd.html', link="./")

@admin.route('/question')
def admin_edit_questions():

            questions = []
            data = {}
            counter = 1
            ansNum = 1

            # Build Dictionary for questions pulled from the db
            for question in database_session.query(Questions.question).distinct():
                data['id'] = counter
                data['question'] = question.question
                for answer in database_session.query(Questions.answer).filter(Questions.question == question.question):
                    ans = 'answer' + str(ansNum)
                    data[ans] = answer.answer
                    ansNum += 1
                questions.append(data)
                ansNum = 1
                counter += 1
                data = {}


            return render_template('questionEditUI.html', questions=questions)

@admin.route('/results')
def admin_view_results():
	return render_template('testResults.html', link="./")


@admin.route('/addQuestion', methods=['POST'])
def add_question():
    if 'section' in request.form:
        mySection = request.form['section']
        if mySection == "multiple-choice":
            if 'question' in request.form and 'answer' in request.form:
                myQuestion = request.form['question']
                myAnswer = request.form['answer']
                question = [Questions(question = myQuestion,
                                   answer = myAnswer,
                                   is_correct = True,
                                   section = 1)
                                   ]
                database_session.add_all(question)
                database_session.commit()
                return 'added section 1'
        elif mySection == "short-answer":
                if 'question' in request.form:
                    myQuestion = request.form['question']
                    question = [Questions(question = myQuestion,
                                    answer = "this is a section 2 question",
                                    is_correct = True,
                                    section = 2)]
                    database_session.add_all(question)
                    database_session.commit()
                    return 'Added Section Two'
        elif mySection == "scratch-answer":
            if 'question' in request.form:
                myQuestion = request.form['question']
                question = [Questions(question = myQuestion,
                                    answer = "this is a section 3 question",
                                    is_correct = True,
                                    section = 3)]
                database_session.add_all(question)
                database_session.commit()
                return 'Added Section Three'
    return 'success'


@admin.route('/addAnswer', methods=['POST'])
def add_answer():
    if 'question' in request.form and 'answer' in request.form:
        currentQuestion = request.form['question'];
        answerToAdd = request.form['answer'];
        new_answer = [Questions(question = currentQuestion,
                                answer = answerToAdd,
                                is_correct = False,
                                section = 1)
                                ]
        database_session.add_all(new_answer);
        database_session.commit();
        return 'success'

def delete_question():
    if 'question' in request.form:
        del_query = database_session.query(Questions).filter(Questions.question==request.form['question'])
        del_query.delete()
        database_session.commit()

def delete_answer():
    if 'question' in request.form and 'answer' in request.form:
        del_query = database_session.query(Questions).filter(and_(Questions.question==request.form['question'] , Questions.answer==request.form['answer']))
        del_query.delete()
        database_session.commit()


def edit_question():
    if 'question' in request.form and 'new_question' in request.form:
        rows_to_update = database_session.query(Questions).filter(Questions.question == request.form['question'])
        for row in rows_to_update:
            row.question = request.form['new_question']
        database_session.commit()

def edit_answer():
    if 'question' in request.form and 'answer' in request.form and 'new_answer' in request.form:
        rows_to_update = database_session.query(Questions).filter(and_(Questions.question == request.form['question'] , Questions.answer == request.form['answer']))
        rows_to_update.answer=request.form['new_answer']
        database_session.commit()

def clear_student_answers():
    del_query = database_session.query(StudentAnswers)
    del_query.delete()
    database_session.commit()
