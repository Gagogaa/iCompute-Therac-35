from flask import Blueprint, render_template
from flask_login import login_required
from logon import required_user_type
from database import database_session
from database.models import *


admin = Blueprint('admin', __name__, template_folder='admin_templates')


@admin.route('/')
@login_required
@required_user_type('Supervisor')
def admin_index():
    return render_template('index.html', link="#", link2="./test", link3="./question", link4="./user", link5="./results")


@admin.route('/test')
@login_required
@required_user_type('Supervisor')
def admin_create_test():
    return render_template('test_create.html', link="./")


@admin.route('/user')
@login_required
@required_user_type('Supervisor')
def admin_edit_users():
    return render_template('userAdd.html', link="./")


@admin.route('/question')
@login_required
@required_user_type('Supervisor')
def admin_edit_questions():
    return render_template('questionEditUI.html', link="./")


@admin.route('/results')
@login_required
@required_user_type('Supervisor')
def admin_view_results():
    exam_results = []
    exam_data = {}

    # Build Dictionary for test names pulled from the db
    for counter, test_name in enumerate(database_session.query(StudentScore.test_name).distinct().order_by(StudentScore.test_name), start=1):
        exam_data['id'] = counter
        exam_data['test_name'] = test_name.test_name

        # Set up for different cards on the accordian html section
        exam_data['accord1'] = "#collapse" + str(counter)
        exam_data['accord2'] = "collapse" + str(counter)

        # Set up for the rest of the data needed
        exam_data['student_teams'] = []

        exam_results.append(exam_data)
        exam_data = {}

    # Add the rest of the data in a sub Dictionary of each test
    details = {}
    for i in range(0, counter):

        # for each test, grab all team results of that test
        for test_result in database_session.query(StudentScore).filter(StudentScore.test_name == exam_results[i]['test_name']).order_by(StudentScore.total_score.desc()):
            details['team_name'] = test_result.team_name

            for schoolName in database_session.query(StudentTeam).filter(StudentTeam.team_name == details['team_name']):
                details['school_name'] = schoolName.school_name

            # TODO Why is team year in details because it's not used on the page?
            details['team_year'] = test_result.team_year
            details['section_one_score'] = test_result.section_one_score
            details['section_two_score'] = test_result.section_two_score
            details['section_three_score'] = test_result.section_three_score
            details['total_score'] = test_result.total_score

            exam_results[i]['student_teams'].append(details)
            details = {}

    return render_template('testResults.html', link="./", exam_results=exam_results)

