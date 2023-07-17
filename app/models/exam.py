from datetime import datetime
from ..webapp import db
from . import User
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_json import MutableJson
from sqlalchemy.ext.mutable import MutableList


class Exam(db.Model):
    __tablename__ = 'exams'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[String] = mapped_column(String)
    questions: Mapped[MutableJson] = mapped_column(MutableJson, nullable=True)
    prof_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    openingDate: Mapped[DateTime] = mapped_column(DateTime)
    closingDate: Mapped[DateTime] = mapped_column(DateTime)
    professor: Mapped["User"] = relationship(back_populates='exams')

    

