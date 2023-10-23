from app import app
from app import db
from app import models
from app import login


@app.cli.command("create_tables")
def create_tables():
    with app.app_context():
        db.create_all()
        print(">>> Tables successfully created: " + ", ".join(db.metadata.tables.keys()))


@login.user_loader
def load_user(id):
    return models.Users.query.get(int(id))
