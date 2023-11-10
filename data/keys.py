import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Keys(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'keys'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    for_who = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    key_available = sqlalchemy.Column(sqlalchemy.String, nullable=True)