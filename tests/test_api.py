
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import database


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use an isolated temporary SQLite database
    test_db = tmp_path / "test_kubeguard.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    with TestClient(app) as test_client:
        yield test_client


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"
    assert response.json()["version"] == "0.3.0"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_create_security_event(client):
    payload = {
        "event_type": "brute_force_attempt",
        "severity": "high",
        "source": "192.168.1.50",
        "description": "Multiple failed SSH logins"
    }

    response = client.post("/events", json=payload)

    assert response.status_code == 201
    assert response.json()["severity"] == "high"
    assert "id" in response.json()
    assert "timestamp" in response.json()


def test_invalid_severity(client):
    payload = {
        "event_type": "failed_login",
        "severity": "extreme",
        "source": "192.168.1.50",
        "description": "Invalid severity test"
    }

    response = client.post("/events", json=payload)

    assert response.status_code == 422


def test_get_security_events(client):
    payload = {
        "event_type": "failed_login",
        "severity": "medium",
        "source": "10.0.0.10",
        "description": "Failed login attempt"
    }

    create_response = client.post("/events", json=payload)
    assert create_response.status_code == 201

    response = client.get("/events")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["event_type"] == "failed_login"


def test_sqlite_persistence(client):
    payload = {
        "event_type": "port_scan",
        "severity": "critical",
        "source": "10.0.0.20",
        "description": "Network scanning detected"
    }

    response = client.post("/events", json=payload)
    assert response.status_code == 201

    # Verify the event was stored in SQLite
    stored_events = database.get_events()

    assert len(stored_events) == 1
    assert stored_events[0].event_type == "port_scan"
    assert stored_events[0].severity == "critical"
