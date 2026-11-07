"""Sector look-through with explicit residual coverage."""
import math
import re
from src.tools.portfolio_input import validate_portfolio

SECTOR_NAMES = {
    "technology": "Technology", "informationtechnology": "Technology",
    "financialservices": "Financial Services", "financials": "Financial Services",
    "healthcare": "Healthcare", "health": "Healthcare",
    "consumerdefensive": "Consumer Defensive", "consumerstaples": "Consumer Defensive",
    "consumercyclical": "Consumer Cyclical", "consumerdiscretionary": "Consumer Cyclical",
    "communicationservices": "Communication Services",
    "basicmaterials": "Basic Materials", "materials": "Basic Materials",
    "realestate": "Real Estate", "industrials": "Industrials",
    "utilities": "Utilities", "energy": "Energy",
}


def canonical_sector(name: str) -> str:
    key = re.sub(r"[^a-z]", "", str(name).lower())
    return SECTOR_NAMES.get(key, "Unknown")


def sector_breakdown(portfolio: dict, asset_metadata: dict | None = None) -> dict:
    portfolio = validate_portfolio(portfolio)
    exposure, warnings = {}, []
    def add(name, weight):
        exposure[name] = exposure.get(name, 0.0) + weight

    for ticker, weight in portfolio.items():
        if ticker == "CASH":
            add("Cash", weight)
            continue
        try:
            if asset_metadata is None:
                from src.tools.market_data import (
                    get_asset_type, get_stock_sector, get_etf_sector_weightings
                )
                kind = get_asset_type(ticker)
                metadata = {"type": kind}
                if kind == "STOCK":
                    metadata["sector"] = get_stock_sector(ticker)
                elif kind == "ETF":
                    metadata["sectors"] = get_etf_sector_weightings(ticker)
            else:
                metadata = asset_metadata.get(ticker, {})
            kind = metadata.get("type", "UNKNOWN")
            if kind == "STOCK":
                add(canonical_sector(metadata.get("sector", "")), weight)
            elif kind == "ETF":
                sectors = metadata.get("sectors", {})
                converted = {}
                for name, value in sectors.items():
                    value = float(value)
                    if not math.isfinite(value) or value < 0:
                        raise ValueError("Invalid sector weights.")
                    sector = canonical_sector(name)
                    converted[sector] = converted.get(sector, 0.0) + value
                total = sum(converted.values())
                if total > 1 + 1e-6:
                    raise ValueError("ETF sector weights exceed 100%.")
                for name, value in converted.items():
                    add(name, weight * value / max(1.0, total))
                add("Unknown", weight * max(0.0, 1 - total))
            else:
                add("Unknown", weight)
        except Exception as exc:
            add("Unknown", weight)
            warnings.append(f"{ticker}: sector data unavailable ({type(exc).__name__}).")
    exposure = {k: v for k, v in exposure.items() if v > 1e-12}
    unknown = exposure.get("Unknown", 0.0)
    if unknown:
        warnings.append(f"Sector data is unknown for {unknown:.1%} of portfolio weight.")
    return {"exposure": exposure, "known_weight": 1 - unknown, "warnings": warnings}


def calculate_sector_exposure(portfolio: dict, asset_metadata: dict | None = None) -> dict:
    return sector_breakdown(portfolio, asset_metadata)["exposure"]


def detect_sector_overexposure(sector_exposure: dict, threshold: float = 0.30) -> list[dict]:
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("Sector threshold must be between 0 and 1.")
    return [{"sector": s, "weight": w, "threshold": threshold}
            for s, w in sector_exposure.items()
            if s not in {"Unknown", "Cash"} and w > threshold]
