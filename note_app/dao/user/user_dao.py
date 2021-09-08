from typing import List

from note_app.dao.base_dao import BaseDao
from note_app.domain.user import User


class UserDao(BaseDao):
    def __init__(self):
        super().__init__('/user/sql/')

    def get_all(self) -> List[User]:
        sql = self.get_sql('get_all.sql')
        return self.query_all(User, sql, dict())

    def get_by_viber_id(self, viber_id: str) -> User:
        sql = self.get_sql('get_by_viber_id.sql')
        return self.query_one(User, sql, dict(viber_id=viber_id))

    def get_by_login(self, login: str) -> User:
        sql = self.get_sql('get_by_login.sql')
        return self.query_one(User, sql, dict(login=login))

    def insert(self, user: User) -> int:
        sql = self.get_sql('insert.sql')
        return self.execute(sql, user.to_dict())
