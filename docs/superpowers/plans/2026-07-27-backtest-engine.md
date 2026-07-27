# Backtest Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a high-performance Python `BacktestEngine` for `ai-trader` to simulate `TradeSignal` performance against historical OHLCV bar data, calculating Total Return %, Win Rate %, Max Drawdown %, Profit Factor, and executed trades log.

**Architecture:** Extend `src/models/schemas.py` with `HistoricalBar` and `BacktestResult`, build `BacktestEngine` in `src/engine/backtest.py`, and cover with pytest unit/integration tests.

**Tech Stack:** Python 3.9+, Pydantic v2, pytest.

## Global Constraints

- All models must inherit from Pydantic `BaseModel`.
- `BacktestEngine` must be deterministic and pure-Python without external API calls.
- Unit test coverage required for every module before implementation.

---

### Task 1: Backtest Schemas (`HistoricalBar` & `BacktestResult`)

**Files:**
- Modify: `src/models/schemas.py`
- Modify: `tests/test_schemas.py`

**Interfaces:**
- Consumes: `pydantic`
- Produces: `HistoricalBar`, `BacktestResult`, `ExecutedTrade`

- [ ] **Step 1: Write failing backtest schema test**

```python
# Add to tests/test_schemas.py
from src.models.schemas import HistoricalBar, BacktestResult, ExecutedTrade, SignalAction

def test_backtest_result_schema():
    bar = HistoricalBar(
        timestamp="2026-07-26T10:00:00Z",
        open=100.0,
        high=105.0,
        low=98.0,
        close=104.0,
        volume=10000.0
    )
    assert bar.close == 104.0

    trade = ExecutedTrade(
        ticker="AAPL",
        action=SignalAction.BUY,
        entry_price=100.0,
        exit_price=105.0,
        quantity=10.0,
        pnl=50.0,
        pnl_pct=5.0,
        exit_reason="TAKE_PROFIT"
    )
    assert trade.pnl == 50.0

    result = BacktestResult(
        ticker="AAPL",
        starting_capital=1000.0,
        ending_capital=1050.0,
        total_return_pct=5.0,
        win_rate_pct=100.0,
        max_drawdown_pct=2.0,
        total_trades=1,
        winning_trades=1,
        losing_trades=0,
        profit_factor=0.0,
        executed_trades=[trade]
    )
    assert result.total_return_pct == 5.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/pytest tests/test_schemas.py::test_backtest_result_schema`  
Expected: FAIL with `ImportError: cannot import name 'HistoricalBar'`

- [ ] **Step 3: Implement Backtest schemas in `src/models/schemas.py`**

```python
# Append to src/models/schemas.py
class HistoricalBar(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class ExecutedTrade(BaseModel):
    ticker: str
    action: SignalAction
    entry_price: float
    exit_price: float
    quantity: float
    pnl: float
    pnl_pct: float
    exit_reason: str


class BacktestResult(BaseModel):
    ticker: str
    starting_capital: float
    ending_capital: float
    total_return_pct: float
    win_rate_pct: float
    max_drawdown_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    profit_factor: float
    executed_trades: List[ExecutedTrade] = Field(default_factory=list)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/pytest tests/test_schemas.py::test_backtest_result_schema`  
Expected: PASS

- [ ] **Step 5: Commit backtest schemas**

```bash
git add src/models/schemas.py tests/test_schemas.py
git commit -m "feat: add HistoricalBar, ExecutedTrade, and BacktestResult schemas"
```

---

### Task 2: Core BacktestEngine Implementation

**Files:**
- Create: `src/engine/backtest.py`
- Create: `tests/test_backtest.py`

**Interfaces:**
- Consumes: `TradeSignal`, `HistoricalBar`, `BacktestResult`, `ExecutedTrade`
- Produces: `BacktestEngine.run_simulation(ticker, starting_capital, bars, signals)`

- [ ] **Step 1: Write failing BacktestEngine tests**

