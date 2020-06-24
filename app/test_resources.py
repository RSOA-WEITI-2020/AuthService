import unittest
import os
import app
import pytest

app_dir = os.path.dirname(os.path.realpath(__file__))
db_uri = 'sqlite:///' + app_dir + '/testing_db.db'
try:
    os.remove(app_dir+'/testing_db.db')
except:
    print('db file not found')
flask_app = app.create_app(db_uri, app_dir + '/../keys')


@pytest.fixture
def app_fixture():
    with flask_app.test_client() as client:
        yield client

    app_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        os.remove(app_dir+'/testing_db.db')
    except:
        print('db file not found')


def test_should_success_registration(app_fixture):
    payload = {
        "password": "super_trudne!haslo!oneone",
        "email": "test@test.com",
        "first_name": "abc",
        "last_name": "def",
        "address": "ghi"
    }

    response = app_fixture.post('/v1/register', data=payload)

    assert 'ok' == response.json['message']
    assert 200 == response.status_code

def test_password_not_strong_enough(app_fixture):
    payload = {
        "password": "abc1234",
        "email": "test@test.com",
        "first_name": "abc",
        "last_name": "def",
        "address": "ghi"
    }

    response = app_fixture.post('/v1/register', data=payload)

    assert 400 == response.status_code
