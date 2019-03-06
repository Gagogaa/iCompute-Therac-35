from flask import Flask, render_template, request, session
from database import database_session, init_db
#from database.models import User

app = Flask(__name__)

app.secret_key = b'dev' # We need to change this in the production env

# Import each of the pages
from admin import admin
app.register_blueprint(admin, url_prefix='/admin', template_folder='templates')

from grader import grader
app.register_blueprint(grader, url_prefix='/grader', template_folder='templates')

from student_team import student_team
app.register_blueprint(student_team, url_prefix='/student_team', template_folder='templates')

# Initialize the database... This might need to move to someplace else later on
init_db()


@app.route('/')
def index():
    return 'Woah! Welcome to the main page.'


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Shutdown the database!"""
    database_session.remove()
