import unittest
import os

from app import create_app
from config import TEST_DATABASE


class RegressionManufacturerLoginTest(unittest.TestCase):

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

    def test_manufacturer_login_still_works(self):
        self.client.post('/register', data={
            'name': 'Bob',
            'email': 'bob@example.com',
            'password': 'Hello@123',
            'role': 'manufacturer'
        })

        response = self.client.post('/login', data={
            'email': 'bob@example.com',
            'password': 'Hello@123',
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/manufacturer', response.location)


if __name__ == '__main__':
    unittest.main()