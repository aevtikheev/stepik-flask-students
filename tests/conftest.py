import os
import tempfile
import random

import pytest

from stepik_p3.app import app
from stepik_p3 import models

TEST_USER = {'email': 'test@email.com',
             'password': '123',
             'name' : 'test_user_name'}


@pytest.fixture(scope='session')
def client(application):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def application(db):
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True


@pytest.fixture(scope='session')
def db():
    """ Create DB and fill it with test data """

    db_fd, app.config['DATABASE'] = tempfile.mkstemp()

    #  TODO: clear database
    with app.app_context():
        models.db.create_all()
        _create_user(TEST_USER)
    yield

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture(scope='session')
def user(db):
    return TEST_USER


def _create_user(user_data):
    user = models.User(email=user_data['email'],
                       name=user_data['name'],
                       password=user_data['password'])
    models.db.session.add(user)
    models.db.session.commit()