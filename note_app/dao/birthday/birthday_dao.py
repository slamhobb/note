from note_app.dao.base_dao import BaseDao
from note_app.domain.birthday import Birthday


class BirthdayDao(BaseDao):
    def __init__(self):
        super(BirthdayDao, self).__init__('/birthday/sql/')

    def get_list(self, user_id: int) -> list[Birthday]:
        sql = self.get_sql('get.sql')
        return self.query_all(Birthday, sql, dict(user_id=user_id))

    def get_by_id(self, user_id: int, id: int) -> Birthday:
        sql = self.get_sql('get_by_id.sql')
        return self.query_one(Birthday, sql, dict(user_id=user_id, id=id))

    def get_by_month_day(self, month: int, day: int):
        sql = self.get_sql('get_by_month_day.sql')
        return self.query_all(Birthday, sql, dict(month=month, day=day))

    def insert(self, birthday: Birthday) -> int:
        sql = self.get_sql('insert.sql')
        return self.execute(sql, birthday.to_dict())

    def update(self, birthday: Birthday):
        sql = self.get_sql('update.sql')
        self.execute(sql, birthday.to_dict())

    def delete(self, user_id: int, id: int):
        sql = self.get_sql('delete.sql')
        self.execute(sql, dict(user_id=user_id, id=id))
