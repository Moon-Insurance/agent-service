import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Agent

class AgentServiceUnitTest(unittest.TestCase):
    def setUp(self):
        # Configure test database (use in-memory SQLite for unit testing)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_agent(self):
        response = self.app.post('/agents', json={
            'agent_id': 'A123', 'name': 'John Doe', 'branch': 'North'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['agent_id'], 'A123')

if __name__ == '__main__':
    unittest.main()
