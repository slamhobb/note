import inject

from typing import List

from datetime import date

from note_app.dao.note.note_dao import NoteDao
from note_app.domain.note import Note


class NoteService:
    note_dao = inject.attr(NoteDao)

    def get_by_type(self, user_id: int, note_type_id: int) -> List[Note]:
        return self.note_dao.get_by_type(user_id, note_type_id)

    def get_by_id(self, user_id: int, id: int):
        return self.note_dao.get_by_id(user_id, id)

    def save(self, note: Note) -> int:
        if len(note.text) == 0:
            return note.id

        if note.id == 0:
            note.create_date = date.today()
            note.modify_date = date.today()
            return self.note_dao.insert(note)
        else:
            note.modify_date = date.today()
            return self.note_dao.update(note)

    def reset_notes_type(self, user_id: int, note_type_id: int):
        self.note_dao.reset_notes_type(user_id, note_type_id, date.today())

    def delete(self, user_id: int, id: int):
        self.note_dao.delete(user_id, id)
