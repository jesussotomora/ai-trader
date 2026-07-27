from typing import List
from src.models.schemas import TradeSignal, SignalAction


class AdvisoryCouncil:
    def synthesize_consensus(self, ticker: str, advisor_signals: List[TradeSignal]) -> TradeSignal:
        if not advisor_signals:
            raise ValueError("No advisor signals provided")

        buy_votes = [s for s in advisor_signals if s.action == SignalAction.BUY]
        sell_votes = [s for s in advisor_signals if s.action == SignalAction.SELL]
        hold_votes = [s for s in advisor_signals if s.action == SignalAction.HOLD]

        avg_confidence = sum(s.confidence_score for s in advisor_signals) / len(advisor_signals)

        if len(buy_votes) > len(sell_votes) and len(buy_votes) >= len(hold_votes):
            winning_action = SignalAction.BUY
        elif len(sell_votes) > len(buy_votes) and len(sell_votes) >= len(hold_votes):
            winning_action = SignalAction.SELL
        else:
            winning_action = SignalAction.HOLD

        avg_stop = sum(s.stop_loss for s in advisor_signals) / len(advisor_signals)
        avg_take = sum(s.take_profit for s in advisor_signals) / len(advisor_signals)

        return TradeSignal(
            ticker=ticker,
            action=winning_action,
            confidence_score=avg_confidence,
            stop_loss=avg_stop,
            take_profit=avg_take,
            reasoning_thesis=f"Consensus of {len(advisor_signals)} advisors ({len(buy_votes)} BUY, {len(sell_votes)} SELL, {len(hold_votes)} HOLD)",
            invalidation_criteria="Consensus invalidated if price breaks technical stop loss",
            advisor_model="Advisory-Council-Consensus"
        )
