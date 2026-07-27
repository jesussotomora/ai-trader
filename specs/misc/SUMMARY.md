# AI Trader: Research & Discovery Summary

**Last Updated:** 2026-07-27  
**Project Workspace:** `/Users/jesussoto/development/projects/ai-trader/ai-trader`  
**Repository Status:** Git initialized & synced with `origin/main`.

---

## 📚 Collected Specs & Research Artifacts

All baseline research and analysis files collected in `specs/misc/`:

1. **[llm-architecture-and-compliance.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/llm-architecture-and-compliance.md)**
   * *Key Topics:* ToS-compliant subscription integration, Model Selection taxonomy, Dual Operating Modes (Arena Competition vs. Advisory Council), and Enterprise Semantic RAG (replacing Taylor Swift gimmick).

2. **[youtube-zh008MNMOlo-analysis.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/youtube-zh008MNMOlo-analysis.md)**
   * *Source:* Video "I Gave My Terrible Trading Bot $10,000 to Trade Stocks" (Lewis Menelaws).
   * *Key Learning:* Python trading bots (Momentum, News Sentiment, AI Vector Lyric Matcher) on Interactive Brokers.
   * *Raw Transcript:* [youtube-zh008MNMOlo-transcript.txt](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/youtube-zh008MNMOlo-transcript.txt)

3. **[github-news-bot-analysis.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/github-news-bot-analysis.md)**
   * *Source:* GitHub Repository `SomeRandomGuy009/news-bot`.
   * *Key Learning:* Full-article news web scraping using `newspaper3k` + `NewsAPI` + `nltk` to extract complete article body and keywords, preventing LLM context loss.

4. **[youtube-DKM94g3Hr_M-analysis.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/youtube-DKM94g3Hr_M-analysis.md)**
   * *Source:* Video "He Told 5 AIs: Make Money or Get Deleted" (The Koerner Office Podcast).
   * *Key Learning:* 6-month real-money competition ($5,000 USD total) pitting Claude, ChatGPT, Gemini, Grok, and Perplexity against each other. Claude won with **+140% return** ($2,400+). Overall AI portfolio beat S&P 500 by **11x-12x** (+56% vs +5%).
   * *Raw Transcript:* [youtube-DKM94g3Hr_M-transcript.txt](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/youtube-DKM94g3Hr_M-transcript.txt)

5. **[ai-subscriptions-cost-benefit.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/ai-subscriptions-cost-benefit.md)**
   * *Source:* Web Subscription Research (July 2026).
   * *Key Learning:* Comparative analysis of user web subscriptions ($20/mo ChatGPT Plus, $20/mo Claude Pro, $20/mo Perplexity Pro, Kimi, Qwen Free, DeepSeek Free). Recommended stack: **Claude Pro + Perplexity Pro + Free DeepSeek/Qwen**.

6. **[mexico-automated-trading-platforms.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/mexico-automated-trading-platforms.md)**
   * *Source:* Brokerage & API Research for Mexico (2026).
   * *Key Learning:* 
     * **Production Stocks:** Interactive Brokers (IBKR) with **SPEI in MXN** (1st free/mo) and institutional FX conversion.
     * **Testing / Paper Trading:** Alpaca Trading ($0 commission, clean REST API).
     * **Crypto in MXN:** Bitso Alpha API (24/7 free SPEI deposits).

---

## 🎯 Architecture Roadmap for `ai-trader`

1. **`ComplianceLayer`:** Human-in-the-loop prompt/response helper & subscription CLI tools (Claude Code) respecting provider ToS.
2. **`DualModeEngine`:** 
   * **Mode A (Arena):** Isolated virtual portfolios competing for returns.
   * **Mode B (Advisory Council):** Technical, Fundamental & Sentiment LLM Specialists feeding a Consensus Chairman.
3. **`FinancialRAGService`:** Semantic vector matching of news against SEC filings and macro metrics (replacing simple gimmicks).
4. **`BrokerAdapter` Layer:**
   * `AlpacaPaperAdapter` for risk-free testing.
   * `IBKRAdapter` (`ib_insync`) for live stock/ETF execution in Mexico.
   * `BitsoAdapter` for MXN crypto trading.
