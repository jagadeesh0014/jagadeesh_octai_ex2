import sys
sys.path.append('..')
from app import app

def test_home_endpoint():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_health_endpoint():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_add_endpoint():
    client = app.test_client()
    response = client.get('/add/2/3')
    assert response.status_code == 200
    assert response.json['result'] == 5