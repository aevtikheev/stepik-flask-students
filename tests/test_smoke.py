""" Just some simple tests for the project. """

AUTH_PAGE_TITLE = b'<title>Authorisation</title>'
ADMIN_HOME_TITLE = b'<title>Home - Admin</title>'
ADMIN_GROUP_TITLE = b'<title>Group - Admin</title>'
ADMIN_USER_TITLE = b'<title>User - Admin</title>'
ADMIN_APPLICANT_TITLE = b'<title>Applicant - Admin</title>'
ADMIN_EMAIL_TITLE = b'<title>Send e-mail - Admin</title>'


#  Test that unauthorized access is prohibited
def test_main_page(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200


def test_admin_page_unauthorized(client):
    response = client.get('/admin/', follow_redirects=True)
    assert AUTH_PAGE_TITLE in response.data


def test_user_page_unauthorized(client):
    response = client.get('/admin/user', follow_redirects=True)
    assert AUTH_PAGE_TITLE in response.data


def test_group_page_unauthorized(client):
    response = client.get('/admin/group', follow_redirects=True)
    assert AUTH_PAGE_TITLE in response.data


def test_applicant_page_unauthorized(client):
    response = client.get('/admin/applicant', follow_redirects=True)
    assert AUTH_PAGE_TITLE in response.data


def test_email_page_unauthorized(client):
    response = client.get('/admin/mail', follow_redirects=True)
    assert AUTH_PAGE_TITLE in response.data


#  Test login/logout
def test_login(client, user):
    """Make sure login and logout works."""
    response = _login(client, user['email'], user['password'])
    assert ADMIN_HOME_TITLE in response.data


def test_logout(client):
    """Make sure login and logout works."""
    response = _logout(client)
    assert AUTH_PAGE_TITLE in response.data


def test_invalid_login(client, user):
    """Make sure login and logout works."""
    response = _login(client, 'invalid_login', user['password'])
    assert AUTH_PAGE_TITLE in response.data


def test_invalid_password(client, user):
    """Make sure login and logout works."""
    response = _login(client, user['email'], 'invalid_password')
    assert AUTH_PAGE_TITLE in response.data


# Test admin pages for logged in user
def test_admin_page_authorized(client, user):
    _login(client, user['email'], user['password'])
    response = client.get('/admin/', follow_redirects=True)
    assert ADMIN_HOME_TITLE in response.data


def test_admin_group_page_authorized(client, user):
    _login(client, user['email'], user['password'])
    response = client.get('/admin/group/', follow_redirects=True)
    assert ADMIN_GROUP_TITLE in response.data


def test_admin_user_page_authorized(client, user):
    _login(client, user['email'], user['password'])
    response = client.get('/admin/user/', follow_redirects=True)
    assert ADMIN_USER_TITLE in response.data


def test_admin_applicant_page_authorized(client, user):
    _login(client, user['email'], user['password'])
    response = client.get('/admin/applicant/', follow_redirects=True)
    assert ADMIN_APPLICANT_TITLE in response.data


def test_admin_email_page_authorized(client, user):
    _login(client, user['email'], user['password'])
    response = client.get('/admin/mail/', follow_redirects=True)
    assert ADMIN_EMAIL_TITLE in response.data


#  Helper functions
def _logout(client):
    return client.get('/logout', follow_redirects=True)


def _login(client, email, password):
    return client.post('/login',
                       data=dict(email=email, password=password),
                       follow_redirects=True)

