"""
╔══════════════════════════════════════════════════════════════════╗
║  MARKET NEXUS — Big Tech Intelligence Platform                   ║
║  Live data: Apple · Microsoft · Google · Amazon · Meta          ║
║             NVIDIA · Tesla · Netflix                             ║
║  Run: streamlit run nexus.py                                     ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ── IMPORTS ──────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from pathlib import Path
from scipy import stats as scipy_stats

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MARKET NEXUS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── MASTER CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
  --bg:       #03060f;
  --bg-card:  #070d1c;
  --bg-glass: rgba(7,13,28,0.85);
  --surface:  #0c1528;
  --cyan:     #00e5ff;
  --orange:   #ff6d2d;
  --green:    #00ff9d;
  --purple:   #bf5af2;
  --yellow:   #ffd60a;
  --pink:     #ff375f;
  --txt:      #dde9ff;
  --txt2:     #6b80a0;
  --txt3:     #2d3f5a;
  --border:   rgba(0,229,255,0.10);
  --border2:  rgba(0,229,255,0.22);
}
.stApp { background: var(--bg) !important; font-family:'Space Grotesk',sans-serif; }
.main .block-container { padding:1.2rem 1.8rem !important; max-width:100% !important; }
*{ box-sizing:border-box; }
[data-testid="stSidebar"] {
  background:linear-gradient(175deg,#040916 0%,#060d1e 100%) !important;
  border-right:1px solid var(--border) !important;
}
.hero {
  position:relative; overflow:hidden;
  background:linear-gradient(135deg,#040916 0%,#091426 50%,#040916 100%);
  border:1px solid var(--border2); border-radius:20px;
  padding:2.8rem 3.2rem 2.4rem; margin-bottom:2rem;
}
.hero-grid {
  position:absolute; inset:0; opacity:0.04;
  background-image:linear-gradient(rgba(0,229,255,0.5) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(0,229,255,0.5) 1px,transparent 1px);
  background-size:40px 40px;
}
.hero-glow1 { position:absolute; width:500px; height:300px; border-radius:50%;
  background:radial-gradient(ellipse,rgba(0,229,255,0.08),transparent 70%); top:-80px; left:-100px; }
.hero-glow2 { position:absolute; width:400px; height:250px; border-radius:50%;
  background:radial-gradient(ellipse,rgba(255,109,45,0.06),transparent 70%); bottom:-60px; right:-80px; }
.hero-eyebrow { font-family:'JetBrains Mono',monospace; font-size:0.65rem; letter-spacing:0.18em;
  color:var(--cyan); text-transform:uppercase; margin-bottom:0.7rem; }
.hero-title { font-family:'Syne',sans-serif; font-size:3.6rem; font-weight:800; line-height:1.0;
  background:linear-gradient(110deg,#00e5ff 0%,#7dd3fc 45%,#ff6d2d 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0 0 0.6rem 0; }
.hero-sub { font-size:0.95rem; color:var(--txt2); line-height:1.6; max-width:600px; }
.hero-chips { display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:1.2rem; }
.chip { display:inline-flex; align-items:center; gap:0.4rem;
  background:rgba(0,229,255,0.07); border:1px solid rgba(0,229,255,0.2);
  color:var(--cyan) !important; font-family:'JetBrains Mono',monospace;
  font-size:0.62rem; padding:0.3rem 0.75rem; border-radius:100px; letter-spacing:0.06em; }
.chip.orange { background:rgba(255,109,45,0.07); border-color:rgba(255,109,45,0.2); color:var(--orange) !important; }
.chip.green  { background:rgba(0,255,157,0.07); border-color:rgba(0,255,157,0.2); color:var(--green)  !important; }
.kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.5rem; }
.kpi {
  background:var(--bg-card); border:1px solid var(--border); border-radius:14px;
  padding:1.4rem 1.5rem; position:relative; overflow:hidden; cursor:default;
  transition:border-color .2s, transform .2s;
}
.kpi:hover { border-color:var(--border2); transform:translateY(-2px); }
.kpi-stripe { position:absolute; inset:0 auto 0 0; width:3px;
  background:linear-gradient(180deg,var(--cyan),transparent); }
.kpi-stripe.orange { background:linear-gradient(180deg,var(--orange),transparent); }
.kpi-stripe.green  { background:linear-gradient(180deg,var(--green),transparent); }
.kpi-stripe.purple { background:linear-gradient(180deg,var(--purple),transparent); }
.kpi-label { font-size:0.65rem; text-transform:uppercase; letter-spacing:0.13em; color:var(--txt2); margin-bottom:0.45rem; }
.kpi-val { font-family:'Syne',sans-serif; font-size:2.1rem; font-weight:800; line-height:1.0; color:var(--cyan) !important; }
.kpi-val.orange { color:var(--orange) !important; }
.kpi-val.green  { color:var(--green)  !important; }
.kpi-val.purple { color:var(--purple) !important; }
.kpi-sub { font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:var(--txt3); margin-top:0.3rem; }
.kpi-icon { position:absolute; right:1.2rem; bottom:1rem; font-size:2rem; opacity:0.07; }
.kpi-badge { position:absolute; top:0.8rem; right:0.8rem;
  font-family:'JetBrains Mono',monospace; font-size:0.55rem; letter-spacing:0.08em;
  padding:0.18rem 0.5rem; border-radius:100px; }
.up   { background:rgba(0,255,157,0.12); color:var(--green)  !important; border:1px solid rgba(0,255,157,0.25); }
.down { background:rgba(255,55,95,0.12);  color:var(--pink)   !important; border:1px solid rgba(255,55,95,0.25); }
.flat { background:rgba(255,214,10,0.12); color:var(--yellow) !important; border:1px solid rgba(255,214,10,0.25); }
.sec { display:flex; align-items:center; gap:0.75rem; margin:2rem 0 1rem 0; }
.sec-title { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700;
  letter-spacing:0.06em; text-transform:uppercase; white-space:nowrap; }
.sec-line  { flex:1; height:1px; background:var(--border); }
.sec-tag   { font-family:'JetBrains Mono',monospace; font-size:0.58rem;
  color:var(--orange) !important; letter-spacing:0.1em; white-space:nowrap; }
.chart-card {
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:14px; padding:1.2rem 1.2rem 0.6rem; margin-bottom:1rem;
}
.rank-row { display:flex; align-items:center; gap:0.75rem;
  padding:0.6rem 0.8rem; border-radius:8px; margin-bottom:0.3rem;
  border:1px solid transparent; transition:border-color .15s; }
.rank-row:hover { border-color:var(--border); background:var(--surface); }
.rank-num { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:800;
  color:var(--txt3); width:1.5rem; text-align:center; }
.rank-name { font-weight:600; font-size:0.85rem; flex:1; }
.rank-val  { font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:var(--cyan); }
.stTabs [data-baseweb="tab-list"] { gap:0.4rem; background:transparent;
  border-bottom:1px solid var(--border); padding-bottom:0; }
.stTabs [data-baseweb="tab"] { background:transparent !important; border:1px solid transparent !important;
  border-radius:8px 8px 0 0 !important; color:var(--txt2) !important;
  font-family:'Space Grotesk',sans-serif; font-size:0.82rem; padding:0.55rem 1.1rem !important; }
.stTabs [aria-selected="true"] { background:var(--bg-card) !important;
  border-color:var(--border) !important; color:var(--cyan) !important; }
.live { display:inline-block; width:7px; height:7px; background:var(--green);
  border-radius:50%; margin-right:5px; vertical-align:middle;
  box-shadow:0 0 6px var(--green); animation:blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.4;} }
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--txt3);border-radius:3px;}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
  font-size:0.65rem; text-transform:uppercase; letter-spacing:0.1em; color:var(--txt3) !important; }
</style>
""", unsafe_allow_html=True)

