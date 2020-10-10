from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class RequestForm(FlaskForm): 
    company = StringField('Название компании',validators=[DataRequired()])
    submit = SubmitField('Отправить')