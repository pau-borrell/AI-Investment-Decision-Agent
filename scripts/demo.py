"""Live local-model demo; use python -m src.demo for the offline walkthrough."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.agent.investment_agent import run_investment_agent
from src.tools.portfolio_input import normalize_portfolio, validate_portfolio
from src.demo import DEFAULT_PORTFOLIO


def _parse_portfolio(value: str | None) -> dict:
    if not value:
        return DEFAULT_PORTFOLIO.copy()
    path = Path(value)
    if path.is_file():
        return validate_portfolio(json.loads(path.read_text(encoding="utf-8")))
    holdings = []
    for item in value.split(","):
        if "=" not in item:
            raise ValueError("Use TICKER=AMOUNT pairs or a JSON file.")
        ticker, amount = item.split("=", 1)
        holdings.append({"ticker": ticker, "amount": amount})
    return normalize_portfolio(holdings)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="How concentrated is my portfolio?")
    parser.add_argument("--portfolio", help="JSON file or TICKER=AMOUNT pairs")
    parser.add_argument("--cases", type=Path, help="Explicitly run a cases file")
    parser.add_argument("--case-id", "--case_id", "--case", dest="case_id")
    parser.add_argument("--save-output", type=Path)
    parser.add_argument("--skip-simulation", action="store_true",
                        help="Compatibility option: simulation is now off by default.")
    parser.add_argument("--simulate", action="store_true", help="Opt in to historical price downloads")
    args = parser.parse_args()
    try:
        if args.cases or args.case_id:
            path = args.cases or ROOT / "data/evaluation_cases.json"
            cases = json.loads(path.read_text(encoding="utf-8"))
            if args.case_id:
                cases = [c for c in cases if c["id"] == args.case_id]
            if not cases:
                raise ValueError("No matching evaluation cases.")
        else:
            cases = [{"id": "custom", "query": args.query,
                      "portfolio": _parse_portfolio(args.portfolio)}]
        results = []
        for case in cases:
            result = run_investment_agent(case["query"], case["portfolio"],
                                          run_simulation=args.simulate and not args.skip_simulation)
            result["case_id"] = case["id"]
            results.append(result)
            print(json.dumps(result, indent=2, allow_nan=False))
        if args.save_output:
            args.save_output.parent.mkdir(parents=True, exist_ok=True)
            args.save_output.write_text(
                "".join(json.dumps(r, allow_nan=False) + "\n" for r in results), encoding="utf-8")
        if any(not r["validation"]["valid"] for r in results):
            raise SystemExit(1)
    except (ValueError, OSError, RuntimeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
