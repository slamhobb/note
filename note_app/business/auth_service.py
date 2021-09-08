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
    user_id_by_code_cache = {}
    user_token_cache = {}

    auth_token_dao = inject.attr(AuthTokenDao)
    user_service = inject.attr(UserService)

    def create_digit_code(self, user_id: int) -> str:
        digit_code = self._generate_digit_code()

        self.user_id_by_code_cache[digit_code] = user_id

        return digit_code

    def authenticate_by_digit_code(self, login: str, digit_code: str) -> str:
        user_id = self.user_id_by_code_cache.pop(digit_code, None)

        if user_id is None:
            return None

        user = self.user_service.get_by_login(login)

        if user is None:
            return None

        if user_id != user.id:
            return None

        auth_token = AuthToken(0, user_id, self._generate_token())
        self.auth_token_dao.insert(auth_token)

        return auth_token.token

    def get_user_context(self, token):
        if token is None:
            return UserContext(None, None, False)

        auth_user = self._get_auth_user(token)

        if auth_user is None:
            return UserContext(None, None, False)

        return UserContext(auth_user.user_id, auth_user.login, True)

    def logout(self, user_id: int, token: str):
        del self.user_token_cache[token]
        self.auth_token_dao.delete(user_id, token)

    def _get_auth_user(self, token: str) -> AuthUser:
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
    def _generate_token():
        random_string = base64.b64encode(os.urandom(30))
        return uuid.uuid1().hex + str(random_string, 'utf-8')
