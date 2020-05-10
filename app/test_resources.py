import unittest
from main import app

class RegistrationTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_should_success_registration(self):
        payload = dict(
            username="test",
            password="abc1234",
            email="test@test.com"
        )
        
        response = self.app.post('/v1/register', data=payload)

        self.assertEqual('ok', response.json['message'])
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        print('teardown')