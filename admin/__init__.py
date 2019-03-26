from flask import Blueprint, render_template
from flask_login import login_required
from logon import required_user_type

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
    return render_template('testResults.html', link="./")
