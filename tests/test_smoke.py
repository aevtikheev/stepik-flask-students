""" Just some simple tests for the project. Deliberately not a full test set needed! """


#  Test that unauthorized access is prohibited
def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 302


def test_admin_page_unauthorized(client):
    response = client.get('/admin/')
    assert response.status_code == 302


def test_user_page_unauthorized(client):
    response = client.get('/admin/user')
    assert response.status_code == 308


def test_group_page_unauthorized(client):
    response = client.get('/admin/group')
    assert response.status_code == 308


def test_applicant_page_unauthorized(client):
    response = client.get('/admin/applicant')
    assert response.status_code == 308


def test_email_page_unauthorized(client):
    response = client.get('/admin/mail')
    assert response.status_code == 308


#  Test login/logout
# TODO:
#  There are some shitty assertions that check that some substring is in the HTML response.
#  Needvto come up with something better than this.
def test_login(client, user):
    """Make sure login and logout works."""
    rv = _login(client, user['email'], user['password'])
    assert b'Home - Admin' in rv.data


def test_logout(client):
    """Make sure login and logout works."""
    rv = _logout(client)
    assert b'Authorisation' in rv.data


def test_invalid_login(client, user):
    """Make sure login and logout works."""
    rv = _login(client, 'invalid_login', user['password'])
    assert b'Authorisation' in rv.data


def test_invalid_password(client, user):
    """Make sure login and logout works."""
    rv = _login(client, user['email'], 'invalid_password')
    assert b'Authorisation' in rv.data


# Test admin pages for logged in user
def test_admin_page_authorized(client, user):
    rv = _login(client, user['email'], user['password'])
    client.get('/admin/')
    assert b'<title>Home - Admin</title>' in rv.data


def _logout(client):
    return client.get('/logout', follow_redirects=True)


def _login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

