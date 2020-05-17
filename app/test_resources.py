import unittest
import os
import app
import models


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        app_dir = os.path.dirname(os.path.realpath(__file__))
        db_uri = 'sqlite:///' + app_dir + '/testing_db.db'
        try:
            os.remove(app_dir+'/testing_db.db')
        except:
            print('db file not found')
        self.app = app.create_app(db_uri, '../keys').test_client()

    def test_should_success_registration(self):
        payload = {
            "username": "test",
            "password": "abc1234",
            "email": "test@test.com"
        }

        response = self.app.post('/v1/register', data=payload)

        self.assertEqual('ok', response.json['message'])
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        app_dir = os.path.dirname(os.path.realpath(__file__))
        try:
            os.remove(app_dir+'/testing_db.db')
        except:
            print('db file not found')
