from ..webapp import db
from . import User
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Exam(db.Model):
    __tablename__ = 'exams'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[String] = mapped_column(String)
    prof_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    professor: Mapped["User"] = relationship(back_populates='exams')
    questions: Mapped[list["Question"]] = relationship(back_populates='exam')
