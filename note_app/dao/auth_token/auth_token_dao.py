from note_app.dao.base_dao import BaseDao
from note_app.domain.auth import AuthToken, AuthUser


class AuthTokenDao(BaseDao):
    def __init__(self):
        super().__init__('/auth_token/sql/')

    def insert(self, auth_token: AuthToken):
        sql = self.get_sql('insert.sql')
        return self.execute(sql, auth_token.to_dict())

    def get_auth_user_by_token(self, token: str) -> AuthUser:
        sql = self.get_sql('get_auth_user_by_token.sql')
        return self.query_one(AuthUser, sql, dict(token=token))

    def delete(self, user_id: int, token: str):
        sql = self.get_sql('delete.sql')
        self.execute(sql, dict(user_id=user_id, token=token))