# ── PLOTLY DEFAULTS ───────────────────────────────────────────────────────────
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Space Grotesk", color="#6b80a0", size=11),
    xaxis=dict(gridcolor="rgba(255,255,255,0.03)", zerolinecolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.03)", zerolinecolor="rgba(255,255,255,0.05)"),
    margin=dict(l=8,r=8,t=36,b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.06)",
                borderwidth=1, font=dict(size=10), orientation='h', y=1.08),
)
COLORS = {
    'Apple':    '#e8e8e8',
    'Microsoft':'#00aff0',
    'Google':   '#fbbc05',
    'Amazon':   '#ff9900',
    'Meta':     '#1877f2',
    'NVIDIA':   '#76b900',
    'Tesla':    '#cc0000',
    'Netflix':  '#e50914',
}
ALL_COMPANIES = list(COLORS.keys())

def hex_to_rgba(hex_color, alpha=0.15):
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2],16), int(hex_color[2:4],16), int(hex_color[4:6],16)
    return f'rgba({r},{g},{b},{alpha})'

def sf(fig, h=360, legend=True):
    kw = dict(**PL, height=h)
    if not legend: kw['showlegend'] = False
    fig.update_layout(**kw)
    return fig

def sec(title, tag=""):
    t = f'<div class="sec-tag">{tag}</div>' if tag else ''
    st.markdown(f'<div class="sec"><div class="sec-title">{title}</div><div class="sec-line"></div>{t}</div>',
                unsafe_allow_html=True)

