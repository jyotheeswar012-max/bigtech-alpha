"""
╔══════════════════════════════════════════════════════════════════╗
║  MARKET NEXUS — Big Tech Intelligence Platform  v6.0            ║
║  Live data: Apple · Microsoft · Google · Amazon · Meta          ║
║             NVIDIA · Tesla · Netflix                             ║
║  Run: streamlit run nexus.py                                     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from pathlib import Path
from scipy import stats as scipy_stats

st.set_page_config(
    page_title="MARKET NEXUS", page_icon="🚀",
    layout="wide", initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;700&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
:root{
  --bg:#f0f4ff;--white:#ffffff;--surface:#f5f7ff;
  --primary:#4f46e5;--accent:#06b6d4;--orange:#f97316;
  --green:#10b981;--red:#ef4444;--purple:#8b5cf6;--pink:#ec4899;--yellow:#f59e0b;
  --txt:#0f172a;--txt2:#475569;--txt3:#94a3b8;--txt4:#cbd5e1;
  --border:rgba(99,102,241,0.12);--border2:rgba(99,102,241,0.22);
  --shadow:0 4px 16px rgba(0,0,0,0.06);--shadow-lg:0 12px 40px rgba(79,70,229,0.12);
  --shadow-xl:0 24px 60px rgba(79,70,229,0.15);
  --radius:16px;--radius-xl:32px;
}
*{box-sizing:border-box;}
.stApp{background:var(--bg)!important;font-family:'Inter',sans-serif;color:var(--txt);}
.main .block-container{padding:1.4rem 2.2rem!important;max-width:100%!important;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#4f46e5 0%,#6366f1 40%,#818cf8 100%)!important;
  border-right:none!important;box-shadow:4px 0 24px rgba(79,70,229,0.15);
}
[data-testid="stSidebar"] *{color:#fff!important;}
[data-testid="stSidebar"] .stSelectbox>div>div,
[data-testid="stSidebar"] .stMultiSelect>div>div{
  background:rgba(255,255,255,0.15)!important;border:1px solid rgba(255,255,255,0.25)!important;
  border-radius:12px!important;color:#fff!important;
}
.hero{
  position:relative;overflow:hidden;
  background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 30%,#06b6d4 70%,#10b981 100%);
  border-radius:var(--radius-xl);padding:3.2rem 3.8rem 3rem;margin-bottom:2rem;
  box-shadow:var(--shadow-xl);color:#fff;
}
.hero-title{font-family:'Outfit',sans-serif;font-size:4.5rem;font-weight:900;line-height:1.0;letter-spacing:-0.035em;margin:0 0 0.8rem 0;}
.hero-sub{font-size:1.05rem;line-height:1.7;max-width:620px;opacity:0.9;}
.hero-chips{display:flex;gap:0.6rem;flex-wrap:wrap;margin-top:1.6rem;}
.chip{display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.3);color:#fff!important;font-size:0.65rem;font-weight:500;padding:0.4rem 1rem;border-radius:100px;}
.ticker-wrap{overflow:hidden;background:var(--white);border:1px solid var(--border);border-radius:100px;padding:0.55rem 0;margin-bottom:1.8rem;white-space:nowrap;}
.ticker-inner{display:inline-block;animation:ticker-scroll 35s linear infinite;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:var(--txt3);}
.ticker-inner span.sym{color:var(--primary);font-weight:700;margin:0 0.25rem;}
@keyframes ticker-scroll{0%{transform:translateX(0);}100%{transform:translateX(-50%);}}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem;margin-bottom:2rem;}
.kpi{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:1.6rem 1.8rem 1.5rem;position:relative;overflow:hidden;box-shadow:var(--shadow);transition:all 0.3s;}
.kpi:hover{transform:translateY(-5px);box-shadow:var(--shadow-xl);}
.kpi-stripe{position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,var(--primary),var(--accent));}
.kpi-stripe.orange{background:linear-gradient(90deg,var(--orange),var(--yellow));}
.kpi-stripe.green{background:linear-gradient(90deg,var(--green),var(--accent));}
.kpi-stripe.purple{background:linear-gradient(90deg,var(--purple),var(--pink));}
.kpi-label{font-size:0.68rem;text-transform:uppercase;letter-spacing:0.14em;color:var(--txt3);margin-bottom:0.6rem;font-weight:600;}
.kpi-val{font-family:'Outfit',sans-serif;font-size:2.3rem;font-weight:800;line-height:1.0;color:var(--primary)!important;}
.kpi-val.orange{color:var(--orange)!important;}
.kpi-val.green{color:var(--green)!important;}
.kpi-val.purple{color:var(--purple)!important;}
.kpi-sub{font-family:'JetBrains Mono',monospace;font-size:0.66rem;color:var(--txt3);margin-top:0.5rem;}
.kpi-icon{position:absolute;right:1.5rem;bottom:1.3rem;font-size:2.5rem;opacity:0.08;}
.kpi-badge{position:absolute;top:1.1rem;right:1rem;font-size:0.58rem;padding:0.22rem 0.7rem;border-radius:100px;font-weight:700;}
.up{background:rgba(16,185,129,0.12);color:var(--green)!important;border:1px solid rgba(16,185,129,0.25);}
.down{background:rgba(239,68,68,0.10);color:var(--red)!important;border:1px solid rgba(239,68,68,0.2);}
.flat{background:rgba(245,158,11,0.10);color:var(--yellow)!important;border:1px solid rgba(245,158,11,0.2);}
.sec{display:flex;align-items:center;gap:1rem;margin:2.5rem 0 1.4rem 0;}
.sec-title{font-family:'Outfit',sans-serif;font-size:0.9rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--txt);}
.sec-line{flex:1;height:1px;background:linear-gradient(90deg,var(--border2),transparent);}
.sec-tag{font-size:0.58rem;color:var(--white)!important;background:linear-gradient(135deg,var(--primary),var(--accent));padding:0.28rem 0.8rem;border-radius:100px;font-weight:600;}
.page-title{font-family:'Outfit',sans-serif;font-size:2.5rem;font-weight:800;letter-spacing:-0.03em;background:linear-gradient(135deg,var(--primary) 0%,var(--accent) 60%,var(--green) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:1.6rem;}
.insight-card{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem 2rem;margin-bottom:1rem;border-left:4px solid var(--primary);box-shadow:var(--shadow);transition:all 0.25s;}
.insight-card:hover{transform:translateX(6px);box-shadow:var(--shadow-lg);}
.insight-title{font-family:'Outfit',sans-serif;font-size:0.95rem;font-weight:700;color:var(--txt);margin-bottom:0.5rem;}
.insight-body{font-size:0.88rem;color:var(--txt2);line-height:1.8;}
.live{display:inline-block;width:8px;height:8px;background:#34d399;border-radius:50%;margin-right:6px;vertical-align:middle;animation:pulse-ring 2s ease infinite;}
@keyframes pulse-ring{0%{box-shadow:0 0 0 0 rgba(52,211,153,0.5);}70%{box-shadow:0 0 0 8px rgba(52,211,153,0);}100%{box-shadow:0 0 0 0 rgba(52,211,153,0);}}
.logo-wrap{padding:1.6rem 0 1.2rem;}
.logo-text{font-family:'Outfit',sans-serif;font-size:1.6rem;font-weight:900;color:#fff!important;}
.logo-sub{font-size:0.55rem;color:rgba(255,255,255,0.55)!important;letter-spacing:0.16em;margin-top:0.25rem;}
.h-divider{height:1px;background:rgba(255,255,255,0.15);margin:0.8rem 0;}
.stTabs [data-baseweb="tab-list"]{gap:0.35rem;background:transparent;border-bottom:2px solid var(--border);}
.stTabs [data-baseweb="tab"]{background:transparent!important;border:none!important;border-bottom:3px solid transparent!important;border-radius:0!important;color:var(--txt3)!important;font-size:0.85rem;font-weight:600;padding:0.7rem 1.3rem!important;transition:all 0.2s;}
.stTabs [data-baseweb="tab"]:hover{color:var(--primary)!important;}
.stTabs [aria-selected="true"]{color:var(--primary)!important;border-bottom-color:var(--primary)!important;background:transparent!important;}
[data-testid="stMetric"]{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:1.1rem 1.3rem;}
[data-testid="stMetricValue"]{font-family:'Outfit',sans-serif!important;color:var(--primary)!important;font-weight:700;}
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--txt4);border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#475569", size=11),
    xaxis=dict(gridcolor="rgba(0,0,0,0.04)", zerolinecolor="rgba(0,0,0,0.07)"),
    yaxis=dict(gridcolor="rgba(0,0,0,0.04)", zerolinecolor="rgba(0,0,0,0.07)"),
    margin=dict(l=10, r=10, t=44, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=1,
                font=dict(size=10, color="#64748b"), orientation='h', y=1.12),
)
COLORS = {
    'Apple': '#1d1d1f', 'Microsoft': '#0078d4', 'Google': '#ea4335',
    'Amazon': '#ff9900', 'Meta': '#0668e1', 'NVIDIA': '#76b900',
    'Tesla': '#cc0000', 'Netflix': '#e50914',
}
ALL_COMPANIES = list(COLORS.keys())

# ✔ Page names — index is the single source of truth for routing
PAGE_NAMES = [
    "🏠  Command Center",
    "📈  Stock Performance",
    "💰  Revenue & Earnings",
    "🏆  Competitive Analysis",
    "🔬  Deep Analytics",
    "🤖  AI Insight Engine",
    "📡  Live Dashboard",
]
PAGE_CC  = 0
PAGE_SP  = 1
PAGE_RE  = 2
PAGE_CA  = 3
PAGE_DA  = 4
PAGE_AI  = 5
PAGE_LD  = 6


def hex_to_rgba(h, a=0.15):
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{a})'


def sf(fig, h=360, legend=True):
    kw = dict(**PL, height=h)
    if not legend:
        kw['showlegend'] = False
    fig.update_layout(**kw)
    return fig


def sec(title, tag=""):
    t = f'<div class="sec-tag">{tag}</div>' if tag else ''
    st.markdown(
        f'<div class="sec"><div class="sec-title">{title}</div>'
        f'<div class="sec-line"></div>{t}</div>',
        unsafe_allow_html=True)


# ── OPTIONAL LIVE IMPORTS ─────────────────────────────────────────────────────
try:
    from live_data import (
        get_live_price, get_intraday_data, get_multi_live_prices,
        get_all_fundamentals, get_all_price_history,
        get_all_quarterly, get_all_annual, merge_with_csv,
        COMPANIES as LIVE_COMPANIES, COMPANY_COLORS, NAME_TO_TICKER,
    )
    _live_ok = True
except ImportError:
    _live_ok = False

try:
    from streamlit_autorefresh import st_autorefresh
    _autorefresh_ok = True
except ImportError:
    _autorefresh_ok = False


# ── DATA LOADERS ──────────────────────────────────────────────────────────────
@st.cache_data
def load_csv():
    base = Path(__file__).parent
    q = pd.read_csv(base / "quarterly_revenue.csv", parse_dates=["Quarter"])
    a = pd.read_csv(base / "annual_metrics.csv")
    p = pd.read_csv(base / "stock_prices.csv", parse_dates=["Date"])
    return q, a, p


@st.cache_data(ttl=43200)
def load_live_annual():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_annual()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=43200)
def load_live_quarterly():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_quarterly()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=86400)
def load_live_prices():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_price_history(period="5y")
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=60)
def load_live_fundamentals():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_fundamentals()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def build_merged_data():
    q_csv, ann_csv, price_csv = load_csv()
    live_ann = load_live_annual()
    live_q   = load_live_quarterly()
    live_p   = load_live_prices()

    ann_df   = merge_with_csv(live_ann, ann_csv, ['Company', 'Year']) if (_live_ok and not live_ann.empty) else ann_csv.copy()

    if _live_ok and not live_q.empty:
        lq = live_q.copy(); lq['Quarter'] = pd.to_datetime(lq['Quarter'])
        cq = q_csv.copy();  cq['Quarter'] = pd.to_datetime(cq['Quarter'])
        q_df = merge_with_csv(lq, cq, ['Company', 'Quarter'])
    else:
        q_df = q_csv.copy()

    if _live_ok and not live_p.empty:
        lp = live_p.copy(); lp['Date'] = pd.to_datetime(lp['Date'])
        cp = price_csv.copy(); cp['Date'] = pd.to_datetime(cp['Date'])
        price_df = merge_with_csv(lp, cp, ['Company', 'Date'])
    else:
        price_df = price_csv.copy()

    if 'Date' not in price_df.columns and price_df.index.name == 'Date':
        price_df = price_df.reset_index()

    q_df['Quarter']  = pd.to_datetime(q_df['Quarter'])
    price_df['Date'] = pd.to_datetime(price_df['Date']).dt.tz_localize(None)
    ann_df['Year']   = ann_df['Year'].astype(int)
    return ann_df, q_df, price_df


ann_df, q_df, price_df = build_merged_data()
fund_df = load_live_fundamentals()


def best_common_year(df, all_cos=None):
    if all_cos is None:
        all_cos = ALL_COMPANIES
    yc = df[df.Company.isin(all_cos)].groupby('Year')['Company'].nunique()
    if yc.empty:
        return int(df['Year'].max())
    valid = yc[yc >= max(1, len(all_cos) // 2)]
    return int(valid.index.max()) if not valid.empty else int(yc.index.max())


COMMON_LATEST_YEAR = best_common_year(ann_df)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <div style="font-size:2rem;margin-bottom:0.35rem;">🚀</div>
      <div class="logo-text">MARKET NEXUS</div>
      <div class="logo-sub">BIG TECH INTELLIGENCE · v6.0</div>
    </div>
    <div class="h-divider"></div>
    """, unsafe_allow_html=True)

    sel_companies = st.multiselect("Companies", ALL_COMPANIES, default=ALL_COMPANIES)
    if not sel_companies:
        sel_companies = ALL_COMPANIES

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    slider_min = int(ann_df['Year'].min()) if not ann_df.empty else 2020
    slider_max = COMMON_LATEST_YEAR
    year_range = st.slider("Year Range", slider_min, slider_max, (slider_min, slider_max))

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)

    # ✔ FIX: use selectbox index — page_idx is a plain integer, no string matching bugs
    page_idx = st.selectbox(
        "Navigation",
        options=list(range(len(PAGE_NAMES))),
        format_func=lambda i: PAGE_NAMES[i],
        key="page_idx"
    )

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    data_src = "yfinance LIVE" if (_live_ok and not ann_df.empty) else "CSV Fallback"
    price_latest = price_df['Date'].max().strftime("%Y-%m-%d") if not price_df.empty else "—"
    st.markdown(
        f"<div style='font-size:0.6rem;opacity:0.5;line-height:2;'>"
        f"🕐 {datetime.now().strftime('%H:%M:%S')}<br>"
        f"📡 {data_src}<br>"
        f"📅 Latest year: {COMMON_LATEST_YEAR}<br>"
        f"📈 Prices to: {price_latest}<br>"
        f"🗂 {len(q_df)+len(ann_df)+len(price_df):,} records"
        f"</div>",
        unsafe_allow_html=True
    )


