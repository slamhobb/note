import inject

from typing import List

from note_app.dao.user.user_dao import UserDao
from note_app.domain.user import User


class UserService:
    user_dao = inject.attr(UserDao)

    def get_all(self) -> List[User]:
        return self.user_dao.get_all()

    def get_by_viber_id(self, viber_id: str) -> User:
        return self.user_dao.get_by_viber_id(viber_id)

    def get_by_login(self, login: str) -> User:
        return self.user_dao.get_by_login(login)

    def insert(self, user: User) -> int:
        return self.user_dao.insert(user)
