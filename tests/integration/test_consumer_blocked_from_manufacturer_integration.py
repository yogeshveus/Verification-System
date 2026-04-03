import unittest
import os

from app import create_app
from config import TEST_DATABASE
from database.db import init_db


class ConsumerBlockedManufacturerIntegrationTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        self.app = create_app({
            'TESTING': True,
            'DATABASE': TEST_DATABASE
        })
        self.client = self.app.test_client()

        init_db(TEST_DATABASE)

    def test_consumer_cannot_access_manufacturer(self):
        with self.client.session_transaction() as sess:
            sess['user_email'] = 'consumer@example.com'
            sess['role'] = 'consumer'
            sess['name'] = 'ConsumerUser'

        response = self.client.get('/manufacturer', follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)


if __name__ == '__main__':
    unittest.main()