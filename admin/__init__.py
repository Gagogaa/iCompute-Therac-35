from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/', methods=('GET', 'POST'))
def admin_index():
    return 'Hello admin'
