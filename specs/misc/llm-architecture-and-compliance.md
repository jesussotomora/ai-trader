# Architectural Specs: Compliant LLM Integration, Model Selection & Dual Operating Modes

**Document Purpose:** Define ToS-compliant usage of web subscriptions, specify supported LLMs (defining Gemini Advanced's primary role as Core Infrastructure & Long-Context Analyst), detail the dual execution modes (Arena Competition vs. Advisory Council), and refine sentiment/semantic strategy logic.

---

## 1. Terms of Service (ToS) Compliance for Web Subscriptions

### The Challenge
Most AI providers (OpenAI, Anthropic, Google, Perplexity) explicitly prohibit automated web scraping, headless browser scripts (Puppeteer/Playwright/Selenium), or reverse-engineering web UI endpoints under their consumer Terms of Service for ChatGPT Plus, Claude Pro, and Gemini Advanced.

### ToS-Compliant Integration Patterns
To utilize user subscriptions legally and safely without risking account suspension, `ai-trader` will implement a **Hybrid Compliant Layer**:

1. **Pattern A: Interactive Prompt & Response Helper (Human-in-the-Loop / Assistant UI):**
   * `ai-trader` prepares standardized, optimized context packages (News + Financial Metrics + System Persona) and presents a 1-click "Copy Prompt / Export File" interface for the user's browser subscription.
   * The user pastes or uploads into ChatGPT Plus / Claude Pro / Gemini Advanced and pastes back the structured JSON response.
2. **Pattern B: Official Subscription CLI / Gateway Tools (Claude Code & OpenCode Go):**
   * Support official developer CLI tools included in subscriptions (e.g. **Claude Code** included in Claude Pro/Team).
   * Support **OpenCode / OpenCode Go ($10/mo gateway key)** for terminal agent execution accessing **Kimi K3, DeepSeek V4, Qwen 3.7 Max, and Grok**.
3. **Pattern C: Hybrid Engine:**
   * Heavy bulk tasks (market data processing, indicators) run locally on Python.
   * Strategic reasoning tasks (sentiment analysis, thesis evaluation, council debates) use the subscription-aligned interface or OpenCode Go CLI.

---

## 2. Selected Models & Model Taxonomy

We will support the following flagship models across platforms:

| Model Family | Primary Strength in `ai-trader` | Subscription Tier |
| :--- | :--- | :--- |
| **Google Gemini Advanced (Active User Sub)** | **Core Infrastructure, Codebase Architecture & Massive 2M Context Analysis.** Reads 500-page SEC 10-K filings, earnings transcripts, and generates fast code/docs. *(Excluded from solo trade decisions until risk-bounded)*. | Gemini AI Premium (Active) |
| **Claude 3.5 / 3.7 Sonnet & Opus** | Code architecture, deep financial report analysis, structured JSON outputs | Claude Pro ($20/mo) |
| **Kimi K3 (Moonshot AI)** | 1M token context, Agent Swarm, Kimi Code, complex codebase search | Kimi Moderato ($19/mo) or OpenCode Go ($10/mo) |
| **OpenCode Go Suite (Kimi K3, DeepSeek V4, Qwen 3.7, Grok)** | Open CLI Gateway for multi-model terminal agent execution | OpenCode Go ($10/mo) |
| **GPT-4o / o1 / o3-mini** | Complex quantitative math, backtesting validation, macro economic logic | ChatGPT Plus ($20/mo) |
| **DeepSeek R1 / V3 / V4** | Multi-step mathematical reasoning, cost-free logic verification | DeepSeek Web (Free) or OpenCode Go |
| **Qwen 2.5 / 3 / 3.7 Max** | Algorithmic code review, quantitative analysis | Qwen Chat (Free) or OpenCode Go |
| **Perplexity Pro (Sonar/GPT/Claude)** | Real-time web news aggregation, sentiment validation | Perplexity Pro ($20/mo) |

---

## 3. Gemini Advanced Role in System Architecture

Given the user's active **Gemini Advanced subscription**, Gemini will serve as the **Primary Infrastructure & Analysis Workhorse**:

1. **Massive Context Reading (2M Token Window):**
   * Parsing complete annual SEC 10-K / 10-Q reports, balance sheets, and full earnings call transcripts in a single prompt.
2. **Fast Code Generation & System Refactoring:**
   * Rapidly drafting Python boilerplate, API adapters, UI components, and markdown documentation due to high inference speed.
3. **Fundamental Risk Auditor (Non-Trading Advisor):**
   * Acts as a fundamental auditor evaluating whether a company's debt-to-equity ratio, cash flow, or SEC risk disclosures flag hidden dangers before trades execute.

---

## 4. Dual Operating Modes

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
 │Claude │         │Kimi K3│         │DeepS. │   │ Tech. │         │ Fund. │         │ Senti.│
 │ Bot   │         │ Bot   │         │ Bot   │   │Analyst│         │ (Gemini)        │Analyst│
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
* Each competing LLM manages an isolated virtual portfolio (e.g. $1,000 USD virtual capital).
* Gemini can participate in Arena mode once strict risk-bounding rules (max drawdown, position limits) are enabled.

### Mode B: Advisory Council (Consensus Mode)
* **Specialist Roles:**
  1. **Technical Analyst (e.g. Qwen / GPT):** Analyzes Price Action, Moving Averages, RSI, MACD, Volume.
  2. **Fundamental Auditor (Gemini Advanced):** Uses 2M token context to review 10-K filings, debt, cash flows, and SEC warnings.
  3. **Sentiment & Macro Analyst (e.g. Perplexity / DeepSeek):** Scrapes live news, social sentiment, macro interest rate trends.
  4. **Risk Manager Guardrail:** Enforces stop-loss limits, position sizing, and drawdown protection.
* **Consensus Synthesizer (Chairman LLM):** Weighs all advisor scores into a single final confidence score (0 to 100) and outputs a single executable trade order.
