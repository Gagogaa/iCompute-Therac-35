from flask import Blueprint, render_template

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
	return render_template('questionEditUI.html', link="./")

@admin.route('/results')
def admin_view_results():
	return render_template('testResults.html', link="./")

def add_question():
    section = 1
    if section == 1:
        if 'question' in request.form and 'answer' in request.form:
            question = [Questions(question = request.form['question'],
                                   answer = request.form['answer'],
                                   is_Correct = True,
                                   section = 1)
                                   ]
            database_session.add(question)
            database_session.commit()
    elif section == 2:
        if 'question' in request.form and 'answer' in request.form:
            question = [Questions(question = request.form['question'],
                                    answer = "this is a section 2 question",
                                    is_Correct = True,
                                    section = 2)]
            database_session.add(question)
            database_session.commit()
    elif section == 3:
        if 'question' in request.form and 'answer' in request.form:
            question = [Questions(question = request.form['question'],
                                    answer = "this is a section 3 question",
                                    is_Correct = True,
                                    section = 3)]
            database_session.add(question)
            database_session.commit()

@admin.route('/addAnswer', methods=['POST'])
def add_answer():
    if 'question' in request.form and 'answer' in request.form:
        question = [Questions(question = request.form.get['question'],
                                answer = request.form.get['answer'],
                                is_Correct = False,
                                section = 1)
                                ]
        database_session.add(question)
        database_session.commit()

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
