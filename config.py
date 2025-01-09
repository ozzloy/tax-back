from os import environ


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise Exception(
            "set SQLALCHEMY_DATABASE_URI, for example in .env file"
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise Exception("set SECRET_KEY, for example in .env file")
    CHECK_EMAIL_DELIVERABILITY = True
