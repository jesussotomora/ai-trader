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
