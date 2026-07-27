from typing import Tuple
from src.models.schemas import TradeSignal, SignalAction, PortfolioState


class RiskManager:
    def __init__(
        self,
        max_position_pct: float = 0.10,
        max_daily_drawdown_pct: float = 0.05,
        min_confidence_score: float = 60.0
    ):
        self.max_position_pct = max_position_pct
        self.max_daily_drawdown_pct = max_daily_drawdown_pct
        self.min_confidence_score = min_confidence_score

    def validate_trade(
        self,
        signal: TradeSignal,
        trade_amount: float,
        portfolio: PortfolioState
    ) -> Tuple[bool, str]:
        if signal.action == SignalAction.HOLD:
            return True, "Hold action approved"

        if signal.confidence_score < self.min_confidence_score:
            return False, f"Confidence score {signal.confidence_score:.1f} below minimum threshold {self.min_confidence_score}"

        max_allowed_amount = portfolio.total_equity * self.max_position_pct
        if trade_amount > max_allowed_amount:
            return False, f"Trade amount ${trade_amount:.2f} exceeds maximum allowed position size of ${max_allowed_amount:.2f}"

        if trade_amount > portfolio.cash_balance and signal.action == SignalAction.BUY:
            return False, f"Insufficient cash balance (${portfolio.cash_balance:.2f}) for trade amount ${trade_amount:.2f}"

        return True, "Trade approved by RiskManager"
