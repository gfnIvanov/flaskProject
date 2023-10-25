import logging
from typing import Union
from flask_login import current_user
from app import db
from app import models
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

logger = logging.getLogger(__name__)

std_return = Union[SQLAlchemyError, None]


def add_user(user_data: models.Users) -> Union[models.Users, std_return]:
    user = models.Users()

    user.username = user_data["username"]
    user.set_password(user_data["password"])
    user.firstname = user_data["firstname"]
    user.lastname = user_data["lastname"]

    try:
        db.session.add(user)
        db.session.commit()
        return get_user_by_username(user_data["username"])
    except SQLAlchemyError as err:
        db.session.rollback()
        logger.error(err)
        return err


def add_post(post_data: models.Posts) -> std_return:
    post = models.Posts()

    post.title = post_data["title"]
    post.body = post_data["body"]
    post.author = current_user.get_id()
    post.tags = post_data["tags"]

    try:
        db.session.add(post)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        logger.error(err)
        return err


def edit_post(post_data: models.Posts, id: int) -> std_return:
    try:
        post = get_post_by_id(str(id))
        if post is None:
            raise SQLAlchemyError("Статья с указанным идентификатором не найдена")
        post.title = post_data["title"]
        post.body = post_data["body"]
        post.author = current_user.get_id()
        post.tags = post_data["tags"]

        db.session.add(post)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        logger.error(err)
        return err


def delete_post(post_data: models.Posts) -> std_return:
    try:
        post = get_post_by_id(post_data["id"])
        if post is None:
            raise SQLAlchemyError("Статья с указанным идентификатором не найдена")
        db.session.delete(post)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        logger.error(err)
        return err


def get_all_posts():
    try:
        return db.paginate(db.select(models.Posts).order_by(models.Posts.date_create))
    except NoResultFound:
        return None
    except SQLAlchemyError as err:
        logger.error(err)
        return err


def get_post_by_id(post_id: str):
    try:
        return db.session.execute(
            db.select(models.Posts).filter_by(id=post_id)
        ).scalar_one()
    except NoResultFound:
        return None
    except SQLAlchemyError as err:
        logger.error(err)
        return err


def get_user_by_username(username: str) -> Union[models.Users, std_return]:
    try:
        return db.session.execute(
            db.select(models.Users).filter_by(username=username)
        ).scalar_one()
    except NoResultFound:
        return None
    except SQLAlchemyError as err:
        logger.error(err)
        return err


def get_user_by_id(id: int) -> Union[models.Users, std_return]:
    try:
        return db.session.execute(
            db.select(models.Users).filter_by(id=id)
        ).scalar_one()
    except NoResultFound:
        return None
    except SQLAlchemyError as err:
        logger.error(err)
        return err
