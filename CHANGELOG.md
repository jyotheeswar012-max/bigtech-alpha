# Changelog

All notable changes to Market Nexus are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2026-06-14

### Added
- 7-page Streamlit dashboard: Command Center, Stock Performance, Revenue & Earnings,
  Competitive Analysis, Deep Analytics, AI Insight Engine, Live Dashboard
- Live market data layer via `yfinance` with 3-tier fallback strategy
- Smart merge pipeline: live yfinance data wins over CSV on shared columns;
  CSV-only columns (e.g. RD_B) are back-filled into live rows
- `constants.py` as single source of truth for all company names, tickers,
  brand colours, sector labels, CSV filenames, and cache TTLs
- `COLORS` (name-keyed) and `COMPANY_COLORS` (ticker-keyed) derived from one
  hex table -- a colour change now requires exactly one edit
- Page modules extracted into `pages/` package:
  `page_command_center`, `page_stock_performance`, `page_revenue_earnings`,
  `page_competitive_analysis`, `page_deep_analytics`, `page_ai_insights`
- `nexus_ld_page.py` -- Live Dashboard with intraday charts, price cards,
  candlestick view, and auto-refresh via `streamlit-autorefresh`
- `live_data.py` -- yfinance data layer: live price, intraday OHLCV,
  fundamentals, price history, quarterly & annual financials, TTM injection
- Ticker tape, KPI tiles, hero banner, dark CSS theme (Inter + JetBrains Mono)
- `pytest` test suite: 6 test classes / 14 assertions for `merge_with_csv()`
- `pytest.ini` with `testpaths = tests`
- `CONTRIBUTING.md` and `LICENSE` (MIT)

### Architecture
- `nexus.py` -- router only (~280 lines); all rendering delegated to page modules
- Shared helpers (`sec`, `sf`, `hex_to_rgba`, `get_latest_slice`,
  `best_common_year`) injected into page modules via `**_HELPERS` dict
- Cache TTLs centralised in `DATA_TTL` dict inside `constants.py`

### Tracked Companies
Apple (AAPL), Microsoft (MSFT), Google (GOOGL), Amazon (AMZN),
Meta (META), NVIDIA (NVDA), Tesla (TSLA), Netflix (NFLX)
