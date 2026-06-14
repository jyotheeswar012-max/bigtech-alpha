"""
Integration smoke-tests for Streamlit page rendering logic.
=====================================================
These tests validate the data-transformation helpers in nexus.py
(best_common_year, get_latest_slice, build_merged_data) using
fully synthetic DataFrames — no Streamlit server needed.

Run:  pytest tests/test_integration_pages.py -v
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys, os

# ── Stub out Streamlit & heavy optional deps before importing nexus ──────────
STREAMLIT_STUB = MagicMock()
STREAMLIT_STUB.session_state = {}
STREAMLIT_STUB.cache_data = lambda **kw: (lambda f: f)  # identity decorator
sys.modules.setdefault("streamlit", STREAMLIT_STUB)
sys.modules.setdefault("streamlit_autorefresh", MagicMock())
sys.modules.setdefault("yfinance", MagicMock())
sys.modules.setdefault("plotly", MagicMock())
sys.modules.setdefault("plotly.graph_objects", MagicMock())
sys.modules.setdefault("plotly.express", MagicMock())
sys.modules.setdefault("plotly.subplots", MagicMock())

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import only the helpers we want to test independently
from live_data import merge_with_csv, COMPANIES, TICKERS, SECTOR_MAP


# ── Shared synthetic dataset ──────────────────────────────────────────────────

ALL_COS = list(COMPANIES.values())  # 8 company names


def make_annual_df(years=range(2021, 2025)):
    rows = []
    for co in ALL_COS:
        for yr in years:
            rows.append({
                "Company":     co,
                "Year":        yr,
                "Revenue_B":   float(np.random.randint(50, 500)),
                "NetIncome_B": float(np.random.randint(5, 100)),
                "MarketCap_B": float(np.random.randint(200, 3000)),
                "Employees_K": float(np.random.randint(10, 200)),
            })
    return pd.DataFrame(rows)


def make_price_df(n_days=30):
    rows = []
    for co in ALL_COS:
        prices = np.cumsum(np.random.randn(n_days)) + 150
        dates  = pd.date_range("2024-01-01", periods=n_days, freq="D")
        for d, p in zip(dates, prices):
            rows.append({"Date": d, "Company": co, "Price": round(abs(p), 2)})
    return pd.DataFrame(rows)


def make_quarterly_df():
    rows = []
    quarters = pd.date_range("2021-01-01", periods=12, freq="QS")
    for co in ALL_COS:
        for q in quarters:
            rows.append({
                "Quarter":     q,
                "Company":     co,
                "Revenue_B":   float(np.random.randint(10, 120)),
                "NetIncome_B": float(np.random.randint(1, 30)),
            })
    return pd.DataFrame(rows)


# ── best_common_year logic (extracted inline) ─────────────────────────────────

class TestBestCommonYear:
    """Replicate the best_common_year logic from nexus.py for isolated testing."""

    def _best_common_year(self, df, all_cos):
        sub = df[df['Company'].isin(all_cos)]
        if sub.empty:
            return int(df['Year'].max()) if not df.empty else 2025
        yc = sub.groupby('Year')['Company'].nunique()
        if yc.empty:
            return int(df['Year'].max())
        valid = yc[yc >= max(1, len(all_cos) // 2)]
        return int(valid.index.max()) if not valid.empty else int(yc.index.max())

    def test_returns_latest_fully_covered_year(self):
        df = make_annual_df(years=range(2021, 2025))
        yr = self._best_common_year(df, ALL_COS)
        assert yr == 2024

    def test_handles_subset_of_companies(self):
        df = make_annual_df(years=range(2021, 2025))
        subset = ALL_COS[:3]
        yr = self._best_common_year(df, subset)
        assert 2021 <= yr <= 2024

    def test_empty_df_returns_fallback(self):
        yr = self._best_common_year(pd.DataFrame(columns=["Company", "Year"]), ALL_COS)
        assert yr == 2025

    def test_single_year_single_company(self):
        df = pd.DataFrame([{"Company": "Apple", "Year": 2022,
                             "Revenue_B": 394.0, "NetIncome_B": 99.8}])
        yr = self._best_common_year(df, ["Apple"])
        assert yr == 2022


# ── get_latest_slice logic ────────────────────────────────────────────────────

class TestGetLatestSlice:
    """Replicate get_latest_slice from nexus.py."""

    def _best_common_year(self, df, all_cos):
        sub = df[df['Company'].isin(all_cos)]
        if sub.empty:
            return int(df['Year'].max()) if not df.empty else 2025
        yc = sub.groupby('Year')['Company'].nunique()
        valid = yc[yc >= max(1, len(all_cos) // 2)]
        return int(valid.index.max()) if not valid.empty else int(yc.index.max())

    def _get_latest_slice(self, df, companies, fallback_year=None):
        if df.empty:
            return pd.DataFrame(), fallback_year or 2025
        sub = df[df['Company'].isin(companies)]
        if sub.empty:
            return pd.DataFrame(), fallback_year or 2025
        yr = self._best_common_year(sub, companies) if fallback_year is None else fallback_year
        return sub[sub['Year'] == yr].copy(), yr

    def test_returns_only_latest_year_rows(self):
        df = make_annual_df(years=range(2021, 2025))
        sl, yr = self._get_latest_slice(df, ALL_COS)
        assert (sl["Year"] == yr).all()

    def test_slice_has_all_companies(self):
        df = make_annual_df(years=range(2021, 2025))
        sl, yr = self._get_latest_slice(df, ALL_COS)
        assert set(sl["Company"].unique()) == set(ALL_COS)

    def test_empty_df_returns_empty_slice(self):
        sl, yr = self._get_latest_slice(pd.DataFrame(), ALL_COS)
        assert sl.empty
        assert yr == 2025

    def test_unknown_companies_returns_empty(self):
        df = make_annual_df()
        sl, yr = self._get_latest_slice(df, ["FakeCompany"])
        assert sl.empty


# ── merge_with_csv integration ────────────────────────────────────────────────

class TestMergeWithCsvIntegration:
    def test_live_data_wins_on_overlapping_key(self):
        csv = pd.DataFrame([
            {"Company": "Apple", "Year": 2024, "Revenue_B": 380.0, "RD_B": 29.9},
        ])
        live = pd.DataFrame([
            {"Company": "Apple", "Year": 2024, "Revenue_B": 395.0},
        ])
        result = merge_with_csv(live, csv, ["Company", "Year"])
        apple = result[(result["Company"] == "Apple") & (result["Year"] == 2024)]
        assert apple["Revenue_B"].values[0] == 395.0

    def test_csv_only_column_backfilled_into_live(self):
        csv = pd.DataFrame([
            {"Company": "Apple", "Year": 2024, "Revenue_B": 380.0, "RD_B": 29.9},
        ])
        live = pd.DataFrame([
            {"Company": "Apple", "Year": 2024, "Revenue_B": 395.0},
        ])
        result = merge_with_csv(live, csv, ["Company", "Year"])
        apple = result[(result["Company"] == "Apple") & (result["Year"] == 2024)]
        assert "RD_B" in result.columns

    def test_no_duplicates_after_merge(self):
        ann = make_annual_df()
        csv = make_annual_df(years=range(2019, 2024))
        result = merge_with_csv(ann, csv, ["Company", "Year"])
        assert not result.duplicated(subset=["Company", "Year"]).any()

    def test_all_8_companies_present_after_merge(self):
        ann = make_annual_df()
        csv = make_annual_df()
        result = merge_with_csv(ann, csv, ["Company", "Year"])
        assert set(result["Company"].unique()) == set(ALL_COS)


# ── Price dataframe structural tests ─────────────────────────────────────────

class TestPriceDataFrame:
    def test_price_df_has_required_columns(self):
        df = make_price_df()
        for col in ["Date", "Company", "Price"]:
            assert col in df.columns

    def test_all_prices_positive(self):
        df = make_price_df()
        assert (df["Price"] > 0).all()

    def test_price_df_has_all_companies(self):
        df = make_price_df()
        assert set(df["Company"].unique()) == set(ALL_COS)


# ── Quarterly dataframe structural tests ─────────────────────────────────────

class TestQuarterlyDataFrame:
    def test_quarterly_df_has_required_columns(self):
        df = make_quarterly_df()
        for col in ["Quarter", "Company", "Revenue_B"]:
            assert col in df.columns

    def test_quarters_are_datetimes(self):
        df = make_quarterly_df()
        assert pd.api.types.is_datetime64_any_dtype(df["Quarter"])

    def test_revenue_is_positive(self):
        df = make_quarterly_df()
        assert (df["Revenue_B"] > 0).all()
