#!/usr/bin/env python3
"""
Interactive CLI Assistant for ai-trader
Prepares LLM analysis prompt for Gemini/Claude/ChatGPT web subscriptions.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.compliance.cli_assistant import CLIAssistant

def main():
    ticker = sys.argv[1] if len(sys.argv) > 1 else "TSLA"
    assistant = CLIAssistant()
    print("=" * 65)
    print(f" 🤖 AI-TRADER SUBSCRIPTION ASSISTANT FOR: {ticker}")
    print("=" * 65)

    prompt = assistant.prepare_prompt_package(ticker, mock_text=f"Surge in {ticker} demand following quarterly earnings release.")
    print("\n📋 COPY THE FOLLOWING PROMPT TO YOUR GEMINI ADVANCED / CLAUDE / CHATGPT WEB APP:\n")
    print("-" * 65)
    print(prompt)
    print("-" * 65)

if __name__ == "__main__":
    main()
