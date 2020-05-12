from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from .model import Register




class CustomerRegisterForm(FlaskForm):
    name = StringField('Имя: ')
    username = StringField('Псевдоним: ', [validators.DataRequired()])
    email = StringField('Электронная почта: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Пароль: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Пароли должны совпадать! ')])
    confirm = PasswordField('Подтвердите пароль: ', [validators.DataRequired()])
    country = StringField('Страна: ', [validators.DataRequired()])
    city = StringField('Город: ', [validators.DataRequired()])
    contact = StringField('Контакты: ', [validators.DataRequired()])
    address = StringField('Адрес: ', [validators.DataRequired()])
    zipcode = StringField('Почтовый индекс: ', [validators.DataRequired()])

    profile = FileField('Профиль', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Только изображение пожалуйста')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("Этот псевдоним уже занят!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("Эта электронная почта уже занята!")

    


class CustomerLoginFrom(FlaskForm):
    email = StringField('Электронная почта: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Пароль: ', [validators.DataRequired()])

   




   

 

    

     

   


    

