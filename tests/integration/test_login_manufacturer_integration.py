import unittest
import sqlite3
import os

from app import create_app
from config import TEST_DATABASE
from database.db import init_db


class ManufacturerLoginIntegrationTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        self.app = create_app({
            'TESTING': True,
            'DATABASE': TEST_DATABASE
        })
        self.client = self.app.test_client()

        init_db(TEST_DATABASE)
    def test_login_manufacturer(self):
        self.client.post('/register', data={
            'name': 'Bob',
            'email': 'bob@example.com',
            'password': 'Hello@123',
            'role': 'manufacturer'
        })

        response = self.client.post('/login', data={
            'email': 'bob@example.com',
            'password': 'Hello@123'
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/manufacturer', response.location)

        with self.client.session_transaction() as sess:
            self.assertEqual(sess['user_email'], 'bob@example.com')
            self.assertEqual(sess['role'], 'manufacturer')
            self.assertEqual(sess['name'], 'Bob')


if __name__ == '__main__':
    unittest.main()