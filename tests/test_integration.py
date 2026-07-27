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
