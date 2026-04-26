def diversification_score(portfolio: dict) -> float:
    return sum(weight ** 2 for weight in portfolio.values())


def diversification_label(score: float) -> str:
    if score >= 0.35:
        return "Low diversification"
    if score >= 0.20:
        return "Moderate diversification"
    return "Good diversification"


def main():
    portfolio = {"AAPL": 0.4, "SPY": 0.5, "TSLA": 0.1}
    score = diversification_score(portfolio)

    print(f"Diversification score: {score:.4f}")
    print(f"Interpretation: {diversification_label(score)}")


if __name__ == "__main__":
    main()