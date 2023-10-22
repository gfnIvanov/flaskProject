from app import app
from flask import render_template, request, redirect, flash
from .queries import *
from .models import Posts
from .forms import *


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


@app.route('/post/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        post_data = PostForm(request.form)
        result = add_post(post_data)
        if isinstance(result, Exception):
            error = result
            return error
    return render_template('add_post.html')
