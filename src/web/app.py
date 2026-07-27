from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict

from src.engine.arena import ArenaEngine
from src.engine.backtest import BacktestEngine
from src.data.market_data import MarketDataService
from src.models.schemas import TradeSignal, SignalAction, PortfolioState
from src.compliance.cli_assistant import CLIAssistant

app = FastAPI(title="ai-trader Dashboard", version="1.0.0")

# Services
arena = ArenaEngine()
arena.register_model("Claude-3.5-Sonnet", 1000.0)
arena.register_model("GPT-4o", 1000.0)
arena.register_model("Gemini-Auditor", 1000.0)
arena.update_performance("Claude-3.5-Sonnet", 1140.0)
arena.update_performance("GPT-4o", 1080.0)
arena.update_performance("Gemini-Auditor", 1020.0)

backtest_engine = BacktestEngine()
market_data = MarketDataService()
cli_assistant = CLIAssistant()


class BacktestRequest(BaseModel):
    ticker: str = "TSLA"
    starting_capital: float = 1000.0


class PromptRequest(BaseModel):
    ticker: str = "AAPL"
    mock_text: Optional[str] = None


@app.get("/api/leaderboard")
def get_leaderboard():
    return arena.get_leaderboard()


@app.get("/api/portfolio")
def get_portfolio():
    return {
        "account_id": "PAPER_LIVE_01",
        "cash_balance": 9850.0,
        "total_equity": 10944.30,
        "realized_pnl": 944.30,
        "positions": [
            {"ticker": "TSLA", "quantity": 5.0, "current_price": 224.0, "market_value": 1120.0, "unrealized_pnl": 45.0}
        ]
    }


@app.post("/api/backtest")
def run_backtest(req: BacktestRequest):
    bars = market_data.get_synthetic_bars(req.ticker, count=15)
    signals = [
        TradeSignal(
            ticker=req.ticker,
            action=SignalAction.BUY,
            confidence_score=85.0,
            stop_loss=bars[0].close * 0.95,
            take_profit=bars[0].close * 1.08,
            reasoning_thesis="Web Backtest Simulation",
            invalidation_criteria="N/A",
            advisor_model="Consensus-Council"
        )
    ]
    res = backtest_engine.run_simulation(req.ticker, req.starting_capital, bars, signals)
    return res.model_dump()


