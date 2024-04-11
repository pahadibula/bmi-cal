import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"BMI Calculator" in response.data

def test_result_page(client):
    response = client.post('/result/', json={"bmi": 22.22, "status": "Healthy", "height": 180, "weight": 72})
    assert response.status_code == 200
    assert b"You are <strong id=\"statuscolor\">Healthy</strong> and your BMI is <strong id=\"statuscolor1\">22.22</strong>" in response.data

def test_metrics_endpoint(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'http_requests_total' in response.data
    assert b'http_request_duration_seconds' in response.data
    assert b'current_users' in response.data
    assert b'processing_time_seconds' in response.data

def test_invalid_input(client):
    data = {'bmi': '', 'status': '', 'height': '', 'weight': ''}
    response = client.post('/result/', json=data)
    assert response.status_code == 400  # Check that the server responds with a bad request status code
    assert b'Invalid or missing input data' in response.data  # Check for an appropriate error message in the response
