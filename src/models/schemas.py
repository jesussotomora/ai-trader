from enum import Enum
from typing import Dict, List, Optional
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

