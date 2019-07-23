import pytest
from flask.testing import FlaskClient

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_root_route(client: FlaskClient):
    rv = client.get('/')
    assert rv.status_code == 200


@pytest.mark.parametrize('ch_id,chapter,page,expected', [
    (1, 'ch1', 1, 200),
    ('s', 'ch1', 1, 404),
    (1, 'ch1', 's', 404),
    (1, 'ch1', 500, 200)
])
def test_page(client: FlaskClient, ch_id, chapter, page, expected):
    rv = client.get(f'/c/{ch_id}/{chapter}/{page}')
    assert rv.status_code == expected


def test_catalog(client: FlaskClient):
    rv = client.get('/c/catalog')
    assert rv.status_code == 200


def test_info(client: FlaskClient):
    rv = client.get('/c/info/1')
    assert rv.status_code == 200


def test_info_no_id(client: FlaskClient):
    rv = client.get('/c/info')
    assert rv.status_code == 404
