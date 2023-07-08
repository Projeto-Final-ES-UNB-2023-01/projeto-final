from ..webapp import db
from sqlalchemy_json import MutableJson
class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String)
    questions = db.Column(MutableJson)
    prof_id = db.Column(db.Integer, db.ForeignKey('users.id'))


