from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models import User, Question, Exam, Attempt
from ..webapp import db
from datetime import datetime, time

exam = Blueprint('exam', __name__)


@exam.route('/')
@login_required
def show():
    if current_user.role == 'professor':
        exams = Exam.query.filter_by(prof_id=current_user.id).all()
        return render_template('exams/show.jinja2', exams=exams, current_user=current_user)

    exams = Exam.query.all()
    done_exams = [student_attempts.exam_id for  student_attempts in  Attempt.query.filter_by(student_id = current_user.id).all()]
    print(done_exams)
    print(exams)
    return render_template('exams/show.jinja2', exams=exams, current_user=current_user, done_exams = done_exams)


@exam.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        description = request.form.get('description')
        openingDate = request.form.get('openingDate')
        closingDate = request.form.get('closingDate')

        date_format = '%Y-%m-%dT%H:%M'
        openingConvertedDate = datetime.strptime(openingDate, date_format)
        closingConvertedDate = datetime.strptime(closingDate, date_format)

        if openingConvertedDate >= closingConvertedDate:
            flash("Invalid Date. Please try again.")
            return redirect(url_for('exam.new'))

        new_exam = Exam(description=description,
                        prof_id=current_user.id,
                        openingDate=openingConvertedDate,
                        closingDate=closingConvertedDate)

        db.session.add(new_exam)
        db.session.commit()

        return redirect(url_for('exam.add_questions', id=new_exam.id))

    return render_template('exams/new.jinja2')


@exam.route('/<id>/delete')
@login_required
def delete(id):
    exam = db.get_or_404(Exam, id)
    db.session.delete(exam)

    attempts = Attempt.query.filter_by(exam_id=id).all()

    for attempt in attempts:
        db.session.delete(attempt)

    db.session.commit()

    return redirect(url_for('exam.show'))


@exam.route('/<id>/add_questions', methods=['POST', 'GET'])
@login_required
def add_questions(id):
    if request.method == 'POST':
        questions_selected = request.form.getlist('checkbox')
        exam = Exam.query.filter_by(id=id).first()

        i = 1
        questions = {}

        for question_id in questions_selected:
            q = f'q{str(i)}'
            questions[q] = Question.query.filter_by(id=question_id).first().toJson()
            i += 1

        exam.questions = questions
        db.session.add(exam)
        db.session.commit()

        return redirect(url_for('exam.show'))

    questions = Question.query.filter_by(prof_id=current_user.id).all()
    return render_template('exams/add_questions.jinja2', questions=questions)


@exam.route('apply/<exam_id>', methods=['GET'])
@login_required
def apply(exam_id):
    done = False
    attempts = Attempt.query.filter_by(exam_id=exam_id).all()
    for attempt in attempts:
        if attempt.student_id == current_user.id:
            done =True
            return render_template('exams/already_answered.jinja2')

    exam = Exam.query.filter_by(id=exam_id).first()

    if exam.openingDate <= datetime.now() <= exam.closingDate:
        exam_questions = exam.questions
        return render_template('exams/apply.jinja2', questions=exam_questions,done = done)

    flash('Exam not avaliable now.')
    return redirect(url_for('exam.show'))


@exam.route('apply/<exam_id>', methods=['POST'])
@login_required
def get_answers(exam_id):
    answers = {}
    grade = 0
    exam_questions = Exam.query.filter_by(id=exam_id).first().questions

    for question in exam_questions:
        answer = request.form.get(question)

        if answer == exam_questions[question]['answer']:
            grade += exam_questions[question]['value']

        answers[question] = answer

    new_attempt = Attempt(student_id=current_user.id,
                          answers=answers,
                          exam_id=exam_id,
                          grade=round(grade,3)
                          )
    db.session.add(new_attempt)
    db.session.commit()

    return redirect(url_for('main.profile'))


@exam.route('/<id>/report')
@login_required
def show_reports(id):
    exam = Exam.query.filter_by(id=id).first()
    attempts = Attempt.query.filter_by(exam_id=id).all()
    

    reports = {}

    for attempt in attempts:
        student = User.query.filter_by(id=attempt.student_id).first()
        reports[student.name] = attempt
    print(reports)
    return render_template('exams/show_reports.jinja2', reports=reports, exam=exam)


@exam.route('/<exam_id>/student/<student_id>/report')
@login_required
def student_report(exam_id, student_id):
    student_name = User.query.filter_by(id = student_id).first().name
    student_attempt = Attempt.query.filter_by(exam_id=exam_id, student_id=student_id).first()
    exam_answered = Exam.query.filter_by(id=exam_id).first()

    return render_template('exams/student_report.jinja2', student_attempt=student_attempt,
                           exam_answered=exam_answered,student_name = student_name)


@exam.route('/<exam_id>/report/<attempt_id>')
@login_required
def report(exam_id, attempt_id):
    exam = Exam.query.filter_by(id=exam_id).first()
    attempt = Attempt.query.filter_by(id=attempt_id).first()
    student = User.query.filter_by(id=attempt.student_id).first()

    return render_template('exams/report.jinja2', student=student, exam=exam, attempt=attempt)
