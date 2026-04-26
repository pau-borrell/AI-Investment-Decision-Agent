from src.tools.portfolio_input import get_portfolio_from_user
from src.tools.diversification import diversification_score, diversification_label
from src.tools.concentration import concentration_risk
from src.tools.sector_exposure import calculate_sector_exposure, detect_sector_overexposure
from src.tools.return_simulator import monte_carlo_simulation


def analyze_portfolio(portfolio: dict, run_simulation: bool = True) -> dict:
    score = diversification_score(portfolio)
    sectors = calculate_sector_exposure(portfolio)

    result = {
        "portfolio_weights": portfolio,
        "diversification": {
            "score": score,
            "label": diversification_label(score)
        },
        "concentration_risk": concentration_risk(portfolio),
        "sector_exposure": sectors,
        "sector_overexposure": detect_sector_overexposure(sectors)
    }

    if run_simulation:
        result["return_simulation"] = monte_carlo_simulation(portfolio)

    return result


def print_analysis(result: dict):
    print("\nPortfolio weights:")
    for ticker, weight in result["portfolio_weights"].items():
        print(f"{ticker}: {weight:.2%}")

    print("\nDiversification:")
    print(f"Score: {result['diversification']['score']:.4f}")
    print(f"Label: {result['diversification']['label']}")

    print("\nConcentration risk:")
    if result["concentration_risk"]:
        for risk in result["concentration_risk"]:
            print(f"{risk['ticker']}: {risk['weight']:.2%}")
    else:
        print("No asset above threshold.")

    print("\nSector exposure:")
    for sector, weight in result["sector_exposure"].items():
        print(f"{sector}: {weight:.2%}")

    print("\nSector overexposure:")
    if result["sector_overexposure"]:
        for risk in result["sector_overexposure"]:
            print(f"{risk['sector']}: {risk['weight']:.2%}")
    else:
        print("No sector above threshold.")

    if "return_simulation" in result:
        print("\nMonte Carlo simulation:")
        for key, value in result["return_simulation"].items():
            print(f"{key}: {value:.2%}")


def main():
    portfolio = get_portfolio_from_user()
    result = analyze_portfolio(portfolio)
    print_analysis(result)


if __name__ == "__main__":
    main()