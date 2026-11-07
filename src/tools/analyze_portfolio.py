"""Portfolio analytics; external data providers can be replaced with fixtures."""
from src.tools.portfolio_input import get_portfolio_from_user, validate_portfolio
from src.tools.diversification import diversification_score, diversification_label
from src.tools.concentration import concentration_risk
from src.tools.sector_exposure import sector_breakdown, detect_sector_overexposure


def analyze_portfolio(portfolio: dict, run_simulation: bool = True,
                      asset_metadata: dict | None = None, seed: int = 42) -> dict:
    portfolio = validate_portfolio(portfolio)
    score = diversification_score(portfolio)
    sectors = sector_breakdown(portfolio, asset_metadata)
    result = {
        "portfolio_weights": portfolio,
        "diversification": {
            "score": score, "label": diversification_label(score),
            "effective_positions": 1 / score,
            "scope": "Position-weight HHI; ETF constituent overlap is not measured.",
        },
        "concentration_risk": concentration_risk(portfolio),
        "sector_exposure": sectors["exposure"],
        "sector_overexposure": detect_sector_overexposure(sectors["exposure"]),
        "sector_known_weight": sectors["known_weight"],
        "warnings": sectors["warnings"],
    }
    if run_simulation:
        from src.tools.return_simulator import monte_carlo_simulation
        try:
            result["return_simulation"] = monte_carlo_simulation(portfolio, seed=seed)
        except (ValueError, RuntimeError) as exc:
            result["warnings"].append(f"Simulation unavailable: {exc}")
    return result


def print_analysis(result: dict):
    import json
    print(json.dumps(result, indent=2, allow_nan=False))


def main():
    print_analysis(analyze_portfolio(get_portfolio_from_user()))


if __name__ == "__main__":
    main()
