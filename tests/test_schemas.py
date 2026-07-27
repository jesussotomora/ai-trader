import pytest
from pydantic import ValidationError
from src.models.schemas import (
    TradeSignal, SignalAction, AssetClass, PortfolioState,
    HistoricalBar, BacktestResult, ExecutedTrade
)

def test_valid_trade_signal():
    signal = TradeSignal(
        ticker="AAPL",
        action=SignalAction.BUY,
        confidence_score=85.5,
        target_price=190.0,
        stop_loss=175.0,
        take_profit=200.0,
        reasoning_thesis="Strong earnings momentum",
        invalidation_criteria="Price drops below MA50",
        advisor_model="Claude-3.5-Sonnet"
    )
    assert signal.ticker == "AAPL"
    assert signal.action == SignalAction.BUY
    assert signal.confidence_score == 85.5

def test_invalid_confidence_score():
    with pytest.raises(ValidationError):
        TradeSignal(
            ticker="AAPL",
            action=SignalAction.BUY,
            confidence_score=150.0,  # Out of range 0-100
            stop_loss=175.0,
            take_profit=200.0,
            reasoning_thesis="Invalid score test",
            invalidation_criteria="N/A",
            advisor_model="GPT-4o"
        )


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

