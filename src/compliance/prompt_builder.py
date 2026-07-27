import json
import re
from typing import Optional

from src.models.schemas import TradeSignal


class PromptPackageBuilder:
    def build_analysis_prompt(
        self,
        ticker: str,
        news_summary: str,
        current_price: float,
        pe_ratio: Optional[float] = None,
    ) -> str:
        pe_str = f"{pe_ratio:.2f}" if pe_ratio else "N/A"
        return f"""
YOU ARE A PROFESSIONAL FINANCIAL ANALYST.
Analyze the following asset and respond ONLY with a valid JSON object.

ASSET TICKER: {ticker}
CURRENT PRICE: ${current_price:.2f}
P/E RATIO: {pe_str}

RECENT NEWS SUMMARY:
{news_summary}

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
