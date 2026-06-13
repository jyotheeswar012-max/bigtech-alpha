# constants.py — Single source of truth for Market Nexus
# ─────────────────────────────────────────────────────────────────────────────
# ALL company names, tickers, colours, sectors, CSV filenames, and TTL values
# live here. Neither live_data.py nor nexus.py should hard-code any of these.
# To add a new company: add one entry each in COMPANIES, COLORS, and SECTOR_MAP.
# ─────────────────────────────────────────────────────────────────────────────

# ── Ticker → Display-name mapping ────────────────────────────────────────────
COMPANIES: dict[str, str] = {
    "AAPL":  "Apple",
    "MSFT":  "Microsoft",
    "GOOGL": "Google",
    "AMZN":  "Amazon",
    "META":  "Meta",
    "NVDA":  "NVIDIA",
    "TSLA":  "Tesla",
    "NFLX":  "Netflix",
}

# Derived helpers — built once from COMPANIES, never duplicated elsewhere
TICKERS: list[str]        = list(COMPANIES.keys())
ALL_COMPANIES: list[str]  = list(COMPANIES.values())
NAME_TO_TICKER: dict[str, str] = {v: k for k, v in COMPANIES.items()}

# ── Brand colours (hex) ───────────────────────────────────────────────────────
COLORS: dict[str, str] = {
    "Apple":     "#e8e8e8",
    "Microsoft": "#00aff0",
    "Google":    "#fbbc05",
    "Amazon":    "#ff9900",
    "Meta":      "#1877f2",
    "NVIDIA":    "#76b900",
    "Tesla":     "#cc0000",
    "Netflix":   "#e50914",
}

# Same colours keyed by ticker (used by live_data / intraday charts)
COMPANY_COLORS: dict[str, str] = {
    ticker: COLORS[name] for ticker, name in COMPANIES.items()
}

# ── Sector labels ─────────────────────────────────────────────────────────────
SECTOR_MAP: dict[str, str] = {
    "Apple":     "Hardware",
    "Microsoft": "Cloud/Software",
    "Google":    "Digital Ads",
    "Amazon":    "E-Commerce/Cloud",
    "Meta":      "Social Media",
    "NVIDIA":    "Semiconductors",
    "Tesla":     "EV/Energy",
    "Netflix":   "Streaming",
}

# ── CSV baseline filenames ────────────────────────────────────────────────────
CSV_FILES: dict[str, str] = {
    "quarterly": "quarterly_revenue.csv",
    "annual":    "annual_metrics.csv",
    "prices":    "stock_prices.csv",
}

# ── Cache TTLs (seconds) ──────────────────────────────────────────────────────
# Change refresh cadence here; nowhere else.
DATA_TTL: dict[str, int] = {
    "fundamentals":   60,       # market cap / PE — changes every second
    "price_history":  86_400,   # daily OHLCV history — one new bar per day
    "annual":         43_200,   # annual earnings — filed quarterly
    "quarterly":      43_200,   # quarterly earnings — filed quarterly
    "merged_pipeline":3_600,    # full ann+q+price merge — hourly
    "intraday":       300,       # intraday bars — 5 min
    "live_price":     30,        # single ticker live price — 30 s
    "all_live_prices":60,        # comparison table — 60 s
}

# ── yfinance fetch settings ───────────────────────────────────────────────────
YF_PRICE_PERIOD:   str = "5y"   # history window for price charts
YF_PRICE_INTERVAL: str = "1d"   # daily bars
YF_MAX_RETRIES:    int = 3      # network retry attempts
YF_RETRY_DELAY:    float = 1.5  # seconds between retries
