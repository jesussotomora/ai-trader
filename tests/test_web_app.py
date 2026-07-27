import pytest
from fastapi.testclient import TestClient
from src.web.app import app

client = TestClient(app)

def test_api_leaderboard():
    response = client.get("/api/leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_api_backtest():
    payload = {"ticker": "TSLA", "starting_capital": 1000.0}
    response = client.post("/api/backtest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "TSLA"
    assert "total_return_pct" in data

def test_api_prompt():
    payload = {"ticker": "AAPL", "mock_text": "Apple announces revolutionary product"}
    response = client.post("/api/prompt", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prompt" in data
    assert "AAPL" in data["prompt"]
