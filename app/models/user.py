from ..webapp import db
from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column()
    email: Mapped[String] = mapped_column(String(200))
    registration: Mapped[String] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[String] = mapped_column(String(200))
    role: Mapped[String] = mapped_column(String)

    questions: Mapped[list["Question"]] = relationship(back_populates='professor')
    exams: Mapped[list["Exam"]] = relationship(back_populates='professor')
