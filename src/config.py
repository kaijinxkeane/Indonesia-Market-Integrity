"""Central place to load API keys and data paths.

Reads from environment variables first (populated from .env locally, or
from GitHub Actions `secrets` in CI), then falls back to Streamlit's
st.secrets when running inside the dashboard. Cleaning/pipeline code should
import the constants below rather than touching os.environ or st.secrets
directly, so the storage mechanism can change without touching that code.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def get_secret(key: str, default: str | None = None) -> str | None:
    value = os.environ.get(key)
    if value:
        return value
    try:
        import streamlit as st

        return st.secrets.get(key, default)
    except Exception:
        return default


BPS_API_KEY = get_secret("BPS_API_KEY")
EODHD_API_KEY = get_secret("EODHD_API_KEY")

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
MANUAL_DATA_DIR = RAW_DATA_DIR / "manual"
PROCESSED_DATA_DIR = ROOT_DIR / "data" / "processed"
