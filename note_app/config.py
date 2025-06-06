from os import path
from base64 import b64decode
from json import load

_basedir = path.abspath(path.dirname(__file__))

_config_path = path.join(_basedir, '..', '..', 'note-cfg', 'config.json')


def _get_config():
    with open(_config_path, 'r') as f:
        return load(f)


config = _get_config()

VIBER_BOT_NAME = config['VIBER_BOT_NAME']
VIBER_BOT_AUTH_TOKEN = config['VIBER_BOT_AUTH_TOKEN']
TELEGRAM_BOT_AUTH_TOKEN = config['TELEGRAM_BOT_AUTH_TOKEN']
DATA_BASE_CONNECTION_STRING = config['DATA_BASE_CONNECTION_STRING']
AUTH_TOKEN_NAME = config['AUTH_TOKEN_NAME']
SESSION_COOKIE_NAME = 'note-session'
# generate SECRET_KEY
# import os;import base64;base64.b64encode(os.urandom(20)).decode()
SECRET_KEY = b64decode(config["SECRET_KEY_BASE64"].encode())
SERVICE_LOGIN = config['SERVICE_LOGIN']
FILE_PATH = config['FILE_PATH']
WEB_FILE_PATH = config['WEB_FILE_PATH']
SITE_PATH = config['SITE_PATH']
