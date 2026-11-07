THRESHOLD = 0.20


def concentration_risk(portfolio: dict, threshold: float = THRESHOLD) -> list[dict]:
    import math
    from src.tools.portfolio_input import validate_portfolio
    portfolio = validate_portfolio(portfolio)
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError('Threshold must be between 0 and 1.')
    risks = []

    for ticker, weight in portfolio.items():
        if weight > threshold:
            risks.append(
                {
                    "ticker": ticker,
                    "weight": weight,
                    "threshold": threshold
                }
            )

    return risks


def main():
    portfolio = {"AAPL": 0.4, "SPY": 0.5, "TSLA": 0.1}
    risks = concentration_risk(portfolio)

    print("Concentration risks:")
    for risk in risks:
        print(f"{risk['ticker']}: {risk['weight']:.2%}")


if __name__ == "__main__":
    main()