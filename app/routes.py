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
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if isinstance(user, Exception):
            flash("Ошибка при обращении к базе данных", "error")
            return redirect(url_for("login"))
        if user is None or not user.check_password(form.password.data):
            flash("Логин или пароль указаны некорректно", "error")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/post/add", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        post_data = PostForm(request.form)
        result = add_post(post_data)
        if isinstance(result, Exception):
            error = result
            return error
    return render_template("add_post.html")
