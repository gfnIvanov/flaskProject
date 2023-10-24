import os
from typing import Dict
from app import app
from flask_login import current_user
from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user
from .config import BASE_DIR
from .queries import *
from .forms import *


@app.route("/")
def index():
    return render_template("index.html",
                           active_page='index',
                           user=_get_user_data())


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


@app.route("/posts", methods=["GET"])
def posts():
    return redirect(url_for("index"))


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


@app.route("/practice", methods=["GET", "POST"])
@login_required
def practice():
    form = FileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(BASE_DIR, 'temp/data.csv'))
        return redirect(url_for("practice"))
    return render_template("practice.html",
                           form=form,
                           active_page='practice',
                           user=_get_user_data())


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def _get_user_data() -> Dict[str, str]:
    firstname = None
    lastname = None
    user = get_user_by_id(current_user.get_id())
    if user is not None and not isinstance(user, Exception):
        firstname = user.firstname
        lastname = user.lastname[0] + '.'
    return {"firstname": firstname, "lastname": lastname}