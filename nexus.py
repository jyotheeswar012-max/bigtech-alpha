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

/* ══ DARK THEME VARIABLES (main content only) ══ */
:root{
  --bg:#0f1117;
  --white:#1a1d27;
  --surface:#13161f;
  --primary:#818cf8;
  --accent:#22d3ee;
  --orange:#fb923c;
  --green:#34d399;
  --red:#f87171;
  --purple:#a78bfa;
  --pink:#f472b6;
  --yellow:#fbbf24;
  --txt:#e2e8f0;
  --txt2:#94a3b8;
  --txt3:#64748b;
  --txt4:#334155;
  --border:rgba(129,140,248,0.15);
  --border2:rgba(129,140,248,0.28);
  --shadow:0 4px 16px rgba(0,0,0,0.4);
  --shadow-lg:0 12px 40px rgba(0,0,0,0.5);
  --shadow-xl:0 24px 60px rgba(0,0,0,0.6);
  --radius:16px;--radius-xl:32px;
}

*{box-sizing:border-box;}

.stApp{background:var(--bg)!important;font-family:'Inter',sans-serif;color:var(--txt);}
.main .block-container{
  background:var(--bg)!important;
  padding:1.4rem 2.2rem!important;
  max-width:100%!important;
}
.main{background:var(--bg)!important;}
[data-testid="stAppViewContainer"]>section.main{background:var(--bg)!important;}

.stTabs [data-baseweb="tab-list"]{
  gap:0.35rem;background:transparent;
  border-bottom:2px solid var(--border);
}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;border:none!important;
  border-bottom:3px solid transparent!important;border-radius:0!important;
  color:var(--txt3)!important;font-size:0.85rem;font-weight:600;
  padding:0.7rem 1.3rem!important;transition:all 0.2s;
}
.stTabs [data-baseweb="tab"]:hover{color:var(--primary)!important;}
.stTabs [aria-selected="true"]{
  color:var(--primary)!important;
  border-bottom-color:var(--primary)!important;
  background:transparent!important;
}

.main .stSelectbox>div>div{
  background:var(--white)!important;
  border:1px solid var(--border)!important;
  border-radius:12px!important;
  color:var(--txt)!important;
}
.main .stSelectbox label, .main .stMultiSelect label,
.main .stSlider label{color:var(--txt2)!important;}

[data-testid="stMetric"]{
  background:var(--white)!important;
  border:1px solid var(--border)!important;
  border-radius:14px;padding:1.1rem 1.3rem;
}
[data-testid="stMetricValue"]{
  font-family:'Outfit',sans-serif!important;
  color:var(--primary)!important;font-weight:700;
}
[data-testid="stMetricLabel"]{color:var(--txt2)!important;}

.main [data-testid="stDataFrame"]{
  background:var(--white)!important;
  border:1px solid var(--border)!important;
  border-radius:12px!important;
}

.main .stInfo, .main .stWarning{background:var(--surface)!important;border-color:var(--border)!important;color:var(--txt)!important;}

#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}

[data-testid="collapsedControl"]{display:none!important;}
[data-testid="stSidebarCollapseButton"]{display:none!important;}
button[aria-label="Close sidebar"]{display:none!important;}
button[aria-label="Collapse sidebar"]{display:none!important;}
section[data-testid="stSidebar"]{
  min-width:240px!important;
  max-width:280px!important;
  transform:none!important;
  visibility:visible!important;
  display:block!important;
}

