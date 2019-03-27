from flask import *

admin = Blueprint('admin', __name__, template_folder='admin_templates')

@admin.route('/')
def admin_index():
    return render_template('index.html', link="#", link2="./test", link3="./question", link4="./user", link5="./results")

@admin.route('/test')
def admin_modify_test():
    return render_template('test_modify.html', link=url_for('admin.admin_create_test'), link2=url_for('admin.admin_edit_test'), link3=url_for('admin.admin_view_test'))

@admin.route('test/test_create')
def admin_create_test():
    return render_template('test_create.html')

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
	return render_template('testResults.html', link="./")
