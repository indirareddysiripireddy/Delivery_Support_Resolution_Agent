from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_chat_requires_authentication():
    response = client.post("/api/v1/chat", json={"message": "Track DS-1001"})

    assert response.status_code == 401


def test_chat_returns_safe_workflow_status_and_evidence():
    response = client.post(
        "/api/v1/chat",
        headers={"Authorization": "Bearer dev-demo-token"},
        json={"message": "My order DS-1001 says delivered but I didn't receive it."},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "DELIVERED_NOT_RECEIVED"
    assert payload["delivery"]["status"] == "delivered"
    assert payload["evidence"][0]["source"] == "delivered_not_received.md"
    assert "tool_results" not in payload