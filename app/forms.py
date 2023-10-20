from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app import models


class RequiredField(DataRequired):
    message = 'Поле обязательно для заполнения'


class EqualFields(EqualTo):
    message = 'Пароли не совпадают'


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[RequiredField()])
    password = PasswordField('Password', validators=[RequiredField()])
    password_confirm = PasswordField('Password confirm',
                                     validators=[RequiredField(), EqualFields('password')])
    firstname = StringField('Firstname', validators=[RequiredField()])
    lastname = StringField('Lastname', validators=[RequiredField()])
