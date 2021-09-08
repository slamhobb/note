from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AuthToken:
    id: int
    user_id: int
    token: str

    @classmethod
    def from_dict(cls, adict: dict) -> AuthToken:
        return AuthToken(
            id=adict['id'],
            user_id=adict['user_id'],
            token=adict['token']
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token
        }


@dataclass
class AuthUser:
    user_id: int
    login: str

    @classmethod
    def from_dict(cls, adict: dict) -> AuthUser:
        return AuthUser(
            user_id=adict['user_id'],
            login=adict['login']
        )

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'login': self.login
        }


@dataclass
class UserContext:
    user_id: int
    login: str
    is_authenticated: bool
