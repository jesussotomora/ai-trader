import pytest
from pydantic import ValidationError
from src.models.schemas import TradeSignal, SignalAction, AssetClass, PortfolioState

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
