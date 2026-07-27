# System Architecture Specification: `ai-trader` Core Platform

**Document Identifier:** `specs/2026-07-27-ai-trader-core-architecture.md`  
**Author / Owner:** Jesús Soto Mora (`jesussotomora`)  
**Date:** 2026-07-27  
**Status:** PROPOSED DESIGN — Backtesting Module Added  
**Target Repository:** [https://github.com/jesussotomora/ai-trader](https://github.com/jesussotomora/ai-trader)

---

## 1. System Overview & Architectural Diagram

The `ai-trader` platform is an automated, multi-LLM, risk-managed trading system engineered to run locally in Python while connecting to web AI subscriptions (ChatGPT, Claude, Gemini Advanced, OpenCode Go), real-time market data feeds, news scrapers, backtesting engines, and broker execution APIs (Alpaca, IBKR, Bitso).

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
 │   - BacktestEngine (Historical OHLCV simulation, Win Rate, Drawdown)     │
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

### 2.2 Data & RAG Engine Layer (`src/data/`)
* **`MarketDataEngine`:** Pulls live/delayed prices and calculates technical indicators (15-min Moving Average, RSI, MACD, Volume, P/E ratios).
* **`NewsScraperService`:** Uses `newspaper3k` to download full article body text and extract summary & keywords (`article.nlp()`).
* **`BacktestEngine` (`src/engine/backtest.py`):**
  * Simulates trade signals against historical OHLCV bars.
  * Calculates total return percentage, win rate percentage, maximum drawdown, total trades, and profit factor.
  * Evaluates signal stop-loss and take-profit thresholds against price movements.

### 2.3 LLM Engine Layer (`src/engine/`)
* **Mode A (Arena):** Model competition on virtual portfolios.
* **Mode B (Advisory Council):** Specialist LLMs (Technical, Fundamental Auditor, Sentiment) feeding a Consensus Chairman.

### 2.4 Risk Manager Guardrail (`src/risk/`)
* **Position Sizing & Circuit Breakers.**

### 2.5 Broker Adapter Layer (`src/brokers/`)
* **Alpaca, IBKR, and Bitso adapters.**
