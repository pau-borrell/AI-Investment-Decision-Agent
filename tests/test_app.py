from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_offline_app_renders():
    app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run(timeout=30)
    assert not app.exception
    assert len(app.metric) == 3
    assert app.metric[0].value == "0.365"
    assert app.metric[2].value == "96.0%"


def test_invalid_portfolio_shows_error():
    app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run(timeout=30)
    app.text_area[0].set_value('{"AAPL": -1}')
    app.button[0].click().run()
    assert not app.exception
    assert len(app.error) == 1
