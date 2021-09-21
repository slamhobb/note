from __future__ import annotations

from dataclasses import dataclass

from datetime import date


@dataclass
class Note:
    id: int
    user_id: int
    text: str
    note_type_id: int
    create_date: date = date.today()
    modify_date: date = date.today()
    hidden: bool = False

    @classmethod
    def from_dict(cls, adict: dict) -> Note:
        return Note(
            id=adict['id'],
            user_id=adict['user_id'],
            text=adict['text'],
            note_type_id=adict['note_type_id'],
            create_date=date.fromisoformat(adict['create_date']),
            modify_date=date.fromisoformat(adict['modify_date']),
            hidden=bool(adict['hidden'])
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'note_type_id': self.note_type_id,
            'create_date': self.create_date.isoformat(),
            'modify_date': self.modify_date.isoformat(),
            'hidden': self.hidden
        }

    def to_web_dict(self) -> dict:
        return {
            'id': self.id,
            'text': self.text,
            'date': self.create_date if self.create_date > self.modify_date
            else self.modify_date,
            'hidden': self.hidden
        }
