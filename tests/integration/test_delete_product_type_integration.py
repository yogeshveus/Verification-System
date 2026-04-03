import unittest
import sqlite3
import os

from app import create_app
from config import TEST_DATABASE
from database.db import init_db


class DeleteProductTypeIntegrationTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        self.app = create_app({
            'TESTING': True,
            'DATABASE': TEST_DATABASE
        })
        self.client = self.app.test_client()

        init_db(TEST_DATABASE)

    def get_db_connection(self):
        conn = sqlite3.connect(TEST_DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    def test_delete_product_type(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO product_types (name, created_by, is_active)
            VALUES (?, ?, ?)
        """, ('Toy', 'maker@example.com', 1))
        conn.commit()
        conn.close()

        with self.client.session_transaction() as sess:
            sess['user_email'] = 'maker@example.com'
            sess['role'] = 'manufacturer'
            sess['name'] = 'Maker'

        response = self.client.post('/delete-product-type', data={
            'product': 'Toy'
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/manufacturer/item', response.location)

        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM product_types WHERE name=?", ('Toy',))
        product = cur.fetchone()
        conn.close()

        self.assertIsNotNone(product)
        self.assertEqual(product['is_active'], 0)


if __name__ == '__main__':
    unittest.main()