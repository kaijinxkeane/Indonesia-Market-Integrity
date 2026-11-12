"""Daily data pipeline: fetch -> clean -> merge -> write to data/processed/.

This is the part you're writing by hand. The functions below are stubs with
the expected inputs/outputs so the GitHub Actions workflow
(.github/workflows/daily_data_refresh.yml) and the dashboard (app.py) have a
stable entry point to call, regardless of what's inside each function.

Run manually with: python -m src.data.pipeline
"""

import pandas as pd
import requests

from src.config import COMTRADE_API_KEY, MANUAL_DATA_DIR, PROCESSED_DATA_DIR  # noqa: F401


def fetch_prices(tickers: list[str]) -> pd.DataFrame:
    """Pull daily OHLCV from yfinance for the given '.JK' tickers.

    TODO: implement with yfinance. No API key needed.
    """
    raise NotImplementedError


def fetch_macro() -> pd.DataFrame:
    """Pull macro series (GDP, inflation) for Indonesia from the World Bank
    Open Data API.

    No key needed. Chosen over BPS WebAPI (blocked, 3-subject limit) and
    IMF IFS (its free SDMX JSON API was retired; the replacement requires
    a portal account) — World Bank is the only option that's actually
    registration-free and confirmed working.

    Verified manually:
    https://api.worldbank.org/v2/country/IDN/indicator/FP.CPI.TOTL.ZG?format=json&date=2015:2027&per_page=1000
    returns real data with no auth.

    TODO: implement via requests, country=IDN, indicators FP.CPI.TOTL.ZG
    (inflation) and NY.GDP.MKTP.KD.ZG (GDP growth).
    """
    raise NotImplementedError


def fetch_trade_balance() -> pd.DataFrame:
    """Pull Indonesia's trade balance (exports/imports) from UN Comtrade.

    Used instead of a third BPS subject: Comtrade mirrors each trade flow
    against partner-country reports, so it's not just BPS's own number
    re-hosted — a genuine independence check, not a redundant one.

    TODO: implement via the UN Comtrade (ComtradePlus) API using
    COMTRADE_API_KEY from src.config — free, but requires registering for
    a key at comtradeplus.un.org, unlike the IMF/World Bank sources above.
    """
    raise NotImplementedError


def load_manual_tables() -> dict[str, pd.DataFrame]:
    """Load hand-maintained CSVs from data/raw/manual/:
    - free_float.csv      (IDX, manual download)
    - ownership.csv        (KSEI, manual download)
    - ojk_sanctions.csv     (hand-coded from OJK announcements)
    - msci_events.csv       (hand-coded from MSCI announcements)

    TODO: implement the actual loading/parsing once these CSVs exist.
    """
    raise NotImplementedError


def clean_and_merge(
    prices: pd.DataFrame,
    macro: pd.DataFrame,
    trade_balance: pd.DataFrame,
    manual: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Clean and merge all sources into the analysis-ready table.

    TODO: this is the core data cleaning/processing logic — flags for free
    float < 15% / insider ownership >= 95%, anomaly features, event
    timeline join, etc. See ProjectBrief.md methodology section.
    """
    raise NotImplementedError


def main() -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    tickers: list[str] = []  # TODO: fill in IDX tickers of interest

    prices = fetch_prices(tickers)
    macro = fetch_macro()
    trade_balance = fetch_trade_balance()
    manual = load_manual_tables()
    merged = clean_and_merge(prices, macro, trade_balance, manual)

    merged.to_parquet(PROCESSED_DATA_DIR / "merged.parquet", index=False)


if __name__ == "__main__":
    main()
