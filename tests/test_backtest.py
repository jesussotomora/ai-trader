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
