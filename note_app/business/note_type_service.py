import inject

from typing import List

from note_app.dao.note_type.note_type_dao import NoteTypeDao
from note_app.business.note_service import NoteService
from note_app.domain.note_type import NoteType


class NoteTypeService:
    note_type_dao = inject.attr(NoteTypeDao)
    note_service = inject.attr(NoteService)

    def get_by_user_id(self, user_id: int) -> List[NoteType]:
        return self.note_type_dao.get_by_user_id(user_id)

    def insert(self, note_type: NoteTypeDao) -> int:
        return self.note_type_dao.insert(note_type)

    def delete(self, user_id: int, id: int):
        self.note_service.reset_notes_type(user_id, id)
        return self.note_type_dao.delete(id, user_id)
