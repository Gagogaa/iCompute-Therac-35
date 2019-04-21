from flask import Blueprint, render_template, request, make_response
from database import database_session
from database.models import *
from flask_login import login_required
from logon import required_user_type


grader = Blueprint('grader', __name__, template_folder='grader_templates')


@grader.route('/', methods=('GET', 'POST'))
@login_required
@required_user_type('Grader')
def grader_index():
    teamsData = []
    tests = []
    for team in database_session.query(StudentTeam):
        teamData = {
            "team_name": team.team_name,
            "team_year": team.team_year,
            "test_name": "?",
            "sec_one_score": "?",
            "sec_two_score": "?",
            "sec_three_score": "?",
            "total_score": "?"
        }
        student_scores = StudentScore.query.filter_by(team_name=team.team_name).order_by(StudentScore.team_year).first()
        if student_scores:
            teamData["test_name"] = student_scores.test_name
            teamData["sec_one_score"] = student_scores.section_one_score
            teamData["sec_two_score"] = student_scores.section_two_score
            teamData["sec_three_score"] = student_scores.section_three_score
            teamData["total_score"] = student_scores.total_score
            test = iComputeTest.query.filter_by(test_name=student_scores.test_name).first()
            if test not in tests:
                if test:
                    tests.append(test)
        teamsData.append(teamData)

    return render_template('grader_home.html', teamsData=teamsData, tests=tests)

@grader.route('/<team_name>/<team_year>')
@login_required
@required_user_type('Grader')
def grade_edit(team_name, team_year):
    student_score = StudentScore.query.filter_by(team_name=team_name, team_year=team_year).first()

    if not student_score:
        return render_template('edit_grade.html', student_score=None, section_one_data=None, section_two_answers=None, section_three_answer=None)

    section_one_answers = StudentAnswer.query.filter_by(team_name=student_score.team_name, team_year=student_score.team_year, section=1)
    section_one_data = None

    if section_one_answers:
        section_one_data = []
        for section_one_answer in section_one_answers:
            answers = Questions.query.filter_by(question=section_one_answer.question).all()
            question_grade = "not-answered"
            for answer in answers:
                if answer.answer == section_one_answer.answer:
                    if answer.is_correct:
                        question_grade = "correct"
                    else:
                        question_grade = "incorrect"
            question_data = {
                "selected_answer": section_one_answer,
                "answers": answers,
                "question_grade": question_grade
            }
            section_one_data.append(question_data)

    section_two_answers = StudentAnswer.query.filter_by(team_name=student_score.team_name, team_year=student_score.team_year, section=2).all()
    section_three_answer = StudentAnswer.query.filter_by(team_name=student_score.team_name, team_year=student_score.team_year, section=3).first()

    return render_template('edit_grade.html', student_score=student_score, section_one_data=section_one_data, section_two_answers=section_two_answers, section_three_answer=section_three_answer)

@grader.route('/download-submission/<team_name>/<team_year>')
@login_required
@required_user_type('Grader')
def download_scratch_question(team_name, team_year):
    # We should only have one answer per test
    student_response = StudentAnswer.query.filter_by(team_name=team_name, team_year=team_year).filter(StudentAnswer.scratch_file!=None).first()

    if student_response:
        response = make_response(student_response.scratch_file)
        response.headers['Cache-Control'] = 'must-revalidate'
        response.headers['Pragma'] = 'must-revalidate'
        response.headers['Content-type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = f'attachment; filename="{student_response.answer}"'

        return response

    return abort(404)

@grader.route('/editGrade', methods=['POST'])
@login_required
@required_user_type('Grader')
def edit_question():
    if 'team_name' in request.form and 'team_year' in request.form and 'section' in request.form and 'score' in request.form:
        if request.form['section'] == 'section_three':
            rows_to_update = database_session.query(StudentScore).filter(StudentScore.team_name == request.form['team_name'], StudentScore.team_year == request.form['team_year'])
            for row in rows_to_update:
                row.section_three_score = request.form['score']
                row.total_score = (row.section_one_score + (row.section_two_score if row.section_two_score else 0) + int(row.section_three_score))
            database_session.commit()
    return "success"
