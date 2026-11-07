"""Validated long-only portfolio input in a single currency/unit."""
import math
from collections.abc import Mapping


def normalize_portfolio(holdings: list[dict]) -> dict:
    if not holdings:
        raise ValueError("Portfolio must contain at least one holding.")
    amounts = {}
    for item in holdings:
        ticker = item.get("ticker")
        if not isinstance(ticker, str) or not ticker.strip():
            raise ValueError("Each holding requires a nonempty ticker.")
        ticker = ticker.strip().upper()
        raw = item.get("amount")
        if isinstance(raw, bool):
            raise ValueError("Amounts must be finite non-negative numbers.")
        try:
            amount = float(raw)
        except (TypeError, ValueError) as exc:
            raise ValueError("Amounts must be finite non-negative numbers.") from exc
        if not math.isfinite(amount) or amount < 0:
            raise ValueError("Amounts must be finite non-negative numbers.")
        amounts[ticker] = amounts.get(ticker, 0.0) + amount
    total = sum(amounts.values())
    if not math.isfinite(total) or total <= 0:
        raise ValueError("Total portfolio value must be finite and positive.")
    return {ticker: amount / total for ticker, amount in amounts.items() if amount > 0}


def validate_portfolio(portfolio: dict) -> dict:
    if not isinstance(portfolio, Mapping):
        raise ValueError("Portfolio must map tickers to amounts or weights.")
    return normalize_portfolio([{"ticker": k, "amount": v} for k, v in portfolio.items()])


def get_portfolio_from_user() -> dict:
    holdings = []
    print("Enter TICKER AMOUNT using one currency or consistent percentages. Type done to finish.")
    while True:
        value = input("Holding: ").strip()
        if value.lower() == "done":
            try:
                return normalize_portfolio(holdings)
            except ValueError as exc:
                print(exc)
                continue
        try:
            ticker, raw = value.split()
            candidate = {"ticker": ticker, "amount": float(raw)}
            normalize_portfolio([candidate])
        except ValueError as exc:
            print(f"Invalid holding: {exc}")
            continue
        holdings.append(candidate)
