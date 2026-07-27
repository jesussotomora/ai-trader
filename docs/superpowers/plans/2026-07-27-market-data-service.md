# Market Data Feed Service Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `MarketDataService` in `src/data/market_data.py` to retrieve current market prices, historical OHLCV bars, and calculate technical indicators (SMA_15, RSI, % Change) for stock and crypto tickers.

**Architecture:** Python `MarketDataService` utilizing `yfinance` / `requests` with local caching, generating `HistoricalBar` models and technical analysis dictionaries.

**Tech Stack:** Python 3.9+, yfinance, pydantic, pytest.

## Global Constraints

- Must output list of `HistoricalBar` Pydantic models.
- Technical indicators calculation must handle edge cases gracefully (e.g. fewer bars than period).
- All unit tests must use mocks or synthetic data without requiring active internet connectivity.

---

### Task 1: MarketDataService & Indicator Calculation

**Files:**
- Create: `src/data/market_data.py`
- Create: `tests/test_market_data.py`

**Interfaces:**
- Consumes: `src/models/schemas.py` (`HistoricalBar`)
- Produces: `MarketDataService.calculate_indicators(bars)`, `MarketDataService.get_synthetic_bars(ticker, count)`

- [ ] **Step 1: Write failing market data test**

```python
# tests/test_market_data.py
import pytest
from src.models.schemas import HistoricalBar
from src.data.market_data import MarketDataService

def test_calculate_indicators():
    service = MarketDataService()
    bars = [
        HistoricalBar(timestamp=f"2026-07-{i:02d}", open=100+i, high=105+i, low=99+i, close=102+i, volume=1000)
        for i in range(1, 20)
    ]
    indicators = service.calculate_indicators(bars)
    
    assert "sma_15" in indicators
    assert "current_price" in indicators
    assert "price_change_pct" in indicators
    assert indicators["current_price"] == 120.0
    assert round(indicators["sma_15"], 2) > 100.0

def test_get_synthetic_bars():
    service = MarketDataService()
    bars = service.get_synthetic_bars(ticker="AAPL", count=10)
    assert len(bars) == 10
    assert bars[-1].close > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/pytest tests/test_market_data.py`  
Expected: FAIL with `ModuleNotFoundError: No module named 'src.data.market_data'`

- [ ] **Step 3: Implement MarketDataService in `src/data/market_data.py`**

```python
# src/data/market_data.py
import random
from typing import List, Dict
from src.models.schemas import HistoricalBar


class MarketDataService:
    def calculate_indicators(self, bars: List[HistoricalBar]) -> Dict[str, float]:
        if not bars:
            return {"current_price": 0.0, "sma_15": 0.0, "price_change_pct": 0.0, "rsi_14": 50.0}

        closes = [b.close for b in bars]
        current_price = closes[-1]
        first_price = closes[0]

        # Calculate SMA 15
        period = 15
        if len(closes) >= period:
            sma_15 = sum(closes[-period:]) / period
        else:
            sma_15 = sum(closes) / len(closes)

        # Price Change %
        price_change_pct = ((current_price - first_price) / first_price) * 100.0 if first_price > 0 else 0.0

        # Simplified RSI Calculation
        gains, losses = [], []
        for i in range(1, len(closes)):
            diff = closes[i] - closes[i - 1]
            if diff >= 0:
                gains.append(diff)
            else:
                losses.append(abs(diff))

        avg_gain = (sum(gains) / len(gains)) if gains else 0.0
        avg_loss = (sum(losses) / len(losses)) if losses else 0.0

        if avg_loss == 0:
            rsi = 100.0 if avg_gain > 0 else 50.0
        else:
            rs = avg_gain / avg_loss
            rsi = 100.0 - (100.0 / (1.0 + rs))

        return {
            "current_price": round(current_price, 2),
            "sma_15": round(sma_15, 2),
            "price_change_pct": round(price_change_pct, 2),
            "rsi_14": round(rsi, 2)
        }

    def get_synthetic_bars(self, ticker: str, count: int = 15, base_price: float = 150.0) -> List[HistoricalBar]:
        bars = []
        price = base_price
        for i in range(1, count + 1):
            change = random.uniform(-2.0, 2.5)
            open_p = price
            close_p = max(1.0, open_p + change)
            high_p = max(open_p, close_p) + random.uniform(0.1, 1.0)
            low_p = min(open_p, close_p) - random.uniform(0.1, 1.0)
            vol = float(random.randint(10000, 50000))
            
            bars.append(HistoricalBar(
                timestamp=f"2026-07-{i:02d}",
                open=round(open_p, 2),
                high=round(high_p, 2),
                low=round(low_p, 2),
                close=round(close_p, 2),
                volume=vol
            ))
            price = close_p
        return bars
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/pytest tests/test_market_data.py`  
Expected: PASS

- [ ] **Step 5: Commit MarketDataService**

```bash
git add src/data/market_data.py tests/test_market_data.py
git commit -m "feat: implement MarketDataService for technical indicators and historical bar generation"
```

---

### Task 2: Integration into Master Test Suite

**Files:**
- Modify: `tests/test_integration.py`

- [ ] **Step 1: Add MarketDataService to integration test**

```python
# Add to tests/test_integration.py
from src.data.market_data import MarketDataService

def test_market_data_integration():
    data_svc = MarketDataService()
    bars = data_svc.get_synthetic_bars("NVDA", count=20, base_price=120.0)
    indicators = data_svc.calculate_indicators(bars)
    
    assert indicators["current_price"] > 0
    assert 0 <= indicators["rsi_14"] <= 100
```

- [ ] **Step 2: Run full test suite**

Run: `./.venv/bin/pytest -v`  
Expected: PASS (all tests pass)

- [ ] **Step 3: Commit integration update**

```bash
git add tests/test_integration.py
git commit -m "test: add MarketDataService integration test to test suite"
```
