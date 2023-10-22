from app import app
from flask import render_template
from queries import *


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
    post_data = {}
    result = add_post(post_data)
    if isinstance(result, Exception):
        error = result
        return error
