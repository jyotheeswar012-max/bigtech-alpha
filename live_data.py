# live_data.py — Live market data module for Market Nexus
# Powered by yfinance (free, no API key required)

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# ── Company registry ──────────────────────────────────────────────────────────
COMPANIES = {
    "AAPL":  "Apple",
    "MSFT":  "Microsoft",
    "GOOGL": "Google",
    "AMZN":  "Amazon",
    "META":  "Meta",
    "NVDA":  "NVIDIA",
    "TSLA":  "Tesla",
    "NFLX":  "Netflix",
}
NAME_TO_TICKER = {v: k for k, v in COMPANIES.items()}
COMPANY_COLORS = {
    "AAPL":  "#e8e8e8",
    "MSFT":  "#00aff0",
    "GOOGL": "#fbbc05",
    "AMZN":  "#ff9900",
    "META":  "#1877f2",
    "NVDA":  "#76b900",
    "TSLA":  "#cc0000",
    "NFLX":  "#e50914",
}
TICKERS = list(COMPANIES.keys())

SECTOR_MAP = {
    "Apple":     "Hardware",
    "Microsoft": "Cloud/Software",
    "Google":    "Digital Ads",
    "Amazon":    "E-Commerce/Cloud",
    "Meta":      "Social Media",
    "NVIDIA":    "Semiconductors",
    "Tesla":     "EV/Energy",
    "Netflix":   "Streaming",
}


def _strip_tz(index):
    """
    Remove timezone information from a pandas DatetimeIndex.

    yfinance returns timezone-aware indices (usually US/Eastern or UTC).
    Streamlit and pandas merge operations work best with naive datetimes,
    so we normalise to UTC then strip the tzinfo entirely.

    Args:
        index (pd.DatetimeIndex): The index to normalise.

    Returns:
        pd.DatetimeIndex: A timezone-naive copy of the index.
    """
    if hasattr(index, "tz") and index.tz is not None:
        return index.tz_convert("UTC").tz_localize(None)
    return index


def is_market_open() -> bool:
    """
    Check whether the US equity market (NYSE / NASDAQ) is currently open.

    Uses the America/New_York timezone.  Does not account for early-close
    days (e.g. day before Thanksgiving) — those are treated as full sessions.

    Returns:
        bool: True if it is currently a weekday between 09:30 and 16:00 ET.
    """
    try:
        et = pytz.timezone("America/New_York")
        now_et = datetime.now(et)
        if now_et.weekday() >= 5:
            return False
        t = now_et.time()
        from datetime import time as dtime
        return dtime(9, 30) <= t <= dtime(16, 0)
    except Exception:
        return False


def get_smart_period_interval(user_period: str, user_interval: str):
    """
    Adjust the yfinance period/interval pair based on market status.

    When the market is closed and the user requests a 1-day window, there
    may be no intraday bars available.  This helper automatically widens
    the period to 5 days so charts always have data to display.

    Args:
        user_period   (str): Requested period string (e.g. "1d", "5d", "1mo").
        user_interval (str): Requested interval string (e.g. "5m", "1h", "1d").

    Returns:
        tuple[str, str, bool]:
            - Effective period string after adjustment.
            - Effective interval string (unchanged).
            - Whether the market is currently open.
    """
    open_ = is_market_open()
    period   = user_period
    interval = user_interval
    if not open_ and user_period == "1d":
        period = "5d"
    return period, interval, open_


# ─────────────────────────────────────────────────────────────────────────────
# 1. LIVE PRICE
# ─────────────────────────────────────────────────────────────────────────────
def get_live_price(ticker: str):
    """
    Fetch the latest trade price, percentage change, and volume for a ticker.

    Priority order for price:
      currentPrice → regularMarketPrice → ask → bid

    Priority order for change %:
      regularMarketChangePercent → computed from regularMarketPreviousClose

    Args:
        ticker (str): A valid Yahoo Finance ticker symbol, e.g. "AAPL".

    Returns:
        tuple[float | None, float | None, int | None]:
            (price, change_pct, volume).  All three are None on any error.
    """
    try:
        info = yf.Ticker(ticker).info
        price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("ask")
            or info.get("bid")
        )
        if price is None:
            return None, None, None
        price = round(float(price), 2)

        change_pct = info.get("regularMarketChangePercent")
        if change_pct is not None:
            change_pct = round(float(change_pct), 2)
        else:
            prev = info.get("regularMarketPreviousClose") or info.get("previousClose")
            change_pct = round((price - prev) / prev * 100, 2) if prev else 0.0

        volume = int(info.get("regularMarketVolume") or info.get("volume") or 0)
        return price, change_pct, volume
    except Exception:
        return None, None, None


