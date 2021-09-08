from typing import List

from datetime import date

from note_app.dao.base_dao import BaseDao
from note_app.domain.note import Note


class NoteDao(BaseDao):
    def __init__(self):
        super(NoteDao, self).__init__('/note/sql/')

    def get_by_type(self, user_id: int, note_type_id: int) -> List[Note]:
        sql = self.get_sql('get_by_type.sql')
        return self.query_all(Note, sql, dict(
            user_id=user_id, note_type_id=note_type_id))

    def get_by_id(self, user_id: int, id: int) -> Note:
        sql = self.get_sql('get_by_id.sql')
        return self.query_one(Note, sql, dict(user_id=user_id, id=id))

    def insert(self, note: Note) -> int:
        sql = self.get_sql('insert.sql')
        return self.execute(sql, note.to_dict())

    def update(self, note: Note):
        sql = self.get_sql('update.sql')
        self.execute(sql, note.to_dict())
        return note.id

    def reset_notes_type(self, user_id: int, note_type_id: int, date: date):
        sql = self.get_sql('reset_notes_type.sql')
        self.execute(sql, dict(
            user_id=user_id, note_type_id=note_type_id, date=date))

    def delete(self, user_id: int, id: int):
        sql = self.get_sql('delete.sql')
        self.execute(sql, dict(user_id=user_id, id=id))
