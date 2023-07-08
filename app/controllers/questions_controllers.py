from flask import Blueprint, render_template, redirect, url_for,request,flash
from flask_login import login_required, current_user
from ..models import Question
from ..webapp import db

question = Blueprint('question',__name__)

@question.route('/new',methods = ['POST','GET'])
@login_required
def new():
    if request.method == 'GET':
        if current_user.role == 'aluno':
            return redirect(url_for('main.profile'))
        return render_template('questions/new_base.jinja2')
    if request.method == 'POST':
        description = request.form.get('description')
        type = request.form.get('type')
        
        new_question = Question(type = type.upper(),
                                description = description,
                                prof_id = current_user.id)
        db.session.add(new_question)
        db.session.commit()


        return redirect(url_for('question.new_type',id = new_question.id))
    """
    PAREI NA PARTE DE DEFINIR A FUNÇÃO NEW_NOVO TIPO E TENTAR FAZER DE UMA FORMA DINÂMICA
    """
    
@question.route('/new/<id>',methods = ['POST','GET'])
@login_required
def new_type(id):
    question = Question.query.filter_by(id = id).first()
    if request.method == 'GET':
        if current_user.role == 'aluno':
            return redirect(url_for('main.profile'))
        return render_template(f'questions/tipo{question.type}.jinja2')
    if request.method == 'POST':
        command = request.form.get('command')
        answer = request.form['answer']
        value = request.form.get('value')
        
        question.command = command
        question.answer = answer
        question.value = value
        
        
        
        db.session.add(question)
        db.session.commit()


        return redirect(url_for('main.profile'))

