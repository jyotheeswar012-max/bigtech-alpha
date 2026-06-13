# 🚀 MARKET NEXUS — Big Tech Intelligence Platform

> **Live financial analytics across Apple · Microsoft · Google · Amazon · Meta · NVIDIA · Tesla · Netflix**
> Powered by yfinance live data, real earnings & competitive benchmarks.

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://python.org)
[![yfinance](https://img.shields.io/badge/Data-yfinance-00C244)](https://github.com/ranaroussi/yfinance)
[![Version](https://img.shields.io/badge/Version-4.1-00e5ff)](#)

---

## ✨ Features

| Page | What you get |
|---|---|
| 🏠 **Command Center** | KPIs, revenue race, stock returns, treemap, revenue/employee |
| 📈 **Stock Performance** | Bollinger bands, MA50/MA200, volatility, annual return heatmap, violin plots |
| 💰 **Revenue & Earnings** | Quarterly deep-dive, CAGR, stacked revenue, net income trends |
| 🏆 **Competitive Analysis** | Radar chart, rankings board, P/S ratio, animated bubble chart |
| 🔬 **Deep Analytics** | Correlation matrix, normality tests, Q-Q plots, drawdown analysis |
| 🤖 **AI Insight Engine** | Auto-generated insights, full company scorecard |
| 📡 **Live Dashboard** | Real-time intraday prices, candlestick charts, 60s auto-refresh |

---

## 📦 Installation

```bash
git clone https://github.com/jyotheeswar012-max/market-nexus.git
cd market-nexus
pip install -r requirements.txt
streamlit run nexus.py
```

---

## 🗄️ Data

### CSV Fallback (offline mode)

| File | Coverage | Last Updated |
|---|---|---|
| `annual_metrics.csv` | 2020–2025 · 8 companies · Revenue, Net Income, Market Cap, Employees | June 2026 |
| `quarterly_revenue.csv` | Q1 2020 – Q2 2025 · 8 companies | June 2026 |
| `stock_prices.csv` | Daily OHLCV · 2020–2025 | yfinance live |

### Live Mode (yfinance)
- `live_data.py` fetches real-time fundamentals, price history, intraday bars and quarterly/annual earnings
- Auto-merges with CSV fallback so the app always has data even when markets are closed
- Prices delayed up to 15 minutes during market hours

---

## 🏗️ Architecture

```
nexus.py          ← main Streamlit app (v4.1)
live_data.py      ← yfinance data layer
annual_metrics.csv
quarterly_revenue.csv
stock_prices.csv
requirements.txt
```

### Key Design Decisions (v4.1)
- **`best_common_year()`** — finds the year where the most selected companies have data, prevents single-company year lock-in when yfinance fiscal calendars differ
- **`get_latest_slice()`** — used on every "latest year" chart/table across all pages, always resolves to the correct shared year
- **`COMMON_LATEST_YEAR`** — computed at startup, used for slider max and all cross-page defaults

---

## 📊 Companies Covered

| Company | Ticker | Sector |
|---|---|---|
| Apple | AAPL | Hardware |
| Microsoft | MSFT | Cloud/Software |
| Google | GOOGL | Digital Ads |
| Amazon | AMZN | E-Commerce/Cloud |
| Meta | META | Social Media |
| NVIDIA | NVDA | Semiconductors |
| Tesla | TSLA | EV/Energy |
| Netflix | NFLX | Streaming |

---

## 🔧 Requirements

```
streamlit>=1.35.0
pandas>=2.2.0
numpy>=1.26.0
plotly>=5.22.0
scipy>=1.13.0
yfinance>=0.2.61
streamlit-autorefresh>=1.0.1
requests>=2.32.0
```

---

## 👨‍💻 Author

**Jyotheeswar Gudipalli**  
B.Tech Data Science 2027 · Manipal University Jaipur  

---

*Data sourced from yfinance, public earnings reports & SEC filings. Prices delayed up to 15 minutes.*
