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
