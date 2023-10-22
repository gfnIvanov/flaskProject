import logging
from typing import Union
import flask_login
from app import db
from app import models
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError, NoResultFound


logger = logging.getLogger(__name__)

std_return = Union[SQLAlchemyError, None]


def add_user(user_data: models.Users) -> Union[models.Users, std_return]:
    user = models.Users()

    user.username = user_data["username"]
    user.password = generate_password_hash(user_data["password"])
    user.firstname = user_data["firstname"]
    user.lastname = user_data["lastname"]

    try:
        db.session.add(user)
        db.session.commit()
        return get_user_with_username(user_data["username"])
    except SQLAlchemyError as err:
        db.session.rollback()
        logger.error(err)
        return err


def add_post(post_data: models.Posts) -> std_return:
    post = models.Posts

    post.title = post_data.title
    post.body = post_data.body
    post.author = flask_login.current_user
    post.tags = post_data.tags

    try:
        db.session.add(post)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        logger.error(err)
        return err


def get_user_with_username(username: str) -> Union[models.Users, std_return]:
    try:
        return db.session.execute(
            db.select(models.Users).filter_by(username=username)
        ).scalar_one()
    except NoResultFound:
        return None
    except SQLAlchemyError as err:
        logger.error(err)
        return err

