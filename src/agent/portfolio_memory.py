"""Interactive input only; no durable memory or storage is implied."""
from src.tools.portfolio_input import get_portfolio_from_user


def collect_portfolio() -> dict:
    return get_portfolio_from_user()


if __name__ == "__main__":
    print(collect_portfolio())
