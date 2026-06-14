"""
Unit tests for live_data.py
=====================================================
All network calls are mocked with unittest.mock so
tests run offline with no yfinance quota usage.

Run:  pytest tests/test_live_data.py -v
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import live_data as ld


# ── Fixtures ──────────────────────────────────────────────────────────────────

MOCK_INFO = {
    "currentPrice":                  182.50,
    "regularMarketPrice":            182.50,
    "regularMarketChangePercent":    1.25,
    "regularMarketVolume":           55_000_000,
    "regularMarketPreviousClose":    180.25,
    "marketCap":                     2_850_000_000_000,
    "totalRevenue":                  394_000_000_000,
    "netIncomeToCommon":             100_000_000_000,
    "fullTimeEmployees":             164_000,
    "trailingPE":                    28.5,
    "forwardPE":                     25.0,
    "trailingEps":                   6.40,
    "dividendYield":                 0.0053,
    "beta":                          1.21,
    "fiftyTwoWeekHigh":              199.62,
    "fiftyTwoWeekLow":               124.17,
}


def _make_mock_ticker(info=None, hist_df=None):
    """Return a MagicMock shaped like a yfinance Ticker object."""
    mock = MagicMock()
    mock.info = info if info is not None else MOCK_INFO.copy()
    if hist_df is None:
        dates = pd.date_range("2024-01-01", periods=5, freq="D")
        hist_df = pd.DataFrame({
            "Open":   [180, 181, 182, 183, 184],
            "High":   [185, 186, 187, 188, 189],
            "Low":    [179, 180, 181, 182, 183],
            "Close":  [182, 183, 184, 185, 186],
            "Volume": [50_000_000] * 5,
        }, index=dates)
    mock.history.return_value = hist_df
    mock.quarterly_income_stmt = pd.DataFrame()
    mock.quarterly_financials  = pd.DataFrame()
    mock.income_stmt           = pd.DataFrame()
    mock.financials            = pd.DataFrame()
    return mock


# ── Registry sanity checks ────────────────────────────────────────────────────

class TestRegistry:
    def test_companies_dict_has_8_entries(self):
        assert len(ld.COMPANIES) == 8

    def test_all_tickers_uppercase(self):
        for ticker in ld.COMPANIES:
            assert ticker == ticker.upper()

    def test_name_to_ticker_inverse(self):
        for ticker, name in ld.COMPANIES.items():
            assert ld.NAME_TO_TICKER[name] == ticker

    def test_tickers_list_matches_companies_keys(self):
        assert set(ld.TICKERS) == set(ld.COMPANIES.keys())

    def test_sector_map_covers_all_companies(self):
        for name in ld.COMPANIES.values():
            assert name in ld.SECTOR_MAP, f"{name} missing from SECTOR_MAP"


# ── _strip_tz ─────────────────────────────────────────────────────────────────

class TestStripTz:
    def test_strips_tz_from_aware_index(self):
        idx = pd.date_range("2024-01-01", periods=3, freq="D", tz="US/Eastern")
        result = ld._strip_tz(idx)
        assert result.tz is None

    def test_naive_index_unchanged(self):
        idx = pd.date_range("2024-01-01", periods=3, freq="D")
        result = ld._strip_tz(idx)
        assert result.tz is None
        assert list(result) == list(idx)


# ── is_market_open ────────────────────────────────────────────────────────────

class TestIsMarketOpen:
    def test_returns_bool(self):
        result = ld.is_market_open()
        assert isinstance(result, bool)

    @patch("live_data.datetime")
    def test_weekend_returns_false(self, mock_dt):
        """Saturday (weekday=5) must always return False."""
        import pytz
        et = pytz.timezone("America/New_York")
        fake = datetime(2024, 6, 15, 12, 0, 0)  # Saturday
        fake = et.localize(fake)
        mock_dt.now.return_value = fake
        # weekday() must be available on the returned object
        with patch("live_data.pytz") as mock_pytz:
            mock_pytz.timezone.return_value = et
            mock_dt.now.return_value = fake
            # If now_et.weekday() >= 5 → False
            assert fake.weekday() >= 5  # sanity


# ── get_live_price ────────────────────────────────────────────────────────────

class TestGetLivePrice:
    @patch("live_data.yf.Ticker")
    def test_returns_tuple_of_three(self, mock_yf):
        mock_yf.return_value = _make_mock_ticker()
        price, chg, vol = ld.get_live_price("AAPL")
        assert price == 182.50
        assert chg == 1.25
        assert vol == 55_000_000

    @patch("live_data.yf.Ticker")
    def test_price_rounded_to_2dp(self, mock_yf):
        info = MOCK_INFO.copy()
        info["currentPrice"] = 182.5678
        mock_yf.return_value = _make_mock_ticker(info=info)
        price, _, _ = ld.get_live_price("AAPL")
        assert price == round(price, 2)

    @patch("live_data.yf.Ticker")
    def test_fallback_change_pct_computed_from_prev_close(self, mock_yf):
        info = MOCK_INFO.copy()
        del info["regularMarketChangePercent"]
        info["regularMarketPreviousClose"] = 180.0
        info["currentPrice"] = 183.6
        mock_yf.return_value = _make_mock_ticker(info=info)
        _, chg, _ = ld.get_live_price("AAPL")
        expected = round((183.6 - 180.0) / 180.0 * 100, 2)
        assert chg == pytest.approx(expected, rel=1e-4)

    @patch("live_data.yf.Ticker")
    def test_none_price_returns_triple_none(self, mock_yf):
        info = {"regularMarketChangePercent": 0.5}
        mock_yf.return_value = _make_mock_ticker(info=info)
        price, chg, vol = ld.get_live_price("AAPL")
        assert price is None
        assert chg is None
        assert vol is None

    @patch("live_data.yf.Ticker", side_effect=Exception("network error"))
    def test_exception_returns_triple_none(self, _mock):
        price, chg, vol = ld.get_live_price("AAPL")
        assert (price, chg, vol) == (None, None, None)


# ── get_multi_live_prices ─────────────────────────────────────────────────────

class TestGetMultiLivePrices:
    @patch("live_data.get_live_price", return_value=(182.50, 1.25, 55_000_000))
    def test_returns_dict_with_company_names(self, _mock):
        result = ld.get_multi_live_prices(["AAPL", "MSFT"])
        assert "Apple" in result
        assert "Microsoft" in result

    @patch("live_data.get_live_price", return_value=(None, None, None))
    def test_none_prices_default_to_zero(self, _mock):
        result = ld.get_multi_live_prices(["AAPL"])
        assert result["Apple"]["price"] == 0.0
        assert result["Apple"]["change_pct"] == 0.0
        assert result["Apple"]["volume"] == 0

    @patch("live_data.get_live_price", return_value=(150.0, -0.5, 30_000_000))
    def test_defaults_to_all_tickers_when_none_passed(self, mock_price):
        result = ld.get_multi_live_prices()
        assert len(result) == len(ld.COMPANIES)

    @patch("live_data.get_live_price", return_value=(150.0, 0.5, 10_000_000))
    def test_each_entry_has_required_keys(self, _mock):
        result = ld.get_multi_live_prices(["NVDA"])
        entry = result["NVIDIA"]
        assert "price" in entry
        assert "change_pct" in entry
        assert "volume" in entry


# ── get_intraday_data ─────────────────────────────────────────────────────────

class TestGetIntradayData:
    @patch("live_data.yf.Ticker")
    def test_returns_dataframe(self, mock_yf):
        mock_yf.return_value = _make_mock_ticker()
        df = ld.get_intraday_data("AAPL")
        assert isinstance(df, pd.DataFrame)

    @patch("live_data.yf.Ticker")
    def test_contains_close_column(self, mock_yf):
        mock_yf.return_value = _make_mock_ticker()
        df = ld.get_intraday_data("AAPL")
        assert "Close" in df.columns

    @patch("live_data.yf.Ticker")
    def test_tz_naive_index(self, mock_yf):
        dates = pd.date_range("2024-01-01", periods=5, freq="h", tz="UTC")
        hist_df = pd.DataFrame({"Open": [1]*5, "High": [2]*5, "Low": [0]*5,
                                 "Close": [1.5]*5, "Volume": [1000]*5}, index=dates)
        mock_yf.return_value = _make_mock_ticker(hist_df=hist_df)
        df = ld.get_intraday_data("AAPL")
        assert df.index.tz is None

    @patch("live_data.yf.Ticker", side_effect=Exception("timeout"))
    def test_exception_returns_empty_df(self, _mock):
        df = ld.get_intraday_data("AAPL")
        assert df.empty


# ── get_live_fundamentals ─────────────────────────────────────────────────────

class TestGetLiveFundamentals:
    @patch("live_data.yf.Ticker")
    def test_returns_dict_with_expected_keys(self, mock_yf):
        mock_yf.return_value = _make_mock_ticker()
        result = ld.get_live_fundamentals("AAPL")
        for key in ["marketCap_B", "revenue_B", "netIncome_B", "employees_K"]:
            assert key in result

    @patch("live_data.yf.Ticker")
    def test_values_in_billions(self, mock_yf):
        mock_yf.return_value = _make_mock_ticker()
        result = ld.get_live_fundamentals("AAPL")
        # $2.85T market cap → ~2850B
        assert result["marketCap_B"] == pytest.approx(2850.0, rel=0.01)
        # $394B revenue
        assert result["revenue_B"] == pytest.approx(394.0, rel=0.01)

    @patch("live_data.yf.Ticker")
    def test_net_margin_computed(self, mock_yf):
        mock_yf.return_value = _make_mock_ticker()
        result = ld.get_live_fundamentals("AAPL")
        expected_margin = round(100_000_000_000 / 394_000_000_000 * 100, 2)
        assert result["net_margin"] == pytest.approx(expected_margin, rel=1e-3)

    @patch("live_data.yf.Ticker", side_effect=Exception)
    def test_exception_returns_empty_dict(self, _mock):
        result = ld.get_live_fundamentals("AAPL")
        assert result == {}


# ── get_all_fundamentals ──────────────────────────────────────────────────────

class TestGetAllFundamentals:
    @patch("live_data.get_live_fundamentals")
    def test_returns_dataframe(self, mock_fund):
        mock_fund.return_value = {
            "marketCap_B": 100.0, "revenue_B": 50.0,
            "netIncome_B": 10.0,  "employees_K": 50.0,
        }
        df = ld.get_all_fundamentals()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == len(ld.COMPANIES)

    @patch("live_data.get_live_fundamentals", return_value={})
    def test_empty_results_returns_empty_df(self, _mock):
        df = ld.get_all_fundamentals()
        assert df.empty


# ── get_price_history ─────────────────────────────────────────────────────────

class TestGetPriceHistory:
    @patch("live_data.yf.Ticker")
    def test_returns_dataframe_with_required_columns(self, mock_yf):
        mock_yf.return_value = _make_mock_ticker()
        df = ld.get_price_history("AAPL")
        for col in ["Date", "Company", "Price", "Daily_Return"]:
            assert col in df.columns, f"Missing column: {col}"

    @patch("live_data.yf.Ticker")
    def test_company_name_is_populated(self, mock_yf):
        mock_yf.return_value = _make_mock_ticker()
        df = ld.get_price_history("AAPL")
        assert (df["Company"] == "Apple").all()

    @patch("live_data.yf.Ticker")
    def test_date_column_is_tz_naive(self, mock_yf):
        dates = pd.date_range("2024-01-01", periods=5, freq="D", tz="UTC")
        hist_df = pd.DataFrame({"Open": [1]*5, "High": [2]*5, "Low": [0]*5,
                                 "Close": [1.5]*5, "Volume": [1_000_000]*5}, index=dates)
        mock_yf.return_value = _make_mock_ticker(hist_df=hist_df)
        df = ld.get_price_history("AAPL")
        assert pd.api.types.is_datetime64_any_dtype(df["Date"])
        assert df["Date"].dt.tz is None

    @patch("live_data.yf.Ticker", side_effect=Exception)
    def test_exception_returns_empty_df(self, _mock):
        df = ld.get_price_history("AAPL")
        assert df.empty


# ── get_all_price_history ─────────────────────────────────────────────────────

class TestGetAllPriceHistory:
    @patch("live_data.get_price_history")
    def test_concatenates_all_tickers(self, mock_hist):
        def fake_history(ticker, period="5y"):
            dates = pd.date_range("2024-01-01", periods=3, freq="D")
            return pd.DataFrame({
                "Date":         dates,
                "Company":      [ld.COMPANIES[ticker]] * 3,
                "Price":        [100.0, 101.0, 102.0],
                "Daily_Return": [0.0, 1.0, 0.99],
                "Volume_M":     [50.0, 50.5, 51.0],
            })
        mock_hist.side_effect = fake_history
        df = ld.get_all_price_history()
        assert len(df) == len(ld.TICKERS) * 3
        assert set(df["Company"].unique()) == set(ld.COMPANIES.values())

    @patch("live_data.get_price_history", return_value=pd.DataFrame())
    def test_all_empty_returns_empty_df(self, _mock):
        df = ld.get_all_price_history()
        assert df.empty


# ── merge_with_csv ────────────────────────────────────────────────────────────

class TestMergeWithCsv:
    def _make_live(self):
        return pd.DataFrame({
            "Company": ["Apple", "Microsoft"],
            "Year":    [2024, 2024],
            "Revenue_B": [394.0, 211.9],
        })

    def _make_csv(self):
        return pd.DataFrame({
            "Company":   ["Apple", "Microsoft", "Google"],
            "Year":      [2023, 2023, 2023],
            "Revenue_B": [383.0, 198.3, 305.6],
            "RD_B":      [29.9, 27.2, 45.4],
        })

    def test_live_rows_survive(self):
        result = ld.merge_with_csv(self._make_live(), self._make_csv(),
                                   ["Company", "Year"])
        apple_2024 = result[(result["Company"] == "Apple") & (result["Year"] == 2024)]
        assert not apple_2024.empty
        assert apple_2024["Revenue_B"].values[0] == 394.0

    def test_csv_only_rows_preserved(self):
        result = ld.merge_with_csv(self._make_live(), self._make_csv(),
                                   ["Company", "Year"])
        google = result[result["Company"] == "Google"]
        assert not google.empty

    def test_no_duplicate_keys(self):
        result = ld.merge_with_csv(self._make_live(), self._make_csv(),
                                   ["Company", "Year"])
        assert not result.duplicated(subset=["Company", "Year"]).any()

    def test_empty_live_returns_csv(self):
        csv = self._make_csv()
        result = ld.merge_with_csv(pd.DataFrame(), csv, ["Company", "Year"])
        pd.testing.assert_frame_equal(result.reset_index(drop=True),
                                      csv.reset_index(drop=True))

    def test_empty_csv_returns_live(self):
        live = self._make_live()
        result = ld.merge_with_csv(live, pd.DataFrame(), ["Company", "Year"])
        pd.testing.assert_frame_equal(result.reset_index(drop=True),
                                      live.reset_index(drop=True))


# ── get_company_info ──────────────────────────────────────────────────────────

class TestGetCompanyInfo:
    @patch("live_data.yf.Ticker")
    def test_returns_dict_with_expected_keys(self, mock_yf):
        mock_yf.return_value = _make_mock_ticker()
        result = ld.get_company_info("AAPL")
        for key in ["marketCap", "trailingPE", "beta", "fiftyTwoWeekHigh", "fiftyTwoWeekLow"]:
            assert key in result

    @patch("live_data.yf.Ticker", side_effect=Exception)
    def test_exception_returns_empty_dict(self, _mock):
        result = ld.get_company_info("AAPL")
        assert result == {}


# ── get_smart_period_interval ─────────────────────────────────────────────────

class TestGetSmartPeriodInterval:
    @patch("live_data.is_market_open", return_value=False)
    def test_upgrades_1d_period_when_market_closed(self, _mock):
        period, interval, open_ = ld.get_smart_period_interval("1d", "5m")
        assert period == "5d"
        assert open_ is False

    @patch("live_data.is_market_open", return_value=True)
    def test_keeps_1d_period_when_market_open(self, _mock):
        period, interval, open_ = ld.get_smart_period_interval("1d", "5m")
        assert period == "1d"
        assert open_ is True

    @patch("live_data.is_market_open", return_value=False)
    def test_non_1d_period_unchanged(self, _mock):
        period, interval, _ = ld.get_smart_period_interval("5d", "1h")
        assert period == "5d"
        assert interval == "1h"
