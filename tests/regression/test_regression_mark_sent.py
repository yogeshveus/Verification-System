import unittest
import sqlite3
import os

from app import create_app
from config import TEST_DATABASE
from database.db import init_db


class RegressionMarkSentTest(unittest.TestCase):

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

    def test_mark_sent_still_works(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO products (itemId, product_type_id, metadataHash, manufacturer_email, sent)
            VALUES (?, ?, ?, ?, ?)
        """, (303, 'Diapers', '0x123', 'maker@example.com', 0))
        conn.commit()
        conn.close()

        response = self.client.post('/mark-sent', json={'itemId': 303})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)

        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE itemId=?", (303,))
        product = cur.fetchone()
        conn.close()

        self.assertEqual(product['sent'], 1)


if __name__ == '__main__':
    unittest.main()