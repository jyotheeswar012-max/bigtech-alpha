# 🚀 BIGTECH ALPHA — Big Tech Intelligence Platform

> **Live financial analytics across Apple · Microsoft · Google · Amazon · Meta · NVIDIA · Tesla · Netflix**  
> Powered by yfinance live data, real earnings & competitive benchmarks.

<div align="center">

### 🌐 [**LIVE DEMO → market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app**](https://market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app)

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Open%20App-00d4ff?style=for-the-badge&logoColor=white)](https://market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![yfinance](https://img.shields.io/badge/Data-yfinance-00C244?style=for-the-badge)](https://github.com/ranaroussi/yfinance)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-6.2-ff6b35?style=for-the-badge)](#)

</div>

---

## ✨ Features

| Page | What you get |
|---|---|
| 🏠 **Command Center** | Live KPIs, revenue race, stock returns, treemap, revenue/employee |
| 📈 **Stock Performance** | Bollinger bands, MA50/MA200, volatility, risk stats table, return analysis |
| 💰 **Revenue & Earnings** | Annual + quarterly revenue trends, net income, profit margin over time |
| 🏆 **Competitive Analysis** | Radar chart, market share pies, efficiency metrics |
| 🔬 **Deep Analytics** | Correlation matrix, regression, YoY growth factor analysis |
| 🤖 **AI Insight Engine** | Auto-generated insights, full company financial snapshot |
| 📡 **Live Dashboard** | Real-time prices, intraday 5-min chart, 30s auto-refresh |

---

## 🗂️ Code Structure

```
bigtech-alpha/
├── nexus.py               # Main Streamlit application — all 7 pages live here
├── live_data.py           # yfinance data fetcher — live prices, fundamentals, history
├── constants.py           # Shared colour palette, company list, CSS tokens
├── annual_metrics.csv     # CSV fallback — annual Revenue, NetIncome, MarketCap, etc.
├── quarterly_revenue.csv  # CSV fallback — quarterly revenue per company
├── stock_prices.csv       # CSV fallback — daily OHLCV price history
├── requirements.txt       # Python dependencies
├── CONTRIBUTING.md        # Contribution guidelines
└── LICENSE                # MIT License
```

### How the files interact

```
┌─────────────────────────────────────────────────────────┐
│                      nexus.py                           │
│  Streamlit UI · 7 pages · charts · filters · sidebar    │
│                                                         │
│  ① tries:  from live_data import get_all_annual, ...    │
│  ② on fail: falls back to CSV files via load_csv()      │
│  ③ always imports: COLORS, PAGE_NAMES from constants.py │
└───────────┬─────────────────────────┬───────────────────┘
            │                         │
            ▼                         ▼
   ┌─────────────────┐      ┌──────────────────────┐
   │   live_data.py  │      │    constants.py       │
   │  yfinance API   │      │  COLORS dict          │
   │  get_all_annual │      │  ALL_COMPANIES list   │
   │  get_all_qtrly  │      │  PAGE_NAMES list      │
   │  merge_with_csv │      │  CSS design tokens    │
   └────────┬────────┘      └──────────────────────┘
            │ merge_with_csv blends live API rows
            │ with CSV rows, preferring live data
            ▼
   ┌─────────────────────────────────┐
   │  annual_metrics.csv             │
   │  quarterly_revenue.csv          │
   │  stock_prices.csv               │
   └─────────────────────────────────┘
```

**Key design decisions:**
- `live_data.py` is an **optional dependency** — the app runs fully offline using only the three CSV files if `live_data.py` or `yfinance` is unavailable.
- `merge_with_csv()` inside `live_data.py` performs a left-join that keeps live API rows and fills any missing columns from the CSV baseline, so historical data is never lost.
- `constants.py` is the single source of truth for colours, company names, and CSS variables. Changes here propagate to both the sidebar and every chart.
- All data loading in `nexus.py` is wrapped in `@st.cache_data` with appropriate TTLs (fundamentals: 5 min, annual/quarterly: 12 h, prices: 24 h) to avoid redundant API calls.

---

## 📦 Installation

```bash
git clone https://github.com/jyotheeswar012-max/bigtech-alpha.git
cd bigtech-alpha
pip install -r requirements.txt
streamlit run nexus.py
```

> **No yfinance account needed.** The app works out of the box with CSV data. Live mode activates automatically when `live_data.py` can reach the yfinance API.

---

## 🗄️ Data

### CSV Fallback (offline mode)

| File | Coverage | Last Updated |
|---|---|---|
| `annual_metrics.csv` | 2020–2025 · 8 companies · Revenue, Net Income, Market Cap, Employees | June 2026 |
| `quarterly_revenue.csv` | Q1 2020 – Q2 2025 · 8 companies | June 2026 |
| `stock_prices.csv` | Daily OHLCV · 2020–2025 | yfinance live |

### Live Mode (yfinance)

When `live_data.py` is present and yfinance is reachable, the app fetches:
- Real-time prices & intraday OHLCV
- Live fundamentals (market cap, P/E, TTM revenue)
- 5-year price history merged with CSV baseline

---

## 🏢 Companies Tracked

| Ticker | Company | Sector |
|---|---|---|
| AAPL | Apple | Consumer Tech |
| MSFT | Microsoft | Cloud / Enterprise |
| GOOGL | Google (Alphabet) | Search / Cloud |
| AMZN | Amazon | E-Commerce / Cloud |
| META | Meta | Social Media |
| NVDA | NVIDIA | Semiconductors / AI |
| TSLA | Tesla | EVs / Energy |
| NFLX | Netflix | Streaming |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | Streamlit |
| **Data** | yfinance, pandas, numpy |
| **Visualisation** | Plotly (graph_objects + express) |
| **Statistics** | scipy.stats |
| **Fonts** | Google Fonts (Inter, Outfit, JetBrains Mono) |

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to report bugs, suggest features, and submit pull requests.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for full terms. You are free to use, modify, and distribute this project with attribution.

---

## 👨‍💻 Author

**Jyotheeswar Reddy**  
B.Tech Data Science 2027 · Manipal University Jaipur

[![GitHub](https://img.shields.io/badge/GitHub-jyotheeswar012--max-181717?style=flat&logo=github)](https://github.com/jyotheeswar012-max)
