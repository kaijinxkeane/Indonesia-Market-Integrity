"""Daily data pipeline: fetch -> clean -> merge -> write to data/processed/.

This is the part you're writing by hand. The functions below are stubs with
the expected inputs/outputs so the GitHub Actions workflow
(.github/workflows/daily_data_refresh.yml) and the dashboard (app.py) have a
stable entry point to call, regardless of what's inside each function.

Run manually with: python -m src.data.pipeline
"""

import pandas as pd
import requests
import yfinance as yf

from src.config import COMTRADE_API_KEY, MANUAL_DATA_DIR, PROCESSED_DATA_DIR  # noqa: F401


def fetch_prices(tickers: list[str]) -> pd.DataFrame:
    raw = yf.download(tickers, start="2023-01-01", auto_adjust=False)
    df = raw.stack(level=1, future_stack=True)
    df = df.rename_axis(index=["date", "ticker"]).reset_index()
    df.columns = [str(c).lower() for c in df.columns]
    return df


def fetch_macro() -> pd.DataFrame:
    URL = "https://api.worldbank.org/v2/country/IDN/indicator/FP.CPI.TOTL.ZG?format=json&date=2015:2027&per_page=1000"
    request = requests.get(URL)
    if request.status_code != 200:
        raise RuntimeError(f"World Bank API returned {request.status_code} for inflation")
    data = request.json()
    if len(data) <= 1 or not isinstance(data[1], list):
        raise ValueError("Unexpected data format from World Bank API.")
    df = pd.DataFrame(data[1])
    df = df[['date', 'value']]
    df.rename(columns={'date': 'year', 'value': 'inflation'}, inplace=True)

    URL2 = "https://api.worldbank.org/v2/country/IDN/indicator/NY.GDP.MKTP.KD.ZG?format=json&date=2015:2027&per_page=1000"
    request2 = requests.get(URL2)
    if request2.status_code != 200:
        raise RuntimeError(f"World Bank API returned {request2.status_code} for GDP growth")
    data2 = request2.json()
    if len(data2) <= 1 or not isinstance(data2[1], list):
        raise ValueError("Unexpected data format from World Bank API.")
    df2 = pd.DataFrame(data2[1])
    df2 = df2[['date', 'value']]
    df2.rename(columns={'date': 'year', 'value': 'gdp_growth'}, inplace=True)

    return df.merge(df2, on='year')


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

    tickers: list[str] = [
        "BBCA.JK",  # Bank Central Asia
        "BBRI.JK",  # Bank Rakyat Indonesia
        "BMRI.JK",  # Bank Mandiri
        "BBNI.JK",  # Bank Negara Indonesia
        "TLKM.JK",  # Telkom Indonesia
        "ASII.JK",  # Astra International
        "UNVR.JK",  # Unilever Indonesia
        "ICBP.JK",  # Indofood CBP
        "ADRO.JK",  # Adaro Energy
        "PGAS.JK",  # Perusahaan Gas Negara
        "PTBA.JK",  # Bukit Asam (coal)
        "ANTM.JK",  # Aneka Tambang (mining)
        "INCO.JK",  # Vale Indonesia (nickel)
        "GOTO.JK",  # GoTo (tech/e-commerce)
        "MDKA.JK",  # Merdeka Copper Gold
    ]  # TODO: refine into free-float / MSCI-constituent groups once manual tables exist

    prices = fetch_prices(tickers)
    macro = fetch_macro()
    trade_balance = fetch_trade_balance()
    manual = load_manual_tables()
    merged = clean_and_merge(prices, macro, trade_balance, manual)

    merged.to_parquet(PROCESSED_DATA_DIR / "merged.parquet", index=False)


if __name__ == "__main__":
    main()
