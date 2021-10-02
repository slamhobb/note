import inject

from datetime import date
from dateutil.relativedelta import relativedelta

from flask import Blueprint, render_template, g, request
from flask import redirect, url_for

from note_app.infrastructure.web import get_token
from note_app.infrastructure.auth import login_required
from note_app.infrastructure.parse import get_bool

from note_app.business.auth_service import AuthService
from note_app.business.note_type_service import NoteTypeService
from note_app.business.note_service import NoteService
from note_app.domain.note import Note


mod = Blueprint('note', __name__)

auth_service = inject.instance(AuthService)
note_type_service = inject.instance(NoteTypeService)
note_service = inject.instance(NoteService)


@mod.before_request
def add_user_context():
    g.user_context = auth_service.get_user_context(get_token())


@mod.route('/')
@mod.route('/by-type/<int:note_type_id>')
@login_required
def index(note_type_id: int = 1):
    hidden = get_bool(request.args.get('hidden'))
    focus_note_id = request.args.get('focus_note_id', 0)
    user_id = g.user_context.user_id

    note_types = note_type_service.get_by_user_id(user_id)
    note_types = [note_type.to_web_dict() for note_type in note_types]

    notes = note_service.get_by_type(user_id, note_type_id, hidden)
    notes.sort(key=lambda n: (n.create_date, n.id), reverse=True)
    notes = [note.to_web_dict() for note in notes]

    def date_delta(date: date, today: date):
        delta = relativedelta(today, date)

        if delta.years > 0:
            return f'{delta.years}г'

        if delta.months > 0:
            return f'{delta.months}м'

        if delta.weeks > 0:
            return f'{delta.weeks}н'

        if delta.days > 0:
            return f'{delta.days}д'

        return 'сегодня'

    today = date.today()
    for note in notes:
        note['date'] = date_delta(note['date'], today)

    return render_template(
        'note/index.html', note_types=note_types, notes=notes,
        note_type_id=note_type_id, hidden=hidden, focus_note_id=focus_note_id)


@mod.route('/edit/<int:id>')
@login_required
def edit(id: int):
    user_id = g.user_context.user_id

    note_types = note_type_service.get_by_user_id(user_id)
    note_types = [note_type.to_web_dict() for note_type in note_types]

    note = note_service.get_by_id(user_id, id)

    note_type_name = list(
        filter(
            lambda nt: nt['id'] == note.note_type_id, note_types))[0]['name']

    return render_template(
        'note/edit.html', note_types=note_types, note=note,
        note_type_name=note_type_name)


@mod.route('/save', methods=['POST'])
@login_required
def save():
    user_id = g.user_context.user_id

    id = request.form.get('id', 0)
    text = request.form['text']
    note_type_id = request.form['note_type_id']

    old_hidden = False
    old_note_type_id = note_type_id

    if id == 0:
        note = Note(0, user_id, text, note_type_id)
    else:
        note = note_service.get_by_id(user_id, id)
        old_note_type_id = note.note_type_id
        old_hidden = note.hidden

        note.text = text
        note.note_type_id = note_type_id

    id = note_service.save(note)

    return redirect(url_for(
        '.index', note_type_id=old_note_type_id, hidden=old_hidden,
        focus_note_id=id))


@mod.route('/hide', methods=['POST'])
@login_required
def hide():
    user_id = g.user_context.user_id

    id = request.form.get('id', 0)

    note = note_service.get_by_id(user_id, id)
    if note is None:
        return redirect(url_for('.index'))

    old_hidden = note.hidden
    note.hidden = not note.hidden
    note_service.save(note)

    return redirect(url_for(
        '.index', note_type_id=note.note_type_id, hidden=old_hidden))


@mod.route('/delete', methods=['POST'])
@login_required
def delete():
    user_id = g.user_context.user_id

    id = request.form['id']

    note = note_service.get_by_id(user_id, id)
    note_service.delete(user_id, id)

    return redirect(url_for(
        '.index', note_type_id=note.note_type_id, hidden=note.hidden))
