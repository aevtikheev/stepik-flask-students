""" Smoke tests for the project """


def test_main_page(client):
    rv = client.get('/')
    assert b'No entries here so far' in rv.data
