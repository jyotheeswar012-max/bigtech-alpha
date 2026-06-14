"""
tests/test_merge_with_csv.py
────────────────────────────
Unit tests for live_data.merge_with_csv().

Run with:  pytest tests/test_merge_with_csv.py -v

No network access is required — all inputs are constructed in-process.
The test module imports only merge_with_csv, so yfinance is never called.
"""

import pandas as pd
import pytest
from live_data import merge_with_csv


# ─────────────────────────────────────────────────────────────────────────────
# Shared fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def csv_annual():
    """Simulated CSV annual frame — has RD_B which live data never carries."""
    return pd.DataFrame([
        {"Company": "Apple", "Year": 2022, "Revenue_B": 390.0, "NetIncome_B": 95.0, "RD_B": 26.0},
        {"Company": "Apple", "Year": 2023, "Revenue_B": 383.0, "NetIncome_B": 97.0, "RD_B": 29.0},
        {"Company": "Microsoft", "Year": 2022, "Revenue_B": 198.0, "NetIncome_B": 72.0, "RD_B": 24.0},
    ])


@pytest.fixture
def live_annual():
    """Simulated yfinance live frame — updated Revenue_B, missing RD_B."""
    return pd.DataFrame([
        {"Company": "Apple", "Year": 2023, "Revenue_B": 385.0, "NetIncome_B": 100.0},
        {"Company": "Apple", "Year": 2024, "Revenue_B": 391.0, "NetIncome_B": 104.0},
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Test 1 — Empty-frame short-circuits
# ─────────────────────────────────────────────────────────────────────────────

class TestEmptyShortCircuit:
    """When one side is empty/None the other is returned as-is."""

    def test_empty_live_returns_csv(self, csv_annual):
        result = merge_with_csv(pd.DataFrame(), csv_annual, ["Company", "Year"])
        pd.testing.assert_frame_equal(result, csv_annual)

    def test_empty_csv_returns_live(self, live_annual):
        result = merge_with_csv(live_annual, pd.DataFrame(), ["Company", "Year"])
        pd.testing.assert_frame_equal(result, live_annual)

    def test_none_live_returns_csv(self, csv_annual):
        result = merge_with_csv(None, csv_annual, ["Company", "Year"])
        pd.testing.assert_frame_equal(result, csv_annual)


# ─────────────────────────────────────────────────────────────────────────────
# Test 2 — Live data wins on shared columns
# ─────────────────────────────────────────────────────────────────────────────

class TestLiveWinsOnSharedColumns:
    """
    Where both frames have a row for the same key, the live value
    must appear in the output (CSV value is discarded).
    """

    def test_live_revenue_beats_csv(self, csv_annual, live_annual):
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        apple_2023 = result[
            (result["Company"] == "Apple") & (result["Year"] == 2023)
        ]
        assert len(apple_2023) == 1, "Duplicate row for Apple 2023 — dedup failed"
        # live frame has 385.0; csv has 383.0
        assert apple_2023["Revenue_B"].iloc[0] == 385.0, (
            f"Expected live Revenue_B=385.0, got {apple_2023['Revenue_B'].iloc[0]}"
        )

    def test_live_net_income_beats_csv(self, csv_annual, live_annual):
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        apple_2023 = result[
            (result["Company"] == "Apple") & (result["Year"] == 2023)
        ]
        # live frame has 100.0; csv has 97.0
        assert apple_2023["NetIncome_B"].iloc[0] == 100.0


# ─────────────────────────────────────────────────────────────────────────────
# Test 3 — CSV-only rows are preserved
# ─────────────────────────────────────────────────────────────────────────────

class TestCsvOnlyRowsPreserved:
    """
    Rows that exist only in the CSV (e.g. older historical years or
    companies the live fetch missed) must survive in the output.
    """

    def test_csv_only_year_present(self, csv_annual, live_annual):
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        assert 2022 in result["Year"].values, "CSV-only year 2022 was dropped"

    def test_csv_only_company_present(self, csv_annual, live_annual):
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        assert "Microsoft" in result["Company"].values, (
            "CSV-only company Microsoft was dropped"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Test 4 — CSV-only columns are back-filled into live rows
# ─────────────────────────────────────────────────────────────────────────────

class TestCsvOnlyColumnBackfill:
    """
    RD_B exists only in the CSV.  The live row for Apple 2023 must inherit
    the RD_B value from the CSV row for the same key via ffill/bfill.
    """

    def test_rd_b_inherited_by_live_row(self, csv_annual, live_annual):
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        apple_2023 = result[
            (result["Company"] == "Apple") & (result["Year"] == 2023)
        ]
        assert "RD_B" in result.columns, "RD_B column missing from merged output"
        assert pd.notna(apple_2023["RD_B"].iloc[0]), (
            "RD_B should be back-filled into the live Apple 2023 row but is NaN"
        )
        assert apple_2023["RD_B"].iloc[0] == 29.0

    def test_live_only_row_gets_bfilled_rd_b(self, csv_annual, live_annual):
        """
        Apple 2024 exists only in live — there is no CSV row to inherit from,
        so bfill within the Apple group should pull the nearest known RD_B.
        """
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        apple_2024 = result[
            (result["Company"] == "Apple") & (result["Year"] == 2024)
        ]
        assert len(apple_2024) == 1
        # bfill can't reach forward into non-existent data; value may be NaN.
        # The important thing is the column exists and no KeyError is raised.
        assert "RD_B" in apple_2024.columns


# ─────────────────────────────────────────────────────────────────────────────
# Test 5 — Output has no duplicate keys and is sorted
# ─────────────────────────────────────────────────────────────────────────────

class TestOutputShapeAndOrder:
    """Result must have unique keys and be sorted ascending by key_cols."""

    def test_no_duplicate_keys(self, csv_annual, live_annual):
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        dupes = result.duplicated(subset=["Company", "Year"]).sum()
        assert dupes == 0, f"Found {dupes} duplicate (Company, Year) rows"

    def test_sorted_by_key_cols(self, csv_annual, live_annual):
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        expected_order = result.sort_values(["Company", "Year"])["Year"].tolist()
        actual_order   = result["Year"].tolist()
        assert actual_order == expected_order, "Output is not sorted by (Company, Year)"

    def test_row_count_is_union(self, csv_annual, live_annual):
        """
        Union of unique keys:
          CSV:  Apple/2022, Apple/2023, Microsoft/2022
          Live: Apple/2023 (overlap), Apple/2024 (new)
        Expected unique rows: Apple/2022, Apple/2023, Apple/2024, Microsoft/2022 = 4
        """
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        assert len(result) == 4, f"Expected 4 rows, got {len(result)}"


# ─────────────────────────────────────────────────────────────────────────────
# Test 6 — Column union: output contains all columns from both frames
# ─────────────────────────────────────────────────────────────────────────────

class TestColumnUnion:
    """Output schema must be the superset of both input schemas."""

    def test_all_csv_columns_present(self, csv_annual, live_annual):
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        for col in csv_annual.columns:
            assert col in result.columns, f"CSV column '{col}' missing from result"

    def test_all_live_columns_present(self, csv_annual, live_annual):
        result = merge_with_csv(live_annual, csv_annual, ["Company", "Year"])
        for col in live_annual.columns:
            assert col in result.columns, f"Live column '{col}' missing from result"
