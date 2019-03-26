from flask import Flask, render_template, request, session, redirect, url_for, abort, flash, current_app, send_from_directory
from database import database_session, init_db
from database.models import Users
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_login import login_required
from functools import wraps
import os

app = Flask(__name__)

app.secret_key = 'dev' # We need to change this in the production env

# Register the login page with flask-login
login_manager = LoginManager()
login_manager.login_view = 'index'
# Set the flashed message category so they show up with the right color
login_manager.login_message_category = 'error'

login_manager.init_app(app)


def required_user_type(user_type='ANY'):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if ((current_user.user_type != user_type) and (user_type != "ANY")):
                if current_user.user_type == 'Supervisor':
                    return redirect(url_for('admin.admin_index'))
                elif current_user.user_type == 'Grader':
                    return redirect(url_for('grader.grader_index'))
                elif current_user.user_type == 'Student':
                    return redirect(url_for('student_team.student_team_index'))
                else: # The user type is some value we don't define here so this is some sort of server error
                    abort(500)

                # return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


# Import each of the pages
from admin import admin
app.register_blueprint(admin, url_prefix='/admin')

from grader import grader
app.register_blueprint(grader, url_prefix='/grader')

from student_team import student_team
app.register_blueprint(student_team, url_prefix='/student_team')

from database import CLIcommands
CLIcommands.init_app(app)
# Initialize the database... This might need to move to someplace else later on
init_db()


@login_manager.user_loader
def load_user(user_id):
    '''Function for flask login to fetch the user object based on the user id'''
    return Users.query.filter_by(username=user_id).first()


@app.route('/', methods=('GET', 'POST'))
def index():
    '''The index for the login page
    It logs users into the web application and redirects them to appropriate user page'''

    if current_user.is_authenticated:
        if current_user.user_type == 'Supervisor':
            return redirect(url_for('admin.admin_index'))
        elif current_user.user_type == 'Grader':
            return redirect(url_for('grader.grader_index'))
        elif current_user.user_type == 'Student':
            return redirect(url_for('student_team.student_team_index'))
        else: # The user type is some value we don't define here so this is some sort of server error
            abort(500)

    if request.method == 'GET':
        return render_template('logon.html')

    elif request.method == 'POST':
        # Check the form to make sure it has the fields we are looking for
        if 'Username' in request.form and 'Password' in request.form:
            user = Users.query.filter(Users.username == request.form['Username']).first()

            # If the Username is not in the database
            if user is None:
                flash('Invalid Username', 'error')
                return redirect(url_for('index'))
            else:
                if check_password_hash(user.password, request.form['Password']):

                    login_user(user)

                    if current_user.user_type == 'Supervisor':
                        return redirect(url_for('admin.admin_index'))
                    elif current_user.user_type == 'Grader':
                        return redirect(url_for('grader.grader_index'))
                    elif current_user.user_type == 'Student':
                        return redirect(url_for('student_team.student_team_index'))
                    else: # The user type is some value we don't define here so this is some sort of server error
                        abort(500)

                else: # If the user did not use the correct password
                    flash('Invalid Password', 'error')
                    return redirect(url_for('index'))

        else: # If the form did not contain a username or password submission
            return render_template('logon.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    '''Shutdown the database!'''
    database_session.remove()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

