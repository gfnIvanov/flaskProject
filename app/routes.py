import os
from typing import Dict, List
from app import app
from flask_login import current_user
from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user
from .config import BASE_DIR
from .ML import model
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
    return render_template("index.html",
                           form=form,
                           show_register=True)


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
    return render_template("index.html",
                           form=form,
                           show_login=True)


@app.route("/posts", methods=["GET"])
@login_required
def get_posts():
    posts = get_all_posts()
    return render_template("posts.html",
                           user=_get_user_data(),
                           posts=posts,
                           active_page="get_posts")


@app.route("/post/<int:id>/watch", methods=["GET"])
@login_required
def watch_post(id: int):
    post = get_post_by_id(str(id))
    user = get_user_by_id(post.author)
    if isinstance(post, Exception):
        flash("Ошибка при обращении к базе данных", "error")
        return redirect(url_for("index"))
    if post is None:
        flash("Пост не найден", "error")
        return redirect(url_for("index"))
    return render_template("watch_post.html",
                           post=post,
                           user=_get_user_data(),
                           active_page="watch_post",
                           author=user)


@app.route("/post/add", methods=["GET", "POST"])
@login_required
def add_new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = add_post(form.data)
        if isinstance(post, Exception):
            flash("Ошибка при обращении к базе данных", "error")
            return redirect(url_for("add_new_post"))
    return render_template("add_post.html",
                           form=form,
                           user=_get_user_data(),
                           active_page="")


@app.route("/post/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_posts(id: int):
    form = PostForm()
    post_to_edit = get_post_by_id(str(id))
    if form.validate_on_submit():
        edited_post = edit_post(form.data, id)
        if isinstance(edited_post, Exception):
            flash("Ошибка при обращении к базе данных", "error")
            return redirect(url_for("edit_post"))
    return render_template("edit_post.html",
                           form=form,
                           user=_get_user_data(),
                           post=post_to_edit,
                           active_page="edit_posts")


@app.route("/post/<int:id>/delete", methods=["POST"])
@login_required
def remove_post(id: int):
    post_to_delete = get_post_by_id(str(id))
    deleted_post = delete_post(post_to_delete)
    if isinstance(deleted_post, Exception):
        flash("Ошибка при обращении к базе данных", "error")
        return redirect(url_for("index"))
    return render_template("edit_post.html",
                           user=_get_user_data())


@app.route("/practice", methods=["GET", "POST"])
@login_required
def practice():
    form = FileForm()
    model_exist = False
    logs = []
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(BASE_DIR, "temp/data.csv"))
        return redirect(url_for("train_model"))
    if os.path.exists(os.path.join(BASE_DIR, 'app/ML/log.txt')):
        model_exist = True
        logs = _get_logs(full=False)
    return render_template("practice.html",
                           form=form,
                           active_page="practice",
                           user=_get_user_data(),
                           model_exist=model_exist,
                           logs=logs)


@app.route("/train-model", methods=["GET"])
@login_required
def train_model():
    model.train()
    logs = ','.join(_get_logs())
    return render_template("train_model.html",
                           active_page="train_model",
                           user=_get_user_data(),
                           logs=logs)


@app.route("/use-model", methods=["GET"])
@login_required
def use_model():
    target, test_data, prediction = model.use()
    return render_template("use_model.html",
                           active_page="use_model",
                           user=_get_user_data(),
                           target=target,
                           test_data=test_data,
                           prediction=prediction)


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


def _get_logs(full: bool = True) -> List[str]:
    logs = []
    with open(os.path.join(BASE_DIR, 'app/ML/log.txt'), 'r') as log_file:
        if full:
            lines = log_file.readlines()
        else:
            lines = log_file.readlines()[:-1]
        for str in lines:
            logs.append(str)
    return logs
