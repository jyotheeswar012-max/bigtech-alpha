# 🚀 MARKET NEXUS — Big Tech Intelligence Platform

> **Live financial analytics across Apple · Microsoft · Google · Amazon · Meta · NVIDIA · Tesla · Netflix**
> Powered by yfinance live data, real earnings & competitive benchmarks.

<div align="center">

### 🌐 [**LIVE DEMO → market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app**](https://market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app)

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Open%20App-00d4ff?style=for-the-badge&logoColor=white)](https://market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![yfinance](https://img.shields.io/badge/Data-yfinance-00C244?style=for-the-badge)](https://github.com/ranaroussi/yfinance)
[![Version](https://img.shields.io/badge/Version-5.0-ff6b35?style=for-the-badge)](#)

</div>

---

## ✨ Features

| Page | What you get |
|---|---|
| 🏠 **Command Center** | Live KPIs, revenue race, stock returns, treemap, revenue/employee |
| 📈 **Stock Performance** | Bollinger bands, MA50/MA200, volatility, annual return heatmap, violin plots |
| 💰 **Revenue & Earnings** | Quarterly deep-dive, CAGR, stacked revenue, net income trends |
| 🏆 **Competitive Analysis** | Radar chart, rankings board, P/S ratio, animated bubble chart |
| 🔬 **Deep Analytics** | Correlation matrix, normality tests, Q-Q plots, drawdown analysis |
| 🤖 **AI Insight Engine** | Auto-generated insights, full company scorecard |
| 📡 **Live Dashboard** | Real-time intraday prices, candlestick charts, 60s auto-refresh |

---

## 🎨 v5.0 Design Highlights

- **Glassmorphism UI** — cards with `backdrop-filter: blur` and layered gradients
- **Aurora Background** — animated radial glow orbs on the hero section
- **Live Ticker Tape** — scrolling symbol bar across the top
- **Spring Hover Physics** — KPI cards lift with `cubic-bezier(0.34, 1.56, 0.64, 1)`
- **Premium Typography** — Plus Jakarta Sans + Syne + JetBrains Mono
- **Curated Palette** — Cyan `#00d4ff` · Orange `#ff6b35` · Green `#00ff9d`

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

When `live_data.py` is available, the app fetches:
- Real-time prices & intraday OHLCV via yfinance
- Live fundamentals (market cap, P/E, revenue TTM)
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
| **Fonts** | Google Fonts (Syne, Plus Jakarta Sans, JetBrains Mono) |

---

## 👨‍💻 Author

**Jyotheeswar Gudipalli**
B.Tech Data Science 2027 · Manipal University Jaipur

[![GitHub](https://img.shields.io/badge/GitHub-jyotheeswar012--max-181717?style=flat&logo=github)](https://github.com/jyotheeswar012-max)
