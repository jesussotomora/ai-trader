import pytest
from unittest.mock import patch, MagicMock
from src.brokers.alpaca_adapter import AlpacaAdapter

@patch("requests.get")
def test_get_account_info(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "ACCOUNT123",
        "cash": "100000.00",
        "portfolio_value": "105000.00",
        "buying_power": "400000.00",
        "currency": "USD"
    }
    mock_get.return_value = mock_response

    adapter = AlpacaAdapter(api_key="TEST_KEY", secret_key="TEST_SECRET")
    acc = adapter.get_account()

    assert acc["id"] == "ACCOUNT123"
    assert acc["cash"] == "100000.00"
    mock_get.assert_called_once_with(
        "https://paper-api.alpaca.markets/v2/account",
        headers={"APCA-API-KEY-ID": "TEST_KEY", "APCA-API-SECRET-KEY": "TEST_SECRET"}
    )
