from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import User, Question, Exam
from ..webapp import db
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_json import MutableJson


class Attempt(db.Model):
    __tablename__ = 'attempts'

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    answers: Mapped[MutableJson] = mapped_column(MutableJson, nullable=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey('exams.id'))
    grade: Mapped[Float] = mapped_column(Float, nullable=True)
