from app import db
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(500), nullable=False)
    firstname: Mapped[str] = mapped_column(db.String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<Users(id={self.id}, username={self.username})>"

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class Posts(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    body: Mapped[str] = mapped_column(db.Text, nullable=False)
    author: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("users.id"))
    date_create: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    tags: Mapped[str] = mapped_column(db.String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<Posts(id={self.id}, title={self.title})>"
