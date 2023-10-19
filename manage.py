from app import app
from app import db


@app.cli.command("create_tables")
def create_tables():
    with app.app_context():
        db.create_all()
        print(">>> Tables successfully created: " + ", ".join(db.metadata.tables.keys()))
