from ..webapp import db
from sqlalchemy_json import MutableJson
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(1))
    command = db.Column(db.String)
    options = db.Column(MutableJson)
    answer = db.Column(db.String)
    value = db.Column(db.Float)
    prof_id = db.Column(db.Integer, db.ForeignKey('users.id'))


