import inject

from flask import Blueprint, request, Response

from viberbot.api.messages import TextMessage

from note_app.viberapi import viber
from note_app.telegramapi import send_message
from note_app.business.request_handle_service import RequestHandleService

mod = Blueprint('bot', __name__)

request_handle_service = inject.instance(RequestHandleService)


@mod.route('/viber', methods=['POST'])
def incoming_viber():
    if not viber.verify_signature(
        request.get_data(),
        request.headers['X-Viber-Content-Signature']
    ):
        return Response(status=403)

    viber_request = viber.parse_request(request.get_data())

    def send_message_fn(message: str):
        viber.send_messages(viber_request.sender.id, [
            TextMessage(text=message)
        ])

    response_message = request_handle_service.handle_viber_request(viber_request, send_message_fn)
    if response_message is not None:
        viber.send_messages(viber_request.sender.id, [
            TextMessage(text=response_message)
        ])

    return Response(status=200)


@mod.route('/telegram', methods=['POST'])
def incoming_telegram():
    req = request.get_json()

    if 'message' not in req:
        return Response(status=200)

    chat_id = req['message']['chat']['id']
    request_message = req['message']['text']

    def send_message_fn(message: str):
        send_message(chat_id, message)

    response_message = request_handle_service.handle_telegram_request(chat_id, request_message, send_message_fn)
    if response_message is not None:
        send_message(chat_id, response_message)

    return Response(status=200)
