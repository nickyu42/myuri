import os
import pytest
import tempfile
from flask import Flask
from flask.testing import FlaskClient

from app.config import TestingConfig


@pytest.fixture
def client():
    db_file, temp_path = tempfile.mkstemp(suffix='.sqlite')

    app = Flask(__name__)
    app.config.from_object(TestingConfig)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{temp_path}'

    with app.test_client() as client:
        with app.app_context():
            from app.database.db import db
            db.init_app(app)
            db.create_all()

        yield client

        db.drop_all()

    os.close(db_file)


# def test_root_route(client: FlaskClient):
#     rv = client.get('/')
#     assert rv.status_code == 200


# @pytest.mark.parametrize('ch_id,chapter,page,expected', [
#     (1, 1, 1, 200),
#     ('s', 1, 1, 404),
#     (1, 1, 's', 404),
#     (1, 1, 500, 200)
# ])
# def test_page(client: FlaskClient, ch_id, chapter, page, expected):
#     rv = client.get(f'/c/{ch_id}/{chapter}/{page}')
#     assert rv.status_code == expected
#
#
# def test_catalog(client: FlaskClient):
#     rv = client.get('/c/catalog')
#     assert rv.status_code == 200


# def test_info(client: FlaskClient):
#     rv = client.get('/c/info/1')
#     assert rv.status_code == 200


# def test_info_no_id(client: FlaskClient):
#     rv = client.get('/c/info')
#     assert rv.status_code == 404
