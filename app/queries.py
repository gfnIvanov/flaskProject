import logging
from typing import Union

import flask_login

from app import db
from app import models
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

logger = logging.getLogger(__name__)


def add_user(user_data: models.Users) -> Union[SQLAlchemyError, None]:
    user = models.Users()

    user.username = user_data.username
    user.password = generate_password_hash(user_data.password)
    user.firstname = user_data.firstname
    user.lastname = user_data.lastname

    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        logger.error(err)
        return err


def add_post(post_data: models.Posts) -> Union[SQLAlchemyError, None]:
    post = models.Posts

    post.title = post_data.title
    post.body = post_data.body
    post.author = flask_login.current_user
    post.tags = post_data.tags

    try:
        db.session.add(post)
        db.session.commit()
    except SQLAlchemyError as err:
        logger.error(err)
        return err


def get_user_with_username(username: str):
    try:
        return db.session.execute(
            db.select(models.Users).filter_by(username=username)
        ).scalar_one()
    except NoResultFound:
        return None
    except SQLAlchemyError as err:
        logger.error(err)
        return err

