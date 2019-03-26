from flask import Blueprint, render_template
from database import database_session
from database.models import *

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

	theScores = []
	data = {}
	counter = 1

	# Build Dictionary for questions pulled from the db
	for testResult in database_session.query(StudentScore).distinct():
		data['id'] = counter
		data['teamName'] = testResult.team_name
		data['teamYear'] = testResult.team_year
		data['section1Score'] = testResult.section_one_score
		data['section2Score'] = testResult.section_two_score
		data['section3Score'] = testResult.section_three_score
		data['section4Score'] = testResult.total_score

		theScores.append(data)
		counter += 1
		data = {}


	return render_template('testResults.html', link="./", theScores=theScores)
