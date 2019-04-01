from flask import Blueprint, render_template, request
from database import database_session
from database.models import *
import csv
import os

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

@admin.route('/results', methods=('GET', 'POST'))
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

	if request.method == 'POST':
		with open('person.csv', 'w') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow('Yo dawg')
			for stuff in theScores[0]['testTakers']:
				writer.writerow(theScores[0]['theTestName'])
				writer.writerows(stuff.items())


		csvFile.close()
	return render_template('testResults.html', link="./", theScores=theScores)
