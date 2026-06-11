# live_data.py — Live market data module for Market Nexus
# Powered by yfinance (free, no API key required)

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# ── Company registry (8 companies matching existing dataset) ──────────────────
COMPANIES = {
    "AAPL":  "Apple Inc.",
    "MSFT":  "Microsoft",
    "GOOGL": "Alphabet (Google)",
    "AMZN":  "Amazon",
    "META":  "Meta Platforms",
    "NVDA":  "NVIDIA",
    "TSLA":  "Tesla",
    "NFLX":  "Netflix",
}

COMPANY_COLORS = {
    "AAPL":  "#A8B8C8",
    "MSFT":  "#00A4EF",
    "GOOGL": "#34A853",
    "AMZN":  "#FF9900",
    "META":  "#1877F2",
    "NVDA":  "#76B900",
    "TSLA":  "#CC0000",
    "NFLX":  "#E50914",
}


def get_live_price(ticker: str):
    """
    Return (latest_close, change_pct, volume) for the given ticker.
    Returns (None, None, None) if data is unavailable.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d", interval="1m")
        if hist.empty:
            # Market closed — fall back to last available daily close
            hist = stock.history(period="5d", interval="1d")
            if hist.empty:
                return None, None, None

        latest = hist.iloc[-1]
        info = stock.info
        prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
        if prev_close is None:
            prev_close = hist["Close"].iloc[-2] if len(hist) > 1 else latest["Close"]

        price = round(float(latest["Close"]), 2)
        change_pct = round((price - prev_close) / prev_close * 100, 2)
        volume = int(latest["Volume"]) if latest["Volume"] else 0
        return price, change_pct, volume
    except Exception:
        return None, None, None


def get_intraday_data(ticker: str, period: str = "1d", interval: str = "5m") -> pd.DataFrame:
    """
    Return OHLCV DataFrame for intraday or short-range plotting.
    Falls back to 5d/1d when market is closed.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        if df.empty and period == "1d":
            # Market closed — return last 5 days of daily data instead
            df = stock.history(period="5d", interval="1d")
        return df
    except Exception:
        return pd.DataFrame()


def get_multi_live_prices(tickers: list) -> pd.DataFrame:
    """
    Fetch latest close prices for multiple tickers at once.
    Returns a DataFrame with columns: Ticker, Company, Price, Change%, Volume.
    """
    rows = []
    for ticker in tickers:
        price, change, vol = get_live_price(ticker)
        rows.append({
            "Ticker":    ticker,
            "Company":   COMPANIES.get(ticker, ticker),
            "Price":     price,
            "Change%":   change,
            "Volume":    vol,
        })
    return pd.DataFrame(rows)


def get_company_info(ticker: str) -> dict:
    """
    Return a dict of key fundamental info for the ticker:
    marketCap, trailingPE, forwardPE, fiftyTwoWeekHigh, fiftyTwoWeekLow.
    """
    try:
        info = yf.Ticker(ticker).info
        return {
            "marketCap":         info.get("marketCap"),
            "trailingPE":        info.get("trailingPE"),
            "forwardPE":         info.get("forwardPE"),
            "fiftyTwoWeekHigh":  info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow":   info.get("fiftyTwoWeekLow"),
            "dividendYield":     info.get("dividendYield"),
            "beta":              info.get("beta"),
        }
    except Exception:
        return {}
