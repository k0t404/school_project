import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Lesssons(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'timetable'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    lesson_pos = sqlalchemy.Column(sqlalchemy.String)
    lesson = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cabinet = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    class_letter = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    day = sqlalchemy.Column(sqlalchemy.String, nullable=True)