from src.compliance.prompt_builder import PromptPackageBuilder, ResponseParser
from src.models.schemas import SignalAction, TradeSignal


def test_prompt_builder():
    builder = PromptPackageBuilder()
    prompt = builder.build_analysis_prompt(
        ticker="TSLA",
        news_summary="Tesla announces new EV battery breakthrough.",
        current_price=220.0,
        pe_ratio=45.0,
    )
    assert "TSLA" in prompt
    assert "220.0" in prompt
    assert "JSON" in prompt


def test_response_parser_valid_json():
    json_response = """
    {
        "ticker": "TSLA",
        "action": "BUY",
        "confidence_score": 90.0,
        "target_price": 250.0,
        "stop_loss": 210.0,
        "take_profit": 260.0,
        "reasoning_thesis": "Battery breakthrough expands margin",
        "invalidation_criteria": "Price falls below 205",
        "advisor_model": "Claude-3.5-Sonnet"
    }
    """
    parser = ResponseParser()
    signal = parser.parse_signal(json_response)
    assert signal.ticker == "TSLA"
    assert signal.action == SignalAction.BUY
    assert signal.confidence_score == 90.0
