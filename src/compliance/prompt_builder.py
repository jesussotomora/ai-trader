import json
import re
from typing import Optional

from src.models.schemas import TradeSignal


class PromptPackageBuilder:
    def build_analysis_prompt(
        self,
        ticker: str,
        news_summary: str = "",
        current_price: float = 0.0,
        pe_ratio: Optional[float] = None,
        news_headline: Optional[str] = None,
        full_text_summary: Optional[str] = None,
        technical_indicators: Optional[dict] = None,
    ) -> str:
        summary = full_text_summary or news_summary
        headline_str = f"HEADLINE: {news_headline}\n" if news_headline else ""
        price_str = f"${current_price:.2f}" if current_price else "N/A"
        pe_str = f"{pe_ratio:.2f}" if pe_ratio else "N/A"
        tech_str = f"\nTECHNICAL INDICATORS:\n{json.dumps(technical_indicators, indent=2)}\n" if technical_indicators else ""

        return f"""
YOU ARE A PROFESSIONAL FINANCIAL ANALYST.
Analyze the following asset and respond ONLY with a valid JSON object.

ASSET TICKER: {ticker}
CURRENT PRICE: {price_str}
P/E RATIO: {pe_str}
{headline_str}
RECENT NEWS SUMMARY:
{summary}
{tech_str}
YOUR RESPONSE MUST STRICTLY MATCH THIS JSON SCHEMA:
{{
    "ticker": "{ticker}",
    "action": "BUY | SELL | HOLD",
    "confidence_score": 0.0 to 100.0,
    "target_price": number or null,
    "stop_loss": number,
    "take_profit": number,
    "reasoning_thesis": "string",
    "invalidation_criteria": "string",
    "advisor_model": "Model-Name"
}}
"""


class ResponseParser:
    def parse_signal(self, raw_response: str) -> TradeSignal:
        # Extract JSON block if wrapped in markdown code fence
        json_match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response string")

        json_str = json_match.group(0)
        data = json.loads(json_str)
        return TradeSignal(**data)
