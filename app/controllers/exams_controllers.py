from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models import User, Question, Exam, Attempt
from ..webapp import db

exam = Blueprint('exam', __name__)


@exam.route('/')
@login_required
def show():
    if current_user.role == 'professor':
        exams = Exam.query.filter_by(prof_id=current_user.id).all()
        return render_template('exams/show.jinja2', exams=exams,current_user = current_user)
    exams = Exam.query.all()
    return render_template('exams/show.jinja2', exams=exams,current_user = current_user)
    


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
        questions_selected = request.form.getlist('checkbox')
        exam = Exam.query.filter_by(id=id).first()
        
        i = 1
        questions = {}
        for question_id in questions_selected:
            q = f'q{str(i)}'
            questions[q] = Question.query.filter_by(id = question_id).first().toJson()
            i+=1


        exam.questions = questions
        db.session.add(exam)
        db.session.commit()

        return redirect(url_for('exam.show'))

    questions = Question.query.filter_by(prof_id=current_user.id).all()
    return render_template('exams/add_questions.jinja2', questions=questions)

# @exam.route('apply/<exam_id>', defaults = {'question':None})
# @exam.route('apply/<exam_id>/<question>',methods = ['POST','GET'])

# @login_required
# def apply_exam(exam_id, question = None):
#     exam = Exam.query.filter_by(id = exam_id).first()
#     questions = list(exam.questions.keys())
#     if not question:
#         new_attempt = Attempt(student_id = current_user.id,
#                               exam_id = exam_id,
#                               )
#         db.session.add(new_attempt),
#         db.session.commit()
#         return redirect(url_for('exam.apply_exam',id = exam_id, question = questions[0]))
#     if request.method == 'GET':
#         print(exam.id,exam.questions[questions[0]] )
#         print(exam.questions)
#         return render_template('exams/apply.jinja2',id = exam.id,question = exam.questions[questions[0]])
#     answer = request.form.get('answer')
#     current_attempt = Attempt.query.filter_by(exam_id = exam_id).first()
#     current_attempt.answers[question] = answer

#     db.session.commit()
#     index = questions.index(question)
#     if index+1 > len(questions)-1:

#         return redirect(url_for('exam.grade'))


    

#     return redirect(url_for(f'exam.apply_exam',exam_id = exam.id, question = questions[index+1] ))

@exam.route('apply/<exam_id>',methods = ['GET'])
@login_required
def apply(exam_id):
    exam_questions = Exam.query.filter_by(id = exam_id).first().questions
    return render_template('exams/apply.jinja2',questions = exam_questions)

@exam.route('apply/<exam_id>',methods = ['POST'])
@login_required
def get_answers(exam_id):
    answers = {}
    grade = 0
    exam_questions = Exam.query.filter_by(id = exam_id).first().questions
    for question in exam_questions:
        answer = request.form.get(question)
        if answer == exam_questions[question]['answer']:
            grade+= exam_questions[question]['value']

        answers[question] = answer

    new_attempt = Attempt(student_id = current_user.id,
                          answers = answers,
                          exam_id = exam_id,
                          grade = grade
    )
    db.session.add(new_attempt)
    db.session.commit()
    return redirect(url_for('main.profile'))

    