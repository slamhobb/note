from .dependency_injection import configure_inject
configure_inject()

from flask import Flask

from note_app import config
from note_app.views.bot import mod as bot
from note_app.views.auth import mod as auth
from note_app.views.redirect import mod as redirect
from note_app.views.note import mod as note
from note_app.views.note_type import mod as note_type


PREFIX = '/note'


def create_app():
    app = Flask(__name__)

    app.secret_key = config.SECRET_KEY

    app.register_blueprint(bot, url_prefix=f'{PREFIX}/viber-bot')
    app.register_blueprint(auth, url_prefix=f'{PREFIX}/auth')
    app.register_blueprint(redirect, url_prefix=f'{PREFIX}/redirect')
    app.register_blueprint(note, url_prefix=f'{PREFIX}')
    app.register_blueprint(note_type, url_prefix=f'{PREFIX}/note-type')

    return app
