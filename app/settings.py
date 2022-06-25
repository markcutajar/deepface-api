"""File containing settings for the app."""
import os
from dotenv import dotenv_values


APP_ROOT = os.path.join(os.path.dirname(__file__), "..")  # refers to application_top
dotenv_path = os.path.join(APP_ROOT, ".env")
env = dotenv_values(dotenv_path)


def check_bool_true(value):
    if isinstance(value, bool):
        return value
    return value in ("true", "True", "yes")


class Config(object):
    RAW = env


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
    ENV = "production"