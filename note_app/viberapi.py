from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

from note_app import config

viber = Api(BotConfiguration(
    name=config.BOT_NAME,
    avatar='http://site.com/avatar.jpg',
    auth_token=config.BOT_AUTH_TOKEN
))