# ── LIVE DATA IMPORT ──────────────────────────────────────────────────────────
try:
    from live_data import (
        get_live_price, get_intraday_data, get_multi_live_prices,
        get_all_fundamentals, get_all_price_history, get_all_quarterly,
        get_all_annual, merge_with_csv,
        COMPANIES as LIVE_COMPANIES, COMPANY_COLORS,
        NAME_TO_TICKER
    )
    _live_ok = True
except ImportError:
    _live_ok = False

try:
    from streamlit_autorefresh import st_autorefresh
    _autorefresh_ok = True
except ImportError:
    _autorefresh_ok = False

# ── CSV FALLBACK DATA LOADING ─────────────────────────────────────────────────
@st.cache_data
def load_csv():
    base = Path(__file__).parent
    q = pd.read_csv(base/"quarterly_revenue.csv", parse_dates=["Quarter"])
    a = pd.read_csv(base/"annual_metrics.csv")
    p = pd.read_csv(base/"stock_prices.csv", parse_dates=["Date"])
    return q, a, p

q_csv, ann_csv, price_csv = load_csv()

# ── LIVE DATA LOADING (cached 10 min for fundamentals, 2 min for prices) ──────
@st.cache_data(ttl=600)
def load_live_annual():
    if not _live_ok: return pd.DataFrame()
    return get_all_annual()

@st.cache_data(ttl=600)
def load_live_quarterly():
    if not _live_ok: return pd.DataFrame()
    return get_all_quarterly()

@st.cache_data(ttl=120)
def load_live_prices():
    if not _live_ok: return pd.DataFrame()
    return get_all_price_history(period="5y")

@st.cache_data(ttl=60)
def load_live_fundamentals():
    if not _live_ok: return pd.DataFrame()
    return get_all_fundamentals()

# ── SMART MERGE: live wins, CSV is fallback ───────────────────────────────────
def get_ann_df():
    live = load_live_annual()
    return merge_with_csv(live, ann_csv, ['Company','Year']) if _live_ok and not live.empty else ann_csv

def get_q_df():
    live = load_live_quarterly()
    if _live_ok and not live.empty:
        live['Quarter'] = pd.to_datetime(live['Quarter'])
        q_csv2 = q_csv.copy()
        q_csv2['Quarter'] = pd.to_datetime(q_csv2['Quarter'])
        return merge_with_csv(live, q_csv2, ['Company','Quarter'])
    return q_csv

def get_price_df():
    live = load_live_prices()
    if _live_ok and not live.empty:
        live['Date'] = pd.to_datetime(live['Date'])
        p2 = price_csv.copy()
        p2['Date'] = pd.to_datetime(p2['Date'])
        merged = merge_with_csv(live, p2, ['Company','Date'])
        return merged
    return price_csv

ann_df   = get_ann_df()
q_df     = get_q_df()
price_df = get_price_df()

