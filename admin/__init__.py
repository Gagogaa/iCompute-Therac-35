from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
def admin_index():
    return render_template('index.html')

@admin.route('/test')
def admin_create_test():
    return render_template('test_create.html')

@admin.route('/user')
def admin_edit_users():
	return render_template('userAddHead.html')