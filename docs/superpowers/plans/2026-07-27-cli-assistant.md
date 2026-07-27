# Interactive Subscription CLI Assistant Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `CLIAssistant` in `src/compliance/cli_assistant.py` and runner `scripts/run_cli_assistant.py` to automate the end-to-end flow: scraping news, calculating indicators, packaging prompts for web LLMs (Gemini Advanced/Claude/ChatGPT), parsing JSON decisions, validating risk, and executing paper orders.

**Architecture:** Python `CLIAssistant` bridging `NewsScraperService`, `MarketDataService`, `PromptPackageBuilder`, `ResponseParser`, `RiskManager`, and `AlpacaAdapter`.

**Tech Stack:** Python 3.9+, pydantic, pytest.

## Global Constraints

- Must output clean CLI prompts formatted for copy/pasting into web subscription UIs.
- Must validate generated `TradeSignal` through `RiskManager` before executing any order.
- Fully unit tested using mocks.

---

### Task 1: CLIAssistant Implementation & Workflow

**Files:**
- Create: `src/compliance/cli_assistant.py`
- Create: `tests/test_cli_assistant.py`
- Create: `scripts/run_cli_assistant.py`

**Interfaces:**
- Consumes: `NewsScraperService`, `MarketDataService`, `PromptPackageBuilder`, `ResponseParser`, `RiskManager`, `AlpacaAdapter`
- Produces: `CLIAssistant.prepare_prompt_package(ticker)`, `CLIAssistant.process_llm_response(ticker, raw_response)`

- [ ] **Step 1: Write failing CLI assistant test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/pytest tests/test_cli_assistant.py`  
Expected: FAIL with `ModuleNotFoundError: No module named 'src.compliance.cli_assistant'`

- [ ] **Step 3: Implement CLIAssistant in `src/compliance/cli_assistant.py`**

```python
# src/compliance/cli_assistant.py
from typing import Tuple, Optional
from src.data.news_scraper import NewsScraperService, ArticleData
from src.data.market_data import MarketDataService
from src.compliance.prompt_builder import PromptPackageBuilder, ResponseParser
from src.risk.risk_manager import RiskManager
from src.models.schemas import TradeSignal, PortfolioState
from src.brokers.alpaca_adapter import AlpacaAdapter


class CLIAssistant:
    def __init__(self, alpaca_key: str = "", alpaca_secret: str = ""):
        self.news_scraper = NewsScraperService()
        self.market_data = MarketDataService()
        self.prompt_builder = PromptPackageBuilder()
        self.response_parser = ResponseParser()
        self.risk_manager = RiskManager()
        self.alpaca = AlpacaAdapter(api_key=alpaca_key, secret_key=alpaca_secret)

    def prepare_prompt_package(self, ticker: str, mock_text: Optional[str] = None) -> str:
        if mock_text:
            article = ArticleData(
                url=f"https://finance.example.com/{ticker}",
                title=f"Market Update for {ticker}",
                full_text=mock_text,
                summary=mock_text,
                keywords=[ticker.lower(), "earnings", "stocks"]
            )
        else:
            article = self.news_scraper.fetch_and_parse(f"https://finance.yahoo.com/quote/{ticker}")

        bars = self.market_data.get_synthetic_bars(ticker, count=15)
        indicators = self.market_data.calculate_indicators(bars)

        return self.prompt_builder.build_analysis_prompt(
            ticker=ticker,
            news_headline=article.title,
            full_text_summary=article.summary,
            technical_indicators=indicators
        )

    def process_llm_response(
        self,
        ticker: str,
        raw_response: str,
        trade_amount: float = 1000.0,
        portfolio: Optional[PortfolioState] = None
    ) -> Tuple[TradeSignal, bool, str]:
        signal = self.response_parser.parse_signal(raw_response)

        if not portfolio:
            portfolio = PortfolioState(
                account_id="CLI_DEMO",
                cash_balance=10000.0,
                total_equity=10000.0,
                realized_pnl=0.0,
                unrealized_pnl=0.0
            )

        approved, reason = self.risk_manager.validate_trade(signal, trade_amount, portfolio)
        return signal, approved, reason
```

- [ ] **Step 4: Create `scripts/run_cli_assistant.py`**

```python
#!/usr/bin/env python3
"""
Interactive CLI Assistant for ai-trader
Prepares LLM analysis prompt for Gemini/Claude/ChatGPT web subscriptions.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.compliance.cli_assistant import CLIAssistant

def main():
    ticker = sys.argv[1] if len(sys.argv) > 1 else "TSLA"
    assistant = CLIAssistant()
    print("=" * 65)
    print(f" 🤖 AI-TRADER SUBSCRIPTION ASSISTANT FOR: {ticker}")
    print("=" * 65)

    prompt = assistant.prepare_prompt_package(ticker, mock_text=f"Surge in {ticker} demand following quarterly earnings release.")
    print("\n📋 COPY THE FOLLOWING PROMPT TO YOUR GEMINI ADVANCED / CLAUDE / CHATGPT WEB APP:\n")
    print("-" * 65)
    print(prompt)
    print("-" * 65)

if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run test to verify it passes**

Run: `./.venv/bin/pytest tests/test_cli_assistant.py`  
Expected: PASS

- [ ] **Step 6: Commit CLI Assistant**

```bash
git add src/compliance/cli_assistant.py tests/test_cli_assistant.py scripts/run_cli_assistant.py
git commit -m "feat: implement CLIAssistant for ToS-compliant prompt generation and response parsing"
```

---

### Task 2: Integration & Master Suite Verification

**Files:**
- Modify: `tests/test_integration.py`

- [ ] **Step 1: Add CLI Assistant integration test**

```python
# Add to tests/test_integration.py
from src.compliance.cli_assistant import CLIAssistant

def test_cli_assistant_integration():
    assistant = CLIAssistant()
    prompt = assistant.prepare_prompt_package("MSFT", mock_text="Microsoft cloud revenue grows 25%")
    assert "MSFT" in prompt
    assert "Microsoft cloud revenue grows 25%" in prompt
```

- [ ] **Step 2: Run full test suite**

Run: `./.venv/bin/pytest -v`  
Expected: PASS (all tests pass)

- [ ] **Step 3: Commit integration update**

```bash
git add tests/test_integration.py
git commit -m "test: add CLIAssistant integration test to pipeline test suite"
```
