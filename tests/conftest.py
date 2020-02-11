import os
import tempfile
import random

import pytest

from stepik_flask_students.app import create_app
from stepik_flask_students import models

TEST_USER = {'email': 'test@email.com',
             'password': '123',
             'name' : 'test_user_name'}


@pytest.fixture(scope='session')
def client(application):
    with application.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def application():
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()

    with app.app_context():
        models.db.create_all()
    yield app

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture(scope='session')
def user(application):
    _create_user(TEST_USER)
    return TEST_USER


def _create_user(user_data):
    user = models.User(email=user_data['email'],
                       name=user_data['name'],
                       password=user_data['password'])
    models.db.session.add(user)
    models.db.session.commit()