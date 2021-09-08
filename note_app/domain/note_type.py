from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NoteType:
    id: int
    user_id: int
    name: str

    @classmethod
    def from_dict(cls, adict: dict) -> NoteType:
        return NoteType(
            id=adict['id'],
            user_id=adict['user_id'],
            name=adict['name']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name
        }

    def to_web_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
