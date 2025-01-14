"""configure the tax app."""

from os import environ

from dotenv import load_dotenv

load_dotenv()


class ConfigMeta(type):
    """configuration metaclass for tax app."""

    def __new__(mcs, name, bases, namespace):
        """Define required class variables on Config class."""
        cls = super().__new__(mcs, name, bases, namespace)
        for var_name in cls.required_env_vars:
            value = environ.get(var_name)
            if not value:
                raise Exception(
                    "set " + var_name + ", for example in .env file"
                )
            setattr(cls, var_name, value)

        cls.SQLALCHEMY_DATABASE_URI = (
            cls.DB_DIALECT
            + "://"
            + cls.DB_USER
            + ":"
            + cls.DB_PASSWORD
            + "@"
            + cls.DB_HOST
            + ":"
            + cls.DB_PORT
            + "/"
            + cls.DB_NAME
        )

        cls.SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "options": "-csearch_path=" + cls.DB_SCHEMA
            }
        }

        return cls


class Config(metaclass=ConfigMeta):
    """gather together the settings for the tax flask app."""

    required_env_vars = [
        "DB_DIALECT",
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_SCHEMA",
        "SECRET_KEY",
    ]

    CHECK_EMAIL_DELIVERABILITY = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
