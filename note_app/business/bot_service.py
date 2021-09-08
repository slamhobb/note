import inject

from note_app.domain.user import User
from note_app.domain.note import Note
from note_app.business.user_service import UserService
from note_app.business.note_service import NoteService
from note_app.business.auth_service import AuthService


class BotService:
    user_service = inject.attr(UserService)
    note_service = inject.attr(NoteService)
    auth_service = inject.attr(AuthService)

    def handle_message(self, user_id: str, message: str) -> str:
        if message.startswith('/'):
            return self._handle_service_message(user_id, message)
        else:
            return self._handle_note_message(user_id, message)

    def _handle_service_message(self, user_id: str, message: str) -> str:
        message = message.lower().strip()

        if message.startswith('/help'):
            commands = [
                'Просмотр заметок по ссылке https://badb.fun/note\n'
                '/help помощь',
                '/id получение идентификатора пользователя viber',
                '/user получение информации о пользователе',
                '/reg {login} регистрация пользователя с выбранным логином',
                '/code сгенерировать код для аутентификации'
            ]

            return '\n'.join(commands)

        if message.startswith('/id'):
            return f'Id: {user_id}'

        if message.startswith('/user'):
            return self._handle_get_user_data(user_id)

        if message.startswith('/reg'):
            return self._handle_reg_user(user_id, message)

        if message.startswith('/code'):
            return self._handle_create_code(user_id)

        return 'Не поддерживаемая команда'

    def _handle_get_user_data(self, viber_id: str) -> str:
        user = self.user_service.get_by_viber_id(viber_id)
        if user is None:
            return 'Пользователь не зарегистрирован'

        return f'ViberId: {user.viber_id}\nLogin: {user.login}'

    def _handle_reg_user(self, viber_id: str, message: str) -> str:
        args = message.split(' ')
        if len(args) < 2:
            return 'Ошибка. Логин не передан'

        login = args[1]

        user = self.user_service.get_by_viber_id(viber_id)
        if user is not None:
            return 'Пользователь уже зарегистрирован'

        user = self.user_service.get_by_login(login)
        if user is not None:
            return 'Логин уже занят'

        user = User(id=0, login=login, viber_id=viber_id)
        self.user_service.insert(user)

        return 'Успешная регистрация'

    def _handle_create_code(self, viber_id: str) -> str:
        user = self.user_service.get_by_viber_id(viber_id)
        if user is None:
            return 'Пользователь не зарегистрирован'

        return self.auth_service.create_digit_code(user.id)

    def _handle_note_message(self, viber_id: str, message: str) -> str:
        user = self.user_service.get_by_viber_id(viber_id)
        if user is None:
            return 'Нужно зрегистрировать пользователя'

        note = Note(0, user.id, message, 1)
        self.note_service.save(note)

        return 'Ок'
