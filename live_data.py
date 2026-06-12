# live_data.py — Live market data module for Market Nexus
# Powered by yfinance (free, no API key required)

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

# Reverse map: company name → ticker
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


# ─────────────────────────────────────────────────────────────────────────────
# 1.  LIVE PRICE  (used by Live Dashboard + Command Center KPIs)
# ─────────────────────────────────────────────────────────────────────────────
def get_live_price(ticker: str):
    """
    Returns (price, change_pct, volume).
    Falls back to last available daily close when market is closed.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d", interval="1m")
        if hist.empty:
            hist = stock.history(period="5d", interval="1d")
            if hist.empty:
                return None, None, None
        latest   = hist.iloc[-1]
        info     = stock.fast_info
        prev_close = getattr(info, "previous_close", None)
        if prev_close is None:
            prev_close = hist["Close"].iloc[-2] if len(hist) > 1 else latest["Close"]
        price      = round(float(latest["Close"]), 2)
        change_pct = round((price - prev_close) / prev_close * 100, 2)
        volume     = int(latest["Volume"]) if latest["Volume"] else 0
        return price, change_pct, volume
    except Exception:
        return None, None, None


def get_multi_live_prices(tickers: list) -> pd.DataFrame:
    rows = []
    for ticker in tickers:
        price, change, vol = get_live_price(ticker)
        rows.append({"Ticker": ticker, "Company": COMPANIES.get(ticker, ticker),
                     "Price": price, "Change%": change, "Volume": vol})
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────────────
# 2.  INTRADAY DATA  (Live Dashboard charts)
# ─────────────────────────────────────────────────────────────────────────────
def get_intraday_data(ticker: str, period: str = "1d", interval: str = "5m") -> pd.DataFrame:
    try:
        df = yf.Ticker(ticker).history(period=period, interval=interval)
        if df.empty and period == "1d":
            df = yf.Ticker(ticker).history(period="5d", interval="1d")
        return df
    except Exception:
        return pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 3.  LIVE MARKET CAP + FUNDAMENTALS  (Command Center KPIs, Competitive)
# ─────────────────────────────────────────────────────────────────────────────
def get_live_fundamentals(ticker: str) -> dict:
    """
    Returns dict with marketCap_B, revenue_B, netIncome_B, employees_K,
    trailingPE, forwardPE, ps_ratio, beta, 52w_high, 52w_low.
    """
    try:
        info = yf.Ticker(ticker).info
        mc   = info.get("marketCap", 0) or 0
        rev  = info.get("totalRevenue", 0) or 0
        ni   = info.get("netIncomeToCommon", 0) or 0
        emp  = info.get("fullTimeEmployees", 0) or 0
        return {
            "marketCap_B":   round(mc  / 1e9, 2),
            "revenue_B":     round(rev / 1e9, 2),
            "netIncome_B":   round(ni  / 1e9, 2),
            "employees_K":   round(emp / 1e3, 1),
            "trailingPE":    info.get("trailingPE"),
            "forwardPE":     info.get("forwardPE"),
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
    Fetch live fundamentals for all 8 companies.
    Returns a DataFrame with one row per company.
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
# 4.  LIVE STOCK PRICE HISTORY  (Stock Performance page)
# ─────────────────────────────────────────────────────────────────────────────
def get_price_history(ticker: str, period: str = "5y", interval: str = "1d") -> pd.DataFrame:
    """
    Returns daily OHLCV + Daily_Return column.
    period options: '1y','2y','5y','max'
    """
    try:
        df = yf.Ticker(ticker).history(period=period, interval=interval)
        if df.empty:
            return pd.DataFrame()
        df = df[["Open","High","Low","Close","Volume"]].copy()
        df.index = pd.to_datetime(df.index).tz_localize(None)
        df["Daily_Return"] = df["Close"].pct_change() * 100
        df["Company"]      = COMPANIES[ticker]
        df["Price"]        = df["Close"]
        df["Volume_M"]     = df["Volume"] / 1e6
        df = df.reset_index().rename(columns={"index": "Date", "Datetime": "Date"})
        if "Date" not in df.columns and df.index.name == "Date":
            df = df.reset_index()
        return df
    except Exception:
        return pd.DataFrame()


def get_all_price_history(period: str = "5y") -> pd.DataFrame:
    """
    Fetch price history for all 8 companies and return combined DataFrame.
    Matches schema of stock_prices.csv: Date, Company, Price, Volume_M, Daily_Return.
    """
    frames = []
    for ticker in TICKERS:
        df = get_price_history(ticker, period=period)
        if not df.empty:
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 5.  LIVE QUARTERLY REVENUE  (Revenue & Earnings page)
# ─────────────────────────────────────────────────────────────────────────────
def get_quarterly_financials(ticker: str) -> pd.DataFrame:
    """
    Returns quarterly revenue + net income from yfinance.
    Matches schema of quarterly_revenue.csv: Quarter, Company, Revenue_B.
    """
    try:
        t  = yf.Ticker(ticker)
        qf = t.quarterly_financials
        if qf is None or qf.empty:
            return pd.DataFrame()

        rev_row = None
        ni_row  = None
        for idx in qf.index:
            il = str(idx).lower()
            if "total revenue" in il or "revenue" in il:
                rev_row = idx
            if "net income" in il:
                ni_row = idx

        if rev_row is None:
            return pd.DataFrame()

        rows = []
        for col in qf.columns:
            rev = qf.loc[rev_row, col]
            ni  = qf.loc[ni_row,  col] if ni_row else None
            rows.append({
                "Quarter":   pd.to_datetime(col).tz_localize(None),
                "Company":   COMPANIES[ticker],
                "Revenue_B": round(float(rev) / 1e9, 2) if pd.notna(rev) else None,
                "NetIncome_B": round(float(ni) / 1e9, 2) if (ni is not None and pd.notna(ni)) else None,
            })
        df = pd.DataFrame(rows).dropna(subset=["Revenue_B"])
        df = df.sort_values("Quarter")
        return df
    except Exception:
        return pd.DataFrame()


def get_all_quarterly(tickers: list = None) -> pd.DataFrame:
    """
    Fetch quarterly revenue for all (or selected) companies.
    """
    tickers = tickers or TICKERS
    frames  = [get_quarterly_financials(t) for t in tickers]
    frames  = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 6.  LIVE ANNUAL METRICS  (replaces annual_metrics.csv on-the-fly)
# ─────────────────────────────────────────────────────────────────────────────
SECTOR_MAP = {
    "Apple":     "Consumer Tech",
    "Microsoft": "Cloud & Software",
    "Google":    "Ad Tech & Cloud",
    "Amazon":    "E-Commerce & Cloud",
    "Meta":      "Social Media",
    "NVIDIA":    "Semiconductors",
    "Tesla":     "EV & Energy",
    "Netflix":   "Streaming",
}

def get_annual_financials(ticker: str) -> pd.DataFrame:
    """
    Returns annual revenue, net income, market cap, employees by year.
    Matches schema of annual_metrics.csv.
    """
    try:
        t    = yf.Ticker(ticker)
        af   = t.financials        # annual income statement
        info = t.info
        name = COMPANIES[ticker]

        rev_row = ni_row = None
        for idx in af.index:
            il = str(idx).lower()
            if "total revenue" in il or "revenue" in il:
                rev_row = idx
            if "net income" in il and "minority" not in il:
                ni_row  = idx

        if rev_row is None:
            return pd.DataFrame()

        mc_now   = (info.get("marketCap") or 0) / 1e9
        emp_now  = (info.get("fullTimeEmployees") or 0) / 1e3
        price_now= info.get("currentPrice") or info.get("regularMarketPrice") or 0

        rows = []
        for col in af.columns:
            year = pd.to_datetime(col).year
            rev  = af.loc[rev_row, col]
            ni   = af.loc[ni_row,  col] if ni_row else None
            # Approximate historical market cap using current as proxy for latest year
            rows.append({
                "Year":         year,
                "Company":      name,
                "Sector":       SECTOR_MAP.get(name, "Tech"),
                "Revenue_B":    round(float(rev) / 1e9, 2) if pd.notna(rev) else None,
                "NetIncome_B":  round(float(ni)  / 1e9, 2) if (ni is not None and pd.notna(ni)) else None,
                "MarketCap_B":  round(mc_now, 2),   # live; historical approximated
                "Employees_K":  round(emp_now, 1),
            })
        df = pd.DataFrame(rows).dropna(subset=["Revenue_B"])
        df = df.sort_values("Year")
        return df
    except Exception:
        return pd.DataFrame()


def get_all_annual(tickers: list = None) -> pd.DataFrame:
    tickers = tickers or TICKERS
    frames  = [get_annual_financials(t) for t in tickers]
    frames  = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# 7.  SMART MERGE  (live data on top of CSV fallback)
# ─────────────────────────────────────────────────────────────────────────────
def merge_with_csv(live_df: pd.DataFrame, csv_df: pd.DataFrame,
                   key_cols: list) -> pd.DataFrame:
    """
    Merge live rows on top of CSV rows — live data wins for matching keys.
    key_cols: e.g. ['Company','Year'] or ['Company','Quarter']
    """
    if live_df.empty:
        return csv_df
    if csv_df.empty:
        return live_df
    combined = pd.concat([csv_df, live_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=key_cols, keep="last")
    return combined.sort_values(key_cols).reset_index(drop=True)


# ─────────────────────────────────────────────────────────────────────────────
# 8.  COMPANY INFO CARD  (AI Insight Engine)
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
