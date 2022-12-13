from typing import Callable

import inject

from note_app.domain.user import User
from note_app.domain.note import Note
from note_app.domain.messanger_type import MessangerType
from note_app.business.auth_service import AuthService
from note_app.business.user_service import UserService
from note_app.business.note_service import NoteService
from note_app.business.youtube_dl_service import YoutubeDlService


class BotService:
    user_service = inject.attr(UserService)
    note_service = inject.attr(NoteService)
    auth_service = inject.attr(AuthService)
    youtube_dl_service = inject.attr(YoutubeDlService)

    def handle_message(
        self,
        msgr_id: str,
        msgr_type: MessangerType,
        message: str,
        send_message_fn: Callable[[str], None]
    ) -> str:
        if message.startswith('/y'):
            return self._handle_youtube_dl_message(msgr_id, msgr_type, message, send_message_fn)
        if message.startswith('/'):
            return self._handle_service_message(msgr_id, msgr_type, message)
        else:
            return self._handle_note_message(msgr_id, msgr_type, message)

    def _handle_service_message(self, msgr_id: str, msgr_type: MessangerType, message: str) -> str:
        user = self.user_service.get_by_messanger_id(msgr_id, msgr_type)

        message = message.lower().strip()

        if message.startswith('/help'):
            commands = [
                'Просмотр заметок по ссылке https://badb.site/note\n'
                '/help помощь',
                '/id получение идентификатора пользователя',
                '/user получение информации о пользователе',
                '/reg {login} регистрация пользователя с выбранным логином',
                '/code сгенерировать код для аутентификации',
                '/attach {login} {code} подключиться к существующему аккаунту',
                '/yd {url} скачать видео с youtube',
                '/yda {url} скачать только аудио с youtube'
            ]

            return '\n'.join(commands)

        if message.startswith('/id'):
            return f'Id: {msgr_id}'

        if message.startswith('/user'):
            return self._handle_get_user_data(user)

        if message.startswith('/reg'):
            return self._handle_reg_user(msgr_id, msgr_type, message)

        if message.startswith('/code'):
            return self._handle_create_code(user)

        if message.startswith('/attach'):
            return self._handle_attach(user, msgr_id, msgr_type, message)

        return 'Не поддерживаемая команда'

    def _handle_get_user_data(self, user: User) -> str:
        if user is None:
            return 'Пользователь не зарегистрирован'

        return f'ViberId: {user.viber_id}\nTelegramId: {user.telegram_id}\nLogin: {user.login}'

    def _handle_reg_user(self, msgr_id: str, msgr_type: MessangerType, message: str) -> str:
        args = message.split(' ')
        if len(args) < 2:
            return 'Ошибка. Логин не передан'

        login = args[1]

        user = self.user_service.get_by_messanger_id(msgr_id, msgr_type)
        if user is not None:
            return 'Пользователь уже зарегистрирован'

        user = self.user_service.get_by_login(login)
        if user is not None:
            return 'Логин уже занят'

        user = User(id=0, login=login, viber_id=None, telegram_id=None)

        if msgr_type == MessangerType.Viber:
            user.viber_id = msgr_id
        elif msgr_type == MessangerType.Telegram:
            user.telegram_id = msgr_id
        else:
            return 'Не поддерживаемый мессенджер'

        self.user_service.insert(user)

        return 'Успешная регистрация'

    def _handle_create_code(self, user: User) -> str:
        if user is None:
            return 'Пользователь не зарегистрирован'

        return self.auth_service.create_digit_code(user.id)

    def _handle_attach(self, user: User, msgr_id: str, msgr_type: MessangerType, message: str) -> str:
        args = message.split(' ')
        if len(args) < 3:
            return 'Ошибка. Логин и код не переданы'

        login = args[1]
        digit_code = args[2]

        if user is not None:
            return 'Пользователь уже привязан'

        user = self.auth_service.get_user_by_digit_code(login, digit_code)
        if user is None:
            return 'Не верный логин или код'

        self.user_service.attach(user, msgr_id, msgr_type)
        return 'Пользователь успешно привязан'

    def _handle_note_message(self, msgr_id: str, msgr_type: MessangerType, message: str) -> str:
        user = self.user_service.get_by_messanger_id(msgr_id, msgr_type)
        if user is None:
            return 'Нужно зарегистрировать пользователя'

        note = Note(0, user.id, message, 1)
        self.note_service.save(note)

        return 'Ок'

    def _handle_youtube_dl_message(
        self,
        msgr_id: str,
        msgr_type: MessangerType,
        message: str,
        send_message_fn: Callable[[str], None]
    ) -> str:
        user = self.user_service.get_by_messanger_id(msgr_id, msgr_type)
        if user is None:
            return 'Нужно зарегистрировать пользователя'

        args = message.split(' ')
        if len(args) < 2:
            return 'Ошибка. Url не передан'

        command = args[0]
        url = args[1]

        if command == '/yd':
            return self.youtube_dl_service.download(url, False, send_message_fn)

        if command == '/yda':
            return self.youtube_dl_service.download(url, True, send_message_fn)

        return 'Не поддерживаемая команда'
