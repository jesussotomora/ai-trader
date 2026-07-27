from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field


class SignalAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class AssetClass(str, Enum):
    US_STOCK = "US_STOCK"
    ETF = "ETF"
    CRYPTO = "CRYPTO"


class TradeSignal(BaseModel):
    ticker: str
    action: SignalAction
    confidence_score: float = Field(ge=0.0, le=100.0)
    target_price: Optional[float] = None
    stop_loss: float
    take_profit: float
    reasoning_thesis: str
    invalidation_criteria: str
    advisor_model: str


class Position(BaseModel):
    ticker: str
    quantity: float
    average_entry_price: float
    current_price: float
    unrealized_pnl: float


class PortfolioState(BaseModel):
    account_id: str
    cash_balance: float
    positions: Dict[str, Position] = Field(default_factory=dict)
    total_equity: float
    realized_pnl: float
    unrealized_pnl: float
