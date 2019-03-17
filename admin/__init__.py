from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)

@admin.route('/')
def admin_index():
    return render_template('header.html')
