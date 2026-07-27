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
