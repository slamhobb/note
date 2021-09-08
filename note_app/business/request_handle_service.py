import inject

from viberbot.api.viber_requests import ViberRequest, ViberMessageRequest
from viberbot.api.messages import TextMessage

from note_app.business.bot_service import BotService


class RequestHandleService:
    bot_service = inject.attr(BotService)

    def handle_request(self, viber_request: ViberRequest) -> str:
        if isinstance(viber_request, ViberMessageRequest):
            message = viber_request.message

            if isinstance(message, TextMessage):
                return self.bot_service.handle_message(
                    viber_request.sender.id,
                    viber_request.message.text)

        return None
