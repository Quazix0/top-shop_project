from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf.file import FileField,FileRequired,FileAllowed

class Addproducts(Form):
    name = StringField('Название', [validators.DataRequired()])
    price = FloatField('Цена', [validators.DataRequired()])
    discount = IntegerField('Скидка', default=0)
    stock = IntegerField('Наличие', [validators.DataRequired()])
    colors = StringField('Цвета', [validators.DataRequired()])
    description = TextAreaField('Описание', [validators.DataRequired()])

    image_1 = FileField('Картинка 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg']), 'только катинки'])
    image_2 = FileField('Картинка 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg']), 'только катинки'])
    image_3 = FileField('Картинка 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg']), 'только катинки'])
