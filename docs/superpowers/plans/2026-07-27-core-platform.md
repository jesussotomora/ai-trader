# Core Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the core Python platform for `ai-trader`, including data modeling, NewsScraperService with full-text parsing, ToS-compliant prompt builder & response parser, dual-mode LLM engine (Arena vs. Advisory Council), RiskManager guardrails, and Alpaca paper trading adapter.

**Architecture:** Python 3.9+ modular package structured into `src/models/`, `src/data/`, `src/compliance/`, `src/risk/`, `src/engine/`, and `src/brokers/`. Fully covered with `pytest` unit/integration tests and TDD.

**Tech Stack:** Python 3.9+, Pydantic v2, pytest, newspaper3k, nltk, requests, sqlite3.

## Global Constraints

- All core domain models must inherit from Pydantic `BaseModel`.
- Strict typing and docstrings for public functions.
- Unit test coverage required for every module before implementation.
- All git commits must be structured with conventional commits (`feat:`, `test:`, `docs:`).

---

### Task 1: Project Scaffolding & Test Suite Setup

**Files:**
- Create: `requirements.txt`
- Create: `pyproject.toml`
- Create: `src/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/test_environment.py`

**Interfaces:**
- Consumes: Python standard library, `pytest`
- Produces: Base project structure and verification suite

- [ ] **Step 1: Write failing environment test**

```python
# tests/test_environment.py
import sys

def test_python_version():
    assert sys.version_info >= (3, 9)
```

- [ ] **Step 2: Run test to verify it passes**

Run: `pytest tests/test_environment.py`  
Expected: PASS

- [ ] **Step 3: Create dependencies and pyproject.toml**

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-trader"
version = "0.1.0"
description = "Autonomous Multi-LLM Trading Platform"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "pydantic>=2.0",
    "requests>=2.28",
    "newspaper3k>=0.2.8",
    "nltk>=3.8"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0"
]
```

- [ ] **Step 4: Create package directory structure**

```bash
mkdir -p src/models src/data src/compliance src/risk src/engine src/brokers
touch src/__init__.py src/models/__init__.py src/data/__init__.py src/compliance/__init__.py src/risk/__init__.py src/engine/__init__.py src/brokers/__init__.py
```

- [ ] **Step 5: Commit scaffolding**

```bash
git add pyproject.toml requirements.txt src/ tests/
git commit -m "feat: initialize project scaffolding and package directory structure"
```

---

### Task 2: Core Data Models & Pydantic Schemas

**Files:**
- Create: `src/models/schemas.py`
- Create: `tests/test_schemas.py`

**Interfaces:**
- Consumes: `pydantic`
- Produces: `SignalAction`, `AssetClass`, `TradeSignal`, `PortfolioState`, `Position`

- [ ] **Step 1: Write failing schema tests**

```python
# tests/test_schemas.py
import pytest
from pydantic import ValidationError
from src.models.schemas import TradeSignal, SignalAction, AssetClass, PortfolioState

def test_valid_trade_signal():
    signal = TradeSignal(
        ticker="AAPL",
        action=SignalAction.BUY,
        confidence_score=85.5,
        target_price=190.0,
        stop_loss=175.0,
        take_profit=200.0,
        reasoning_thesis="Strong earnings momentum",
        invalidation_criteria="Price drops below MA50",
        advisor_model="Claude-3.5-Sonnet"
    )
    assert signal.ticker == "AAPL"
    assert signal.action == SignalAction.BUY
    assert signal.confidence_score == 85.5

