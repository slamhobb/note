import uuid
import base64
import os
import string
import random

import inject

from note_app.dao.auth_token.auth_token_dao import AuthTokenDao
from note_app.business.user_service import UserService
from note_app.domain.auth import AuthToken, AuthUser, UserContext


class AuthService:
    code_by_user_id_cache = {}
    user_token_cache = {}

    auth_token_dao = inject.attr(AuthTokenDao)
    user_service = inject.attr(UserService)

    def create_digit_code(self, user_id: int) -> str:
        digit_code = self._generate_digit_code()

        self.code_by_user_id_cache[user_id] = digit_code

        return digit_code

    def get_user_by_digit_code(self, login: str, digit_code: str):
        user = self.user_service.get_by_login(login)

        if user is None:
            return None

        saved_digit_code = self.code_by_user_id_cache.pop(user.id, None)

        if digit_code != saved_digit_code:
            return None

        return user

    def authenticate_by_digit_code(self, login: str, digit_code: str) -> str | None:
        user = self.get_user_by_digit_code(login, digit_code)
        if user is None:
            return None

        auth_token = AuthToken(0, user.id, self._generate_token())
        self.auth_token_dao.insert(auth_token)

        return auth_token.token

    def authenticate_by_login(self, login: str) -> str | None:
        user = self.user_service.get_by_login(login)

        if user is None:
            return None

        auth_token = AuthToken(0, user.id, self._generate_token())
        self.auth_token_dao.insert(auth_token)

        return auth_token.token

    def get_user_context(self, token) -> UserContext:
        if token is None:
            return UserContext(None, None, False)

        auth_user = self._get_auth_user(token)

        if auth_user is None:
            return UserContext(None, None, False)

        return UserContext(auth_user.user_id, auth_user.login, True)

    def logout(self, user_id: int, token: str):
        if token is None:
            return

        del self.user_token_cache[token]
        self.auth_token_dao.delete(user_id, token)

    def _get_auth_user(self, token: str) -> AuthUser | None:
        auth_user = self.user_token_cache.get(token, None)
        if auth_user is not None:
            return auth_user

        auth_user = self.auth_token_dao.get_auth_user_by_token(token)
        if auth_user is None:
            return None

        self.user_token_cache[token] = auth_user

        return auth_user

    @staticmethod
    def _generate_digit_code() -> str:
        return ''.join(random.choice(string.digits) for i in range(6))

    @staticmethod
    def _generate_token() -> str:
        random_string = base64.b64encode(os.urandom(30))
        return uuid.uuid1().hex + str(random_string, 'utf-8')
