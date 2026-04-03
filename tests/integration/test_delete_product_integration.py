import unittest
import sqlite3
import os

from app import create_app
from config import TEST_DATABASE
from database.db import init_db


class DeleteProductIntegrationTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        self.app = create_app({
            'TESTING': True,
            'DATABASE': TEST_DATABASE
        })
        self.client = self.app.test_client()

        init_db(TEST_DATABASE)

    def tearDown(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

    def get_db_connection(self):
        conn = sqlite3.connect(TEST_DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    def test_delete_product(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO products (itemId, product_type_id, metadataHash, manufacturer_email)
            VALUES (?, ?, ?, ?)
        """, (202, 'Bottle', 'hash202', 'maker@example.com'))
        conn.commit()
        conn.close()

        with self.client.session_transaction() as sess:
            sess['user_email'] = 'maker@example.com'
            sess['role'] = 'manufacturer'
            sess['name'] = 'Maker'

        response = self.client.post('/delete-item', data={
            'itemId': '202'
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/manufacturer/item', response.location)

        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE itemId=?", (202,))
        product = cur.fetchone()
        conn.close()

        self.assertIsNone(product)


if __name__ == '__main__':
    unittest.main()