import os

basedir = os.path.abspath(os.path.dirname(__file__))
from flask import Flask, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
index = Blueprint('index', 'index')



def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    db.init_app(app)
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .controllers import blueprints
    for bp in blueprints():
        app.register_blueprint(bp, url_prefix=f"/{bp.name}")

    from .auth.loaders import load_user

    app.register_blueprint(index, url_prefix='/')

    return app


app = create_app()

