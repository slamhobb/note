from os import path
from base64 import b64decode
from json import load

_basedir = path.abspath(path.dirname(__file__))

_config_path = path.join(_basedir, '..', '..', 'note-cfg', 'config.json')


def _get_config():
    with open(_config_path, 'r') as f:
        return load(f)


config = _get_config()

BOT_NAME = config['BOT_NAME']
BOT_AUTH_TOKEN = config['BOT_AUTH_TOKEN']
DATA_BASE_CONNECTION_STRING = config['DATA_BASE_CONNECTION_STRING']
AUTH_TOKEN_NAME = config['AUTH_TOKEN_NAME']
SESSION_COOKIE_NAME = 'note-session'
# generate SECRET_KEY
# import os;import base64;base64.b64encode(os.urandom(20)).decode()
SECRET_KEY = b64decode(config["SECRET_KEY_BASE64"].encode())
