import inject

from flask import Blueprint, render_template, g, request
from flask import redirect, url_for

from note_app.infrastructure.web import get_token
from note_app.infrastructure.auth import login_required

from note_app.business.auth_service import AuthService
from note_app.business.note_type_service import NoteTypeService
from note_app.domain.note_type import NoteType

mod = Blueprint('note_type', __name__)

auth_service = inject.instance(AuthService)
note_type_service = inject.instance(NoteTypeService)


@mod.before_request
def add_user_context():
    g.user_context = auth_service.get_user_context(get_token())


@mod.route('/')
@login_required
def index():
    user_id = g.user_context.user_id

    note_types = note_type_service.get_by_user_id(user_id)
    note_types = [note_type.to_web_dict() for note_type in note_types]

    return render_template(
        'note_type/index.html', note_types=note_types)


@mod.route('/add', methods=['POST'])
@login_required
def add():
    user_id = g.user_context.user_id

    name = request.form['name']

    note_type = NoteType(0, user_id, name)
    note_type_service.insert(note_type)

    return redirect(url_for('.index'))


@mod.route('/delete/<int:id>')
@login_required
def delete(id: int):
    user_id = g.user_context.user_id

    note_type_service.delete(user_id, id)

    return redirect(url_for('.index'))
