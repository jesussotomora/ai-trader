# System Architecture Specification: `ai-trader` Core Platform

**Document Identifier:** `specs/2026-07-27-ai-trader-core-architecture.md`  
**Author / Owner:** Jesús Soto Mora (`jesussotomora`)  
**Date:** 2026-07-27  
**Status:** PROPOSED DESIGN — Pending User Review  
**Target Repository:** [https://github.com/jesussotomora/ai-trader](https://github.com/jesussotomora/ai-trader)

---

## 1. System Overview & Architectural Diagram

The `ai-trader` platform is an automated, multi-LLM, risk-managed trading system engineered to run locally in Python while connecting to web AI subscriptions (ChatGPT, Claude, Gemini Advanced, OpenCode Go), real-time market data feeds, news scrapers, and broker execution APIs (Alpaca, IBKR, Bitso).

```
 ┌──────────────────────────────────────────────────────────────────────────┐
 │                            USER INTERFACE LAYER                          │
 │       (FastAPI Web Dashboard / CLI Tools / Subscription Prompt Helper)   │
 └────────────────────────────────────┬─────────────────────────────────────┘
                                      │
 ┌────────────────────────────────────▼─────────────────────────────────────┐
 │                         COMPLIANCE & INTEGRATION LAYER                   │
 │   - Subscription Prompt Package Formatter (JSON Input/Output Schemas)    │
 │   - OpenCode Go CLI / Gateway Client ($10/mo Gateway)                    │
 │   - Local Cache & Payload Validator                                      │
 └────────────────────────────────────┬─────────────────────────────────────┘
                                      │
 ┌────────────────────────────────────▼─────────────────────────────────────┐
 │                              LLM ENGINE LAYER                            │
 │                                                                          │
 │   ┌───────────────────────────────┐   ┌──────────────────────────────┐   │
 │   │  MODE A: MULTI-LLM ARENA      │   │   MODE B: ADVISORY COUNCIL   │   │
 │   │  - Virtual Portfolio Manager  │   │   - Technical Analyst        │   │
 │   │  - Model Leaderboard          │   │   - Fundamental Auditor      │   │
 │   │  - Performance Stats          │   │     (Gemini 2M Context)      │   │
 │   └───────────────┬───────────────┘   │   - Sentiment Analyst        │   │
 │                   │                   │   - Consensus Chairman       │   │
 │                   │                   └──────────────┬───────────────┘   │
 └───────────────────┼──────────────────────────────────┼───────────────────┘
                     │                                  │
 ┌───────────────────▼──────────────────────────────────▼───────────────────┐
 │                            DATA & RAG LAYER                              │
 │   - Market Data Engine (Price Feeds, MA, RSI, MACD, Volume)              │
 │   - NewsScraperService (newspaper3k + NewsAPI + Full-Text Extraction)    │
 │   - Financial RAG Engine (Vector DB + SEC 10-K Risk Factors)             │
 └────────────────────────────────────┬─────────────────────────────────────┘
                                      │
 ┌────────────────────────────────────▼─────────────────────────────────────┐
 │                           RISK MANAGER GUARDRAIL                         │
 │   - Position Sizing Limiter (Max % per trade)                            │
 │   - Stop-Loss & Take-Profit Auto Execution                               │
 │   - Account Drawdown Circuit Breakers                                    │
 └────────────────────────────────────┬─────────────────────────────────────┘
                                      │
 ┌────────────────────────────────────▼─────────────────────────────────────┐
 │                           BROKER ADAPTER LAYER                           │
 │   - AlpacaAdapter (Paper Trading Sandbox - $0 Commission)                │
 │   - IBKRAdapter (Interactive Brokers via SPEI MXN - Production Stocks)   │
 │   - BitsoAdapter (Bitso Alpha API - Crypto in MXN via SPEI 24/7)          │
 └──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Specifications

### 2.1 Compliance & Integration Layer (`src/compliance/`)
* **Purpose:** Ensures 100% compliance with consumer Terms of Service for web subscriptions (ChatGPT Plus, Claude Pro, Gemini Advanced) without automated headless scraping.
* **Modules:**
  * `PromptPackageBuilder`: Assembles structured JSON contexts containing market indicators, full news text, portfolio state, and system prompts.
  * `ResponseParser`: Validates and parses raw text/JSON responses pasted or returned from web subscriptions into strictly typed Pydantic models (`TradeSignal`).
  * `OpenCodeClient`: Integrates with the **OpenCode Go** gateway ($10/mo key) for terminal-based execution of Kimi K3, DeepSeek V4, Qwen 3.7 Max, and Grok.

### 2.2 Data & RAG Engine Layer (`src/data/`)
* **`MarketDataEngine`:** Pulls live/delayed prices and calculates technical indicators (15-min Moving Average, RSI, MACD, Volume, P/E ratios).
* **`NewsScraperService`:**
  * Uses `NewsAPI` to discover headlines.
  * Uses `newspaper3k` to download full article body text and extract summary & keywords (`article.nlp()`).
  * Caches scraped articles in SQLite to avoid re-downloading.
* **`FinancialRAGEngine`:**
  * Indexes SEC 10-K risk factors and company guidance in a local vector database (ChromaDB / Qdrant).
  * Computes cosine similarity scores between breaking news articles and company fundamentals.

### 2.3 LLM Engine Layer (`src/engine/`)

#### Mode A: Multi-LLM Arena (`src/engine/arena/`)
* Each supported LLM (Claude, ChatGPT, Kimi K3, DeepSeek, Qwen, Gemini) manages a virtual sub-portfolio with starting capital (e.g. $1,000 USD virtual balance).
* Tracks individual Sharpe Ratios, Win Rates, and Net Returns.
* Renders a real-time Leaderboard displaying model performance across market cycles.

#### Mode B: Advisory Council (`src/engine/council/`)
* **Technical Analyst:** Evaluates price action, MA cross, RSI overbought/oversold levels.
* **Fundamental Auditor (Gemini Advanced):** Uses 2M token context window to audit balance sheets, cash flow statements, SEC filing risk disclaimers, and P/E valuation.
* **Sentiment Analyst:** Processes breaking news sentiment scores and social trends.
* **Consensus Chairman:** Aggregates specialist advisor scores into a unified trade decision (BUY, SELL, HOLD) with a confidence score (0-100).

### 2.4 Risk Manager Guardrail (`src/risk/`)
* **Position Sizing:** Enforces maximum allocation limits per trade (e.g. max 10% of portfolio per single stock, max 20% in leveraged ETFs).
* **Automated Stop-Loss & Take-Profit:** Attaches hard stop-loss (e.g. -3%) and take-profit (e.g. +8%) orders to every executed trade.
* **Drawdown Circuit Breaker:** Suspends automated trading if daily account drawdown exceeds a safety threshold (e.g. -5% in 24 hours).

### 2.5 Broker Adapter Layer (`src/brokers/`)
* **`AlpacaPaperAdapter`:** Uses `alpaca-py` to connect to Alpaca's $0 commission paper trading API for risk-free strategy verification.
* **`IBKRAdapter`:** Uses `ib_insync` / `ib_async` to connect to Interactive Brokers for live US stock/ETF trading, funded in MXN via SPEI.
* **`BitsoAdapter`:** Connects to Bitso Alpha API for crypto trading in Pesos (MXN) with 24/7 instant SPEI funding.

---

## 3. Data Schema & Core Models (Pydantic)

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

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
    target_price: Optional[float]
    stop_loss: float
    take_profit: float
    reasoning_thesis: str
    invalidation_criteria: str
    advisor_model: str

class PortfolioState(BaseModel):
    account_id: str
    cash_balance: float
    positions: dict  # ticker -> quantity
    total_equity: float
    realized_pnl: float
    unrealized_pnl: float
```

---

## 4. Verification & Testing Plan

1. **Unit & Integration Tests (`pytest`):**
   * Test `NewsScraperService` full-text extraction and SQLite caching.
   * Test `ResponseParser` schema validation against mock LLM JSON responses.
   * Test `RiskManager` position size limiters and stop-loss rules.
2. **Paper Trading Verification (`Alpaca Paper Trading`):**
   * Run initial strategy cycles against Alpaca Paper Sandbox to verify end-to-end execution without real money.
3. **Static Analysis & Linting:**
   * Enforce clean code with `flake8` / `black` / `mypy`.
