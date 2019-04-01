import database
from database.models import *
from database.__init__ import *
from flask import Blueprint, render_template, request, jsonify
from pprint import pprint

admin = Blueprint('admin', __name__, template_folder='admin_templates')

@admin.route('/')
def admin_index():
    return render_template('index.html', link="#", link2="./test", link3="./question", link4="./user", link5="./results")

@admin.route('/test')
def admin_modify_test():
    return render_template('test_modify.html', link=url_for('admin.admin_create_test'), link2=url_for('admin.admin_edit_test'), link3=url_for('admin.admin_view_test'))

@admin.route('test/test_create')
def admin_create_test():
    questions = []
    for question in database_session.query(Questions.question).distinct():
        questions.append(question.question)

    return render_template('test_create.html', questions=questions)

@admin.route('test/test_edit')
def admin_edit_test():
    return render_template('test_edit.html')

@admin.route('test/test_view')
def admin_view_test():
    return render_template('test_view.html')

@admin.route('/user')
def admin_edit_users():

    usernames = []
    data = {}
    counter = 1

    for users in database_session.query(Users.username).distinct():
        data['username'] = counter
        currentUser = Users.username
        data['Users'] = currentUser

        users.append(data)
        counter += 1
        data = {}

	return render_template('userAdd.html', link="./")

@admin.route('/question')
def admin_edit_questions():

            questions = []
            answers = []
            ansData = {}
            data = {}
            counter = 1
            ansNum = 1

            # Build Dictionary for questions pulled from the db
            for question in database_session.query(Questions.question, Questions.section).distinct():
                data['id'] = counter
                currentQuestion = question.question
                data['question'] = currentQuestion
                section = question.section
                data['section'] = section

                for answer in database_session.query(Questions.answer, Questions.is_correct).filter(Questions.question == question.question):
                    ansData = {}
                    if isCorrect:
                        ansData['is_correct'] = True
                    else:
                        ansData['is_correct'] = False
                    ansData['ansCounter'] = counter
                    ansData['ans_id'] = ansNum
                    ansData['answer'] = answer.answer
                    ansData['is_correct'] = answer.is_correct
                    answers.append(ansData)
                    ansNum += 1

                questions.append(data)
                ansNum = 1
                counter += 1
                data = {}




            return render_template('questionEditUI.html', questions=questions, answers=answers )

@admin.route('/results')
def admin_view_results():


	theScores = []
	data = {}
	counter = 0

	# Build Dictionary for test names pulled from the db
	for testName in database_session.query(StudentScore.test_name).distinct().order_by(StudentScore.test_name):
		data['id'] = counter
		data['theTestName'] = testName.test_name

		# Set up for different cards on the accordian html section
		data['accord1'] = "#collapse" + str(counter)
		data['accord2'] = "collapse" + str(counter)

		#Set up for the rest of the data needed
		theTestTakers = []
		data['testTakers'] = theTestTakers


		theScores.append(data)
		counter += 1
		data = {}

	#Add the rest of the data in a sub Dictionary of each test
	details = {}
	for i in range(0, counter):
		#for each test, grab all team results of that test
		for testResult in database_session.query(StudentScore).filter(StudentScore.test_name == theScores[i]['theTestName']).order_by(StudentScore.total_score.desc()):
			details['teamName'] = testResult.team_name
			for schoolName in database_session.query(StudentTeam).filter(StudentTeam.team_name == details['teamName']):
				details['theSchoolName'] = schoolName.school_name
			details['teamYear'] = testResult.team_year
			details['section1Score'] = testResult.section_one_score
			details['section2Score'] = testResult.section_two_score
			details['section3Score'] = testResult.section_three_score
			details['section4Score'] = testResult.total_score

			theScores[i]['testTakers'].append(details)
			details = {}


	return render_template('testResults.html', link="./", theScores=theScores)



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
                return render_template('questionEditUI.html')
        elif mySection == "short-answer":
                if 'question' in request.form:
                    myQuestion = request.form['question']
                    question = [Questions(question = myQuestion,
                                    answer = "this is a section 2 question",
                                    is_correct = True,
                                    section = 2)]
                    database_session.add_all(question)
                    database_session.commit()
                    return render_template('questionEditUI.html')
        elif mySection == "scratch-answer":
            if 'question' in request.form:
                myQuestion = request.form['question']
                question = [Questions(question = myQuestion,
                                    answer = "this is a section 3 question",
                                    is_correct = True,
                                    section = 3)]
                database_session.add_all(question)
                database_session.commit()
                return render_template('questionEditUI.html')
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

@admin.route('/delQuestion', methods=['POST'])
def delete_question():
    if 'question' in request.form:
        del_query = database_session.query(Questions).filter(Questions.question==request.form['question'])
        del_query.delete()
        database_session.commit()

@admin.route('/delAnswer', methods=['POST'])
def delete_answer():
    if 'question' in request.form and 'answer' in request.form:
        del_query = database_session.query(Questions.answer).filter(and_(Questions.question==request.form['question'] , Questions.answer==request.form['answer']))
        del_query.delete()
        database_session.commit()
    return"success"
@admin.route('/editQuestion', methods=['POST'])
def edit_question():
    if 'question' in request.form and 'new_question' in request.form:
        rows_to_update = database_session.query(Questions).filter(Questions.question == request.form['question'])
        for row in rows_to_update:
            row.question = request.form['new_question']
        database_session.commit()
    return "success"

@admin.route('/editAnswer', methods=['POST'])
def edit_answer():
    if 'question' in request.form and 'answer' in request.form and 'new_answer' in request.form:
        print(request.form['question'])
        print(request.form['answer'])
        print(request.form['new_answer'])

        rows_to_update = database_session.query(Questions).filter(Questions.question == request.form['question'] , Questions.answer == request.form['answer'])
        print(rows_to_update)
        for row in rows_to_update:
            row.answer = request.form['new_answer']
        print("supposedly updated")
        database_session.commit()
    return "success answer"


def clear_student_answers():
    del_query = database_session.query(StudentAnswers)
    del_query.delete()
    database_session.commit()
