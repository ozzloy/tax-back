from dotenv import load_dotenv
from os import environ


load_dotenv()


class Config:
    DB_DIALECT = environ.get("DB_DIALECT")
    if not DB_DIALECT:
        raise Exception("set DB_DIALECT, for example in .env file")

    DB_USER = environ.get("DB_USER")
    if not DB_USER:
        raise Exception("set DB_USER, for example in .env file")

    DB_PASSWORD = environ.get("DB_PASSWORD")
    if not DB_PASSWORD:
        raise Exception("set DB_PASSWORD, for example in .env file")

    DB_HOST = environ.get("DB_HOST")
    if not DB_HOST:
        raise Exception("set DB_HOST, for example in .env file")

    DB_PORT = environ.get("DB_PORT")
    if not DB_PORT:
        raise Exception("set DB_PORT, for example in .env file")

    DB_NAME = environ.get("DB_NAME")
    if not DB_NAME:
        raise Exception("set DB_NAME, for example in .env file")

    DB_SCHEMA = environ.get("DB_SCHEMA")
    if not DB_SCHEMA:
        raise Exception("set DB_SCHEMA, for example in .env file")

    SECRET_KEY = environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise Exception("set SECRET_KEY, for example in .env file")

    SQLALCHEMY_DATABASE_URI = (
        DB_DIALECT
        + "://"
        + DB_USER
        + ":"
        + DB_PASSWORD
        + "@"
        + DB_HOST
        + ":"
        + DB_PORT
        + "/"
        + DB_NAME
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"options": "-csearch_path=" + DB_SCHEMA}
    }

    CHECK_EMAIL_DELIVERABILITY = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
