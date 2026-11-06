"""Indonesia Market Integrity dashboard.

Reads pre-processed data written by src/data/pipeline.py (run daily by
.github/workflows/daily_data_refresh.yml) — no API calls or heavy
computation happen at request time.
"""

import pandas as pd
import streamlit as st

from src.config import PROCESSED_DATA_DIR

st.set_page_config(page_title="Indonesia Market Integrity", layout="wide")


@st.cache_data
def load_merged() -> pd.DataFrame | None:
    path = PROCESSED_DATA_DIR / "merged.parquet"
    if not path.exists():
        return None
    return pd.read_parquet(path)


def section_index_vs_events(df: pd.DataFrame) -> None:
    st.subheader("IDX index vs. event timeline")
    st.info("TODO: plot IDX index with MSCI/OJK event markers.")


def section_anomaly_by_free_float(df: pd.DataFrame) -> None:
    st.subheader("Anomaly rate by free float group")
    st.info("TODO: plot anomaly rate, split by free float group.")


def section_flagged_stocks(df: pd.DataFrame) -> None:
    st.subheader("Flagged stocks")
    st.info(
        "TODO: table of statistical outliers. Wording must make clear this "
        "is not an accusation of manipulation (see ProjectBrief.md risks)."
    )


def section_countdown() -> None:
    st.subheader("Countdown to MSCI's June 2027 classification decision")
    st.info("TODO: compute and display days remaining.")


def main() -> None:
    st.title("Indonesia Market Integrity")

    df = load_merged()
    if df is None:
        st.warning(
            "No processed data found yet. Run `python -m src.data.pipeline` "
            "locally, or wait for the daily GitHub Actions refresh."
        )
        return

    section_index_vs_events(df)
    section_anomaly_by_free_float(df)
    section_flagged_stocks(df)
    section_countdown()


if __name__ == "__main__":
    main()
