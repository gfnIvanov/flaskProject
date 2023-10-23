from app import app
from flask import render_template, request, redirect, url_for
from flask_login import login_user
from .queries import *
from .forms import *


@app.route("/")
def index():
    return render_template("index.html")


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
    return render_template("index.html", form=form, show_register=True)


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
    return render_template("index.html", form=form, show_login=True)


@app.route("/post/<int:id>/watch", methods=["GET"])
def watch_post():
    post = get_post_by_id("")  # TODO разобраться как получать id поста
    if isinstance(post, Exception):
        flash("Ошибка при обращении к базе данных", "error")
        return redirect(url_for("index"))
    if post is None:
        flash("Пост не найден", "error")
        return redirect(url_for("index"))


@app.route("/post/add", methods=["GET", "POST"])
def add_new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = add_post(form.data)

        if isinstance(post, Exception):
            flash("Ошибка при обращении к базе данных", "error")
            return redirect(url_for("add_new_post"))
    return render_template("add_post.html", form=form)


@app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id: int):
    form = PostForm()
    if form.validate_on_submit():
        post = edit_post(post_id)
        if isinstance(post, Exception):
            flash("Ошибка при обращении к базе данных", "error")
            return redirect(url_for("edit_post"))
    return render_template("edit_post.html", form=form)


@app.route("/post/<int:post_id>/delete", methods=["POST"])
def remove_post(post_id: int):
    post = delete_post(post_id) # TODO разобраться от куда брать post_id
    if isinstance(post, Exception):
        flash("Ошибка при обращении к базе данных", "error")
        return redirect(url_for("index"))
    return render_template("edit_post.html")
