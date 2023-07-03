from ..webapp import db
from flask_login import UserMixin
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String(200),nullable = False)
    registration = db.Column(db.String,unique = True, nullable = False)
    password = db.Column(db.String(200))
    role = db.Column(db.String)
    questions = db.relationship('Question', backref = 'user')
