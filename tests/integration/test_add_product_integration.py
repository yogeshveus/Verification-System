import unittest
import os
import sqlite3

from app import create_app
from config import TEST_DATABASE


class AddProductIntegrationTest(unittest.TestCase):

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

    def get_db_connection(self):
        conn = sqlite3.connect(TEST_DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    def login_manufacturer_session(self):
        with self.client.session_transaction() as sess:
            sess['user_email'] = 'maker@example.com'
            sess['role'] = 'manufacturer'
            sess['name'] = 'Maker'

    def test_add_product(self):
        self.login_manufacturer_session()

        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO product_types (name, created_by, is_active) VALUES (?, ?, ?)",
            ('Baby Formula', 'maker@example.com', 1)
        )
        conn.commit()
        conn.close()

        response = self.client.post('/manufacturer/item', data={
            'itemId': '101',
            'productDropdown': 'Baby Formula',
            'metadataHash': 'abc123hash'
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/manufacturer/item', response.location)

        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE itemId=?", ('101',))
        product = cur.fetchone()
        conn.close()

        self.assertIsNotNone(product)
        self.assertEqual(product['metadataHash'], 'abc123hash')


if __name__ == '__main__':
    unittest.main()