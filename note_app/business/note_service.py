import inject

from datetime import date
import copy

from note_app.dao.note.note_dao import NoteDao
from note_app.domain.note import Note


class NoteService:
    note_dao = inject.attr(NoteDao)

    def get_by_type(
            self, user_id: int, note_type_id: int, hidden: bool) -> list[Note]:
        return self.note_dao.get_by_type(user_id, note_type_id, hidden)

    def get_by_id(self, user_id: int, id: int):
        return self.note_dao.get_by_id(user_id, id)

    def save(self, note: Note) -> (int, Note):
        if len(note.text) == 0:
            return note.id, note

        if note.id == 0:
            note.create_date = date.today()
            note.modify_date = date.today()
            return self.note_dao.insert(note), note
        else:
            old_note = self.note_dao.get_by_id(note.user_id, note.id)
            new_note = copy.copy(old_note)

            if new_note.text != note.text:
                new_note.text = note.text
                new_note.modify_date = date.today()

            new_note.note_type_id = note.note_type_id

            self.note_dao.update(new_note)
            return new_note.id, old_note

    def hide(self, user_id: int, id: int) -> Note:
        old_note = self.note_dao.get_by_id(user_id, id)
        new_note = copy.copy(old_note)

        new_note.hidden = not new_note.hidden
        self.note_dao.update(new_note)

        return old_note

    def reset_notes_type(self, user_id: int, note_type_id: int):
        self.note_dao.reset_notes_type(user_id, note_type_id, date.today())

    def delete(self, user_id: int, id: int):
        self.note_dao.delete(user_id, id)