```python
# tests/test_backtest.py
from src.models.schemas import HistoricalBar, TradeSignal, SignalAction
from src.engine.backtest import BacktestEngine

def test_backtest_engine_buy_and_take_profit():
    bars = [
        HistoricalBar(timestamp="2026-07-01", open=100.0, high=101.0, low=99.0, close=100.0, volume=1000.0),
        HistoricalBar(timestamp="2026-07-02", open=100.0, high=110.0, low=99.0, close=108.0, volume=1000.0),  # Hits take profit at 108
    ]
    
    signals = [
        TradeSignal(
            ticker="TSLA",
            action=SignalAction.BUY,
            confidence_score=85.0,
            stop_loss=95.0,
            take_profit=105.0,
            reasoning_thesis="Breakout test",
            invalidation_criteria="Drop below 95",
            advisor_model="Claude-3.5-Sonnet"
        )
    ]
    
    engine = BacktestEngine()
    result = engine.run_simulation(ticker="TSLA", starting_capital=1000.0, bars=bars, signals=signals)
    
    assert result.total_trades == 1
    assert result.winning_trades == 1
    assert result.win_rate_pct == 100.0
    assert result.executed_trades[0].exit_reason == "TAKE_PROFIT"
    assert result.ending_capital > 1000.0

def test_backtest_engine_stop_loss():
    bars = [
        HistoricalBar(timestamp="2026-07-01", open=100.0, high=101.0, low=99.0, close=100.0, volume=1000.0),
        HistoricalBar(timestamp="2026-07-02", open=99.0, high=99.5, low=90.0, close=91.0, volume=1000.0),  # Hits stop loss at 95
    ]
    
    signals = [
        TradeSignal(
            ticker="TSLA",
            action=SignalAction.BUY,
            confidence_score=85.0,
            stop_loss=95.0,
            take_profit=110.0,
            reasoning_thesis="Fail test",
            invalidation_criteria="N/A",
            advisor_model="Claude-3.5-Sonnet"
        )
    ]
    
    engine = BacktestEngine()
    result = engine.run_simulation(ticker="TSLA", starting_capital=1000.0, bars=bars, signals=signals)
    
    assert result.total_trades == 1
    assert result.losing_trades == 1
    assert result.win_rate_pct == 0.0
    assert result.executed_trades[0].exit_reason == "STOP_LOSS"
    assert result.ending_capital < 1000.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/pytest tests/test_backtest.py`  
Expected: FAIL with `ModuleNotFoundError: No module named 'src.engine.backtest'`

- [ ] **Step 3: Implement BacktestEngine in `src/engine/backtest.py`**

