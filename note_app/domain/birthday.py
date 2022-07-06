from __future__ import annotations

import datetime
from dataclasses import dataclass

from datetime import date, datetime


@dataclass
class Birthday:
    id: int
    user_id: int
    birth_date: date
    name: str

    @classmethod
    def from_dict(cls, adict: dict) -> Birthday:
        return Birthday(
            id=adict['id'],
            user_id=adict['user_id'],
            birth_date=datetime.fromisoformat(adict['birth_date']).date(),
            name=adict['name']
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'birth_date': self.birth_date.isoformat(),
            'name': self.name
        }

    def to_web_dict(self) -> dict:
        return {
            'id': self.id,
            'birth_date': self.birth_date,
            'name': self.name
        }
