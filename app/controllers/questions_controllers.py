from flask import Blueprint, render_template, redirect, url_for,request
from flask_login import login_required, current_user
from ..models import Question
from ..webapp import db

question = Blueprint('question',__name__)

@question.route('/new',methods = ['POST','GET'])
@login_required
def new():
    if request.method == 'GET':
        return render_template('questions/new.jinja2')
    if request.method == 'POST':
        command = request.form.get('command')
        answer = request.form['answer']
        value = request.form.get('value')
        
        new_question = Question(type = 'A',
                                command = command,
                                options = None,
                                answer = answer,
                                value=value,
                                prof_id = current_user.id)
        db.session.add(new_question)
        db.session.commit()


        return redirect(url_for('question.new'))