[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#4f46e5 0%,#6366f1 40%,#818cf8 100%)!important;
  border-right:none!important;
  box-shadow:4px 0 24px rgba(79,70,229,0.15);
}
[data-testid="stSidebar"] *{color:#fff!important;}
[data-testid="stSidebar"] .stSelectbox>div>div,
[data-testid="stSidebar"] .stMultiSelect>div>div{
  background:rgba(255,255,255,0.15)!important;
  border:1px solid rgba(255,255,255,0.25)!important;
  border-radius:12px!important;color:#fff!important;
}
[data-testid="stSidebar"] .stButton>button{
  width:100%!important;
  background:rgba(255,255,255,0.10)!important;
  border:1px solid rgba(255,255,255,0.18)!important;
  border-radius:12px!important;
  color:#fff!important;
  font-size:0.82rem!important;
  font-weight:500!important;
  padding:0.55rem 1rem!important;
  text-align:left!important;
  margin-bottom:0.25rem!important;
  transition:all 0.2s!important;
}
[data-testid="stSidebar"] .stButton>button:hover{
  background:rgba(255,255,255,0.22)!important;
  border-color:rgba(255,255,255,0.4)!important;
  transform:translateX(4px)!important;
}
[data-testid="stSidebar"] .stButton>button[kind="primary"]{
  background:rgba(255,255,255,0.30)!important;
  border-color:rgba(255,255,255,0.6)!important;
  font-weight:700!important;
  box-shadow:0 2px 12px rgba(0,0,0,0.15)!important;
}

.hero{
  position:relative;overflow:hidden;
  background:linear-gradient(135deg,#312e81 0%,#4c1d95 30%,#0e7490 70%,#065f46 100%);
  border-radius:var(--radius-xl);padding:3.2rem 3.8rem 3rem;margin-bottom:2rem;
  box-shadow:var(--shadow-xl);color:#fff;
}
.hero-title{font-family:'Outfit',sans-serif;font-size:4.5rem;font-weight:900;line-height:1.0;letter-spacing:-0.035em;margin:0 0 0.8rem 0;}
.hero-sub{font-size:1.05rem;line-height:1.7;max-width:620px;opacity:0.9;}
.hero-chips{display:flex;gap:0.6rem;flex-wrap:wrap;margin-top:1.6rem;}
.chip{display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.22);color:#fff!important;font-size:0.65rem;font-weight:500;padding:0.4rem 1rem;border-radius:100px;}

.ticker-wrap{
  overflow:hidden;
  background:var(--white);
  border:1px solid var(--border);
  border-radius:100px;padding:0.55rem 0;margin-bottom:1.8rem;white-space:nowrap;
}
.ticker-inner{display:inline-block;animation:ticker-scroll 35s linear infinite;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:var(--txt3);}
.ticker-inner span.sym{color:var(--primary);font-weight:700;margin:0 0.25rem;}
@keyframes ticker-scroll{0%{transform:translateX(0);}100%{transform:translateX(-50%);}}

.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem;margin-bottom:2rem;}
.kpi{
  background:var(--white);
  border:1px solid var(--border);
  border-radius:var(--radius);padding:1.6rem 1.8rem 1.5rem;
  position:relative;overflow:hidden;
  box-shadow:var(--shadow);transition:all 0.3s;
}
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
.kpi-icon{position:absolute;right:1.5rem;bottom:1.3rem;font-size:2.5rem;opacity:0.06;}
.kpi-badge{position:absolute;top:1.1rem;right:1rem;font-size:0.58rem;padding:0.22rem 0.7rem;border-radius:100px;font-weight:700;}
.up{background:rgba(52,211,153,0.15);color:var(--green)!important;border:1px solid rgba(52,211,153,0.3);}
.down{background:rgba(248,113,113,0.12);color:var(--red)!important;border:1px solid rgba(248,113,113,0.25);}
.flat{background:rgba(251,191,36,0.12);color:var(--yellow)!important;border:1px solid rgba(251,191,36,0.25);}

.sec{display:flex;align-items:center;gap:1rem;margin:2.5rem 0 1.4rem 0;}
.sec-title{font-family:'Outfit',sans-serif;font-size:0.9rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--txt);}
.sec-line{flex:1;height:1px;background:linear-gradient(90deg,var(--border2),transparent);}
.sec-tag{font-size:0.58rem;color:#fff!important;background:linear-gradient(135deg,var(--primary),var(--accent));padding:0.28rem 0.8rem;border-radius:100px;font-weight:600;}

.page-title{
  font-family:'Outfit',sans-serif;font-size:2.5rem;font-weight:800;letter-spacing:-0.03em;
  background:linear-gradient(135deg,var(--primary) 0%,var(--accent) 60%,var(--green) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;margin-bottom:1.6rem;
}

.insight-card{
  background:var(--white);border:1px solid var(--border);
  border-radius:var(--radius);padding:1.5rem 2rem;margin-bottom:1rem;
  border-left:4px solid var(--primary);box-shadow:var(--shadow);transition:all 0.25s;
}
.insight-card:hover{transform:translateX(6px);box-shadow:var(--shadow-lg);}
.insight-title{font-family:'Outfit',sans-serif;font-size:0.95rem;font-weight:700;color:var(--txt);margin-bottom:0.5rem;}
.insight-body{font-size:0.88rem;color:var(--txt2);line-height:1.8;}

.live{display:inline-block;width:8px;height:8px;background:#34d399;border-radius:50%;margin-right:6px;vertical-align:middle;animation:pulse-ring 2s ease infinite;}
@keyframes pulse-ring{0%{box-shadow:0 0 0 0 rgba(52,211,153,0.5);}70%{box-shadow:0 0 0 8px rgba(52,211,153,0);}100%{box-shadow:0 0 0 0 rgba(52,211,153,0);}}

.logo-wrap{padding:1.6rem 0 1.2rem;}
.logo-text{font-family:'Outfit',sans-serif;font-size:1.6rem;font-weight:900;color:#fff!important;}
.logo-sub{font-size:0.55rem;color:rgba(255,255,255,0.55)!important;letter-spacing:0.16em;margin-top:0.25rem;}
.h-divider{height:1px;background:rgba(255,255,255,0.15);margin:0.8rem 0;}

::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--txt4);border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY DARK LAYOUT DEFAULTS ──────────────────────────────────────────────
PL = dict(
    paper_bgcolor="#1a1d27",
    plot_bgcolor="#13161f",
    font=dict(family="Inter", color="#94a3b8", size=11),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)", color="#64748b"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)", color="#64748b"),
    margin=dict(l=10, r=10, t=44, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=1,
                font=dict(size=10, color="#94a3b8"), orientation='h', y=1.12),
)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
COLORS = {
    'Apple': '#e2e8f0', 'Microsoft': '#60a5fa', 'Google': '#f87171',
    'Amazon': '#fbbf24', 'Meta': '#60a5fa', 'NVIDIA': '#86efac',
    'Tesla': '#f87171', 'Netflix': '#f87171',
}
ALL_COMPANIES = list(COLORS.keys())

PAGE_NAMES = [
    "🏠  Command Center",
    "📈  Stock Performance",
    "💰  Revenue & Earnings",
    "🏆  Competitive Analysis",
    "🔬  Deep Analytics",
    "🤖  AI Insight Engine",
    "📡  Live Dashboard",
]
PAGE_CC = 0
PAGE_SP = 1
PAGE_RE = 2
PAGE_CA = 3
PAGE_DA = 4
PAGE_AI = 5
PAGE_LD = 6

if "page_idx" not in st.session_state:
    st.session_state.page_idx = 0


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


def nav_to(idx):
    st.session_state.page_idx = idx


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

    ann_df = merge_with_csv(live_ann, ann_csv, ['Company','Year']) if (_live_ok and not live_ann.empty) else ann_csv.copy()

    if _live_ok and not live_q.empty:
        lq = live_q.copy(); lq['Quarter'] = pd.to_datetime(lq['Quarter'])
        cq = q_csv.copy();  cq['Quarter'] = pd.to_datetime(cq['Quarter'])
        q_df = merge_with_csv(lq, cq, ['Company','Quarter'])
    else:
        q_df = q_csv.copy()

    if _live_ok and not live_p.empty:
        lp = live_p.copy(); lp['Date'] = pd.to_datetime(lp['Date'])
        cp = price_csv.copy(); cp['Date'] = pd.to_datetime(cp['Date'])
        price_df = merge_with_csv(lp, cp, ['Company','Date'])
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


# ── SIDEBAR ── Logo → Nav → Companies → Year Range → Footer ───────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <div style="font-size:2rem;margin-bottom:0.35rem;">🚀</div>
      <div class="logo-text">MARKET NEXUS</div>
      <div class="logo-sub">BIG TECH INTELLIGENCE · v6.0</div>
    </div>
    <div class="h-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.6rem;letter-spacing:0.12em;text-transform:uppercase;opacity:0.6;margin-bottom:0.5rem;'>Navigation</div>", unsafe_allow_html=True)
    for i, label in enumerate(PAGE_NAMES):
        is_active = (st.session_state.page_idx == i)
        if st.button(label, key=f"nav_{i}", type="primary" if is_active else "secondary"):
            nav_to(i)
            st.rerun()

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.6rem;letter-spacing:0.12em;text-transform:uppercase;opacity:0.6;margin-bottom:0.5rem;'>Filter Companies</div>", unsafe_allow_html=True)
    sel_companies = st.multiselect("Companies", ALL_COMPANIES, default=ALL_COMPANIES, label_visibility="collapsed")
    if not sel_companies:
        sel_companies = ALL_COMPANIES

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.6rem;letter-spacing:0.12em;text-transform:uppercase;opacity:0.6;margin-bottom:0.5rem;'>Year Range</div>", unsafe_allow_html=True)
    slider_min = int(ann_df['Year'].min()) if not ann_df.empty else 2020
    slider_max = COMMON_LATEST_YEAR
    year_range = st.slider("Year Range", slider_min, slider_max, (slider_min, slider_max), label_visibility="collapsed")

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

page_idx = st.session_state.page_idx

# ── FILTERED DATA ─────────────────────────────────────────────────────────────
ann_f = ann_df[(ann_df.Company.isin(sel_companies)) & (ann_df.Year.between(*year_range))]
q_f   = q_df[(q_df.Company.isin(sel_companies)) & (q_df.Quarter.dt.year.between(*year_range))]
p_f   = price_df[(price_df.Company.isin(sel_companies)) & (price_df.Date.dt.year.between(*year_range))]


def get_latest_slice(df, companies, fallback_year=None):
    sub = df[df.Company.isin(companies)]
    yr  = best_common_year(sub, companies) if fallback_year is None else fallback_year
    return sub[sub.Year == yr].copy(), yr


# ── TICKER TAPE ───────────────────────────────────────────────────────────────
ticker_syms = ["AAPL","MSFT","GOOGL","AMZN","META","NVDA","TSLA","NFLX"]
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
            title=dict(text="Quarterly Revenue ($B)", font=dict(size=13, color='#94a3b8')),
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
            title=dict(text="Market Cap by Year ($B)", font=dict(size=13, color='#94a3b8')),
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
        fig.add_hline(y=100, line_dash='dot', line_color='rgba(255,255,255,0.1)')
        sf(fig, 340).update_layout(
            title=dict(text="Normalised Stock Performance (Base=100)", font=dict(size=13, color='#94a3b8')),
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
                colorscale=[[0,'#f87171'],[0.4,'#fb923c'],[1,'#34d399']], line=dict(width=0)),
            text=[f"{v:.1f}%" for v in margin_sl.Margin], textposition='outside',
            hovertemplate='<b>%{y}</b><br>Margin: %{x:.1f}%<extra></extra>'))
        sf(fig, 340, legend=False).update_layout(
            title=dict(text=f"Net Profit Margin {m_yr}", font=dict(size=13, color='#94a3b8')),
            xaxis_title="Net Margin %")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    sec("Revenue Distribution & Headcount", "STRUCTURAL VIEW")
    c1, c2 = st.columns(2)
    with c1:
        treemap_sl, t_yr = get_latest_slice(ann_df, sel_companies)
        if not treemap_sl.empty:
            fig = px.treemap(treemap_sl, path=['Sector','Company'], values='Revenue_B',
                color='NetIncome_B',
                color_continuous_scale=[[0,'#f87171'],[0.5,'#1e293b'],[1,'#34d399']],
                hover_data={'Revenue_B':':.1f','NetIncome_B':':.1f'})
            fig.update_traces(textfont_size=13, textfont_color='#e2e8f0',
                hovertemplate='<b>%{label}</b><br>Revenue: $%{value:.1f}B<extra></extra>')
            fig.update_layout(**PL, height=330,
                title=dict(text=f"Revenue Treemap {t_yr}", font=dict(size=13, color='#94a3b8')),
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
            title=dict(text=f"Revenue per Employee {e_yr} ($M)", font=dict(size=13, color='#94a3b8')),
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
            line=dict(color='rgba(129,140,248,0.2)', width=1, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.Lower, name='BB Lower', fill='tonexty',
            fillcolor='rgba(129,140,248,0.06)',
            line=dict(color='rgba(129,140,248,0.2)', width=1, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.Price, name='Price',
            line=dict(color=COLORS[co1], width=2.5),
            hovertemplate='<b>'+co1+'</b><br>%{x|%b %d, %Y}<br>$%{y:.2f}<extra></extra>'))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.MA50, name='MA50',
            line=dict(color='#fbbf24', width=1.5, dash='dot')))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.MA200, name='MA200',
            line=dict(color='#a78bfa', width=1.5, dash='dash')))
        sf(fig, 420).update_layout(
            title=dict(text=f"{co1} — Price + Bollinger Bands + MAs", font=dict(size=13, color='#94a3b8')),
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
            title=dict(text="30-Day Rolling Volatility", font=dict(size=13, color='#94a3b8')),
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
                            line=dict(width=2, color='rgba(255,255,255,0.15)')),
                hovertemplate=f'<b>{row.Company}</b><br>Vol:{row.Volatility:.2f}%<br>Return:{row.Total_Return_Pct:.0f}%<extra></extra>'))
        fig2.add_hline(y=0, line_dash='dot', line_color='rgba(255,255,255,0.08)')
        fig2.add_vline(x=stats.Volatility.mean(), line_dash='dot', line_color='rgba(255,255,255,0.08)')
        sf(fig2, 340).update_layout(
            title=dict(text="Risk vs Total Return", font=dict(size=13, color='#94a3b8')),
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
            colorscale=[[0,'#f87171'],[0.45,'#1e293b'],[1,'#34d399']], zmid=0,
            text=[[f"{v:.0f}%" if not np.isnan(v) else "" for v in row] for row in pivot.values],
            texttemplate='%{text}', textfont=dict(size=11, color='#e2e8f0'),
            hovertemplate='<b>%{y}</b> %{x}<br>Return: %{z:.1f}%<extra></extra>'))
        sf(fig, 360, legend=False).update_layout(
            title=dict(text="Annual Stock Return %", font=dict(size=13, color='#94a3b8')))
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
                hovertemplate=f'<b>{co}</b