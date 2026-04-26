from src.tools.market_data import get_asset_type, get_stock_sector, get_etf_sector_weightings


def calculate_sector_exposure(portfolio: dict) -> dict:
    sector_exposure = {}

    for ticker, portfolio_weight in portfolio.items():
        asset_type = get_asset_type(ticker)

        if asset_type == "ETF":
            etf_sectors = get_etf_sector_weightings(ticker)

            if etf_sectors:
                for sector, sector_weight in etf_sectors.items():
                    sector_exposure[sector] = sector_exposure.get(sector, 0) + portfolio_weight * sector_weight
            else:
                sector_exposure["Unknown ETF exposure"] = sector_exposure.get("Unknown ETF exposure", 0) + portfolio_weight

        elif asset_type == "STOCK":
            sector = get_stock_sector(ticker)
            sector_exposure[sector] = sector_exposure.get(sector, 0) + portfolio_weight

        else:
            sector_exposure["Unknown"] = sector_exposure.get("Unknown", 0) + portfolio_weight

    return sector_exposure


def detect_sector_overexposure(sector_exposure: dict, threshold: float = 0.30) -> list[dict]:
    risks = []

    for sector, weight in sector_exposure.items():
        if weight > threshold:
            risks.append(
                {
                    "sector": sector,
                    "weight": weight,
                    "threshold": threshold
                }
            )

    return risks


def main():
    portfolio = {"AAPL": 0.4, "SPY": 0.5, "TSLA": 0.1}

    exposure = calculate_sector_exposure(portfolio)
    risks = detect_sector_overexposure(exposure)

    print("Sector exposure:")
    for sector, weight in exposure.items():
        print(f"{sector}: {weight:.2%}")

    print("\nSector overexposure:")
    for risk in risks:
        print(f"{risk['sector']}: {risk['weight']:.2%}")


if __name__ == "__main__":
    main()