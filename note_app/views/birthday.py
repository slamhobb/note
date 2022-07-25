import inject

from datetime import datetime, date

from flask import Blueprint, render_template, g, request, Response
from flask import redirect, url_for

from note_app.infrastructure.web import get_token
from note_app.infrastructure.auth import login_required

from note_app.business.auth_service import AuthService
from note_app.business.birthday_service import BirthdayService
from note_app.business.birthday_notify_service import BirthdayNotifyService
from note_app.domain.birthday import Birthday

mod = Blueprint('birthday', __name__)

auth_service = inject.instance(AuthService)
birthday_service = inject.instance(BirthdayService)
birthday_notify_service = inject.instance(BirthdayNotifyService)


@mod.before_request
def add_user_context():
    g.user_context = auth_service.get_user_context(get_token())


@mod.route('/')
@login_required
def index():
    user_id = g.user_context.user_id

    birthdays = birthday_service.get_list(user_id)
    for birthday in birthdays:
        birthday.birth_date = date(date.today().year, birthday.birth_date.month, birthday.birth_date.day)
    birthdays.append(Birthday(id=0, user_id=0, name='Сегодня', birth_date=date.today()))
    birthdays = [birthday.to_web_dict() for birthday in birthdays]
    birthdays.sort(key=lambda x: (x['birth_date'], x['id']))

    return render_template('birthday/index.html', birthdays=birthdays)


@mod.route('/edit/<int:id>')
@login_required
def edit(id: int):
    user_id = g.user_context.user_id

    birthday = birthday_service.get_by_id(user_id, id)
    birthday = birthday.to_web_dict()

    return render_template('birthday/edit.html', birthday=birthday)


@mod.route('/save', methods=['POST'])
@login_required
def save():
    user_id = g.user_context.user_id

    id = int(request.form.get('id', 0))
    birth_date = datetime.strptime(request.form['birth_date'], '%d.%m.%Y').date()
    name = request.form['name']

    if id == 0:
        birthday = Birthday(0, user_id, birth_date, name)
    else:
        birthday = birthday_service.get_by_id(user_id, id)
        birthday.birth_date = birth_date
        birthday.name = name

    birthday_service.save(birthday)

    return redirect(url_for('.index'))


@mod.route('/delete', methods=['POST'])
@login_required
def delete():
    user_id = g.user_context.user_id

    id = int(request.form['id'])

    birthday_service.delete(user_id, id)

    return redirect(url_for('.index'))


@mod.route('/notify')
def notify():
    today = date.today()
    birthday_notify_service.notify_about_birthday_on_date(today)
    return Response(status=200)
