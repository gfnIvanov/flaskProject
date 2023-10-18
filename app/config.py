import os
import environ
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# get environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class DevConfig():
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{env('DB_USER')}:{env('DB_PASSWORD')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"