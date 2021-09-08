from flask import session
from note_app import config


def set_token(token, permanent):
    session[config.AUTH_TOKEN_NAME] = token
    session.permanent = permanent


def remove_token():
    session.pop(config.AUTH_TOKEN_NAME, None)


def get_token():
    if config.AUTH_TOKEN_NAME in session:
        return session[config.AUTH_TOKEN_NAME]
    return None
