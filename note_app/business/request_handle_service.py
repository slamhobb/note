import inject

from viberbot.api.viber_requests.viber_request import ViberRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.messages import TextMessage

from note_app.domain.messanger_type import MessangerType
from note_app.business.bot_service import BotService


class RequestHandleService:
    bot_service = inject.attr(BotService)

    def handle_viber_request(self, viber_request: ViberRequest) -> str:
        if isinstance(viber_request, ViberMessageRequest):
            message = viber_request.message

            if isinstance(message, TextMessage):
                return self.bot_service.handle_message(
                    viber_request.sender.id,
                    MessangerType.Viber,
                    viber_request.message.text)

        return None

    def handle_telegram_request(self, sender_id: str, message: str) -> str:
        if len(message) > 0:
            return self.bot_service.handle_message(
                sender_id,
                MessangerType.Telegram,
                message)

        return None
