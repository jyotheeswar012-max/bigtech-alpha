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
    """Safely strip timezone from a DatetimeIndex."""
    if hasattr(index, "tz") and index.tz is not None:
        return index.tz_convert("UTC").tz_localize(None)
    return index


def is_market_open() -> bool:
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
    Returns (price, change_pct, volume).
    Uses currentPrice from info for accuracy.
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
    FIX: tickers now optional (defaults to all companies).
    FIX: returns dict {company_name: {price, change_pct, volume}}
         so nexus.py can iterate as: for company, info in live_prices.items()
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
            # FIX: expose all columns nexus.py needs
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
    frames = [get_price_history(t, period=period) for t in TICKERS]
    frames = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 5. LIVE QUARTERLY REVENUE
# ─────────────────────────────────────────────────────────────────────────────
def get_quarterly_financials(ticker: str) -> pd.DataFrame:
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
    tickers = tickers or TICKERS
    frames  = [get_quarterly_financials(t) for t in tickers]
    frames  = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 6. LIVE ANNUAL METRICS  +  CURRENT YEAR TTM INJECTION
# ─────────────────────────────────────────────────────────────────────────────
def get_ttm_as_current_year(ticker: str) -> dict | None:
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
    Merge strategy:
      1. Concat csv THEN live  (so live rows sort last → keep='last' keeps live).
      2. For any column that exists only in csv_df (e.g. RD_B), backfill NaNs
         in the live rows from the csv rows BEFORE deduplication.
    """
    if live_df is None or (hasattr(live_df, "empty") and live_df.empty):
        return csv_df
    if csv_df is None or (hasattr(csv_df, "empty") and csv_df.empty):
        return live_df

    # Align columns — union of both frames
    all_cols = list(dict.fromkeys(list(csv_df.columns) + list(live_df.columns)))
    csv_aligned  = csv_df.reindex(columns=all_cols)
    live_aligned = live_df.reindex(columns=all_cols)

    # Concat: csv first so live rows are the "last" duplicate → kept by keep='last'
    combined = pd.concat([csv_aligned, live_aligned], ignore_index=True)

    # For each key group, forward-fill CSV-only columns into live rows
    # (csv rows come first in the concat, live rows second)
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
