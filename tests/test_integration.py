from unittest.mock import patch, MagicMock
from src.models.schemas import PortfolioState, SignalAction, HistoricalBar, TradeSignal
from src.data.news_scraper import NewsScraperService, ArticleData
from src.compliance.prompt_builder import PromptPackageBuilder, ResponseParser
from src.risk.risk_manager import RiskManager
from src.engine.council import AdvisoryCouncil
from src.engine.backtest import BacktestEngine
from src.brokers.alpaca_adapter import AlpacaAdapter


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


def test_integration_with_backtest_engine():
    bars = [
        HistoricalBar(timestamp="2026-07-01", open=50.0, high=52.0, low=49.0, close=51.0, volume=5000.0),
        HistoricalBar(timestamp="2026-07-02", open=51.0, high=60.0, low=50.0, close=58.0, volume=5000.0),  # Hits Take Profit at 55
    ]
    signals = [
        TradeSignal(
            ticker="AMD",
            action=SignalAction.BUY,
            confidence_score=80.0,
            stop_loss=48.0,
            take_profit=55.0,
            reasoning_thesis="Integration test",
            invalidation_criteria="N/A",
            advisor_model="Consensus"
        )
    ]
    engine = BacktestEngine()
    result = engine.run_simulation(ticker="AMD", starting_capital=2000.0, bars=bars, signals=signals)
    assert result.total_return_pct > 0
    assert result.win_rate_pct == 100.0


@patch("requests.post")
def test_alpaca_adapter_integration(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "ORD_TEST_99", "status": "accepted"}
    mock_post.return_value = mock_response

    # Signal & Risk check
    signal = TradeSignal(
        ticker="AAPL", action=SignalAction.BUY, confidence_score=85.0,
        stop_loss=170.0, take_profit=200.0, reasoning_thesis="Buy signal",
        invalidation_criteria="N/A", advisor_model="Claude-3.5-Sonnet"
    )
    risk_mgr = RiskManager()
    portfolio = PortfolioState(account_id="A1", cash_balance=5000.0, total_equity=10000.0, realized_pnl=0.0, unrealized_pnl=0.0)
    approved, _ = risk_mgr.validate_trade(signal, trade_amount=500.0, portfolio=portfolio)
    assert approved

    # Execute via AlpacaAdapter
    adapter = AlpacaAdapter(api_key="KEY", secret_key="SECRET")
    order = adapter.submit_order(symbol=signal.ticker, qty=3.0, side="buy")
    assert order["id"] == "ORD_TEST_99"


