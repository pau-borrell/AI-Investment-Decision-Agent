import numpy as np
import pandas as pd
import pytest
from src.tools.return_simulator import portfolio_returns_from_prices, monte_carlo_simulation


def test_returns_align_by_ticker_not_download_column_order():
    prices = pd.DataFrame({"A": [100., 110., 121.], "Z": [100., 100., 100.]})
    out = portfolio_returns_from_prices(prices, {"Z": .9, "A": .1})
    np.testing.assert_allclose(out, [.01, .01])


def test_single_ticker_dataframe_and_series_supported():
    frame = pd.DataFrame({"A": [100., 110., 121.]})
    np.testing.assert_allclose(portfolio_returns_from_prices(frame, {"A": 1}), [.1, .1])
    np.testing.assert_allclose(portfolio_returns_from_prices(frame.A, {"A": 1}), [.1, .1])


def test_cash_does_not_download_or_renormalize_risky_weight():
    prices = pd.DataFrame({"A": [100., 110., 121.]})
    np.testing.assert_allclose(portfolio_returns_from_prices(prices, {"A": .5, "CASH": .5}), [.05, .05])


def test_missing_price_history_fails():
    with pytest.raises(ValueError, match="Missing"):
        portfolio_returns_from_prices(pd.DataFrame({"A": [1, 2, 3]}), {"B": 1})


def test_no_forward_fill_of_missing_prices():
    frame = pd.DataFrame({"A": [100., np.nan, 121., 130.]})
    with pytest.raises(ValueError, match="aligned"):
        portfolio_returns_from_prices(frame, {"A": 1})


def test_bootstrap_repeatability_and_horizon():
    kwargs = dict(portfolio={"A": 1}, historical_returns=[-.01, .01, .005],
                  simulations=100, days=10, seed=17)
    a, b = monte_carlo_simulation(**kwargs), monte_carlo_simulation(**kwargs)
    assert a == b
    assert a["days"] == 10 and a["seed"] == 17
    assert a["percentile_5"] <= a["percentile_95"]


@pytest.mark.parametrize("values", [[], [np.nan, .1], [-1.1, .2]])
def test_invalid_historical_returns(values):
    with pytest.raises(ValueError):
        monte_carlo_simulation({"A": 1}, historical_returns=values)
