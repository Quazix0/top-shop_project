from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError
from flask_wtf import FlaskForm, Form
from .models import User
#подробнее в документации flask.palletsprojects.com/en/1.1.x/patterns/wtforms/
class RegistrationForm(FlaskForm):
    name = StringField('Имя', [validators.Length(min=2, max=40)])
    username = StringField('Псевдоним', [validators.Length(min=2, max=40)])
    email = StringField('Электронная почта', [validators.Length(min=2, max=40)])
    password = PasswordField('Пароль', [validators.DataRequired(),validators.EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Подтвердите пароль')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Псевдоним занят.')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Электронная почта занята.')



class LoginForm(FlaskForm):
    email = StringField('Электронная почта', [validators.Length(min=2, max=40)])
    password = PasswordField('Пароль', [validators.DataRequired()])
