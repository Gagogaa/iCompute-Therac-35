from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/')
def admin_index():
    return 'Hello admin'

