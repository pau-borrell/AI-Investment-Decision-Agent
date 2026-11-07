"""Offline walkthrough: python -m src.demo --out outputs/offline_demo.json."""
import argparse
import hashlib
import json
from pathlib import Path
from src.rag.offline import retrieve_offline
from src.tools.analyze_portfolio import analyze_portfolio
from src.tools.portfolio_input import validate_portfolio

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PORTFOLIO = {"AAPL": 0.45, "MSFT": 0.35, "SPY": 0.20}
DEFAULT_QUERY = "How diversified is this portfolio and what sector concentration is present?"


def run_offline_demo(portfolio=None, query=DEFAULT_QUERY) -> dict:
    portfolio = validate_portfolio(DEFAULT_PORTFOLIO if portfolio is None else portfolio)
    snapshot_path = ROOT / "data/demo_snapshot.json"
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    analysis = analyze_portfolio(portfolio, run_simulation=False, asset_metadata=snapshot["assets"])
    sources = retrieve_offline(query)
    return {
        "mode": "offline_analytics", "uses_llm": False,
        "notice": snapshot["description"],
        "query": query, "portfolio_analysis": analysis,
        "retrieved_chunks": sources,
        "snapshot_sha256": hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),
        "corpus_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted((ROOT / "data/raw").glob("*.txt"))},
        "recommendation": None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--portfolio", type=Path, help="JSON ticker-to-amount mapping")
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--out", type=Path, default=Path("outputs/offline_demo.json"))
    args = parser.parse_args()
    try:
        portfolio = json.loads(args.portfolio.read_text()) if args.portfolio else None
        result = run_offline_demo(portfolio, args.query)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
