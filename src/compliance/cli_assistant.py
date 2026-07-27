# src/compliance/cli_assistant.py
from typing import Tuple, Optional
from src.data.news_scraper import NewsScraperService, ArticleData
from src.data.market_data import MarketDataService
from src.compliance.prompt_builder import PromptPackageBuilder, ResponseParser
from src.risk.risk_manager import RiskManager
from src.models.schemas import TradeSignal, PortfolioState
from src.brokers.alpaca_adapter import AlpacaAdapter


class CLIAssistant:
    def __init__(self, alpaca_key: str = "", alpaca_secret: str = ""):
        self.news_scraper = NewsScraperService()
        self.market_data = MarketDataService()
        self.prompt_builder = PromptPackageBuilder()
        self.response_parser = ResponseParser()
        self.risk_manager = RiskManager()
        self.alpaca = AlpacaAdapter(api_key=alpaca_key, secret_key=alpaca_secret)

    def prepare_prompt_package(self, ticker: str, mock_text: Optional[str] = None) -> str:
        if mock_text:
            article = ArticleData(
                url=f"https://finance.example.com/{ticker}",
                title=f"Market Update for {ticker}",
                full_text=mock_text,
                summary=mock_text,
                keywords=[ticker.lower(), "earnings", "stocks"]
            )
        else:
            article = self.news_scraper.fetch_and_parse(f"https://finance.yahoo.com/quote/{ticker}")

        bars = self.market_data.get_synthetic_bars(ticker, count=15)
        indicators = self.market_data.calculate_indicators(bars)

        return self.prompt_builder.build_analysis_prompt(
            ticker=ticker,
            news_headline=article.title,
            full_text_summary=article.summary,
            technical_indicators=indicators
        )

    def process_llm_response(
        self,
        ticker: str,
        raw_response: str,
        trade_amount: float = 1000.0,
        portfolio: Optional[PortfolioState] = None
    ) -> Tuple[TradeSignal, bool, str]:
        signal = self.response_parser.parse_signal(raw_response)

        if not portfolio:
            portfolio = PortfolioState(
                account_id="CLI_DEMO",
                cash_balance=10000.0,
                total_equity=10000.0,
                realized_pnl=0.0,
                unrealized_pnl=0.0
            )

        approved, reason = self.risk_manager.validate_trade(signal, trade_amount, portfolio)
        return signal, approved, reason
