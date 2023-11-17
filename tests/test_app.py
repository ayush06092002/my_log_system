import json
from app import app, db, Log

def test_ingest_log_success():
    log_data = {
        "level": "error",
        "message": "Failed to connect to DB",
        "resourceId": "server-1234",
        "timestamp": "2023-09-15T08:00:00Z",
        "traceId": "abc-xyz-123",
        "spanId": "span-456",
        "commit": "5e5342f",
        "metadata": {
            "parentResourceId": "server-0987"
        }
    }

    with app.test_client() as client:
        response = client.post('/ingest', json=log_data)
        assert response.status_code == 200

def test_ingest_log_missing_field():
    log_data = {
        "level": "error",
        "message": "Failed to connect to DB",
        "timestamp": "2023-09-15T08:00:00Z",
        "traceId": "abc-xyz-123",
        "spanId": "span-456",
        "commit": "5e5342f",
        "metadata": {
            "parentResourceId": "server-0987"
        }
    }

    with app.test_client() as client:
        response = client.post('/ingest', json=log_data)
        assert response.status_code == 400

def test_query_logs_by_level():
    with app.test_client() as client:
        response = client.get('/query?level=error')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert len(data) > 0

def test_query_logs_by_resource_id():
    with app.test_client() as client:
        response = client.get('/query?resourceId=server-1234')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert len(data) > 0

def test_query_logs_by_date_range():
    with app.test_client() as client:
        response = client.get('/query?start_date=2023-09-15T00:00:00Z&end_date=2023-09-16T23:59:59Z')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert len(data) > 0
