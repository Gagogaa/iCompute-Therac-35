from flask import *
from database import database_session
from database.models import *

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

    if request.method == 'POST':
        is_validated = True
        if 'test_name' not in request.form:
            is_validated = False

        for i in range(0, len(request.form)-1):
            if ('question' + str(i)) not in request.form:
                is_validated = False

        if is_validated:
            if request.form['test_name'] not in database_session.query(iComputeTest.test_name).distinct():
                for i in range(0, len(request.form)-1):
                    temp = iComputeTest(orderId=i,
                                        question=(request.form['question'] + str(i)),
                                        section=1,
                                        test_name=request.form['test_name'],
                                        year=request.form['year'],
                                        student_grade=request.form['grade'])
                    database_session.add(temp)
                database_session.commit()
                return redirect(url_for('admin_view_test'), test_name=request.form['test_name'])
            else:
                flash('A test with this test name already exists. Please try again with a different name or edit a pre-existing test.')
                return redirect(url_for('admin_create_test'))
        else:
            flash('Something went wrong with the data you tried to submit.')
            return redirect(url_for('admin_create_test'))

    return render_template('test_create.html', questions=questions)

@admin.route('test/test_edit')
def admin_edit_test():
    return render_template('test_edit.html')

@admin.route('test/test_view')
def admin_view_test():
    return render_template('test_view.html')

@admin.route('/user')
def admin_edit_users():
	return render_template('userAdd.html', link="./")

@admin.route('/question')
def admin_edit_questions():
	return render_template('questionEditUI.html', link="./")

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
