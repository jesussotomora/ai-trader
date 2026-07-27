from src.models.schemas import TradeSignal, SignalAction
from src.engine.arena import ArenaEngine
from src.engine.council import AdvisoryCouncil

def test_arena_engine_leaderboard():
    arena = ArenaEngine()
    arena.register_model("Claude-3.5-Sonnet", starting_capital=1000.0)
    arena.register_model("GPT-4o", starting_capital=1000.0)
    
    arena.update_performance("Claude-3.5-Sonnet", current_equity=1200.0)
    arena.update_performance("GPT-4o", current_equity=950.0)
    
    leaderboard = arena.get_leaderboard()
    assert leaderboard[0]["model_name"] == "Claude-3.5-Sonnet"
    assert leaderboard[0]["return_pct"] == 20.0

def test_advisory_council_consensus():
    council = AdvisoryCouncil()
    signals = [
        TradeSignal(
            ticker="NVDA", action=SignalAction.BUY, confidence_score=90.0,
            stop_loss=110.0, take_profit=140.0, reasoning_thesis="Strong AI demand",
            invalidation_criteria="N/A", advisor_model="Technical-Analyst"
        ),
        TradeSignal(
            ticker="NVDA", action=SignalAction.BUY, confidence_score=80.0,
            stop_loss=110.0, take_profit=140.0, reasoning_thesis="Solid P/E ratio",
            invalidation_criteria="N/A", advisor_model="Fundamental-Auditor"
        ),
        TradeSignal(
            ticker="NVDA", action=SignalAction.HOLD, confidence_score=50.0,
            stop_loss=110.0, take_profit=140.0, reasoning_thesis="Slight overbought signal",
            invalidation_criteria="N/A", advisor_model="Sentiment-Analyst"
        )
    ]
    
    consensus = council.synthesize_consensus("NVDA", signals)
    assert consensus.action == SignalAction.BUY
    assert consensus.confidence_score > 70.0
