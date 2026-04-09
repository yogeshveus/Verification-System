import unittest
import os

from database.db import init_db
from app import create_app
from config import TEST_DATABASE

class ConsumerLoginIntegrationTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        self.app = create_app({
            'TESTING': True,
            'DATABASE': TEST_DATABASE
        })
        self.client = self.app.test_client()

    def tearDown(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        init_db(TEST_DATABASE)
    def test_login_consumer(self):
        self.client.post('/register', data={
            'name': 'Charlie',
            'email': 'charlie@example.com',
            'password': 'Hello@123',
            'role': 'consumer'
        })

        response = self.client.post('/login', data={
            'email': 'charlie@example.com',
            'password': 'Hello@123'
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/consumer', response.location)


if __name__ == '__main__':
    unittest.main()