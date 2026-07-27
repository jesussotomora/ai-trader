# Alpaca Paper Trading Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `AlpacaAdapter` in `src/brokers/alpaca_adapter.py` to communicate with Alpaca Securities Paper Trading REST API, fetching account balances, retrieving positions, submitting market/limit paper orders, and cancelling open orders.

**Architecture:** Python `AlpacaAdapter` class utilizing `requests` to interact with `https://paper-api.alpaca.markets/v2`, covered with unit tests using `unittest.mock` for mock HTTP responses.

**Tech Stack:** Python 3.9+, requests, pytest, unittest.mock.

## Global Constraints

- Must target Alpaca Paper API default base URL `https://paper-api.alpaca.markets/v2`.
- Must send `APCA-API-KEY-ID` and `APCA-API-SECRET-KEY` headers.
- Full test coverage required using mocks (no external network dependency during tests).
- All commits must follow conventional commits (`feat:`, `test:`).

---

### Task 1: Core AlpacaAdapter Implementation & Account Info

**Files:**
- Create: `src/brokers/alpaca_adapter.py`
- Create: `tests/test_alpaca_adapter.py`

**Interfaces:**
- Consumes: `requests`, `src/models/schemas.py`
- Produces: `AlpacaAdapter.get_account()`, `AlpacaAdapter.get_positions()`

- [ ] **Step 1: Write failing AlpacaAdapter account test**

```python
# tests/test_alpaca_adapter.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/pytest tests/test_alpaca_adapter.py`  
Expected: FAIL with `ModuleNotFoundError: No module named 'src.brokers.alpaca_adapter'`

- [ ] **Step 3: Implement AlpacaAdapter in `src/brokers/alpaca_adapter.py`**

```python
# src/brokers/alpaca_adapter.py
import requests
from typing import Dict, List, Optional


class AlpacaAdapter:
    def __init__(
        self,
        api_key: str = "",
        secret_key: str = "",
        base_url: str = "https://paper-api.alpaca.markets/v2"
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key
        }

    def get_account(self) -> Dict:
        url = f"{self.base_url}/account"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_positions(self) -> List[Dict]:
        url = f"{self.base_url}/positions"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/pytest tests/test_alpaca_adapter.py`  
Expected: PASS

- [ ] **Step 5: Commit core AlpacaAdapter**

```bash
git add src/brokers/alpaca_adapter.py tests/test_alpaca_adapter.py
git commit -m "feat: implement AlpacaAdapter account and positions retrieval"
```

---

### Task 2: Order Submission & Order Cancellation

**Files:**
- Modify: `src/brokers/alpaca_adapter.py`
- Modify: `tests/test_alpaca_adapter.py`

**Interfaces:**
- Consumes: `requests`
- Produces: `AlpacaAdapter.submit_order(symbol, qty, side, type, time_in_force)`, `AlpacaAdapter.cancel_all_orders()`

- [ ] **Step 1: Write failing order submission and cancellation tests**

```python
# Add to tests/test_alpaca_adapter.py
@patch("requests.post")
def test_submit_order(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "ORDER_123",
        "client_order_id": "client_1",
        "symbol": "AAPL",
        "qty": "10",
        "side": "buy",
        "type": "market",
        "status": "new"
    }
    mock_post.return_value = mock_response

    adapter = AlpacaAdapter(api_key="TEST_KEY", secret_key="TEST_SECRET")
    order = adapter.submit_order(symbol="AAPL", qty=10, side="buy")

    assert order["id"] == "ORDER_123"
    assert order["symbol"] == "AAPL"
    assert order["side"] == "buy"
    mock_post.assert_called_once()

@patch("requests.delete")
def test_cancel_all_orders(mock_delete):
    mock_response = MagicMock()
    mock_response.status_code = 207
    mock_response.json.return_value = [{"id": "ORDER_123", "status": 200}]
    mock_delete.return_value = mock_response

    adapter = AlpacaAdapter(api_key="TEST_KEY", secret_key="TEST_SECRET")
    res = adapter.cancel_all_orders()

    assert res is True
    mock_delete.assert_called_once_with(
        "https://paper-api.alpaca.markets/v2/orders",
        headers={"APCA-API-KEY-ID": "TEST_KEY", "APCA-API-SECRET-KEY": "TEST_SECRET"}
    )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/pytest tests/test_alpaca_adapter.py::test_submit_order`  
Expected: FAIL with `AttributeError: 'AlpacaAdapter' object has no attribute 'submit_order'`

- [ ] **Step 3: Implement `submit_order` and `cancel_all_orders` in `src/brokers/alpaca_adapter.py`**

```python
# Add methods to AlpacaAdapter class in src/brokers/alpaca_adapter.py
    def submit_order(
        self,
        symbol: str,
        qty: float,
        side: str = "buy",
        order_type: str = "market",
        time_in_force: str = "gtc"
    ) -> Dict:
        url = f"{self.base_url}/orders"
        payload = {
            "symbol": symbol.upper(),
            "qty": str(qty),
            "side": side.lower(),
            "type": order_type.lower(),
            "time_in_force": time_in_force.lower()
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def cancel_all_orders(self) -> bool:
        url = f"{self.base_url}/orders"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return True
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/pytest tests/test_alpaca_adapter.py`  
Expected: PASS

- [ ] **Step 5: Commit order execution methods**

```bash
git add src/brokers/alpaca_adapter.py tests/test_alpaca_adapter.py
git commit -m "feat: add submit_order and cancel_all_orders methods to AlpacaAdapter"
```

---

### Task 3: Integration & Full Test Suite Run

**Files:**
- Modify: `tests/test_integration.py`

- [ ] **Step 1: Write integration test for AlpacaAdapter with RiskManager**

```python
# Add to tests/test_integration.py
from unittest.mock import patch, MagicMock
from src.brokers.alpaca_adapter import AlpacaAdapter
from src.models.schemas import TradeSignal, SignalAction, PortfolioState
from src.risk.risk_manager import RiskManager

@patch("requests.post")
def test_alpaca_adapter_integration(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "ORD_TEST_99", "status": "accepted"}
    mock_post.return_value = mock_response

    # Signal & Risk check
    signal = TradeSignal(
        ticker="AAPL", action=SignalAction.BUY, confidence_score=85.0,
        stop_loss=170.0, take_profit=200.0, reasoning_thesis="Buy signal",
        invalidation_criteria="N/A", advisor_model="Claude-3.5-Sonnet"
    )
    risk_mgr = RiskManager()
    portfolio = PortfolioState(account_id="A1", cash_balance=5000.0, total_equity=10000.0, realized_pnl=0.0, unrealized_pnl=0.0)
    approved, _ = risk_mgr.validate_trade(signal, trade_amount=500.0, portfolio=portfolio)
    assert approved

    # Execute via AlpacaAdapter
    adapter = AlpacaAdapter(api_key="KEY", secret_key="SECRET")
    order = adapter.submit_order(symbol=signal.ticker, qty=3.0, side="buy")
    assert order["id"] == "ORD_TEST_99"
```

- [ ] **Step 2: Run full test suite to verify 100% pass rate**

Run: `./.venv/bin/pytest -v`  
Expected: PASS (all tests pass across schemas, scraper, compliance, risk, engine, backtest, alpaca, integration)

- [ ] **Step 3: Commit integration update**

```bash
git add tests/test_integration.py
git commit -m "test: add AlpacaAdapter integration test to pipeline test suite"
```
