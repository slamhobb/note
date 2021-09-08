from typing import List

from note_app.dao.base_dao import BaseDao
from note_app.domain.note_type import NoteType


class NoteTypeDao(BaseDao):
    def __init__(self):
        super().__init__('/note_type/sql/')

    def get_by_user_id(self, user_id: int) -> List[NoteType]:
        sql = self.get_sql('get_by_user_id.sql')
        return self.query_all(NoteType, sql, dict(user_id=user_id))

    def insert(self, note_type: NoteType) -> int:
        sql = self.get_sql('insert.sql')
        return self.execute(sql, note_type.to_dict())

    def delete(self, id: int, user_id: int):
        sql = self.get_sql('delete.sql')
        return self.execute(sql, dict(id=id, user_id=user_id))
