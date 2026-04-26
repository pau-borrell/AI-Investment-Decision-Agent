import yfinance as yf


def get_ticker_info(ticker: str) -> dict:
    asset = yf.Ticker(ticker)
    return asset.info


def get_asset_type(ticker: str) -> str:
    info = get_ticker_info(ticker)
    quote_type = info.get("quoteType", "").upper()

    if quote_type in {"ETF", "MUTUALFUND"}:
        return "ETF"

    if quote_type in {"EQUITY", "STOCK"}:
        return "STOCK"

    return quote_type or "UNKNOWN"


def get_stock_sector(ticker: str) -> str:
    info = get_ticker_info(ticker)
    return info.get("sector", "Unknown")


def get_etf_sector_weightings(ticker: str) -> dict:
    asset = yf.Ticker(ticker)

    try:
        funds_data = asset.funds_data
        sector_weightings = funds_data.sector_weightings

        if not sector_weightings:
            return {}

        return {
            str(sector): float(weight)
            for sector, weight in sector_weightings.items()
            if weight is not None
        }

    except Exception:
        return {}


def get_etf_top_holdings(ticker: str):
    asset = yf.Ticker(ticker)

    try:
        funds_data = asset.funds_data
        holdings = funds_data.top_holdings
        return holdings
    except Exception:
        return None


def main():
    ticker = input("Ticker: ").upper().strip()

    asset_type = get_asset_type(ticker)
    print(f"Asset type: {asset_type}")

    if asset_type == "STOCK":
        print(f"Sector: {get_stock_sector(ticker)}")

    elif asset_type == "ETF":
        print("ETF sector weightings:")
        print(get_etf_sector_weightings(ticker))

        print("\nETF top holdings:")
        print(get_etf_top_holdings(ticker))


if __name__ == "__main__":
    main()