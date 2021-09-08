import inject

from flask import Blueprint, url_for
from flask import redirect as flask_redirect

from note_app.infrastructure.web import get_token
from note_app.business.auth_service import AuthService


mod = Blueprint('redirect', __name__)

auth_service = inject.instance(AuthService)


@mod.route('')
def redirect():
    user_context = auth_service.get_user_context(get_token())
    if not user_context.is_authenticated:
        return flask_redirect(url_for('auth.login_page'))

    return flask_redirect(url_for('note.index'))
