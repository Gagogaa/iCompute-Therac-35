from flask import Flask, render_template, request, session, redirect, url_for, abort, flash
from database import database_session, init_db
from database.models import Users
from werkzeug.security import check_password_hash

app = Flask(__name__)

app.secret_key = b'dev' # We need to change this in the production env

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


# TODO work with secure sessions to lock down parts of the web application
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('logon.html')

    elif request.method == 'POST':
        # Check the form to make sure it has the fields we are looking for
        if 'Username' in request.form and 'Password' in request.form:
            current_user = Users.query.filter(Users.username == request.form['Username']).first()

            # If the Username is not in the database
            if current_user is None:
                flash('Invalid Username')
                return redirect(url_for('index'))
            else:
                if check_password_hash(current_user.password, request.form['Password']):

                    if current_user.user_type == 'Supervisor':
                        return redirect(url_for('admin.admin_index'))
                    elif current_user.user_type == 'Grader':
                        return redirect(url_for('grader.grader_index'))
                    elif current_user.user_type == 'Student':
                        return redirect(url_for('student_team.student_team_index'))
                    else: # The user type is some value we don't define here so this is some sort of server error
                        abort(500)

                else: # If the user did not use the correct password
                    flash('Invalid Password')
                    return redirect(url_for('index'))

        else: # If the form did not contain a username or password submission
            return render_template('logon.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Shutdown the database!"""
    database_session.remove()
