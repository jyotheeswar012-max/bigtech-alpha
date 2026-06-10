# 🚀 Market Nexus — Big Tech Intelligence Platform

[![Live App](https://img.shields.io/badge/🚀%20Live%20App-Streamlit-FF4B4B?style=for-the-badge)](https://market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

> **Real-time financial analytics dashboard** tracking Apple · Microsoft · Google · Amazon · Meta · NVIDIA · Tesla · Netflix — powered by real earnings data, 5-year stock history & competitive intelligence.

🔗 **Live Demo:** [market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app](https://market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app)

---

## 📸 Overview

Market Nexus is a **Big Tech Intelligence Platform** built with Streamlit and Plotly that gives you deep financial insights across 8 major technology companies. Featuring 6 fully interactive pages with 20+ chart types, all driven by real public earnings data.

---

## ✨ Features

| Page | What You Get |
|------|-------------|
| 🏠 **Command Center** | KPI dashboard, revenue race, stock returns, market cap evolution, treemap |
| 📈 **Stock Performance** | Price history, Bollinger Bands, moving averages, volatility analysis, return heatmap |
| 💰 **Revenue & Earnings** | Quarterly deep-dive, YoY growth, CAGR, stacked revenue, net income trends |
| 🏆 **Competitive Analysis** | Multi-dimensional radar chart, rankings board, P/S ratio, animated scatter |
| 🔬 **Deep Analytics** | Correlation matrix, statistical normality tests, Q-Q plots, drawdown analysis |
| 🤖 **AI Insight Engine** | Auto-generated insights from real data, full company scorecard 2024 |

---

## 🗂️ Project Structure

```
market-nexus/
├── nexus.py                 # Main Streamlit application (700+ lines)
├── stock_prices.csv         # Daily stock prices 2020–2024 (10,000+ rows)
├── quarterly_revenue.csv    # Quarterly earnings for 8 companies
├── annual_metrics.csv       # Annual KPIs: revenue, net income, market cap, headcount
└── requirements.txt         # Python dependencies
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.8+

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/jyotheeswar012-max/market-nexus.git
cd market-nexus

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run nexus.py
```

The app will open at `http://localhost:8501`

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io)** — Web app framework
- **[Plotly](https://plotly.com)** — Interactive charts (Scatter, Bar, Heatmap, Violin, Radar, Treemap)
- **[Pandas](https://pandas.pydata.org)** — Data wrangling & analysis
- **[NumPy](https://numpy.org)** — Numerical computing
- **[SciPy](https://scipy.org)** — Statistical tests (Shapiro-Wilk, linear regression)
- **Python 3.11** — Core language

---

## 📊 Data Coverage

- **8 Companies:** Apple, Microsoft, Google (Alphabet), Amazon, Meta, NVIDIA, Tesla, Netflix
- **Time Range:** 2020 – 2024 (5 years)
- **Records:** 10,656+ data points
- **Source:** Public earnings reports, SEC filings, historical stock records

---

## 👤 Author

**Jyotheeswar Gudipalli**
B.Tech Data Science 2027 · Manipal University Jaipur
GitHub: [@jyotheeswar012-max](https://github.com/jyotheeswar012-max)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
