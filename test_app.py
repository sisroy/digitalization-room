import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_and_allocation(client):
    # Simulate file uploads (you may need sample files for testing)
    group_csv = open('tests/test_groups.csv', 'rb')
    hostel_csv = open('tests/test_hostel_rooms.csv', 'rb')

    # Send POST request to /upload endpoint
    response = client.post('/upload', data={
        'group_csv': (group_csv, 'test_groups.csv'),
        'hostel_csv': (hostel_csv, 'test_hostel_rooms.csv')
    }, content_type='multipart/form-data')

    assert response.status_code == 200
    assert b'Room Allocation Results' in response.data
    # Add more assertions to verify specific output or behavior
