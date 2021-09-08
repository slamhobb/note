import inject

from flask import Blueprint, request, Response

from viberbot.api.messages import TextMessage

from note_app.viberapi import viber
from note_app.business.request_handle_service import RequestHandleService

mod = Blueprint('bot', __name__)

request_handle_service = inject.instance(RequestHandleService)


@mod.route('', methods=['POST'])
def incoming():
    if not viber.verify_signature(
        request.get_data(),
        request.headers['X-Viber-Content-Signature']
    ):
        return Response(status=403)

    viber_request = viber.parse_request(request.get_data())

    message = request_handle_service.handle_request(viber_request)
    if message is not None:
        viber.send_messages(viber_request.sender.id, [
            TextMessage(text=message)
        ])

    return Response(status=200)
