from ..webapp import db
from .user import User
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AnsweredExam(db.Model):
    __tablename__ = 'answered_exams'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey('exams.id'), primary_key=True)

    answers: Mapped[list["Answer"]] = relationship(back_populates='answered_exam')
