from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
def admin_index():
    return render_template('index.html')
