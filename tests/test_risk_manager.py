from src.models.schemas import TradeSignal, SignalAction, PortfolioState
from src.risk.risk_manager import RiskManager

def test_risk_manager_exceeds_max_position():
    risk_mgr = RiskManager(max_position_pct=0.10)  # Max 10% of portfolio per position
    portfolio = PortfolioState(
        account_id="ACC123",
        cash_balance=1000.0,
        total_equity=10000.0,
        realized_pnl=0.0,
        unrealized_pnl=0.0
    )
    
    # Attempting trade of $2,000 (20% of portfolio)
    signal = TradeSignal(
        ticker="AAPL",
        action=SignalAction.BUY,
        confidence_score=90.0,
        stop_loss=170.0,
        take_profit=200.0,
        reasoning_thesis="Test",
        invalidation_criteria="Test",
        advisor_model="Claude-3.5-Sonnet"
    )
    
    is_valid, reason = risk_mgr.validate_trade(signal, trade_amount=2000.0, portfolio=portfolio)
    assert not is_valid
    assert "exceeds maximum allowed position size" in reason


def test_risk_manager_low_confidence():
    risk_mgr = RiskManager(min_confidence_score=60.0)
    portfolio = PortfolioState(
        account_id="ACC123",
        cash_balance=5000.0,
        total_equity=10000.0,
        realized_pnl=0.0,
        unrealized_pnl=0.0
    )
    signal = TradeSignal(
        ticker="AAPL",
        action=SignalAction.BUY,
        confidence_score=50.0,
        stop_loss=170.0,
        take_profit=200.0,
        reasoning_thesis="Test",
        invalidation_criteria="Test",
        advisor_model="Claude-3.5-Sonnet"
    )
    is_valid, reason = risk_mgr.validate_trade(signal, trade_amount=500.0, portfolio=portfolio)
    assert not is_valid
    assert "below minimum threshold" in reason


def test_risk_manager_insufficient_cash():
    risk_mgr = RiskManager(max_position_pct=0.50)
    portfolio = PortfolioState(
        account_id="ACC123",
        cash_balance=100.0,
        total_equity=10000.0,
        realized_pnl=0.0,
        unrealized_pnl=0.0
    )
    signal = TradeSignal(
        ticker="AAPL",
        action=SignalAction.BUY,
        confidence_score=90.0,
        stop_loss=170.0,
        take_profit=200.0,
        reasoning_thesis="Test",
        invalidation_criteria="Test",
        advisor_model="Claude-3.5-Sonnet"
    )
    is_valid, reason = risk_mgr.validate_trade(signal, trade_amount=500.0, portfolio=portfolio)
    assert not is_valid
    assert "Insufficient cash balance" in reason


def test_risk_manager_hold_action():
    risk_mgr = RiskManager()
    portfolio = PortfolioState(
        account_id="ACC123",
        cash_balance=1000.0,
        total_equity=10000.0,
        realized_pnl=0.0,
        unrealized_pnl=0.0
    )
    signal = TradeSignal(
        ticker="AAPL",
        action=SignalAction.HOLD,
        confidence_score=90.0,
        stop_loss=170.0,
        take_profit=200.0,
        reasoning_thesis="Test",
        invalidation_criteria="Test",
        advisor_model="Claude-3.5-Sonnet"
    )
    is_valid, reason = risk_mgr.validate_trade(signal, trade_amount=0.0, portfolio=portfolio)
    assert is_valid
    assert "Hold action approved" in reason


def test_risk_manager_valid_trade():
    risk_mgr = RiskManager(max_position_pct=0.10, min_confidence_score=60.0)
    portfolio = PortfolioState(
        account_id="ACC123",
        cash_balance=5000.0,
        total_equity=10000.0,
        realized_pnl=0.0,
        unrealized_pnl=0.0
    )
    signal = TradeSignal(
        ticker="AAPL",
        action=SignalAction.BUY,
        confidence_score=85.0,
        stop_loss=170.0,
        take_profit=200.0,
        reasoning_thesis="Test",
        invalidation_criteria="Test",
        advisor_model="Claude-3.5-Sonnet"
    )
    is_valid, reason = risk_mgr.validate_trade(signal, trade_amount=500.0, portfolio=portfolio)
    assert is_valid
    assert "Trade approved by RiskManager" in reason
