from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/', methods=('GET', 'POST'))
def admin_index():
    return 'Hello admin'


@admin.route('/user_create', methods=('GET', 'POST'))
def admin_index():
    return render_template('user_create.html')
