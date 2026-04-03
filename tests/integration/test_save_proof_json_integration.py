import unittest
import os
import json
import shutil
from app import create_app
from config import TEST_DATABASE


class SaveProofJsonIntegrationTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        self.app = create_app({
            'TESTING': True,
            'DATABASE': TEST_DATABASE
        })
        self.client = self.app.test_client()

        self.proof_path = os.path.join(self.app.root_path, "static", "generated", "proofData.json")
        self.backup_path = self.proof_path + ".backup"

        os.makedirs(os.path.dirname(self.proof_path), exist_ok=True)

        # Backup real proofData.json if it exists
        if os.path.exists(self.proof_path):
            shutil.copy2(self.proof_path, self.backup_path)


    def tearDown(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        if os.path.exists(self.proof_path):
            os.remove(self.proof_path)

        if os.path.exists(self.backup_path):
            shutil.move(self.backup_path, self.proof_path)

    def test_save_proof_json(self):
        with self.client.session_transaction() as sess:
            sess['user_email'] = 'maker@example.com'
            sess['role'] = 'manufacturer'
            sess['name'] = 'Maker'

        proof_data = {
            "a": ["1", "2"],
            "b": [["3", "4"], ["5", "6"]],
            "c": ["7", "8"],
            "publicSignals": ["9"]
        }

        response = self.client.post('/save-proof-json', json=proof_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)
        self.assertTrue(os.path.exists(self.proof_path))

        with open(self.proof_path, 'r') as f:
            saved_data = json.load(f)

        self.assertEqual(saved_data, proof_data)


if __name__ == '__main__':
    unittest.main()