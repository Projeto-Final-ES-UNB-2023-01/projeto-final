from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models import User, Question, Exam
from ..webapp import db

exam = Blueprint('exam', __name__)


@exam.route('/')
@login_required
def show():
    exams = Exam.query.filter_by(prof_id=current_user.id).all()
    return render_template('exams/show.jinja2', exams=exams)


@exam.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        description = request.form.get('description')
        new_exam = Exam(description=description, prof_id=current_user.id)

        db.session.add(new_exam)
        db.session.commit()

        return redirect(url_for('exam.add_questions', id=new_exam.id))

    return render_template('exams/new.jinja2')


@exam.route('/<id>/delete')
@login_required
def delete(id):
    exam = db.get_or_404(Exam, id)
    db.session.delete(exam)
    db.session.commit()

    return redirect(url_for('exam.show'))


@exam.route('/<id>/add_questions', methods=['POST', 'GET'])
@login_required
def add_questions(id):
    if request.method == 'POST':
        selected = request.form.getlist('checkbox')
        exam = Exam.query.filter_by(id=id).first()

        for question_id in selected:
            question = Question.query.filter_by(id=int(question_id)).first()
            question.exam = exam

            db.session.commit()

        return redirect(url_for('exam.show'))

    questions = Question.query.filter_by(prof_id=current_user.id).all()
    return render_template('exams/add_questions.jinja2', questions=questions)
