import pytest

import app.database.models as models
import flask.json


@pytest.mark.parametrize('ch_id,chapter,page,expected', [
    (1, 1, 1, 200),
    ('s', 1, 1, 404),
    (1, 1, 's', 404),
    (1, 1, 500, 200)
])
def test_page(client_db, ch_id, chapter, page, expected):
    c = models.Comic()
    client_db.db.session.add(c)
    client_db.db.session.commit()

    rv = client_db.get(f'/{ch_id}/{chapter}/{page}')
    assert rv.status_code == expected


def test_catalog(client_db):
    rv = client_db.get('/catalog')
    assert rv.status_code == 200


def test_info(client_db):
    c = models.Comic()
    client_db.db.session.add(c)
    client_db.db.session.commit()

    rv = client_db.get('/info/1')
    assert rv.status_code == 200


def test_info_meta(client_db):
    c = models.Comic()
    n = models.ComicName(name='foo', comic_id='1')

    client_db.db.session.add(c)
    client_db.db.session.add(n)
    client_db.db.session.commit()

    rv = client_db.get('/info/1')
    json_data = rv.get_json()
    assert json_data['names'] == ['foo']


def test_info_no_id(client_db):
    rv = client_db.get('/info')
    assert rv.status_code == 404


def test_info_chap(client_db):
    c = models.Chapter(number='1', total_pages=1, comic_id=1)
    client_db.db.session.add(c)
    client_db.db.session.commit()

    rv = client_db.get('/info/chap/1')
    assert rv.status_code == 200


def test_info_chap_meta(client_db):
    c = models.Chapter(number='1', title='foo', total_pages=1, comic_id=1)
    client_db.db.session.add(c)
    client_db.db.session.commit()

    rv = client_db.get('/info/chap/1')
    json_data = flask.json.loads(rv.get_json())
    assert json_data['total_pages'] == 1
    assert json_data['title'] == 'foo'
