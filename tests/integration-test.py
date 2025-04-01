import pytest
import os
import requests

BASE_URL = os.getenv('BASE_URL', 'http://localhost:5002')

# Sample test data for an agent
test_agent = {
    "agent_id": "A111",
    "name": "Senura",
    "branch": "Colombo"
}

@pytest.fixture(scope='function', autouse=True)
def cleanup_database():
    """Cleanup after each test by deleting the test agent."""
    # Run the test first.
    yield
    # Attempt to delete the test agent.
    # This assumes the DELETE endpoint is idempotent or returns a success even if the record doesn't exist.
    requests.delete(f"{BASE_URL}/{test_agent['agent_id']}")

def test_create_agent():
    # Create the agent via POST request.
    response = requests.post(f"{BASE_URL}/", json=test_agent)
    assert response.status_code == 201
    data = response.json()
    assert data['agent_id'] == test_agent['agent_id']

def test_get_agent():
    # Insert the agent first.
    create_resp = requests.post(f"{BASE_URL}/", json=test_agent)
    assert create_resp.status_code == 201

    # Retrieve the agent via GET request.
    response = requests.get(f"{BASE_URL}/{test_agent['agent_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data['agent_id'] == test_agent['agent_id']

def test_update_agent():
    # Insert the agent first.
    create_resp = requests.post(f"{BASE_URL}/", json=test_agent)
    assert create_resp.status_code == 201

    # Update the agent's branch.
    update_data = {"branch": "kalutara"}
    response = requests.put(f"{BASE_URL}/{test_agent['agent_id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['branch'] == update_data['branch']

def test_delete_agent():
    # Insert the agent first.
    create_resp = requests.post(f"{BASE_URL}/", json=test_agent)
    assert create_resp.status_code == 201

    # Delete the agent.
    response = requests.delete(f"{BASE_URL}/{test_agent['agent_id']}")
    assert response.status_code == 200
    assert response.json()['message'] == 'Agent deleted'

    # Verify deletion: a GET request should return a 404.
    get_resp = requests.get(f"{BASE_URL}/{test_agent['agent_id']}")
    assert get_resp.status_code == 404
