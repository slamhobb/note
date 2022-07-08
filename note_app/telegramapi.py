import requests

from note_app import config


def set_web_hook(url: str):
    pass


def send_message(chat_id: str, text: str):
    url = f'https://api.telegram.org/bot{config.TELEGRAM_BOT_AUTH_TOKEN}/sendMessage'
    payload = dict(chat_id=chat_id, text=text)

    requests.post(url, payload)

