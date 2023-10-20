import os
import environ
import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# get environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# logging configuration
logging.basicConfig(level = logging.DEBUG if env("MODE") == "dev" else logging.INFO,
                    filename = os.path.join(BASE_DIR, 'logs/app_log.log'),
                    filemode = "w",
                    format = "%(asctime)s - %(name)s[%(funcName)s(%(lineno)d)] - %(levelname)s - %(message)s")


# app configuration
class DevConfig():
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{env('DB_USER')}:{env('DB_PASSWORD')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
    SECRET_KEY = os.urandom(12).hex()
