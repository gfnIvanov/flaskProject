from app import app
from flask import render_template, request, redirect
from .queries import *
from .models import Posts
from .forms import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/register', methods=['POST'])
def register():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_data = {}
    result = add_user(user_data)
    if isinstance(result, Exception):
        error = result
        return


@app.route('/post/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        post_data = PostForm(request.form)
        result = add_post(post_data)
        if isinstance(result, Exception):
            error = result
            return error
    return render_template('add_post.html')
