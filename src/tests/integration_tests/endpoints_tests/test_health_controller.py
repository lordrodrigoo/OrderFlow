from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.api.dependencies import get_db


client = TestClient(app, base_url="http://localhost")

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "ok"}

def test_health_check_db_failure():
    mock_db = MagicMock()
    mock_db.session.execute.side_effect = Exception("DB connection failed")

    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db
    response = client.get("/health")
    app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {"detail": "Service unhealthy"}
