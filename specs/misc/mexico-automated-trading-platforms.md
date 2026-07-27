# Automated Trading Platforms & Architecture in Mexico

**Document Purpose:** Analysis of trading automation mechanisms, broker API availability, funding methods (SPEI/Wire), and complete cost/commission structures for users residing in Mexico.

---

## 1. How Trading Automation Works

There are three primary ways to automate trades:

1. **Direct Broker API (Python SDK / REST / WebSockets):**
   * Your Python program executes logic, calculates signals, and calls broker API endpoints directly (e.g., `POST /v2/orders`).
   * *Best for:* Custom LLM bots, backtested quantitative strategies, complex multi-asset execution.
2. **Webhook Automation (TradingView -> Python Server -> Broker API):**
   * TradingView indicators (written in Pine Script) generate buy/sell alerts.
   * TradingView sends a JSON payload via HTTP Webhook to a lightweight Python (FastAPI/Flask) bridge server, which executes the order on the broker API.
   * *Best for:* Technical indicator strategies (RSI, MA cross, MACD).
3. **Institutional Fix Protocol / Third-Party Platforms:**
   * Using intermediate platforms like MetaTrader (MT4/MT5) or TradeStation via FIX protocol.

---

## 2. Top Brokerage Platforms for Mexican Residents

### 🏆 1. Interactive Brokers (IBKR) — *Best Overall for US & Global Stocks/ETFs*

* **Availability in Mexico:** Fully supported for Mexican citizens and tax residents. Automatic W-8BEN form handling.
* **Funding & Deposit Method:** 
  * **SPEI in Pesos (MXN):** You can deposit MXN via SPEI directly into IBKR's local Mexican bank account.
  * **SPEI Cost:** **1st deposit of each month is FREE**. Subsequent deposits in the same month cost 100 MXN.
  * **FX Conversion:** Converts MXN to USD inside IBKR at institutional spot rates (very low FX spread, ~$2 USD flat fee).
* **API Capability:**
  * Exceptional Python integration via `ib_insync`, `ib_async`, or native `ibapi` and Client Portal REST API.
  * Full support for stocks, options, ETFs, futures, and Forex.
* **Cost & Commission Breakdown:**
  * **Tiered Pricing:** ~$0.0035 USD per share (minimum $0.35 USD per order).
  * **Fixed Pricing:** $0.005 USD per share (minimum $1.00 USD per order).
  * **Inactivity Fee:** $0 USD (No minimum balance required).
  * **Market Data:** Free delayed data; real-time US Level 1 data bundle ~$1.50–$4.50 USD/month.

---

### 🚀 2. Alpaca Trading — *Best $0 Commission & Developer API Experience*

* **Availability in Mexico:** Accepts individual accounts for Mexican residents.
* **Funding & Deposit Method:**
  * Requires International Wire Transfer (SWIFT) from Mexican bank accounts (e.g., BBVA, Banorte) to Alpaca.
  * **Wire Transfer Cost:** Sending bank fee (~$20–$50 USD) + Alpaca wire fee ($35–$50 USD per wire).
* **API Capability:**
  * Built natively for developers with clean REST APIs, WebSockets, and `alpaca-py` SDK.
  * Built-in **Paper Trading Sandbox** (simulated trading environment for testing code risk-free).
* **Cost & Commission Breakdown:**
  * **Trade Commissions:** **$0.00 USD (Commission-Free)** on US stocks & ETFs.
  * **Monthly Account Fee:** $0 USD.
  * **Data Feed:** Free real-time IEX feed included.

---

### 🇲🇽 3. Bitso (Bitso Alpha API) — *Best for Crypto Trading in Mexican Pesos (MXN)*

* **Availability in Mexico:** 100% Mexican regulated crypto platform.
* **Funding & Deposit Method:**
  * **SPEI in MXN:** **100% FREE 24/7** instant deposits and withdrawals.
* **API Capability:**
  * Bitso Alpha REST & WebSocket API, native Python support, and full `ccxt` library integration.
* **Cost & Commission Breakdown:**
  * **Maker-Taker Volume Tiered Pricing (MXN Pairs):**
    * *Base Volume (< $20k MXN/mo):* Maker: 0.60% | Taker: 0.78%
    * *Medium Volume (> $500k MXN/mo):* Maker: 0.56% | Taker: 0.728%
    * *High Volume (> $5M MXN/mo):* Maker: 0.45% | Taker: 0.585%

---

### 🏦 4. Local Mexican Brokers (GBM+ / Bursanet)

* **GBM+ (Grupo Bursátil Mexicano):**
  * *Commissions:* 0.25% + VAT per trade.
  * *Automation Limitation:* **Does NOT offer an open retail API** for custom Python trading scripts. Trades must be executed manually or via limited partner tools.
* **Bursanet (Actinver):**
  * *Commissions:* ~0.25% + VAT. Limited/no public API for automated Python scripts.

---

## 3. Summary & Comparison Table

| Platform | Asset Classes | Mexico Funding | Trade Commission | API Quality | Paper Trading Sandbox | Best Choice For |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **Interactive Brokers (IBKR)** | US & Global Stocks, ETFs, Options, Futures | **SPEI (MXN)** (1st free/mo) | ~$0.0035/share (Min $0.35 USD) | ⭐️⭐️⭐️⭐️⭐️ (High) | Yes | **Production Live Trading** (Easy MXN funding, low fees) |
| **Alpaca Trading** | US Stocks & ETFs, Options | International Wire ($35–$50 USD) | **$0.00 USD** | ⭐️⭐️⭐️⭐️⭐️ (Native Dev) | Yes | **Paper Trading & Development** (Zero commissions) |
| **Bitso Alpha** | Crypto (BTC, ETH, SOL, USDT/MXN) | **SPEI (MXN)** (Free 24/7) | 0.45% – 0.78% Maker/Taker | ⭐️⭐️⭐️⭐️ (Good) | No | **Crypto Trading in Pesos** |
| **GBM+ / Bursanet** | BMV & SIC (Mexican/Global Stocks) | SPEI (MXN) (Free) | 0.25% + IVA | ❌ (No retail API) | No | Manual Trading Only |

---

## 4. Recommended Roadmap for `ai-trader`

1. **Development & Testing Phase:**
   * Use **Alpaca Paper Trading API** (Free sandbox, clean API, zero financial risk) to test our LLM signals and execution engine.
2. **Production Execution Engine (Stocks/ETFs):**
   * Use **Interactive Brokers (IBKR)** via `ib_insync` or REST API. Fund easily using **SPEI in MXN**, convert to USD in IBKR, and execute trades with minimal commissions ($0.35 min).
3. **Production Crypto Engine:**
   * Use **Bitso Alpha API** for direct SPEI funding and trading MXN/Crypto pairs.
