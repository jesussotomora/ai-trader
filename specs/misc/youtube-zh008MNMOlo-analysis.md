# Video Analysis: "I Gave My Terrible Trading Bot $10,000 to Trade Stocks"

**Source URL:** [https://www.youtube.com/watch?v=zh008MNMOlo](https://www.youtube.com/watch?v=zh008MNMOlo)  
**Creator:** Lewis Menelaws (Coding with Lewis)  
**Published:** November 16, 2023  
**Analysis Date:** 2026-07-26  
**Document Purpose:** Baseline research and strategy extraction for building our autonomous AI Trading Bot platform in `ai-trader`.

---

## 1. Executive Summary

In this experiment, Lewis built 3 distinct algorithmic stock trading bots in Python using $10,000 of real capital, executing trades over a 3-to-4 day live market period via Interactive Brokers. 

The experiment yielded:
* **Gross Trading Revenue:** +$109.35 (across 13 different stocks).
* **Market Data & Subscription Costs:** -$117.70 (Interactive Brokers market data feeds & API credits).
* **Net Profit / Loss:** -$8.35.

Despite the minor overall financial loss driven by data subscription overhead, the video demonstrates a modular architecture for combining **Technical Indicators**, **News Sentiment Analysis**, and **Vector Embeddings (LLM/Semantic Match)** into multi-strategy automated trading.

---

## 2. Core Tech Stack & Infrastructure

1. **Programming Language:** Python 3
2. **Broker & Execution API:** Interactive Brokers API (wrapped with an open-source Python wrapper like `ib_insync`).
3. **Backtesting Framework:** `Backtrader` (Python).
4. **Database & Vector Search:** DataStacks Astra DB (Cassandra-based Serverless Vector DB) for storing stock company descriptions, news embeddings, and lyric/sentiment embeddings.
5. **AI / Sentiment Processing:** OpenAI API / Embeddings for company-to-news text similarity and sentiment classification.
6. **Stock Universe Data:** Scraped lists of all NASDAQ & NYSE tickers.

---

## 3. Deep Dive into the 3 Bot Strategies

### Bot 1: Momentum + Fundamental Value Hybrid ("Safe Bot")
* **Concept:** Trades pre-selected "safe" / blue-chip stocks based on price averages and fundamental valuation metrics.
* **Execution Interval:** Evaluates market conditions every minute.
* **Entry Logic (BUY):**
  * Current Stock Price > 15-minute Moving Average (MA).
  * Price-to-Earnings (P/E) Ratio < Sector/Stock Average P/E.
* **Exit Logic (SELL):**
  * Moving Average slope turns downward.
* **Optimization & Backtesting:**
  * Used `Backtrader` to test historical data over several months.
  * Optimized across 22,500 combinations (25 period intervals × 30 overbought thresholds × 3 oversold thresholds).
  * Utilized 24 CPU cores in parallel for multi-processing (runtime ~25 mins).
  * Best backtest parameter configuration returned +$23 over test window.
* **Live Performance:**
  * **Duke Energy (DUK):** Bought 16 shares @ $90.09 ($1,441.44 total). Sold 2h later @ $89.66 (**-$6.88 loss**).
  * **Marathon Digital (MARA):** Bought 24 shares @ $9.38 ($225.24 total). Sold @ $10.22 (**+$20.16 profit**).
  * **Bot 1 Net Subtotal:** **+$13.28**

---

### Bot 2: Real-time News Sentiment Trader ("Risky Bot")
* **Concept:** Reacts in real time to breaking financial news headlines by mapping articles to stock tickers via vector search and measuring news sentiment.
* **Setup & Indexing:**
  1. Downloaded all NASDAQ & NYSE tickers.
  2. Generated company descriptions for each ticker via OpenAI.
  3. Generated vector embeddings for company descriptions and uploaded to Astra DB.
  4. Scanned News API for breaking news articles.
  5. Vector searched article text against Astra DB company embeddings to identify affected stock tickers.
* **Entry Logic (BUY):**
  * News sentiment for target ticker evaluates to POSITIVE -> Buy target stock.
* **Exit Logic (SELL):**
  * Breaking news sentiment evaluates to NEGATIVE for a currently held stock -> Immediately sell 100%.
* **Live Performance:**
  * **GameStop (GME):** Bought 22 @ $12.76, sold @ $13.23 (**+$10.15 profit**).
  * **Grindr (GRND):** Bought 46 @ $6.14, sold @ $6.76 (**+$28.29 profit**).
  * **Take-Two Interactive (TTWO):** Bought 1 @ $153.94, sold @ $154.00 (**+$0.06 profit**).
  * **Insulet Corp (PODD):** Bought 1 @ $170.05, sold @ $174.26 (**+$4.22 profit**).
  * **Hudson Pacific Properties (HPP):** Bought 50 @ $5.63, sold @ $5.73 (**+$4.80 profit**).
  * **AT&T (T):** Bought 18 @ $15.56, sold @ $15.78 (**+$3.91 profit**).
  * **Astra Space (ASTR):** Bought 195 @ $1.04, sold @ $1.04 (**-$1.33 loss**).
  * **Hudson Global (HSON):** Bought 18 @ $15.40, sold @ $15.47 (**+$1.26 profit**).
  * **Molson Coors (TAP):** Bought 4 @ $59.65, sold @ $59.66 (**+$0.04 profit**).
  * **Bot 2 Net Subtotal:** **+$51.34**

---

### Bot 3: Experimental Semantic AI Matcher ("SwiftTrade 1.0")
* **Concept:** High-variance experimental strategy mapping stock news to Taylor Swift song lyric sentiments.
* **Setup & Pipeline:**
  1. Downloaded full dataset of Taylor Swift song lyrics (from GitHub).
  2. Computed sentiment scores for every lyric line and stored vector embeddings in Astra DB.
  3. Selected a stock ticker completely at random from NASDAQ/NYSE list.
  4. Pulled the 5 most recent news articles for that ticker.
  5. Vector matched article embeddings against Taylor Swift lyric embeddings.
* **Entry Logic (BUY):**
  * Matched lyric has a HAPPY/POSITIVE sentiment -> Allocate 50% of available cash into stock.
* **Exit Logic (SELL):**
  * Subsequent news match yields a NEGATIVE lyric sentiment -> Sell entire position.
* **Live Performance:**
  * **Nuveen Global High Income (JGH):** Matched lyric "Stay Beautiful". Bought 101 @ $11.22, sold @ $11.20 (**-$2.02 loss**).
  * **Railcar Leasing Corp (TRN):** Matched lyric "Tim McGraw". Bought 10 @ $108.63, sold @ $110.87 (**+$22.45 profit**).
  * **Bot 3 Net Subtotal:** **+$44.73**

---

## 4. Financial Summary Matrix

| Strategy Bot | Trades Executed | Gross Profit/Loss |
| :--- | :---: | :---: |
| **Bot 1 (Momentum & Value)** | 2 | +$13.28 |
| **Bot 2 (News Sentiment)** | 9 | +$51.34 |
| **Bot 3 (SwiftTrade 1.0 AI)** | 2 | +$44.73 |
| **Gross Total** | **13** | **+$109.35** |
| **IB Market Data Subscriptions** | - | **-$117.70** |
| **Net Final Outcome** | **13** | **-$8.35** |

---

## 5. Architectural Takeaways & Roadmap for `ai-trader`

To build an improved, robust version of this concept in `ai-trader`, we should address the pain points identified in the video:

1. **Broker API Layer:**
   * Interactive Brokers native API is cumbersome. 
   * Design `ai-trader` with an abstract `BrokerInterface` supporting modern APIs like **Alpaca**, **Tradier**, or **Paper Trading Simulator** out of the box, alongside Interactive Brokers (`ib_insync`).

2. **Vector DB & Knowledge Base:**
   * Use an easily self-hostable or cloud-native Vector Database (e.g. Qdrant, ChromaDB, or Astra DB) for indexing company metadata, SEC filings, social sentiment (Reddit/X/News), and indicator strategies.

3. **Data Feed & Cost Optimization:**
   * Cache market data and news locally during backtesting to eliminate API rate limits and recurring costs.
   * Support free real-time data feeds (e.g., Yahoo Finance, Alpaca Free Tier, Polygon.io Free) before requiring paid subscriptions.

4. **Multi-Strategy Architecture:**
   * Modularize strategy engine:
     * `TechnicalStrategy` (MA, RSI, MACD, P/E ratio).
     * `SentimentStrategy` (News, Financial LLM sentiment like FinBERT / Llama / Claude / GPT).
     * `CustomVectorStrategy` (Arbitrary semantic embeddings & rag trading).

5. **Risk Management & Execution Controls:**
   * Automated Stop-Loss, Take-Profit, Trailing Stops.
   * Position sizing limiters to avoid over-exposure.
   * Realistic fee and slippage modeling in backtests.

---

## 6. Next Steps & Artifacts Created
* Created Git repository (`git init`).
* Created directory structure `specs/misc/`.
* Saved raw transcript to `specs/misc/youtube-zh008MNMOlo-transcript.txt`.
* Saved detailed video analysis & breakdown to `specs/misc/youtube-zh008MNMOlo-analysis.md`.
