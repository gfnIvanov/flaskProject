from app import app
from flask import request, render_template, flash
from .forms import RegistrationForm
from .queries import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username = form.username.data
    user_exist = get_user_with_username(username)
    if isinstance(user_exist, Exception):
        return render_template('register.html', form=form)
    if user_exist is not None:
        flash('Пользователь с указанным логином уже есть в базе', 'user_exist')
    if form.validate_on_submit():
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_data = {}
    result = add_user(user_data)
    if isinstance(result, Exception):
        error = result
        return error