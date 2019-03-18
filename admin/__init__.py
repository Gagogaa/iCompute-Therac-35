from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
def admin_index():
    return render_template('index.html', link="#", link2="./test", link3="./question", link4="./user")

@admin.route('/test')
def admin_create_test():
    return render_template('test_create.html', link="./")

@admin.route('/user')
def admin_edit_users():
	return render_template('userAdd.html', link="./")

@admin.route('/question')
def admin_edit_questions():
	return render_template('questionEditUI.html', link="./")