```python
# src/engine/backtest.py
from typing import List
from src.models.schemas import (
    HistoricalBar, TradeSignal, SignalAction, BacktestResult, ExecutedTrade
)

class BacktestEngine:
    def run_simulation(
        self,
        ticker: str,
        starting_capital: float,
        bars: List[HistoricalBar],
        signals: List[TradeSignal]
    ) -> BacktestResult:
        if not bars:
            return BacktestResult(
                ticker=ticker,
                starting_capital=starting_capital,
                ending_capital=starting_capital,
                total_return_pct=0.0,
                win_rate_pct=0.0,
                max_drawdown_pct=0.0,
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                profit_factor=0.0,
                executed_trades=[]
            )

        capital = starting_capital
        peak_capital = starting_capital
        max_drawdown = 0.0
        executed_trades: List[ExecutedTrade] = []

        active_position = None  # (signal, entry_price, quantity)

        signal_idx = 0
        for bar in bars:
            # Check active position for exit conditions
            if active_position:
                sig, entry_price, qty = active_position
                
                # Check Stop Loss
                if bar.low <= sig.stop_loss:
                    exit_price = sig.stop_loss
                    pnl = (exit_price - entry_price) * qty
                    pnl_pct = ((exit_price - entry_price) / entry_price) * 100.0
                    capital += pnl
                    executed_trades.append(ExecutedTrade(
                        ticker=ticker,
                        action=sig.action,
                        entry_price=entry_price,
                        exit_price=exit_price,
                        quantity=qty,
                        pnl=pnl,
                        pnl_pct=pnl_pct,
                        exit_reason="STOP_LOSS"
                    ))
                    active_position = None

                # Check Take Profit
                elif bar.high >= sig.take_profit:
                    exit_price = sig.take_profit
                    pnl = (exit_price - entry_price) * qty
                    pnl_pct = ((exit_price - entry_price) / entry_price) * 100.0
                    capital += pnl
                    executed_trades.append(ExecutedTrade(
                        ticker=ticker,
                        action=sig.action,
                        entry_price=entry_price,
                        exit_price=exit_price,
                        quantity=qty,
                        pnl=pnl,
                        pnl_pct=pnl_pct,
                        exit_reason="TAKE_PROFIT"
                    ))
                    active_position = None

            # Process new signal if no active position
            if not active_position and signal_idx < len(signals):
                sig = signals[signal_idx]
                if sig.action == SignalAction.BUY:
                    entry_price = bar.close
                    qty = (capital * 0.95) / entry_price  # 95% position sizing
                    active_position = (sig, entry_price, qty)
                signal_idx += 1

            # Update Peak Capital & Max Drawdown
            if capital > peak_capital:
                peak_capital = capital
            drawdown = ((peak_capital - capital) / peak_capital) * 100.0
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        # Calculate Summary Metrics
        total_trades = len(executed_trades)
        winning_trades = sum(1 for t in executed_trades if t.pnl > 0)
        losing_trades = sum(1 for t in executed_trades if t.pnl < 0)
        win_rate = (winning_trades / total_trades * 100.0) if total_trades > 0 else 0.0
        total_return = ((capital - starting_capital) / starting_capital) * 100.0

        gross_gains = sum(t.pnl for t in executed_trades if t.pnl > 0)
        gross_losses = abs(sum(t.pnl for t in executed_trades if t.pnl < 0))
        profit_factor = (gross_gains / gross_losses) if gross_losses > 0 else (gross_gains if gross_gains > 0 else 0.0)

        return BacktestResult(
            ticker=ticker,
            starting_capital=starting_capital,
            ending_capital=capital,
            total_return_pct=total_return,
            win_rate_pct=win_rate,
            max_drawdown_pct=max_drawdown,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            profit_factor=profit_factor,
            executed_trades=executed_trades
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/pytest tests/test_backtest.py`  
Expected: PASS

- [ ] **Step 5: Commit BacktestEngine**

```bash
git add src/engine/backtest.py tests/test_backtest.py
git commit -m "feat: implement BacktestEngine with OHLCV simulation, win rate, drawdown, and profit factor"
```

---

### Task 3: Master Integration & Full Test Suite Verification

**Files:**
- Modify: `tests/test_integration.py`

- [ ] **Step 1: Write integration test for BacktestEngine**

```python
# Add to tests/test_integration.py
from src.engine.backtest import BacktestEngine
from src.models.schemas import HistoricalBar, TradeSignal, SignalAction

def test_integration_with_backtest_engine():
    bars = [
        HistoricalBar(timestamp="2026-07-01", open=50.0, high=52.0, low=49.0, close=51.0, volume=5000.0),
        HistoricalBar(timestamp="2026-07-02", open=51.0, high=60.0, low=50.0, close=58.0, volume=5000.0),  # Hits Take Profit at 55
    ]
    signals = [
        TradeSignal(
            ticker="AMD",
            action=SignalAction.BUY,
            confidence_score=80.0,
            stop_loss=48.0,
            take_profit=55.0,
            reasoning_thesis="Integration test",
            invalidation_criteria="N/A",
            advisor_model="Consensus"
        )
    ]
    engine = BacktestEngine()
    result = engine.run_simulation(ticker="AMD", starting_capital=2000.0, bars=bars, signals=signals)
    assert result.total_return_pct > 0
    assert result.win_rate_pct == 100.0
```

- [ ] **Step 2: Run full test suite to verify 100% pass rate**

Run: `./.venv/bin/pytest -v`  
Expected: PASS (all tests pass across schemas, scraper, compliance, risk, engine, backtest, integration)

- [ ] **Step 3: Commit integration update**

```bash
git add tests/test_integration.py
git commit -m "test: add BacktestEngine pipeline validation to integration test suite"
```