# ── FILTERED DATA ─────────────────────────────────────────────────────────────
ann_f = ann_df[(ann_df.Company.isin(sel_companies)) & (ann_df.Year.between(*year_range))]
q_f   = q_df[(q_df.Company.isin(sel_companies)) & (q_df.Quarter.dt.year.between(*year_range))]
p_f   = price_df[(price_df.Company.isin(sel_companies)) & (price_df.Date.dt.year.between(*year_range))]


def get_latest_slice(df, companies, fallback_year=None):
    sub = df[df.Company.isin(companies)]
    yr  = best_common_year(sub, companies) if fallback_year is None else fallback_year
    return sub[sub.Year == yr].copy(), yr


# ── TICKER TAPE ───────────────────────────────────────────────────────────────
ticker_syms = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "NFLX"]
ticker_html = " &nbsp;·&nbsp; ".join([f'<span class="sym">{s}</span>' for s in ticker_syms * 2])
st.markdown(
    f'<div class="ticker-wrap"><div class="ticker-inner">{ticker_html} &nbsp;&nbsp; {ticker_html}</div></div>',
    unsafe_allow_html=True
)


# ════════════════════════════════════════════════════════════════════
# PAGE 1 — COMMAND CENTER
# ════════════════════════════════════════════════════════════════════
if page_idx == PAGE_CC:

    st.markdown("""
    <div class="hero">
      <div style="position:relative;z-index:1;">
        <div style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;opacity:0.8;margin-bottom:0.8rem;">⚡ Live Big Tech Intelligence Platform</div>
        <p class="hero-title">MARKET<br>NEXUS</p>
        <p class="hero-sub">
          Real-time financial intelligence across
          <strong>Apple · Microsoft · Google · Amazon · Meta · NVIDIA · Tesla · Netflix</strong>
          — powered by yfinance live feeds.
        </p>
        <div class="hero-chips">
          <span class="chip">📊 Live Earnings</span>
          <span class="chip">📈 Stock History</span>
          <span class="chip">🏆 Competitive Intel</span>
          <span class="chip">💡 AI Insights</span>
          <span class="chip">📡 Live Prices</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not fund_df.empty:
        kpi_cos     = fund_df[fund_df.Company.isin(sel_companies)]
        total_rev   = kpi_cos.revenue_B.sum()
        total_mcap  = kpi_cos.marketCap_B.sum()
        top_row     = kpi_cos.loc[kpi_cos.marketCap_B.idxmax()]
        top_mcap_co = top_row['Company']
        top_mcap    = top_row['marketCap_B']
        nvda_row    = kpi_cos[kpi_cos.Company == 'NVIDIA']
        nvda_ni     = nvda_row['netIncome_B'].values[0] if not nvda_row.empty else 0
        data_label  = "Live · yfinance"
    else:
        latest_sl, lyr = get_latest_slice(ann_df, sel_companies)
        if latest_sl.empty:
            latest_sl, lyr = get_latest_slice(ann_df, ALL_COMPANIES)
        total_rev   = latest_sl.Revenue_B.sum()
        total_mcap  = latest_sl.MarketCap_B.sum()
        top_idx     = latest_sl.MarketCap_B.idxmax()
        top_mcap_co = latest_sl.loc[top_idx, 'Company']
        top_mcap    = latest_sl.loc[top_idx, 'MarketCap_B']
        nvda_sl     = latest_sl[latest_sl.Company == 'NVIDIA']
        nvda_ni     = nvda_sl['NetIncome_B'].values[0] if not nvda_sl.empty else 0
        data_label  = f"CSV · {lyr}"

    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi"><div class="kpi-stripe"></div><div class="kpi-icon">💰</div>
        <div class="kpi-label">Combined Revenue (TTM)</div>
        <div class="kpi-val">${total_rev/1000:.2f}T</div>
        <div class="kpi-sub">{len(sel_companies)} companies · {data_label}</div>
        <div class="kpi-badge up">↑ LIVE</div></div>
      <div class="kpi"><div class="kpi-stripe orange"></div><div class="kpi-icon">🏦</div>
        <div class="kpi-label">Combined Market Cap</div>
        <div class="kpi-val orange">${total_mcap/1000:.1f}T</div>
        <div class="kpi-sub">{data_label}</div>
        <div class="kpi-badge up">↑ LIVE</div></div>
      <div class="kpi"><div class="kpi-stripe green"></div><div class="kpi-icon">🥇</div>
        <div class="kpi-label">Largest by Market Cap</div>
        <div class="kpi-val green">{top_mcap_co}</div>
        <div class="kpi-sub">${top_mcap:,.0f}B cap</div>
        <div class="kpi-badge flat">LIVE</div></div>
      <div class="kpi"><div class="kpi-stripe purple"></div><div class="kpi-icon">⚡</div>
        <div class="kpi-label">NVIDIA Net Income (TTM)</div>
        <div class="kpi-val purple">${nvda_ni:.1f}B</div>
        <div class="kpi-sub">AI boom · {data_label}</div>
        <div class="kpi-badge up">↑ LIVE</div></div>
    </div>
    """, unsafe_allow_html=True)

    sec("Revenue Race & Market Cap", "LIVE yfinance DATA")
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        for co in sel_companies:
            sub = q_f[q_f.Company == co].sort_values('Quarter')
            if sub.empty: continue
            fig.add_trace(go.Scatter(x=sub.Quarter, y=sub.Revenue_B, name=co, mode='lines',
                line=dict(color=COLORS[co], width=2.5),
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>${{y:.1f}}B<extra></extra>'))
        sf(fig, 350).update_layout(
            title=dict(text="Quarterly Revenue ($B)", font=dict(size=13, color='#334155')),
            yaxis_title="Revenue ($B)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        mc_data = ann_f.pivot(index='Year', columns='Company', values='MarketCap_B').fillna(0)
        fig = go.Figure()
        for co in [c for c in sel_companies if c in mc_data.columns]:
            fig.add_trace(go.Bar(x=mc_data.index, y=mc_data[co], name=co,
                marker_color=COLORS[co], opacity=0.88,
                hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:,.0f}}B<extra></extra>'))
        fig.update_layout(barmode='group')
        sf(fig, 350).update_layout(
            title=dict(text="Market Cap by Year ($B)", font=dict(size=13, color='#334155')),
            yaxis_title="Market Cap ($B)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    sec("Stock Returns & Profitability", "LIVE PRICE HISTORY")
    c1, c2 = st.columns([3, 2])
    with c1:
        fig = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f.Company == co].sort_values('Date')
            if sub.empty: continue
            base = sub.Price.iloc[0]
            fig.add_trace(go.Scatter(x=sub.Date, y=sub.Price / base * 100, name=co, mode='lines',
                line=dict(color=COLORS[co], width=2),
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>%{{y:.0f}}<extra></extra>'))
        fig.add_hline(y=100, line_dash='dot', line_color='rgba(0,0,0,0.08)')
        sf(fig, 340).update_layout(
            title=dict(text="Normalised Stock Performance (Base=100)", font=dict(size=13, color='#334155')),
            yaxis_title="Indexed Return")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        margin_sl, m_yr = get_latest_slice(ann_df, sel_companies)
        margin_sl = margin_sl.copy()
        margin_sl['Margin'] = (margin_sl.NetIncome_B / margin_sl.Revenue_B * 100).round(1)
        margin_sl = margin_sl.sort_values('Margin')
        fig = go.Figure(go.Bar(
            x=margin_sl.Margin, y=margin_sl.Company, orientation='h',
            marker=dict(color=margin_sl.Margin,
                colorscale=[[0,'#ef4444'],[0.4,'#f97316'],[1,'#10b981']], line=dict(width=0)),
            text=[f"{v:.1f}%" for v in margin_sl.Margin], textposition='outside',
            hovertemplate='<b>%{y}</b><br>Margin: %{x:.1f}%<extra></extra>'))
        sf(fig, 340, legend=False).update_layout(
            title=dict(text=f"Net Profit Margin {m_yr}", font=dict(size=13, color='#334155')),
            xaxis_title="Net Margin %")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    sec("Revenue Distribution & Headcount", "STRUCTURAL VIEW")
    c1, c2 = st.columns(2)
    with c1:
        treemap_sl, t_yr = get_latest_slice(ann_df, sel_companies)
        if not treemap_sl.empty:
            fig = px.treemap(treemap_sl, path=['Sector','Company'], values='Revenue_B',
                color='NetIncome_B',
                color_continuous_scale=[[0,'#ef4444'],[0.5,'#f0f4ff'],[1,'#10b981']],
                hover_data={'Revenue_B':':.1f','NetIncome_B':':.1f'})
            fig.update_traces(textfont_size=13, textfont_color='#1e293b',
                hovertemplate='<b>%{label}</b><br>Revenue: $%{value:.1f}B<extra></extra>')
            fig.update_layout(**PL, height=330,
                title=dict(text=f"Revenue Treemap {t_yr}", font=dict(size=13, color='#334155')),
                coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        emp_sl, e_yr = get_latest_slice(ann_df, sel_companies)
        emp_sl = emp_sl.copy()
        emp_sl['RevPerEmp'] = (emp_sl.Revenue_B * 1e9 / (emp_sl.Employees_K * 1e3) / 1e6).round(2)
        emp_sl = emp_sl.sort_values('RevPerEmp')
        fig = go.Figure(go.Bar(
            x=emp_sl.RevPerEmp, y=emp_sl.Company, orientation='h',
            marker=dict(color=[COLORS[c] for c in emp_sl.Company], line=dict(width=0)),
            text=[f"${v:.2f}M" for v in emp_sl.RevPerEmp], textposition='outside',
            hovertemplate='<b>%{y}</b><br>$%{x:.2f}M per employee<extra></extra>'))
        sf(fig, 330, legend=False).update_layout(
            title=dict(text=f"Revenue per Employee {e_yr} ($M)", font=dict(size=13, color='#334155')),
            xaxis_title="$M per Employee")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════
# PAGE 2 — STOCK PERFORMANCE
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_SP:
    st.markdown('<p class="page-title">📈 Stock Performance</p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 Price History", "📉 Volatility & Risk", "🎯 Return Analysis"])

    with tab1:
        co1 = st.selectbox("Company", sel_companies, key='sp1')
        sub = p_f[p_f.Company == co1].sort_values('Date').copy()
        sub['MA50']  = sub.Price.rolling(50).mean()
        sub['MA200'] = sub.Price.rolling(200).mean()
        sub['Upper'] = sub.Price.rolling(20).mean() + 2 * sub.Price.rolling(20).std()
        sub['Lower'] = sub.Price.rolling(20).mean() - 2 * sub.Price.rolling(20).std()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.Upper, name='BB Upper',
            line=dict(color='rgba(79,70,229,0.15)', width=1, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.Lower, name='BB Lower', fill='tonexty',
            fillcolor='rgba(79,70,229,0.05)',
            line=dict(color='rgba(79,70,229,0.15)', width=1, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.Price, name='Price',
            line=dict(color=COLORS[co1], width=2.5),
            hovertemplate='<b>'+co1+'</b><br>%{x|%b %d, %Y}<br>$%{y:.2f}<extra></extra>'))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.MA50, name='MA50',
            line=dict(color='#f59e0b', width=1.5, dash='dot')))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.MA200, name='MA200',
            line=dict(color='#8b5cf6', width=1.5, dash='dash')))
        sf(fig, 420).update_layout(
            title=dict(text=f"{co1} — Price + Bollinger Bands + MAs", font=dict(size=13, color='#334155')),
            yaxis_title="Price (USD)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        fig2 = go.Figure(go.Bar(x=sub.Date, y=sub.Volume_M,
            marker_color=COLORS[co1], opacity=0.35, name='Volume'))
        sf(fig2, 120, legend=False).update_layout(yaxis_title="Volume (M)", margin=dict(t=10))
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab2:
        fig = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f.Company == co].sort_values('Date')
            if sub.empty: continue
            vol = sub.Daily_Return.rolling(30).std()
            fig.add_trace(go.Scatter(x=sub.Date, y=vol, name=co, mode='lines',
                line=dict(color=COLORS[co], width=1.8),
                hovertemplate=f'<b>{co}</b> %{{x|%b %Y}}<br>Vol: %{{y:.2f}}%<extra></extra>'))
        sf(fig, 340).update_layout(
            title=dict(text="30-Day Rolling Volatility", font=dict(size=13, color='#334155')),
            yaxis_title="Volatility (%)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        stats = p_f.groupby('Company').agg(
            Avg_Return=('Daily_Return','mean'), Volatility=('Daily_Return','std')).reset_index()
        total_ret = (p_f.groupby('Company')
            .apply(lambda g: (g.sort_values('Date').Price.iloc[-1] /
                              g.sort_values('Date').Price.iloc[0] - 1) * 100)
            .reset_index(name='Total_Return_Pct'))
        stats = stats.merge(total_ret, on='Company')
        fig2 = go.Figure()
        for _, row in stats.iterrows():
            fig2.add_trace(go.Scatter(
                x=[row.Volatility], y=[row.Total_Return_Pct], mode='markers+text',
                name=row.Company, text=[row.Company], textposition='top center',
                textfont=dict(size=10, color=COLORS[row.Company]),
                marker=dict(size=20, color=COLORS[row.Company],
                            line=dict(width=2, color='rgba(255,255,255,0.8)')),
                hovertemplate=f'<b>{row.Company}</b><br>Vol:{row.Volatility:.2f}%<br>Return:{row.Total_Return_Pct:.0f}%<extra></extra>'))
        fig2.add_hline(y=0, line_dash='dot', line_color='rgba(0,0,0,0.08)')
        fig2.add_vline(x=stats.Volatility.mean(), line_dash='dot', line_color='rgba(0,0,0,0.08)')
        sf(fig2, 340).update_layout(
            title=dict(text="Risk vs Total Return", font=dict(size=13, color='#334155')),
            xaxis_title="Daily Volatility (Std Dev %)", yaxis_title="Total Return %", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        p_f2 = p_f.copy(); p_f2['Year'] = p_f2.Date.dt.year
        annual_ret = (p_f2.groupby(['Company','Year'])
            .apply(lambda g: (g.sort_values('Date').Price.iloc[-1] /
                              g.sort_values('Date').Price.iloc[0] - 1) * 100)
            .reset_index(name='Annual_Return'))
        pivot = annual_ret.pivot(index='Company', columns='Year', values='Annual_Return')
        fig = go.Figure(go.Heatmap(
            z=pivot.values, x=[str(c) for c in pivot.columns], y=list(pivot.index),
            colorscale=[[0,'#ef4444'],[0.45,'#f8fafc'],[1,'#10b981']], zmid=0,
            text=[[f"{v:.0f}%" if not np.isnan(v) else "" for v in row] for row in pivot.values],
            texttemplate='%{text}', textfont=dict(size=11, color='#334155'),
            hovertemplate='<b>%{y}</b> %{x}<br>Return: %{z:.1f}%<extra></extra>'))
        sf(fig, 360, legend=False).update_layout(
            title=dict(text="Annual Stock Return %", font=dict(size=13, color='#334155')))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        fig2 = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f.Company == co]
            if sub.empty: continue
            fig2.add_trace(go.Violin(
                x=[co]*len(sub), y=sub.Daily_Return, name=co,
                box_visible=True, meanline_visible=True,
                fillcolor=hex_to_rgba(COLORS[co], 0.2),
                line_color=COLORS[co], opacity=0.85,
                hovertemplate=f'<b>{co}</b><br>%{{y:.3f}}%<extra></extra>'))
        sf(fig2, 340).update_layout(
            title=dict(text="Daily Return Distribution", font=dict(size=13, color='#334155')),
            yaxis_title="Daily Return %")
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════
# PAGE 3 — REVENUE & EARNINGS
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_RE:
    st.markdown('<p class="page-title">💰 Revenue &amp; Earnings</p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 Quarterly Deep-Dive", "📈 Growth Trends", "💎 Profitability"])

    with tab1:
        co2 = st.selectbox("Company", sel_companies, key='re1')
        sub = q_f[q_f.Company == co2].sort_values('Quarter').copy()
        sub['YoY'] = sub.Revenue_B.pct_change(4) * 100
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
            row_heights=[0.65, 0.35], vertical_spacing=0.08)
        fig.add_trace(go.Bar(x=sub.Quarter, y=sub.Revenue_B, name='Revenue ($B)',
            marker_color=COLORS[co2], opacity=0.85,
            hovertemplate='%{x|%b %Y}<br>$%{y:.1f}B<extra></extra>'), row=1, col=1)
        fig.add_trace(go.Scatter(x=sub.Quarter, y=sub.Revenue_B.rolling(4).mean(), name='4Q Avg',
            line=dict(color='#f59e0b', width=2, dash='dot')), row=1, col=1)
        fig.add_trace(go.Bar(x=sub.Quarter, y=sub.YoY, name='YoY %',
            marker_color=['#10b981' if v >= 0 else '#ef4444' for v in sub.YoY.fillna(0)],
            hovertemplate='%{x|%b %Y}<br>YoY: %{y:.1f}%<extra></extra>'), row=2, col=1)
        sf(fig, 440).update_layout(
            title=dict(text=f"{co2} — Quarterly Revenue + YoY Growth", font=dict(size=13, color='#334155')))
        fig.update_yaxes(title_text="Revenue ($B)", row=1, col=1)
        fig.update_yaxes(title_text="YoY %", row=2, col=1)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with tab2:
        yr_min, yr_max = int(ann_df.Year.min()), COMMON_LATEST_YEAR
        cagr_rows = []
        for co in sel_companies:
            sub = ann_df[(ann_df.Company==co) & ann_df.Year.isin([yr_min,yr_max])].sort_values('Year')
            if len(sub) == 2:
                r0, r1 = sub.Revenue_B.iloc[0], sub.Revenue_B.iloc[1]
                n = yr_max - yr_min
                cagr_rows.append({'Company': co, 'CAGR': round(((r1/r0)**(1/n)-1)*100 if n>0 else 0, 1)})
        cagr_df = pd.DataFrame(cagr_rows).sort_values('CAGR')
        c1, c2 = st.columns(2)
        with c1:
            if not cagr_df.empty:
                fig = go.Figure(go.Bar(
                    x=cagr_df.CAGR, y=cagr_df.Company, orientation='h',
                    marker=dict(color=[COLORS[c] for c in cagr_df.Company], line=dict(width=0)),
                    text=[f"{v:.1f}%" for v in cagr_df.CAGR], textposition='outside',
                    hovertemplate='<b>%{y}</b><br>CAGR: %{x:.1f}%<extra></extra>'))
                sf(fig, 340, legend=False).update_layout(
                    title=dict(text=f"Revenue CAGR {yr_min}–{yr_max}", font=dict(size=13, color='#334155')),
                    xaxis_title="CAGR %")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with c2:
            rev_pivot = ann_f.pivot(index='Year', columns='Company', values='Revenue_B').fillna(0)
            fig = go.Figure()
            for co in [c for c in sel_companies if c in rev_pivot.columns]:
                fig.add_trace(go.Scatter(x=rev_pivot.index, y=rev_pivot[co], name=co, mode='lines+markers',
                    line=dict(color=COLORS[co], width=2.5),
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:.1f}}B<extra></extra>'))
            sf(fig, 340).update_layout(
                title=dict(text="Annual Revenue Trend ($B)", font=dict(size=13, color='#334155')),
                yaxis_title="Revenue ($B)")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        prof_sl, p_yr = get_latest_slice(ann_df, sel_companies)
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            for co in sel_companies:
                sub = ann_f[ann_f.Company==co].sort_values('Year')
                if sub.empty: continue
                fig.add_trace(go.Scatter(x=sub.Year, y=(sub.NetIncome_B/sub.Revenue_B*100),
                    name=co, mode='lines+markers', line=dict(color=COLORS[co], width=2),
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>%{{y:.1f}}%<extra></extra>'))
            sf(fig, 340).update_layout(
                title=dict(text="Net Margin Trend (%)", font=dict(size=13, color='#334155')),
                yaxis_title="Net Margin %")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with c2:
            if not prof_sl.empty:
                fig = go.Figure(go.Scatter(
                    x=prof_sl.Revenue_B, y=prof_sl.NetIncome_B,
                    mode='markers+text', text=prof_sl.Company, textposition='top center',
                    marker=dict(size=prof_sl.MarketCap_B/50,
                        color=[COLORS[c] for c in prof_sl.Company],
                        line=dict(width=2, color='white')),
                    hovertemplate='<b>%{text}</b><br>Rev: $%{x:.1f}B<br>NI: $%{y:.1f}B<extra></extra>'))
                sf(fig, 340, legend=False).update_layout(
                    title=dict(text=f"Revenue vs Net Income {p_yr}", font=dict(size=13, color='#334155')),
                    xaxis_title="Revenue ($B)", yaxis_title="Net Income ($B)")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════
# PAGE 4 — COMPETITIVE ANALYSIS
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_CA:
    st.markdown('<p class="page-title">🏆 Competitive Analysis</p>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📊 Benchmarks", "🕸 Radar Chart"])

    with tab1:
        latest_sl, l_yr = get_latest_slice(ann_df, sel_companies)
        metrics = ['Revenue_B','NetIncome_B','MarketCap_B','Employees_K']
        metric_labels = ['Revenue ($B)','Net Income ($B)','Market Cap ($B)','Employees (K)']
        for metric, label in zip(metrics, metric_labels):
            if metric not in latest_sl.columns: continue
            srt = latest_sl[['Company',metric]].dropna().sort_values(metric, ascending=False)
            fig = go.Figure(go.Bar(
                x=srt.Company, y=srt[metric],
                marker_color=[COLORS[c] for c in srt.Company],
                text=[f"{v:.1f}" for v in srt[metric]], textposition='outside',
                hovertemplate=f'<b>%{{x}}</b><br>{label}: %{{y:.1f}}<extra></extra>'))
            sf(fig, 260, legend=False).update_layout(
                title=dict(text=f"{label} — {l_yr}", font=dict(size=13, color='#334155')),
                yaxis_title=label)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with tab2:
        radar_sl, r_yr = get_latest_slice(ann_df, sel_companies)
        radar_metrics = ['Revenue_B','NetIncome_B','MarketCap_B']
        if all(m in radar_sl.columns for m in radar_metrics):
            norm = radar_sl.copy()
            for m in radar_metrics:
                mn, mx = norm[m].min(), norm[m].max()
                norm[m] = (norm[m] - mn) / (mx - mn + 1e-9) * 100
            categories = ['Revenue','Net Income','Market Cap','Revenue']
            fig = go.Figure()
            for co in sel_companies:
                row = norm[norm.Company == co]
                if row.empty: continue
                vals = [row.Revenue_B.values[0], row.NetIncome_B.values[0],
                        row.MarketCap_B.values[0], row.Revenue_B.values[0]]
                fig.add_trace(go.Scatterpolar(
                    r=vals, theta=categories, name=co, fill='toself',
                    line=dict(color=COLORS[co], width=2),
                    fillcolor=hex_to_rgba(COLORS[co], 0.08)))
            sf(fig, 420).update_layout(
                title=dict(text=f"Competitive Radar {r_yr}", font=dict(size=13, color='#334155')),
                polar=dict(radialaxis=dict(visible=True, range=[0,100],
                    gridcolor='rgba(0,0,0,0.06)'), bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════
# PAGE 5 — DEEP ANALYTICS
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_DA:
    st.markdown('<p class="page-title">🔬 Deep Analytics</p>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📈 Correlation Matrix", "📊 Regression"])

    with tab1:
        if not ann_f.empty:
            pivot_rev = ann_f.pivot(index='Year', columns='Company', values='Revenue_B').ffill()
            corr = pivot_rev.corr()
            fig = go.Figure(go.Heatmap(
                z=corr.values, x=list(corr.columns), y=list(corr.index),
                colorscale=[[0,'#ef4444'],[0.5,'#f8fafc'],[1,'#10b981']],
                zmid=0, zmin=-1, zmax=1,
                text=[[f"{v:.2f}" for v in row] for row in corr.values],
                texttemplate='%{text}', textfont=dict(size=10),
                hovertemplate='%{y} × %{x}<br>r = %{z:.2f}<extra></extra>'))
            sf(fig, 420, legend=False).update_layout(
                title=dict(text="Revenue Correlation Matrix", font=dict(size=13, color='#334155')))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Not enough data for correlation.")

    with tab2:
        co_reg = st.selectbox("Company", sel_companies, key='reg1')
        sub = ann_f[ann_f.Company==co_reg].sort_values('Year').dropna(subset=['Revenue_B'])
        if len(sub) >= 3:
            slope, intercept, r, p_val, se = scipy_stats.linregress(sub.Year, sub.Revenue_B)
            y_pred = intercept + slope * sub.Year
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=sub.Year, y=sub.Revenue_B, name='Actual',
                mode='markers', marker=dict(size=10, color=COLORS[co_reg])))
            fig.add_trace(go.Scatter(x=sub.Year, y=y_pred, name=f'Trend (r²={r**2:.2f})',
                mode='lines', line=dict(color='#f59e0b', width=2, dash='dot')))
            sf(fig, 380).update_layout(
                title=dict(text=f"{co_reg} Revenue Regression (slope={slope:.1f}B/yr)",
                    font=dict(size=13, color='#334155')),
                xaxis_title="Year", yaxis_title="Revenue ($B)")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Need at least 3 years of data for regression.")


# ════════════════════════════════════════════════════════════════════
# PAGE 6 — AI INSIGHT ENGINE
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_AI:
    st.markdown('<p class="page-title">🤖 AI Insight Engine</p>', unsafe_allow_html=True)
    latest_sl, l_yr = get_latest_slice(ann_df, sel_companies)

    def make_insight(title, body, color="var(--primary)"):
        st.markdown(
            f'<div class="insight-card" style="border-left-color:{color};">'
            f'<div class="insight-title">{title}</div>'
            f'<div class="insight-body">{body}</div></div>',
            unsafe_allow_html=True)

    sec("Automated Market Intelligence", f"FY {l_yr}")
    if not latest_sl.empty:
        top_rev    = latest_sl.loc[latest_sl.Revenue_B.idxmax()]
        top_mc     = latest_sl.loc[latest_sl.MarketCap_B.idxmax()]
        latest_sl['Margin'] = latest_sl.NetIncome_B / latest_sl.Revenue_B * 100
        top_margin = latest_sl.loc[latest_sl.Margin.idxmax()]
        lowest_m   = latest_sl.loc[latest_sl.Margin.idxmin()]
        make_insight(f"👑 Revenue Leader: {top_rev.Company}",
            f"{top_rev.Company} leads with <b>${top_rev.Revenue_B:.1f}B</b> in revenue for {l_yr}.", "#4f46e5")
        make_insight(f"🏆 Market Cap Champion: {top_mc.Company}",
            f"{top_mc.Company} commands the highest market cap at <b>${top_mc.MarketCap_B:,.0f}B</b>.", "#06b6d4")
        make_insight(f"💎 Profitability Star: {top_margin.Company}",
            f"{top_margin.Company} achieves the highest net margin at <b>{top_margin.Margin:.1f}%</b>.", "#10b981")
        make_insight(f"⚠️ Margin Watch: {lowest_m.Company}",
            f"{lowest_m.Company} carries the lowest net margin at <b>{lowest_m.Margin:.1f}%</b>.", "#f97316")

    nvda = ann_f[ann_f.Company=='NVIDIA'].sort_values('Year')
    if len(nvda) >= 2:
        rev_growth = (nvda.Revenue_B.iloc[-1]/nvda.Revenue_B.iloc[-2]-1)*100 if nvda.Revenue_B.iloc[-2]>0 else 0
        make_insight("⚡ NVIDIA AI Boom",
            f"NVIDIA's revenue grew <b>{rev_growth:.0f}%</b> YoY. FY{l_yr} revenue: <b>${nvda.Revenue_B.iloc[-1]:.1f}B</b>.",
            "#76b900")

    sec("Data Table", f"FY {l_yr}")
    if not latest_sl.empty:
        dcols = [c for c in ['Company','Revenue_B','NetIncome_B','MarketCap_B','Employees_K']
                 if c in latest_sl.columns]
        st.dataframe(latest_sl[dcols].set_index('Company').style.format("{:.1f}"),
                     use_container_width=True)


# ════════════════════════════════════════════════════════════════════
# PAGE 7 — LIVE DASHBOARD
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_LD:
    st.markdown('<p class="page-title">📡 Live Dashboard</p>', unsafe_allow_html=True)

    if _autorefresh_ok:
        st_autorefresh(interval=60000, key="live_refresh")

    if not _live_ok:
        st.warning("⚠️ `live_data.py` not found. Install yfinance and create live_data.py to enable live prices.")
    else:
        sec("Live Prices", datetime.now().strftime("%H:%M:%S"))
        try:
            live_prices = get_multi_live_prices()
        except Exception:
            live_prices = {}

        if live_prices:
            cols = st.columns(4)
            for i, (company, info) in enumerate(live_prices.items()):
                price  = info.get('price', 0)
                change = info.get('change_pct', 0)
                badge  = 'up' if change >= 0 else 'down'
                arrow  = '↑' if change >= 0 else '↓'
                stripe = 'green' if change >= 0 else ''
                with cols[i % 4]:
                    st.markdown(
                        f'<div class="kpi"><div class="kpi-stripe {stripe}"></div>'
                        f'<div class="kpi-label">{company}</div>'
                        f'<div class="kpi-val" style="font-size:1.6rem;">${price:,.2f}</div>'
                        f'<div class="kpi-sub">Today</div>'
                        f'<div class="kpi-badge {badge}">{arrow} {abs(change):.2f}%</div></div>',
                        unsafe_allow_html=True)
        else:
            st.info("Live price feed unavailable. Check your internet connection or yfinance quota.")

        sec("Intraday Charts", "TODAY")
        intraday_co = st.selectbox("Select Company", sel_companies, key='ld1')
        try:
            intraday_df = get_intraday_data(intraday_co)
            if intraday_df is not None and not intraday_df.empty:
                color = COLORS.get(intraday_co, '#4f46e5')
                fig = go.Figure()
                x_vals = (intraday_df.index if intraday_df.index.name == 'Datetime'
                          else intraday_df.get('Datetime', intraday_df.index))
                y_vals = (intraday_df['Close'] if 'Close' in intraday_df.columns
                          else intraday_df.iloc[:, 0])
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name=intraday_co, mode='lines',
                    line=dict(color=color, width=2),
                    fill='tozeroy', fillcolor=hex_to_rgba(color, 0.07),
                    hovertemplate='%{x}<br>$%{y:.2f}<extra></extra>'))
                sf(fig, 340, legend=False).update_layout(
                    title=dict(text=f"{intraday_co} — Intraday Price",
                        font=dict(size=13, color='#334155')),
                    yaxis_title="Price (USD)")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info(f"No intraday data available for {intraday_co} right now.")
        except Exception as e:
            st.warning(f"Could not load intraday data for {intraday_co}: {e}")

        if not fund_df.empty:
            sec("Live Fundamentals", "yfinance TTM")
            disp = fund_df[fund_df.Company.isin(sel_companies)].copy()
            dcols = [c for c in ['Company','marketCap_B','revenue_B','netIncome_B',
                                  'peRatio','eps','dividendYield'] if c in disp.columns]
            st.dataframe(disp[dcols].set_index('Company'), use_container_width=True)
