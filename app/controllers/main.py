from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..webapp import index


@index.route('/')
def index():
    return render_template('index.jinja2')


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.jinja2")


@main.route('/profile/')
@login_required
def profile():
    return render_template("profile.jinja2")
