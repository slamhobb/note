import inject

from flask import Blueprint, redirect, render_template, request, url_for, g

from note_app import config

from note_app.infrastructure.web import get_token, set_token, remove_token
from note_app.business.auth_service import AuthService

mod = Blueprint('auth', __name__)

auth_service = inject.instance(AuthService)


@mod.before_request
def add_user_context():
    g.user_context = auth_service.get_user_context(get_token())


@mod.route('/')
def login_page():
    user_id = g.user_context.user_id
    if user_id is not None:
        return redirect(url_for('redirect.redirect'))

    error_message = request.args.get('error', None)
    return render_template('auth/index.html', error_message=error_message)


@mod.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    code = request.form['code']
    token = auth_service.authenticate_by_digit_code(login, code)

    if token is None:
        return redirect(url_for('.login_page', error='Неверный логин или код'))

    set_token(token, True)
    return redirect(url_for('redirect.redirect'))


@mod.route('/service-login/<string:login>')
def service_login(login: str):
    if not config.SERVICE_LOGIN:
        return redirect(url_for('redirect.redirect'))

    token = auth_service.authentificate_by_login(login)

    set_token(token, True)
    return redirect(url_for('redirect.redirect'))


@mod.route('/logout')
def logout():
    token = get_token()
    user_id = g.user_context.user_id

    auth_service.logout(user_id, token)
    remove_token()
    return redirect(url_for('auth.login_page'))
