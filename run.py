import os

from note_app import create_app
from note_app.dao.base_dao import BaseDao

app = create_app()

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.static_folder = os.path.join(basedir, 'static')
    app.run(host='0.0.0.0')


def init_db():
    with app.app_context():
        dao = BaseDao()
        with app.open_resource('schema.sql', mode='r') as f:
            dao.executescript(f.read())
