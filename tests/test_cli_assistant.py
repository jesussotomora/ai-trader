# tests/test_cli_assistant.py
import pytest
from unittest.mock import MagicMock
from src.compliance.cli_assistant import CLIAssistant
from src.models.schemas import TradeSignal, SignalAction

def test_cli_assistant_workflow():
    assistant = CLIAssistant(alpaca_key="MOCK_KEY", alpaca_secret="MOCK_SECRET")
    
    # 1. Prepare prompt
    prompt = assistant.prepare_prompt_package("AAPL", mock_text="Apple reports strong iPhone sales")
    assert "AAPL" in prompt
    assert "Apple reports strong iPhone sales" in prompt

    # 2. Process mock LLM response
    mock_json_resp = '''{
        "ticker": "AAPL",
        "action": "BUY",
        "confidence_score": 85.0,
        "stop_loss": 170.0,
        "take_profit": 200.0,
        "reasoning_thesis": "Strong earnings surprise",
        "invalidation_criteria": "Drop below 170",
        "advisor_model": "Gemini-Advanced"
    }'''
    
    signal, approved, msg = assistant.process_llm_response("AAPL", mock_json_resp, trade_amount=500.0)
    assert signal.action == SignalAction.BUY
    assert approved is True
