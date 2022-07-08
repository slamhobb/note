from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

from note_app import config

viber = Api(BotConfiguration(
    name=config.VIBER_BOT_NAME,
    avatar='http://site.com/avatar.jpg',
    auth_token=config.VIBER_BOT_AUTH_TOKEN
))
