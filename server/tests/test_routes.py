def test_root_route(client):
    rv = client.get('/')
    assert rv.status_code == 200
