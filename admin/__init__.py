from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, template_folder='templates')

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
	return render_template('questionEditUI.html', link="./")

@admin.route('/results')
def admin_view_results():
	return render_template('testResults.html', link="./")

def add_question():
    section = 1
    if section =1:
        question = [Questions(question = request.form['question'],
                                   answer = request.form['answer'],
                                   is_Correct = True,
                                   section = 1)
                                   ]
        database_session.add(question)
        database_session.commit()
    elif section = 2:
        question = [Questions(question = request.form['question'],
                                    answer = "this is a section 2 question",
                                    is_Correct = True,
                                    section = 2)]
        database_session.add(question)
        database_session.commit()
    elif section = 3:
        question = [Questions(question = request.form['question'],
                                    answer = "this is a section 3 question",
                                    is_Correct = True,
                                    section = 3)]
        database_session.add(question)
        database_session.commit()


def add_answer():
    question = [Questions(question = request.form['question'],
                                answer = request.form['answer'],
                                is_Correct = False,
                                section = 1)
                                ]
    database_session.add(question)
    database_session.commit()

def delete_question():
    question = Questions.query.filter(question = request.form['question'])
    database_session.delete(question)
    database_session.commit()

def delete_answer():
    answer = Questions.query.filter(and_(question = request.form['question'], answer = request.form['answer']))
    database_session.delete(answer)
    database_session.commit()

def edit_question():
    Questions.update().values(question = request.form['new_question']).where(Questions.c.question = request.form['question'])
    database_session.commit()

def edit_answer():
    Questions.update()values(answer = request.form['new_answer']).where(Questions.c.question = request.form['question']).and(Questions.c.answer = request.form['answer'])
    database_session.commit()

def clear_student_answers():
    StudentAnswer.query().delete()
    database_session.commit()