def get_multi_live_prices(tickers: list = None) -> dict:
    """
    Fetch live prices for multiple tickers in a single call.

    Iterates over each ticker and calls get_live_price().  Missing or failed
    lookups default to 0.0 / 0 so callers never receive None values.

    Args:
        tickers (list[str] | None): Ticker symbols to fetch.  Defaults to
            all 8 companies in the TICKERS registry.

    Returns:
        dict[str, dict]: Keyed by *company name* (not ticker), each value is::

            {
                "price":      float,  # latest trade price (USD)
                "change_pct": float,  # % change vs previous close
                "volume":     int,    # shares traded today
            }
    """
    if tickers is None:
        tickers = TICKERS
    result = {}
    for ticker in tickers:
        price, change, vol = get_live_price(ticker)
        company = COMPANIES.get(ticker, ticker)
        result[company] = {
            "price":      price  if price  is not None else 0.0,
            "change_pct": change if change is not None else 0.0,
            "volume":     vol    if vol    is not None else 0,
        }
    return result


# ─────────────────────────────────────────────────────────────────────────────
# 2. INTRADAY DATA
# ─────────────────────────────────────────────────────────────────────────────
def get_intraday_data(ticker: str, period: str = "1d", interval: str = "5m") -> pd.DataFrame:
    """
    Download intraday OHLCV bars for a single ticker.

    Uses a three-tier fallback strategy to handle market-closed / thin-data
    situations:
      1. Requested period + interval with prepost=True.
      2. Same period + interval without prepost.
      3. 5-day daily bars as a last resort.

    Timezone is stripped from the index before returning (see _strip_tz).

    Args:
        ticker   (str): Yahoo Finance ticker symbol.
        period   (str): Data window, e.g. "1d", "5d".  Auto-adjusted when
                        the market is closed (see get_smart_period_interval).
        interval (str): Bar size, e.g. "5m", "15m", "1h".

    Returns:
        pd.DataFrame: Columns = [Open, High, Low, Close, Volume] with a
            timezone-naive DatetimeIndex.  Empty DataFrame on any error.
    """
    try:
        period, interval, market_open = get_smart_period_interval(period, interval)
        t  = yf.Ticker(ticker)
        df = t.history(period=period, interval=interval,
                       auto_adjust=True, prepost=True)
        if df.empty or len(df) < 3:
            df = t.history(period=period, interval=interval, auto_adjust=True)
        if df.empty or len(df) < 3:
            df = t.history(period="5d", interval="1d", auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        df.index = _strip_tz(df.index)
        keep = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
        df = df[keep].copy().dropna(subset=["Close"])
        return df
    except Exception:
        return pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 3. LIVE FUNDAMENTALS
# ─────────────────────────────────────────────────────────────────────────────
def get_live_fundamentals(ticker: str) -> dict:
    """
    Pull key fundamental metrics for a single ticker from yfinance.

    All monetary values are normalised to billions (B) or thousands (K)
    for consistency with the CSV datasets used in the app.

    Derived metrics computed here:
      - ``net_margin``    : netIncomeToCommon / totalRevenue × 100
      - ``ps_ratio``      : marketCap / totalRevenue
      - ``rev_per_emp_M`` : totalRevenue / fullTimeEmployees / 1e6

    Args:
        ticker (str): Yahoo Finance ticker symbol.

    Returns:
        dict: Fundamental metrics.  Empty dict on any network/parse error.
    """
    try:
        info = yf.Ticker(ticker).info
        mc   = info.get("marketCap")            or 0
        rev  = info.get("totalRevenue")         or 0
        ni   = info.get("netIncomeToCommon")    or 0
        emp  = info.get("fullTimeEmployees")    or 0
        return {
            "marketCap_B":   round(mc  / 1e9, 2),
            "revenue_B":     round(rev / 1e9, 2),
            "netIncome_B":   round(ni  / 1e9, 2),
            "employees_K":   round(emp / 1e3, 1),
            "peRatio":       info.get("trailingPE"),
            "trailingPE":    info.get("trailingPE"),
            "forwardPE":     info.get("forwardPE"),
            "eps":           info.get("trailingEps"),
            "dividendYield": info.get("dividendYield"),
            "ps_ratio":      round(mc / rev, 2) if rev else None,
            "beta":          info.get("beta"),
            "52w_high":      info.get("fiftyTwoWeekHigh"),
            "52w_low":       info.get("fiftyTwoWeekLow"),
            "net_margin":    round(ni / rev * 100, 2) if rev else None,
            "rev_per_emp_M": round((rev / emp) / 1e6, 2) if emp else None,
        }
    except Exception:
        return {}


def get_all_fundamentals() -> pd.DataFrame:
    """
    Fetch fundamentals for all 8 tracked companies and return as a DataFrame.

    Calls get_live_fundamentals() for each ticker in COMPANIES, appends
    ``Company`` and ``Ticker`` columns, then concatenates into a single frame.

    Returns:
        pd.DataFrame: One row per company.  Empty DataFrame if all calls fail.
    """
    rows = []
    for ticker, name in COMPANIES.items():
        d = get_live_fundamentals(ticker)
        if d:
            d["Company"] = name
            d["Ticker"]  = ticker
            rows.append(d)
    return pd.DataFrame(rows) if rows else pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 4. LIVE PRICE HISTORY
# ─────────────────────────────────────────────────────────────────────────────
def get_price_history(ticker: str, period: str = "5y", interval: str = "1d") -> pd.DataFrame:
    """
    Download daily adjusted closing prices and derived columns for one ticker.

    Adds convenience columns on top of the raw yfinance OHLCV data:
      - ``Price``        : alias for Close (used throughout nexus.py)
      - ``Daily_Return`` : percentage price change from previous close
      - ``Volume_M``     : volume in millions
      - ``Company``      : human-readable company name from COMPANIES registry

    The Date index is reset to a plain column and stripped of timezone info.

    Args:
        ticker   (str): Yahoo Finance ticker symbol.
        period   (str): History window, e.g. "5y", "2y".  Default "5y".
        interval (str): Bar size.  Default "1d" (daily).

    Returns:
        pd.DataFrame: Columns include Date, Open, High, Low, Close, Volume,
            Price, Daily_Return, Volume_M, Company.  Empty on error.
    """
    try:
        df = yf.Ticker(ticker).history(period=period, interval=interval, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        df.index = _strip_tz(df.index)
        df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
        df["Daily_Return"] = df["Close"].pct_change() * 100
        df["Company"]      = COMPANIES[ticker]
        df["Price"]        = df["Close"]
        df["Volume_M"]     = (df["Volume"] / 1e6).round(2)
        df = df.reset_index()
        first_col = df.columns[0]
        if first_col != "Date":
            df = df.rename(columns={first_col: "Date"})
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
        return df
    except Exception:
        return pd.DataFrame()


def get_all_price_history(period: str = "5y") -> pd.DataFrame:
    """
    Download price history for all 8 companies and concatenate into one frame.

    Args:
        period (str): History window passed to get_price_history().  Default "5y".

    Returns:
        pd.DataFrame: Combined frame with a ``Company`` column to distinguish rows.
            Empty DataFrame if every individual call fails.
    """
    frames = [get_price_history(t, period=period) for t in TICKERS]
    frames = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 5. LIVE QUARTERLY REVENUE
# ─────────────────────────────────────────────────────────────────────────────
def get_quarterly_financials(ticker: str) -> pd.DataFrame:
    """
    Parse quarterly revenue and net income from yfinance income statements.

    Row detection is fuzzy — it searches for 'total revenue' and 'net income'
    (case-insensitive) in the statement index, skipping rows that contain
    noise words like 'cost', 'minority', or 'loss'.

    Args:
        ticker (str): Yahoo Finance ticker symbol.

    Returns:
        pd.DataFrame: Columns = [Quarter (datetime), Company, Revenue_B,
            NetIncome_B], sorted by Quarter ascending.
            Empty DataFrame if no revenue row is found or on any error.
    """
    try:
        t  = yf.Ticker(ticker)
        qf = getattr(t, "quarterly_income_stmt", None)
        if qf is None or (hasattr(qf, "empty") and qf.empty):
            qf = t.quarterly_financials
        if qf is None or qf.empty:
            return pd.DataFrame()

        rev_row = ni_row = None
        for idx in qf.index:
            il = str(idx).lower()
            if rev_row is None and ("total revenue" in il or ("revenue" in il and "cost" not in il)):
                rev_row = idx
            if ni_row is None and "net income" in il and "minority" not in il and "loss" not in il:
                ni_row = idx
        if rev_row is None:
            return pd.DataFrame()

        rows = []
        for col in qf.columns:
            rev = qf.loc[rev_row, col]
            ni  = qf.loc[ni_row, col] if ni_row else None
            try:
                qt = pd.Timestamp(col)
                if qt.tz:
                    qt = qt.tz_localize(None)
            except Exception:
                continue
            rows.append({
                "Quarter":     qt,
                "Company":     COMPANIES[ticker],
                "Revenue_B":   round(float(rev) / 1e9, 2) if pd.notna(rev) else None,
                "NetIncome_B": round(float(ni)  / 1e9, 2) if (ni is not None and pd.notna(ni)) else None,
            })
        df = pd.DataFrame(rows).dropna(subset=["Revenue_B"])
        return df.sort_values("Quarter").reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


def get_all_quarterly(tickers: list = None) -> pd.DataFrame:
    """
    Fetch quarterly financials for multiple tickers and concatenate.

    Args:
        tickers (list[str] | None): Ticker symbols to fetch.  Defaults to
            all entries in the TICKERS registry.

    Returns:
        pd.DataFrame: Combined quarterly data.  Empty if all calls fail.
    """
    tickers = tickers or TICKERS
    frames  = [get_quarterly_financials(t) for t in tickers]
    frames  = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 6. LIVE ANNUAL METRICS  +  CURRENT YEAR TTM INJECTION
# ─────────────────────────────────────────────────────────────────────────────
def get_ttm_as_current_year(ticker: str) -> dict | None:
    """
    Build a synthetic "current year" row from trailing-twelve-month (TTM) data.

    yfinance's annual income_stmt only goes to the last *fiscal year end*.
    This function injects a TTM row for the *current calendar year* so the
    charts stay up-to-date between annual report releases.

    Args:
        ticker (str): Yahoo Finance ticker symbol.

    Returns:
        dict | None: A single-row dict matching the schema of get_annual_financials()
            rows, tagged with ``is_ttm=True``.  None if revenue is zero or on error.
    """
    try:
        current_year = datetime.now().year
        name = COMPANIES[ticker]
        info = yf.Ticker(ticker).info

        rev = info.get("totalRevenue")      or 0
        ni  = info.get("netIncomeToCommon") or 0
        mc  = info.get("marketCap")         or 0
        emp = info.get("fullTimeEmployees") or 0

        if rev == 0:
            return None

        return {
            "Year":        current_year,
            "Company":     name,
            "Sector":      SECTOR_MAP.get(name, "Tech"),
            "Revenue_B":   round(float(rev) / 1e9, 2),
            "NetIncome_B": round(float(ni)  / 1e9, 2),
            "MarketCap_B": round(float(mc)  / 1e9, 2),
            "Employees_K": round(float(emp) / 1e3, 1),
            "is_ttm":      True,
        }
    except Exception:
        return None


def get_annual_financials(ticker: str) -> pd.DataFrame:
    """
    Download and parse annual income-statement data for one ticker.

    Revenue and net income rows are detected by fuzzy label matching
    (same strategy as get_quarterly_financials).  Market cap and headcount
    are read from yfinance .info (point-in-time, not historical) and
    attached to every annual row as a best-effort approximation.

    A TTM row for the current calendar year is automatically appended if the
    most recent fiscal year in the data is older than the current year
    (see get_ttm_as_current_year).

    Args:
        ticker (str): Yahoo Finance ticker symbol.

    Returns:
        pd.DataFrame: Annual financials with columns [Year, Company, Sector,
            Revenue_B, NetIncome_B, MarketCap_B, Employees_K, is_ttm],
            sorted by Year ascending.  Empty DataFrame on error.
    """
    try:
        t  = yf.Ticker(ticker)
        af = getattr(t, "income_stmt", None)
        if af is None or (hasattr(af, "empty") and af.empty):
            af = t.financials
        if af is None or af.empty:
            return pd.DataFrame()

        info = t.info
        name = COMPANIES[ticker]

        rev_row = ni_row = None
        for idx in af.index:
            il = str(idx).lower()
            if rev_row is None and ("total revenue" in il or ("revenue" in il and "cost" not in il)):
                rev_row = idx
            if ni_row is None and "net income" in il and "minority" not in il and "loss" not in il:
                ni_row = idx
        if rev_row is None:
            return pd.DataFrame()

        mc_now  = (info.get("marketCap")         or 0) / 1e9
        emp_now = (info.get("fullTimeEmployees") or 0) / 1e3

        rows = []
        for col in af.columns:
            try:
                year = pd.Timestamp(col).year
            except Exception:
                continue
            rev = af.loc[rev_row, col]
            ni  = af.loc[ni_row,  col] if ni_row else None
            rows.append({
                "Year":        year,
                "Company":     name,
                "Sector":      SECTOR_MAP.get(name, "Tech"),
                "Revenue_B":   round(float(rev) / 1e9, 2) if pd.notna(rev) else None,
                "NetIncome_B": round(float(ni)  / 1e9, 2) if (ni is not None and pd.notna(ni)) else None,
                "MarketCap_B": round(mc_now, 2),
                "Employees_K": round(emp_now, 1),
                "is_ttm":      False,
            })
        df = pd.DataFrame(rows).dropna(subset=["Revenue_B"])
        df = df.sort_values("Year").reset_index(drop=True)

        current_year = datetime.now().year
        if current_year not in df["Year"].values:
            ttm_row = get_ttm_as_current_year(ticker)
            if ttm_row is not None:
                df = pd.concat(
                    [df, pd.DataFrame([ttm_row])],
                    ignore_index=True
                ).sort_values("Year").reset_index(drop=True)

        return df
    except Exception:
        return pd.DataFrame()


def get_all_annual(tickers: list = None) -> pd.DataFrame:
    """
    Fetch annual financials for multiple tickers and concatenate.

    Args:
        tickers (list[str] | None): Ticker symbols to fetch.  Defaults to
            all entries in the TICKERS registry.

    Returns:
        pd.DataFrame: Combined annual data.  Empty if all calls fail.
    """
    tickers = tickers or TICKERS
    frames  = [get_annual_financials(t) for t in tickers]
    frames  = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 7. SMART MERGE  —  live data wins on shared columns;
#                    CSV fills in columns the live frame lacks (e.g. RD_B)
# ─────────────────────────────────────────────────────────────────────────────
def merge_with_csv(live_df: pd.DataFrame, csv_df: pd.DataFrame,
                   key_cols: list) -> pd.DataFrame:
    """
    Merge live yfinance data with the bundled CSV fallback datasets.

    Merge strategy:
      1. Union both frames' columns so neither loses CSV-only fields (e.g. RD_B).
      2. Concatenate csv THEN live (live rows land last).
      3. Forward-fill CSV-only columns into the live rows within each key group
         so live rows inherit CSV metadata they don't carry themselves.
      4. Deduplicate on key_cols keeping the **last** occurrence (= live row).

    This ensures:
      - Live data always wins for shared columns (Revenue_B, NetIncome_B, …).
      - CSV-only columns (R&D spend, etc.) are still available on live rows.
      - Rows present only in CSV (older years) are preserved.

    Args:
        live_df  (pd.DataFrame): Frame from yfinance (may be empty).
        csv_df   (pd.DataFrame): Frame from the bundled CSV files.
        key_cols (list[str]):    Columns that uniquely identify a row,
                                 e.g. ['Company', 'Year'] or ['Company', 'Date'].

    Returns:
        pd.DataFrame: Merged frame sorted by key_cols.  Returns the non-empty
            input unchanged if the other is empty.
    """
    if live_df is None or (hasattr(live_df, "empty") and live_df.empty):
        return csv_df
    if csv_df is None or (hasattr(csv_df, "empty") and csv_df.empty):
        return live_df

    all_cols = list(dict.fromkeys(list(csv_df.columns) + list(live_df.columns)))
    csv_aligned  = csv_df.reindex(columns=all_cols)
    live_aligned = live_df.reindex(columns=all_cols)

    combined = pd.concat([csv_aligned, live_aligned], ignore_index=True)

    csv_only_cols = [c for c in all_cols if c not in live_df.columns and c not in key_cols]
    if csv_only_cols:
        combined = combined.sort_values(key_cols).reset_index(drop=True)
        combined[csv_only_cols] = (
            combined.groupby(key_cols)[csv_only_cols]
            .transform(lambda s: s.ffill().bfill())
        )

    combined = combined.drop_duplicates(subset=key_cols, keep="last")
    return combined.sort_values(key_cols).reset_index(drop=True)


# ─────────────────────────────────────────────────────────────────────────────
# 8. COMPANY INFO CARD
# ─────────────────────────────────────────────────────────────────────────────
def get_company_info(ticker: str) -> dict:
    """
    Fetch a concise set of valuation and risk metrics for a company info card.

    Unlike get_live_fundamentals, this function returns raw yfinance values
    (not normalised to billions) and focuses on the subset needed for the
    sidebar / info-card widget in the Live Dashboard page.

    Args:
        ticker (str): Yahoo Finance ticker symbol.

    Returns:
        dict: Keys: marketCap, trailingPE, forwardPE, fiftyTwoWeekHigh,
            fiftyTwoWeekLow, dividendYield, beta.  Empty dict on any error.
    """
    try:
        info = yf.Ticker(ticker).info
        return {
            "marketCap":        info.get("marketCap"),
            "trailingPE":       info.get("trailingPE"),
            "forwardPE":        info.get("forwardPE"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow":  info.get("fiftyTwoWeekLow"),
            "dividendYield":    info.get("dividendYield"),
            "beta":             info.get("beta"),
        }
    except Exception:
        return {}