# Ensure Date column exists in price_df
if 'Date' not in price_df.columns and price_df.index.name == 'Date':
    price_df = price_df.reset_index()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 1.4rem;">
      <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;
                  background:linear-gradient(110deg,#00e5ff,#ff6d2d);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        🚀 MARKET NEXUS
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;
                  color:#2d3f5a;letter-spacing:0.12em;margin-top:0.2rem;">
        BIG TECH INTELLIGENCE v4.0
      </div>
      <div style="margin-top:0.8rem;">
        <span class="live"></span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:#00ff9d;">
          LIVE DATA · 8 COMPANIES · yfinance
        </span>
      </div>
    </div>
    <hr style="border-color:rgba(0,229,255,0.07);margin:0 0 1rem;">
    """, unsafe_allow_html=True)

    page = st.selectbox("", [
        "🏠  Command Center",
        "📈  Stock Performance",
        "💰  Revenue & Earnings",
        "🏆  Competitive Analysis",
        "🔬  Deep Analytics",
        "🤖  AI Insight Engine",
        "📡  Live Dashboard",
    ], label_visibility="hidden")

    st.markdown("<hr style='border-color:rgba(0,229,255,0.07);margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.62rem;text-transform:uppercase;letter-spacing:0.1em;color:#2d3f5a;margin-bottom:0.5rem;">COMPANIES</div>', unsafe_allow_html=True)
    sel_companies = st.multiselect("", ALL_COMPANIES, default=ALL_COMPANIES, label_visibility="hidden")
    if not sel_companies: sel_companies = ALL_COMPANIES

    st.markdown("<hr style='border-color:rgba(0,229,255,0.07);margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.62rem;text-transform:uppercase;letter-spacing:0.1em;color:#2d3f5a;margin-bottom:0.5rem;">YEAR RANGE</div>', unsafe_allow_html=True)
    max_year = int(ann_df['Year'].max()) if not ann_df.empty else 2024
    year_range = st.slider("", 2020, max_year, (2020, max_year), label_visibility="hidden")

    st.markdown("<hr style='border-color:rgba(0,229,255,0.07);margin:0.8rem 0;'>", unsafe_allow_html=True)
    data_src = "yfinance LIVE" if _live_ok else "CSV Fallback"
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#2d3f5a;line-height:2.0;">
      UPDATED: {datetime.now().strftime("%H:%M:%S")}<br>
      SOURCE: {data_src}<br>
      RECORDS: {len(q_df)+len(ann_df)+len(price_df):,}<br>
      PERIOD: 2020 – {max_year}
    </div>
    """, unsafe_allow_html=True)

# ── Filtered data ─────────────────────────────────────────────────────────────
ann_f   = ann_df[(ann_df.Company.isin(sel_companies)) & (ann_df.Year.between(*year_range))]
q_f     = q_df[(q_df.Company.isin(sel_companies)) & (q_df.Quarter.dt.year.between(*year_range))]
p_f     = price_df[(price_df.Company.isin(sel_companies)) &
                   (price_df.Date.dt.year.between(*year_range))]

# ── Live fundamentals snapshot (for KPIs) ─────────────────────────────────────
fund_df = load_live_fundamentals()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: COMMAND CENTER
# ══════════════════════════════════════════════════════════════════════════════
if "Command Center" in page:

    st.markdown(f"""
    <div class="hero">
      <div class="hero-grid"></div><div class="hero-glow1"></div><div class="hero-glow2"></div>
      <div style="position:relative;z-index:1;">
        <div class="hero-eyebrow">⚡ Live Big Tech Intelligence Platform</div>
        <p class="hero-title">MARKET NEXUS</p>
        <p class="hero-sub">
          Live financial analytics across <strong style="color:#00e5ff;">Apple · Microsoft · Google ·
          Amazon · Meta · NVIDIA · Tesla · Netflix</strong> —
          powered by yfinance live data, real earnings & competitive benchmarks.
        </p>
        <div class="hero-chips">
          <span class="chip">📊 Live Earnings</span>
          <span class="chip orange">📈 Real Stock History</span>
          <span class="chip gree