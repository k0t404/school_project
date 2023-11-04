from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class LessonForm(FlaskForm):
    lesson_pos = StringField('Название', validators=[DataRequired()])
    lesson = TextAreaField("Содержание")
    cabinet = BooleanField("Личное")
    class_letter = IntegerField('Цена')
    day = StringField('Ссылка')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')