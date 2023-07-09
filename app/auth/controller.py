from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..webapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from flask_login import login_user, login_required, logout_user, current_user
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.jinja2')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User not found")
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, password):
            flash('WRONG PASSWORD. TRY AGAIN')
            return redirect(url_for('auth.login'))

        login_user(user)

    return redirect(url_for('main.profile'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.jinja2')

    if request.method == 'POST':
        registration_number = request.form.get('registration-number')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        user = User.query.filter_by(registration=registration_number).first()

        if user:
            flash('user already registered ')
            return redirect(url_for('auth.login'))
        else:
            new_user = User(registration=registration_number,
                            email=email,
                            name=name,
                            password=generate_password_hash(password, method='sha256'),
                            role=role)

    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)

    return redirect(url_for('main.profile'))


@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))
