# 🚀 Market Nexus — Big Tech Intelligence Platform

[![Live App](https://img.shields.io/badge/🚀%20Live%20App-Streamlit-FF4B4B?style=for-the-badge)](https://market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Built by Me](https://img.shields.io/badge/Built%20%26%20Deployed-by%20Jyotheeswar-01696f?style=for-the-badge)](https://github.com/jyotheeswar012-max)

> A full-stack financial analytics dashboard I built from scratch and deployed on Streamlit Cloud — tracking Apple · Microsoft · Google · Amazon · Meta · NVIDIA · Tesla · Netflix using real earnings data, 5-year stock history & competitive intelligence.

🔗 **Live Demo:** [market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app](https://market-nexus-myds7qdhci8mnmhvpylbmw.streamlit.app)

---

## 👨‍💻 About This Project

I built **Market Nexus** entirely by myself — from collecting and cleaning the datasets, to designing the multi-page dashboard architecture, writing all the Python/Plotly code, and deploying it live on Streamlit Cloud.

The idea came from wanting a single platform to compare the Big Tech giants across revenue, stock performance, and financial health — all in one interactive experience.

- ✅ **Dataset built by me** — sourced from public SEC filings and earnings reports
- ✅ **All charts coded by me** — 20+ custom Plotly visualizations
- ✅ **Deployed by me** — hosted live on Streamlit Cloud with zero-config CI/CD
- ✅ **Design & UX by me** — custom dark theme, layout, and page structure

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
├── nexus.py                 # Main Streamlit app — written entirely by me (700+ lines)
├── stock_prices.csv         # Daily stock prices 2020–2024 — collected & cleaned by me
├── quarterly_revenue.csv    # Quarterly earnings for 8 companies — built by me
├── annual_metrics.csv       # Annual KPIs: revenue, net income, market cap — built by me
└── requirements.txt         # Dependencies
```

---

## 🛠️ How I Built It

### 1. Data Collection
I gathered publicly available financial data from SEC filings, earnings press releases, and historical stock records for 8 Big Tech companies spanning 2020–2024 (10,000+ data points). I cleaned and structured this into 3 CSV files that power the entire app.

### 2. App Development
I built the entire Streamlit app in Python using:
- **Plotly** for all 20+ interactive charts (Scatter, Bar, Heatmap, Violin, Radar, Treemap, Q-Q plots)
- **Pandas & NumPy** for all data transformations and calculations
- **SciPy** for statistical analysis (Shapiro-Wilk normality tests, linear regression)
- Custom color theming and a `hex_to_rgba()` utility I wrote for consistent chart transparency

### 3. Deployment
I deployed the app on **Streamlit Cloud** directly from this GitHub repository. Every push to `main` auto-redeploys the live app — no additional configuration needed.

---

## 🚀 Run It Locally

```bash
# Clone my repo
git clone https://github.com/jyotheeswar012-max/market-nexus.git
cd market-nexus

# Install dependencies
pip install -r requirements.txt

# Launch
streamlit run nexus.py
```

Opens at `http://localhost:8501`

---

## 📊 Data Coverage

- **8 Companies:** Apple, Microsoft, Google (Alphabet), Amazon, Meta, NVIDIA, Tesla, Netflix
- **Time Range:** 2020 – 2024 (5 years)
- **Records:** 10,656+ data points
- **Source:** Public SEC filings, earnings reports, historical stock records

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web app framework & cloud deployment |
| [Plotly](https://plotly.com) | All interactive visualizations |
| [Pandas](https://pandas.pydata.org) | Data wrangling & analysis |
| [NumPy](https://numpy.org) | Numerical computing |
| [SciPy](https://scipy.org) | Statistical tests |
| Python 3.11 | Core language |

---

## 👤 Author

**Jyotheeswar Gudipalli**
B.Tech Data Science 2027 · Manipal University Jaipur
GitHub: [@jyotheeswar012-max](https://github.com/jyotheeswar012-max)

*Built, designed, and deployed entirely by me as a personal portfolio project.*

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
