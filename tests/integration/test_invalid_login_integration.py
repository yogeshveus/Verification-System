import unittest
import os

from app import create_app
from config import TEST_DATABASE
from database.db import init_db


class InvalidLoginIntegrationTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        self.app = create_app({
            'TESTING': True,
            'DATABASE': TEST_DATABASE
        })
        self.client = self.app.test_client()

        init_db(TEST_DATABASE)

    def test_invalid_login(self):
        self.client.post('/register', data={
            'name': 'David',
            'email': 'david@example.com',
            'password': 'Hello@123',
            'role': 'consumer'
        })

        response = self.client.post('/login', data={
            'email': 'david@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)


if __name__ == '__main__':
    unittest.main()