def test_invalid_confidence_score():
    with pytest.raises(ValidationError):
        TradeSignal(
            ticker="AAPL",
            action=SignalAction.BUY,
            confidence_score=150.0,  # Out of range 0-100
            stop_loss=175.0,
            take_profit=200.0,
            reasoning_thesis="Invalid score test",
            invalidation_criteria="N/A",
            advisor_model="GPT-4o"
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_schemas.py`  
Expected: FAIL with `ModuleNotFoundError: No module named 'src.models.schemas'`

- [ ] **Step 3: Implement data schemas in `src/models/schemas.py`**

```python
# src/models/schemas.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_schemas.py`  
Expected: PASS

- [ ] **Step 5: Commit schemas**

```bash
git add src/models/schemas.py tests/test_schemas.py
git commit -m "feat: add Pydantic schemas for TradeSignal and PortfolioState"
```

---

### Task 3: NewsScraperService with Full-Text Parsing & Caching

**Files:**
- Create: `src/data/news_scraper.py`
- Create: `tests/test_news_scraper.py`

**Interfaces:**
- Consumes: `newspaper3k`, `sqlite3`
- Produces: `ArticleData`, `NewsScraperService.fetch_and_parse_article(url)`

- [ ] **Step 1: Write failing news scraper test**

```python
# tests/test_news_scraper.py
import os
import pytest
from src.data.news_scraper import NewsScraperService, ArticleData

def test_article_caching(tmp_path):
    db_path = str(tmp_path / "test_news.db")
    scraper = NewsScraperService(db_path=db_path)
    
    mock_url = "https://example.com/test-news-article"
    mock_article = ArticleData(
        url=mock_url,
        title="Test Financial News",
        full_text="Apple reports record Q3 earnings with strong iPhone sales.",
        summary="Apple reports record Q3 earnings.",
        keywords=["Apple", "earnings", "iPhone"]
    )
    
    scraper.cache_article(mock_article)
    cached = scraper.get_cached_article(mock_url)
    
    assert cached is not None
    assert cached.title == "Test Financial News"
    assert "Apple" in cached.keywords
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_news_scraper.py`  
Expected: FAIL with `ModuleNotFoundError: No module named 'src.data.news_scraper'`

- [ ] **Step 3: Implement NewsScraperService in `src/data/news_scraper.py`**

```python
# src/data/news_scraper.py
import json
import sqlite3
from typing import List, Optional
from pydantic import BaseModel
from newspaper import Article


class ArticleData(BaseModel):
    url: str
    title: str
    full_text: str
    summary: str
    keywords: List[str]


class NewsScraperService:
    def __init__(self, db_path: str = "news_cache.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS article_cache (
                    url TEXT PRIMARY KEY,
                    title TEXT,
                    full_text TEXT,
                    summary TEXT,
                    keywords TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def get_cached_article(self, url: str) -> Optional[ArticleData]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT url, title, full_text, summary, keywords FROM article_cache WHERE url = ?", (url,))
            row = cursor.fetchone()
            if row:
                return ArticleData(
                    url=row[0],
                    title=row[1],
                    full_text=row[2],
                    summary=row[3],
                    keywords=json.loads(row[4])
                )
        return None

    def cache_article(self, article: ArticleData):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO article_cache (url, title, full_text, summary, keywords)
                VALUES (?, ?, ?, ?, ?)
            """, (article.url, article.title, article.full_text, article.summary, json.dumps(article.keywords)))
            conn.commit()

    def fetch_and_parse(self, url: str) -> ArticleData:
        cached = self.get_cached_article(url)
        if cached:
            return cached

        art = Article(url)
        art.download()
        art.parse()
        try:
            art.nlp()
            summary = art.summary
            keywords = art.keywords
        except Exception:
            summary = art.text[:300]
            keywords = []

        data = ArticleData(
            url=url,
            title=art.title or "Untitled",
            full_text=art.text or "",
            summary=summary or "",
            keywords=keywords or []
        )
        self.cache_article(data)
        return data
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_news_scraper.py`  
Expected: PASS

- [ ] **Step 5: Commit NewsScraperService**

```bash
git add src/data/news_scraper.py tests/test_news_scraper.py
git commit -m "feat: implement NewsScraperService with full-text parsing and SQLite caching"
```

---

### Task 4: Compliance Layer & Prompt Package Builder

**Files:**
- Create: `src/compliance/prompt_builder.py`
- Create: `tests/test_compliance.py`

**Interfaces:**
- Consumes: `TradeSignal`, `ArticleData`, `PortfolioState`
- Produces: `PromptPackageBuilder.build_analysis_prompt(...)`, `ResponseParser.parse_signal(...)`

- [ ] **Step 1: Write failing prompt builder tests**

```python
# tests/test_compliance.py
from src.compliance.prompt_builder import PromptPackageBuilder, ResponseParser
from src.models.schemas import SignalAction, TradeSignal

def test_prompt_builder():
    builder = PromptPackageBuilder()
    prompt = builder.build_analysis_prompt(
        ticker="TSLA",
        news_summary="Tesla announces new EV battery breakthrough.",
        current_price=220.0,
        pe_ratio=45.0
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_compliance.py`  
Expected: FAIL with `ModuleNotFoundError: No module named 'src.compliance.prompt_builder'`

- [ ] **Step 3: Implement PromptPackageBuilder & ResponseParser in `src/compliance/prompt_builder.py`**

```python
# src/compliance/prompt_builder.py
import json
import re
from typing import Optional
from src.models.schemas import TradeSignal


class PromptPackageBuilder:
    def build_analysis_prompt(
        self,
        ticker: str,
        news_summary: str,
        current_price: float,
        pe_ratio: Optional[float] = None
    ) -> str:
        pe_str = f"{pe_ratio:.2f}" if pe_ratio else "N/A"
        return f"""
YOU ARE A PROFESSIONAL FINANCIAL ANALYST.
Analyze the following asset and respond ONLY with a valid JSON object.

ASSET TICKER: {ticker}
CURRENT PRICE: ${current_price:.2f}
P/E RATIO: {pe_str}

RECENT NEWS SUMMARY:
{news_summary}

YOUR RESPONSE MUST STRICTLY MATCH THIS JSON SCHEMA:
{{
    "ticker": "{ticker}",
    "action": "BUY | SELL | HOLD",
    "confidence_score": 0.0 to 100.0,
    "target_price": number or null,
    "stop_loss": number,
    "take_profit": number,
    "reasoning_thesis": "string",
    "invalidation_criteria": "string",
    "advisor_model": "Model-Name"
}}
"""


class ResponseParser:
    def parse_signal(self, raw_response: str) -> TradeSignal:
        # Extract JSON block if wrapped in markdown code fence
        json_match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response string")
        
        json_str = json_match.group(0)
        data = json.loads(json_str)
        return TradeSignal(**data)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_compliance.py`  
Expected: PASS

- [ ] **Step 5: Commit Compliance Layer**

```bash
git add src/compliance/prompt_builder.py tests/test_compliance.py
git commit -m "feat: implement PromptPackageBuilder and ResponseParser for ToS-compliant UI interactions"
```

---

### Task 5: RiskManager Guardrail Engine

**Files:**
- Create: `src/risk/risk_manager.py`
- Create: `tests/test_risk_manager.py`

**Interfaces:**
- Consumes: `TradeSignal`, `PortfolioState`
- Produces: `RiskManager.validate_trade(...) -> (bool, str)`

- [ ] **Step 1: Write failing RiskManager test**

```python
# tests/test_risk_manager.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_risk_manager.py`  
Expected: FAIL with `ModuleNotFoundError: No module named 'src.risk.risk_manager'`

- [ ] **Step 3: Implement RiskManager in `src/risk/risk_manager.py`**

```python
# src/risk/risk_manager.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_risk_manager.py`  
Expected: PASS

- [ ] **Step 5: Commit RiskManager**

```bash
git add src/risk/risk_manager.py tests/test_risk_manager.py
git commit -m "feat: implement RiskManager with position limits and confidence threshold validation"
```

---

### Task 6: Dual Mode Engine (Arena Mode & Advisory Council)

**Files:**
- Create: `src/engine/arena.py`
- Create: `src/engine/council.py`
- Create: `tests/test_engine.py`

**Interfaces:**
- Consumes: `TradeSignal`, `PortfolioState`
- Produces: `ArenaEngine.update_leaderboard(...)`, `AdvisoryCouncil.synthesize_consensus(...)`

- [ ] **Step 1: Write failing engine tests**

```python
# tests/test_engine.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_engine.py`  
Expected: FAIL with `ModuleNotFoundError: No module named 'src.engine.arena'`

- [ ] **Step 3: Implement ArenaEngine & AdvisoryCouncil in `src/engine/arena.py` & `src/engine/council.py`**

```python
# src/engine/arena.py
from typing import List, Dict

class ArenaEngine:
    def __init__(self):
        self.models: Dict[str, dict] = {}

    def register_model(self, model_name: str, starting_capital: float = 1000.0):
        self.models[model_name] = {
            "starting_capital": starting_capital,
            "current_equity": starting_capital,
            "return_pct": 0.0
        }

    def update_performance(self, model_name: str, current_equity: float):
        if model_name in self.models:
            start = self.models[model_name]["starting_capital"]
            self.models[model_name]["current_equity"] = current_equity
            self.models[model_name]["return_pct"] = ((current_equity - start) / start) * 100.0

    def get_leaderboard(self) -> List[dict]:
        results = [
            {
                "model_name": name,
                "current_equity": data["current_equity"],
                "return_pct": data["return_pct"]
            }
            for name, data in self.models.items()
        ]
        return sorted(results, key=lambda x: x["return_pct"], reverse=True)
```

```python
# src/engine/council.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_engine.py`  
Expected: PASS

- [ ] **Step 5: Commit Dual Mode Engine**

```bash
git add src/engine/arena.py src/engine/council.py tests/test_engine.py
git commit -m "feat: implement ArenaEngine leaderboard and AdvisoryCouncil consensus synthesis"
```

---

### Task 7: Master Integration & Verification Run

**Files:**
- Create: `tests/test_integration.py`

**Interfaces:**
- Consumes: All components (`schemas`, `news_scraper`, `prompt_builder`, `risk_manager`, `arena`, `council`)

- [ ] **Step 1: Write end-to-end integration test**

```python
# tests/test_integration.py
from src.models.schemas import PortfolioState, SignalAction
from src.data.news_scraper import NewsScraperService, ArticleData
from src.compliance.prompt_builder import PromptPackageBuilder, ResponseParser
from src.risk.risk_manager import RiskManager
from src.engine.council import AdvisoryCouncil

def test_full_pipeline_flow(tmp_path):
    # 1. Scrape & Cache News
    db_path = str(tmp_path / "integration_news.db")
    scraper = NewsScraperService(db_path=db_path)
    article = ArticleData(
        url="https://example.com/nvda-earnings",
        title="NVIDIA Q4 Earnings Surge",
        full_text="NVIDIA reports massive data center revenue growth.",
        summary="NVIDIA revenue up 200%.",
        keywords=["NVIDIA", "AI", "Revenue"]
    )
    scraper.cache_article(article)

    # 2. Build Prompt
    builder = PromptPackageBuilder()
    prompt = builder.build_analysis_prompt(
        ticker="NVDA",
        news_summary=article.summary,
        current_price=120.0,
        pe_ratio=50.0
    )
    assert "NVDA" in prompt

    # 3. Parse Mock Response
    mock_llm_json = """
    {
        "ticker": "NVDA",
        "action": "BUY",
        "confidence_score": 88.0,
        "target_price": 140.0,
        "stop_loss": 110.0,
        "take_profit": 145.0,
        "reasoning_thesis": "Strong Q4 revenue growth",
        "invalidation_criteria": "Price drops below 105",
        "advisor_model": "Claude-3.5-Sonnet"
    }
    """
    parser = ResponseParser()
    signal = parser.parse_signal(mock_llm_json)

    # 4. Consensus Check
    council = AdvisoryCouncil()
    final_signal = council.synthesize_consensus("NVDA", [signal])

    # 5. Risk Check
    risk_mgr = RiskManager(max_position_pct=0.10)
    portfolio = PortfolioState(
        account_id="ACC_TEST",
        cash_balance=5000.0,
        total_equity=10000.0,
        realized_pnl=0.0,
        unrealized_pnl=0.0
    )
    approved, msg = risk_mgr.validate_trade(final_signal, trade_amount=500.0, portfolio=portfolio)

    assert approved
    assert "approved" in msg.lower()
```

- [ ] **Step 2: Run all tests to verify 100% pass rate**

Run: `pytest -v`  
Expected: PASS (all tests pass across schemas, scraper, compliance, risk, engine, integration)

- [ ] **Step 3: Commit integration test suite**

```bash
git add tests/test_integration.py
git commit -m "test: add full pipeline end-to-end integration test suite"
```
