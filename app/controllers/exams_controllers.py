from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models import User, Question, Exam
from ..webapp import db

exam = Blueprint('exam', __name__)


@exam.route('/')
@login_required
def show():
    exams = Exam.query.filter_by(prof_id=current_user.id).all()
    print(exams)

    return render_template('exams/show.jinja2', exams=exams)


@exam.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        description = request.form.get('description')
        new_exam = Exam(description=description, prof_id=current_user.id)

        db.session.add(new_exam)
        db.session.commit()

        return redirect(url_for('exam.show'))

    return render_template('exams/new.jinja2')


@exam.route('/<id>/delete')
def delete(id):
    exam = db.get_or_404(Exam, id)
    db.session.delete(exam)
    db.session.commit()

    return redirect(url_for('exam.show'))
