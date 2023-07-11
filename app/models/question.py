from ..webapp import db
from . import User, Exam
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_json import MutableJson


class Question(db.Model):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[String] = mapped_column(String)
    type: Mapped[String] = mapped_column(String(1))
    command: Mapped[String] = mapped_column(String, nullable=True)
    options: Mapped[MutableJson] = mapped_column(MutableJson, nullable=True)
    answer: Mapped[String] = mapped_column(String, nullable=True)
    value: Mapped[Float] = mapped_column(Float, nullable=True)
    prof_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    exam_id: Mapped[int] = mapped_column(ForeignKey('exams.id'), nullable=True)

    professor: Mapped["User"] = relationship(back_populates='questions')

    def toJson(self):
        return {"id": self.id,
                "description": self.description,
                "type": self.type,
                "command": self.command,
                "options": self.options,
                "answer": self.answer,
                "value": self.value
                }