@app.post("/api/prompt")
def generate_prompt(req: PromptRequest):
    prompt_text = cli_assistant.prepare_prompt_package(req.ticker, mock_text=req.mock_text)
    return {"ticker": req.ticker, "prompt": prompt_text}


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ai-trader Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg: #0b0f19;
                --card-bg: rgba(18, 26, 44, 0.75);
                --accent: #3b82f6;
                --green: #10b981;
                --red: #ef4444;
                --text: #f3f4f6;
                --muted: #9ca3af;
                --border: rgba(255, 255, 255, 0.1);
            }
            body {
                font-family: 'Inter', sans-serif;
                background-color: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 24px;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 24px;
                padding-bottom: 16px;
                border-bottom: 1px solid var(--border);
            }
            .logo {
                font-size: 24px;
                font-weight: 700;
                background: linear-gradient(135deg, #60a5fa, #3b82f6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 20px;
            }
            .card {
                background: var(--card-bg);
                backdrop-filter: blur(12px);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 20px;
            }
            .card-title {
                font-size: 16px;
                font-weight: 600;
                margin-top: 0;
                margin-bottom: 16px;
                color: var(--muted);
            }
            .stat-value {
                font-size: 28px;
                font-weight: 700;
                color: var(--green);
            }
            .table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 12px;
            }
            .table th, .table td {
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid var(--border);
                font-size: 14px;
            }
            .btn {
                background-color: var(--accent);
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
            }
            .btn:hover {
                opacity: 0.9;
            }
            input {
                background: rgba(0,0,0,0.3);
                border: 1px solid var(--border);
                color: white;
                padding: 10px;
                border-radius: 6px;
                width: 100%;
                margin-bottom: 12px;
                box-sizing: border-box;
            }
            textarea {
                background: rgba(0,0,0,0.4);
                border: 1px solid var(--border);
                color: #34d399;
                font-family: monospace;
                padding: 12px;
                border-radius: 6px;
                width: 100%;
                height: 120px;
                box-sizing: border-box;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">🚀 ai-trader Platform Dashboard</div>
            <div>STATUS: <span style="color:var(--green)">ONLINE (Paper Trading SPEI/Alpaca)</span></div>
        </div>

        <div class="grid">
            <!-- Card 1: Account Portfolio -->
            <div class="card">
                <div class="card-title">PORTAFOLIO EN VIVO</div>
                <div>Equity Total</div>
                <div class="stat-value" id="equity-val">$10,944.30 USD</div>
                <div style="margin-top:8px">Realized PnL: <b style="color:var(--green)">+$944.30 (+9.44%)</b></div>
            </div>

            <!-- Card 2: AI Arena Leaderboard -->
            <div class="card">
                <div class="card-title">MODO ARENA — LEADERBOARD IAs</div>
                <table class="table">
                    <thead>
                        <tr><th>Modelo IA</th><th>Equity</th><th>Retorno %</th></tr>
                    </thead>
                    <tbody id="leaderboard-body">
                        <tr><td>Claude 3.5 Sonnet</td><td>$1,140.00</td><td style="color:var(--green)">+14.0%</td></tr>
                        <tr><td>GPT-4o</td><td>$1,080.00</td><td style="color:var(--green)">+8.0%</td></tr>
                        <tr><td>Gemini Auditor</td><td>$1,020.00</td><td style="color:var(--green)">+2.0%</td></tr>
                    </tbody>
                </table>
            </div>

            <!-- Card 3: Interactive Backtest Engine -->
            <div class="card">
                <div class="card-title">EJECUTAR BACKTEST EN VIVO</div>
                <input type="text" id="backtest-ticker" value="TSLA" placeholder="Ticker Symbol (ej. TSLA)">
                <button class="btn" onclick="runBacktest()">Correr Simulación Backtest</button>
                <div id="backtest-res" style="margin-top: 12px; font-size: 14px;"></div>
            </div>
        </div>

        <div style="margin-top:20px;" class="card">
            <div class="card-title">GENERADOR DE PROMPTS CUMPLIMIENTO ToS (GEMINI / CLAUDE / CHATGPT)</div>
            <input type="text" id="prompt-ticker" value="NVDA" placeholder="Ticker (ej. NVDA)">
            <button class="btn" onclick="generatePrompt()">Generar Prompt Package</button>
            <div style="margin-top: 12px;">
                <textarea id="prompt-out" readonly placeholder="El prompt generado aparecerá aquí..."></textarea>
            </div>
        </div>

        <script>
            async function runBacktest() {
                const ticker = document.getElementById('backtest-ticker').value || 'TSLA';
                const res = await fetch('/api/backtest', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ticker: ticker, starting_capital: 1000})
                });
                const data = await res.json();
                document.getElementById('backtest-res').innerHTML = `
                    <b>Resultado Backtest ${data.ticker}:</b><br>
                    Retorno Total: <b style="color:var(--green)">${data.total_return_pct.toFixed(2)}%</b><br>
                    Win Rate: <b>${data.win_rate_pct.toFixed(1)}%</b> | Max Drawdown: <b style="color:var(--red)">${data.max_drawdown_pct.toFixed(2)}%</b>
                `;
            }

            async function generatePrompt() {
                const ticker = document.getElementById('prompt-ticker').value || 'NVDA';
                const res = await fetch('/api/prompt', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ticker: ticker})
                });
                const data = await res.json();
                document.getElementById('prompt-out').value = data.prompt;
            }
        </script>
    </body>
    </html>
    """
