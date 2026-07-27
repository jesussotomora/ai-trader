# Architectural Specs: Compliant LLM Integration, Model Selection & Dual Operating Modes

**Document Purpose:** Define ToS-compliant usage of web subscriptions, specify supported LLMs, detail the dual execution modes (Arena Competition vs. Advisory Council), and refine sentiment/semantic strategy logic.

---

## 1. Terms of Service (ToS) Compliance for Web Subscriptions

### The Challenge
Most AI providers (OpenAI, Anthropic, Google, Perplexity) explicitly prohibit automated web scraping, headless browser scripts (Puppeteer/Playwright/Selenium), or reverse-engineering web UI endpoints under their consumer Terms of Service for ChatGPT Plus, Claude Pro, and Gemini Advanced.

### ToS-Compliant Integration Patterns
To utilize user subscriptions legally and safely without risking account suspension, `ai-trader` will implement a **Hybrid Compliant Layer**:

1. **Pattern A: Interactive Prompt & Response Helper (Human-in-the-Loop / Assistant UI):**
   * `ai-trader` prepares standardized, optimized context packages (News + Financial Metrics + System Persona) and presents a 1-click "Copy Prompt / Export File" interface for the user's browser subscription.
   * The user pastes or uploads into ChatGPT Plus / Claude Pro / Gemini Advanced and pastes back the structured JSON response (or uses a lightweight browser extension helper where permitted).
2. **Pattern B: Official Subscription CLI / Extensions / Official API Integrations:**
   * Support official developer CLI tools included in subscriptions (e.g. **Claude Code** included in Claude Pro/Team).
   * Support official API key options when available, with per-token cost estimation and budget caps for users who opt into pay-as-you-go.
3. **Pattern C: Hybrid Engine:**
   * Heavy bulk tasks (market data processing, indicators) run locally on Python.
   * Strategic reasoning tasks (sentiment analysis, thesis evaluation, council debates) use the subscription-aligned interface.

---

## 2. Selected Models & Model Taxonomy

We will support the following flagship models across platforms:

| Model Family | Primary Strength in `ai-trader` | Subscription Tier |
| :--- | :--- | :--- |
| **Claude 3.5 / 3.7 Sonnet & Opus** | Code architecture, deep financial report analysis, structured JSON outputs | Claude Pro ($20/mo) |
| **GPT-4o / o1 / o3-mini** | Complex quantitative math, backtesting validation, macro economic logic | ChatGPT Plus ($20/mo) |
| **DeepSeek R1 / V3** | Multi-step mathematical reasoning, cost-free logic verification | DeepSeek Web (Free) |
| **Qwen 2.5 / 3 Max** | Algorithmic code review, quantitative analysis | Qwen Chat (Free) |
| **Perplexity Pro (Sonar/GPT/Claude)** | Real-time web news aggregation, sentiment validation | Perplexity Pro ($20/mo) |
| **Gemini 1.5 / 3.0 Pro** | Massive 2M context analysis (entire SEC 10-K filings + earnings calls) | Gemini AI Pro ($19.99/mo) |

---

## 3. Dual Operating Modes

`ai-trader` will natively support two distinct operating modes:

```
                          ┌──────────────────────────────────────────┐
                          │            ai-trader Engine              │
                          └────────────────────┬─────────────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
         ┌──────────────────────────┐                    ┌──────────────────────────┐
         │     MODE A: ARENA        │                    │    MODE B: ADVISORY      │
         │     (Competition)        │                    │         COUNCIL          │
         └─────────────┬────────────┘                    └─────────────┬────────────┘
                       │                                               │
     ┌─────────────────┼─────────────────┐           ┌─────────────────┼─────────────────┐
     ▼                 ▼                 ▼           ▼                 ▼                 ▼
 ┌───────┐         ┌───────┐         ┌───────┐   ┌───────┐         ┌───────┐         ┌───────┐
 │Claude │         │ GPT-4 │         │DeepS. │   │ Tech. │         │ Fund. │         │ Senti.│
 │ Bot   │         │ Bot   │         │ Bot   │   │Analyst│         │Analyst│         │Analyst│
 └───┬───┘         └───┬───┘         └───┬───┘   └───┬───┘         └───┬───┘         └───┬───┘
     │                 │                 │           └─────────────────┼─────────────────┘
     ▼                 ▼                 ▼                             ▼
 [Sub-Port 1]    [Sub-Port 2]    [Sub-Port 3]                 ┌──────────────────┐
 ($1k Capital)   ($1k Capital)   ($1k Capital)                │ Chairman/Synth.  │
                                                              └────────┬─────────┘
                                                                       ▼
                                                              [Unified Execution]
```

### Mode A: Multi-LLM Arena (Competition Mode)
* **Concept:** Inspired by Video #2 (5 AIs with $1K real money).
* **Execution:**
  * Each LLM manages an isolated virtual portfolio (e.g. $1,000 USD virtual capital).
  * Models compete on Sharpe Ratio, Win Rate, and Total Return over daily/weekly cycles.
  * Leaderboard tracks performance live, allowing users to discover which model excels in current market regimes.

### Mode B: Advisory Council (Consensus Mode)
* **Concept:** Collaborative multi-agent decision making.
* **Specialist Roles:**
  1. **Technical Analyst (e.g. Qwen / GPT):** Analyzes Price Action, Moving Averages, RSI, MACD, Volume.
  2. **Fundamental Analyst (e.g. Gemini / Claude):** Analyzes P/E ratios, earnings growth, SEC filing risks.
  3. **Sentiment & Macro Analyst (e.g. Perplexity / DeepSeek):** Scrapes live news, social sentiment, macro interest rate trends.
  4. **Risk Manager Guardrail:** Enforces stop-loss limits, position sizing, and drawdown protection.
* **Consensus Synthesizer (Chairman LLM):** Weighs all advisor scores into a single final confidence score (0 to 100) and outputs a single executable trade order.

---

## 4. Refining Video #1: Discarding Gimmicks for Real RAG

* **Replacing Taylor Swift Gimmick:** In Video #1, matching news to Taylor Swift lyrics was purely for YouTube entertainment.
* **Real Semantic RAG Engine:** We replace lyric matching with a **Financial Knowledge Base**:
  * Vector search news articles against **SEC 10-K Risk Factors**, **Company Guidance Notes**, **Financial Glossary Definitions**, and **Macro Economic Indicators**.
  * Use semantic vector similarity (Cosine distance via Qdrant/ChromaDB/Astra DB) to score how news impacts specific corporate fundamentals.
