import inject

from note_app.dao.birthday.birthday_dao import BirthdayDao
from note_app.domain.birthday import Birthday


class BirthdayService:
    birthday_dao = inject.attr(BirthdayDao)

    def get_list(self, user_id: int) -> [Birthday]:
        return self.birthday_dao.get_list(user_id)

    def get_by_id(self, user_id: int, id: int) -> Birthday:
        return self.birthday_dao.get_by_id(user_id, id)

    def save(self, birthday: Birthday) -> int:
        if birthday.id == 0:
            return self.birthday_dao.insert(birthday)
        else:
            return self.birthday_dao.update(birthday)

    def delete(self, user_id: int, id: int):
        return self.birthday_dao.delete(user_id, id)
