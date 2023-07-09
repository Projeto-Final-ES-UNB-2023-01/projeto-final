from ..webapp import db
from .user import User
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Answer(db.Model):
    __tablename__ = 'answers'

    user_id: Mapped[int] = mapped_column(ForeignKey('answered_exams.user_id'), primary_key=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey('answered_exams.exam_id'), primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'), primary_key=True)
    answer: Mapped[String] = mapped_column(String, nullable=True)

    answered_exam: Mapped["AnsweredExam"] = relationship(back_populates='answers')
    question: Mapped["Question"] = relationship(back_populates='answers')
