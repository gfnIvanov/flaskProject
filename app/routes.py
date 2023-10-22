from app import app
from flask import render_template, request, redirect, url_for
from flask_login import login_user
from .queries import *
from .forms import *


@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = add_user(form.data)
        if isinstance(user, Exception) or user is None:
            flash("Ошибка при обращении к базе данных", "error")
            return redirect(url_for("register"))
        login_user(user)
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    user_data = {}
    result = add_user(user_data)
    if isinstance(result, Exception):
        error = result
    return error


@app.route("/post/add", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        post_data = PostForm(request.form)
        result = add_post(post_data)
        if isinstance(result, Exception):
            error = result
            return error
    return render_template("add_post.html")
