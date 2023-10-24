from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_wtf.file import FileField, FileAllowed
from .queries import get_user_by_username


class RequiredField(DataRequired):
    def __init__(self, message="Поле обязательно для заполнения"):
        self.message = message


def check_user_exist(form, field: str):
    user_exist = get_user_by_username(field.data)
    if isinstance(user_exist, Exception):
        flash("Ошибка при обращении к базе данных", "error")
    if user_exist:
        raise ValidationError("Пользователь с указанным логином уже есть в базе", "user_exist")


class RegistrationForm(FlaskForm):
    username = StringField("Введите логин", validators=[RequiredField(), check_user_exist])
    password = PasswordField("Введите пароль", validators=[RequiredField()])
    password_confirm = PasswordField("Повторите пароль",
                                     validators=[
                                        RequiredField(),
                                        EqualTo(fieldname="password", message="Пароли не совпадают")
                                    ])
    firstname = StringField("Введите имя", validators=[RequiredField()])
    lastname = StringField("Введите фамилию", validators=[RequiredField()])
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    username = StringField("Введите логин", validators=[RequiredField()])
    password = PasswordField("Введите пароль", validators=[RequiredField()])
    submit = SubmitField("Войти")


class PostForm(FlaskForm):
    title = StringField("Введите название", validators=[RequiredField()])
    body = TextAreaField("Введите текст", validators=[RequiredField()])
    tags = StringField("Введите теги")
    submit = SubmitField("Добавить пост")


class FileForm(FlaskForm):
    file = FileField(validators=[
        RequiredField(message="Требуется выбрать файл"),
        FileAllowed(['csv'], 'Принимаются только csv-файлы')
    ])
    submit = SubmitField("Отправить")

