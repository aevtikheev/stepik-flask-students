""" Just some simple tests for the project. """
import pytest


AUTH_PAGE_TITLE = b'<title>Authorisation</title>'
ADMIN_HOME_TITLE = b'<title>Home - Admin</title>'
ADMIN_GROUP_TITLE = b'<title>Group - Admin</title>'
ADMIN_USER_TITLE = b'<title>User - Admin</title>'
ADMIN_APPLICANT_TITLE = b'<title>Applicant - Admin</title>'
ADMIN_EMAIL_TITLE = b'<title>Send e-mail - Admin</title>'


def test_main_page(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.parametrize('url',
                         ['/admin/',
                          '/admin/user',
                          '/admin/group',
                          '/admin/applicant',
                          '/admin/mail'])
def test_admin_pages_unauthorized(client, url):
    _logout(client)
    response = client.get(url, follow_redirects=True)
    assert AUTH_PAGE_TITLE in response.data


@pytest.mark.parametrize('url,expected_title',
                         [('/admin/', ADMIN_HOME_TITLE),
                          ('/admin/user', ADMIN_USER_TITLE),
                          ('/admin/group', ADMIN_GROUP_TITLE),
                          ('/admin/applicant', ADMIN_APPLICANT_TITLE),
                          ('/admin/mail', ADMIN_EMAIL_TITLE)])
def test_admin_pages_authorized(client, user, url, expected_title):
    _login(client, user['email'], user['password'])
    response = client.get(url, follow_redirects=True)
    assert expected_title in response.data


def test_login(client, user):
    response = _login(client, user['email'], user['password'])
    assert ADMIN_HOME_TITLE in response.data


def test_logout(client):
    response = _logout(client)
    assert AUTH_PAGE_TITLE in response.data


def test_invalid_login(client, user):
    response = _login(client, 'invalid_login', user['password'])
    assert AUTH_PAGE_TITLE in response.data


def test_invalid_password(client, user):
    response = _login(client, user['email'], 'invalid_password')
    assert AUTH_PAGE_TITLE in response.data


def _logout(client):
    return client.get('/logout', follow_redirects=True)


def _login(client, email, password):
    return client.post('/login',
                       data=dict(email=email, password=password),
                       follow_redirects=True)

