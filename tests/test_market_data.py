import pytest
from src.models.schemas import HistoricalBar
from src.data.market_data import MarketDataService

def test_calculate_indicators():
    service = MarketDataService()
    bars = [
        HistoricalBar(timestamp=f"2026-07-{i:02d}", open=100+i, high=105+i, low=99+i, close=102+i, volume=1000)
        for i in range(1, 19)
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
