def normalize_portfolio(holdings: list[dict]) -> dict:
    total = sum(item["amount"] for item in holdings)

    if total <= 0:
        raise ValueError("Total portfolio value must be greater than zero.")

    portfolio = {}

    for item in holdings:
        ticker = item["ticker"].upper().strip()
        portfolio[ticker] = item["amount"] / total

    return portfolio


def get_portfolio_from_user() -> dict:
    holdings = []

    print("Enter your portfolio holdings.")
    print("You can enter percentages or money amounts.")
    print("Example: AAPL 40 or SPY 1000")
    print("Type 'done' when finished.\n")

    while True:
        user_input = input("Holding: ").strip()

        if user_input.lower() == "done":
            break

        parts = user_input.split()

        if len(parts) != 2:
            print("Invalid format. Use: TICKER AMOUNT")
            continue

        ticker, amount = parts

        try:
            amount = float(amount)
        except ValueError:
            print("Amount must be a number.")
            continue

        holdings.append({"ticker": ticker, "amount": amount})

    return normalize_portfolio(holdings)


def main():
    portfolio = get_portfolio_from_user()
    print("\nNormalized portfolio weights:")
    for ticker, weight in portfolio.items():
        print(f"{ticker}: {weight:.2%}")


if __name__ == "__main__":
    main()