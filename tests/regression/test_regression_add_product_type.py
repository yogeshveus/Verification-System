import unittest
import sqlite3
import os

from app import create_app
from config import TEST_DATABASE
from database.db import init_db


class RegressionAddProductTypeTest(unittest.TestCase):

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

    def test_add_product_type_still_works(self):
        with self.client.session_transaction() as sess:
            sess['user_email'] = 'maker@example.com'
            sess['role'] = 'manufacturer'
            sess['name'] = 'Maker'

        response = self.client.post('/add-product-type', data={
            'newProduct': 'Milk Powder'
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/manufacturer/item', response.location)

        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM product_types WHERE name=? AND created_by=?", ('Milk Powder', 'maker@example.com'))
        product = cur.fetchone()
        conn.close()

        self.assertIsNotNone(product)


if __name__ == '__main__':
    unittest.main()