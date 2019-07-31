import pytest

from app.database.models import Comic


@pytest.mark.parametrize('ch_id,chapter,page,expected', [
    (1, 1, 1, 200),
    ('s', 1, 1, 404),
    (1, 1, 's', 404),
    (1, 1, 500, 200)
])
def test_page(client_db, ch_id, chapter, page, expected):
    c = Comic()
    client_db.db.session.add(c)
    client_db.db.session.commit()

    rv = client_db.get(f'/c/{ch_id}/{chapter}/{page}')
    assert rv.status_code == expected


def test_catalog(client_db):
    rv = client_db.get('/c/catalog')
    assert rv.status_code == 200


def test_info(client_db):
    c = Comic()
    client_db.db.session.add(c)
    client_db.db.session.commit()

    rv = client_db.get('/c/info/1')
    assert rv.status_code == 200


def test_info_no_id(client_db):
    rv = client_db.get('/c/info')
    assert rv.status_code == 404
