import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from app import app, db

class AgentServiceIntegrationTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_full_crud(self):
        # Create
        res = self.client.post('/agents', json={'agent_id': 'A001', 'name': 'Alice', 'branch': 'West'})
        self.assertEqual(res.status_code, 201)

        # Read
        res = self.client.get('/agents/A001')
        data = res.get_json()
        self.assertEqual(data['name'], 'Alice')

        # Update
        res = self.client.put('/agents/A001', json={'name': 'Alice Updated'})
        data = res.get_json()
        self.assertEqual(data['name'], 'Alice Updated')

        # Delete
        res = self.client.delete('/agents/A001')
        self.assertEqual(res.status_code, 200)

        # Verify deletion
        res = self.client.get('/agents/A001')
        self.assertEqual(res.status_code, 404)

if __name__ == '__main__':
    unittest.main()
