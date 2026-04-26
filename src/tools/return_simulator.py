import numpy as np
import yfinance as yf


def get_portfolio_returns(portfolio: dict, period: str = "10y") -> np.ndarray:
    tickers = list(portfolio.keys())
    weights = np.array(list(portfolio.values()))

    data = yf.download(
        tickers,
        period=period,
        auto_adjust=True,
        progress=False
    )["Close"]

    if len(tickers) == 1:
        returns = data.pct_change().dropna().to_frame()
    else:
        returns = data.pct_change().dropna()

    portfolio_returns = returns.dot(weights)
    return portfolio_returns.to_numpy()


def monte_carlo_simulation(
    portfolio: dict,
    simulations: int = 1000,
    days: int = 252,
    period: str = "10y"
) -> dict:
    historical_returns = get_portfolio_returns(portfolio, period=period)

    mean_return = np.mean(historical_returns)
    volatility = np.std(historical_returns)

    simulated_final_returns = []

    for _ in range(simulations):
        simulated_daily_returns = np.random.normal(mean_return, volatility, days)
        cumulative_return = np.prod(1 + simulated_daily_returns) - 1
        simulated_final_returns.append(cumulative_return)

    simulated_final_returns = np.array(simulated_final_returns)

    return {
        "expected_1y_return": float(np.mean(simulated_final_returns)),
        "volatility": float(np.std(simulated_final_returns)),
        "worst_5_percent": float(np.percentile(simulated_final_returns, 5)),
        "best_5_percent": float(np.percentile(simulated_final_returns, 95))
    }


def main():
    portfolio = {"AAPL": 0.4, "SPY": 0.5, "TSLA": 0.1}
    result = monte_carlo_simulation(portfolio)

    print("Monte Carlo simulation:")
    for key, value in result.items():
        print(f"{key}: {value:.2%}")


if __name__ == "__main__":
    main()