"""Seeded historical bootstrap scenarios, not return forecasts."""
import numpy as np
from src.tools.portfolio_input import validate_portfolio


def portfolio_returns_from_prices(prices, portfolio: dict) -> np.ndarray:
    import pandas as pd
    portfolio = validate_portfolio(portfolio)
    tickers = [t for t in portfolio if t != "CASH"]
    if not tickers:
        raise ValueError("Cash-only portfolios have no risky return history to simulate.")
    if isinstance(prices, pd.Series):
        if len(tickers) != 1:
            raise ValueError("A price series can only represent one risky ticker.")
        prices = prices.to_frame(name=tickers[0])
    if not isinstance(prices, pd.DataFrame) or any(t not in prices for t in tickers):
        raise ValueError("Missing adjusted price data for one or more holdings.")
    frame = prices.loc[:, tickers].sort_index()
    if frame.index.has_duplicates:
        raise ValueError("Duplicate price timestamps.")
    if frame.dropna().le(0).any().any():
        raise ValueError("Prices must be positive.")
    returns = frame.pct_change(fill_method=None).replace([np.inf, -np.inf], np.nan).dropna()
    if len(returns) < 2:
        raise ValueError("At least two aligned daily returns are required.")
    # Explicit labels avoid yfinance's alphabetical column-order mismatch.
    values = returns.dot(pd.Series({t: portfolio[t] for t in tickers}))
    if not np.isfinite(values).all():
        raise ValueError("Non-finite portfolio returns.")
    return values.to_numpy()


def get_portfolio_returns(portfolio: dict, period: str = "10y") -> np.ndarray:
    import yfinance as yf
    portfolio = validate_portfolio(portfolio)
    tickers = [t for t in portfolio if t != "CASH"]
    if not tickers:
        raise ValueError("Cash-only portfolios are not simulated.")
    try:
        downloaded = yf.download(tickers, period=period, auto_adjust=True, progress=False)
        prices = downloaded["Close"]
    except Exception as exc:
        raise RuntimeError("Historical price download failed.") from exc
    return portfolio_returns_from_prices(prices, portfolio)


def monte_carlo_simulation(portfolio: dict, simulations: int = 1000, days: int = 252,
                           period: str = "10y", seed: int = 42,
                           historical_returns=None) -> dict:
    validate_portfolio(portfolio)
    for name, value in [("simulations", simulations), ("days", days)]:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")
    if simulations * days > 10_000_000:
        raise ValueError("Requested simulation exceeds the 10 million sample limit.")
    history = np.asarray(get_portfolio_returns(portfolio, period) if historical_returns is None
                         else historical_returns, dtype=float)
    if history.ndim != 1 or len(history) < 2 or not np.isfinite(history).all() or (history < -1).any():
        raise ValueError("Need at least two finite portfolio returns, each >= -100%.")
    rng = np.random.default_rng(seed)
    final = np.prod(1 + rng.choice(history, size=(simulations, days), replace=True), axis=1) - 1
    return {
        "mean_scenario_return": float(final.mean()),
        "scenario_std": float(final.std()),
        "percentile_5": float(np.percentile(final, 5)),
        "percentile_95": float(np.percentile(final, 95)),
        "days": days, "simulations": simulations, "seed": seed,
        "historical_observations": len(history),
        "method": "iid historical bootstrap; daily rebalanced weights; zero cash yield",
    }
