"""Interactive local-model entry point."""
import json
from src.agent.investment_agent import run_investment_agent
from src.agent.portfolio_memory import collect_portfolio


def main():
    portfolio = collect_portfolio()
    query = input("\nQuestion: ").strip()
    result = run_investment_agent(query, portfolio)
    print("\nMODEL RESPONSE")
    print(result["answer"])
    print("\nRETRIEVED SOURCES")
    for chunk in result["retrieved_chunks"]:
        print(f"{chunk['metadata']['source']} - {chunk['id']}")
    print("\nPORTFOLIO TOOL OUTPUT")
    print(json.dumps(result["portfolio_analysis"], indent=2, allow_nan=False))
    for warning in result["warnings"]:
        print(f"Warning: {warning}")
    print("\nRESPONSE VALIDATION")
    print(json.dumps(result["validation"], indent=2))
    if not result["validation"]["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
