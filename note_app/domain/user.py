from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User(object):
    id: int
    login: str
    viber_id: int

    @classmethod
    def from_dict(cls, adict: dict) -> User:
        return User(
            id=adict['id'],
            login=adict['login'],
            viber_id=adict['viber_id']
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'login': self.login,
            'viber_id': self.viber_id
        }

    def to_web_dict(self) -> dict:
        return {
            'id': self.id,
            'login': self.login
        }
