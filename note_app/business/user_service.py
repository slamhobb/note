import inject

from note_app.dao.user.user_dao import UserDao
from note_app.domain.user import User
from note_app.domain.messanger_type import MessangerType


class UserService:
    user_dao = inject.attr(UserDao)

    def get_all(self) -> list[User]:
        return self.user_dao.get_all()

    def get_by_login(self, login: str) -> User:
        return self.user_dao.get_by_login(login)

    def get_by_messanger_id(self, messanger_id: str, messanger_type: MessangerType) -> User | None:
        if messanger_type == MessangerType.Viber:
            return self.user_dao.get_by_viber_id(messanger_id)

        if messanger_type == MessangerType.Telegram:
            return self.user_dao.get_by_telegram_id(messanger_id)

        return None

    def insert(self, user: User) -> int:
        return self.user_dao.insert(user)

    def attach(self, user: User, msgr_id: str, msgr_type: MessangerType):
        if msgr_type == MessangerType.Viber:
            user.viber_id = msgr_id
            self.user_dao.update(user)

        if msgr_type == MessangerType.Telegram:
            user.telegram_id = msgr_id
            self.user_dao.update(user)
