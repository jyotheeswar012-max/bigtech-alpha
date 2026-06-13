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

st.set_page_config(page_title="MARKET NEXUS", page_icon="🚀",
                   layout="wide", initial_sidebar_state="expanded")

# ══════════════════════════════════════════════════════════════════════════════
# LIGHT PREMIUM CSS — Vibrant, modern, WOW factor
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;700&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

/* ── DESIGN TOKENS ─────────────────────────────────────────────── */
:root {
  --bg:         #f0f4ff;
  --bg2:        #e8eeff;
  --white:      #ffffff;
  --card:       #ffffff;
  --card-alt:   #fafbff;
  --surface:    #f5f7ff;
  --primary:    #4f46e5;
  --primary-l:  #6366f1;
  --primary-xl: #818cf8;
  --accent:     #06b6d4;
  --accent2:    #0ea5e9;
  --orange:     #f97316;
  --orange2:    #fb923c;
  --green:      #10b981;
  --green2:     #34d399;
  --red:        #ef4444;
  --red2:       #f87171;
  --purple:     #8b5cf6;
  --pink:       #ec4899;
  --yellow:     #f59e0b;
  --txt:        #0f172a;
  --txt2:       #475569;
  --txt3:       #94a3b8;
  --txt4:       #cbd5e1;
  --border:     rgba(99,102,241,0.12);
  --border2:    rgba(99,102,241,0.22);
  --shadow-sm:  0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.04);
  --shadow:     0 4px 16px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.04);
  --shadow-lg:  0 12px 40px rgba(79,70,229,0.12), 0 4px 12px rgba(0,0,0,0.06);
  --shadow-xl:  0 24px 60px rgba(79,70,229,0.15), 0 8px 20px rgba(0,0,0,0.08);
  --radius:     16px;
  --radius-lg:  24px;
  --radius-xl:  32px;
}

/* ── GLOBAL RESET ──────────────────────────────────────────────── */
* { box-sizing: border-box; }

.stApp {
  background: var(--bg) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  color: var(--txt);
}

/* Animated mesh gradient background */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 100% 80% at 0% 0%, rgba(99,102,241,0.08) 0%, transparent 50%),
    radial-gradient(ellipse 80% 60% at 100% 100%, rgba(6,182,212,0.06) 0%, transparent 50%),
    radial-gradient(ellipse 60% 50% at 50% 0%, rgba(249,115,22,0.04) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.main .block-container {
  padding: 1.4rem 2.2rem !important;
  max-width: 100% !important;
  position: relative;
  z-index: 1;
}

/* ── HIDE STREAMLIT DEFAULTS ───────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── SIDEBAR ───────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #4f46e5 0%, #6366f1 40%, #818cf8 100%) !important;
  border-right: none !important;
  box-shadow: 4px 0 24px rgba(79,70,229,0.15);
}
[data-testid="stSidebar"] * {
  color: #fff !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
  background: rgba(255,255,255,0.15) !important;
  border: 1px solid rgba(255,255,255,0.25) !important;
  border-radius: 12px !important;
  backdrop-filter: blur(12px);
  color: #fff !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
  font-size: 0.65rem !important;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  opacity: 0.7;
}
[data-testid="stSidebar"] .stSlider > div > div > div {
  background: rgba(255,255,255,0.3) !important;
}
[data-testid="stSidebar"] [data-testid="stSliderTickBarMin"],
[data-testid="stSidebar"] [data-testid="stSliderTickBarMax"] {
  color: rgba(255,255,255,0.7) !important;
}

/* ── HERO BANNER ───────────────────────────────────────────────── */
.hero {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 30%, #06b6d4 70%, #10b981 100%);
  border-radius: var(--radius-xl);
  padding: 3.2rem 3.8rem 3rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-xl);
  color: #fff;
}
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle 400px at 20% 50%, rgba(255,255,255,0.15) 0%, transparent 70%),
    radial-gradient(circle 300px at 80% 30%, rgba(255,255,255,0.1) 0%, transparent 70%);
  pointer-events: none;
}
.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.06;
  background-image:
    linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
}
.hero-orb1 {
  position: absolute; width: 300px; height: 300px; border-radius: 50%;
  background: rgba(255,255,255,0.08);
  top: -80px; right: -60px;
  animation: orb-float 8s ease-in-out infinite;
}
.hero-orb2 {
  position: absolute; width: 200px; height: 200px; border-radius: 50%;
  background: rgba(255,255,255,0.06);
  bottom: -50px; left: 10%;
  animation: orb-float 10s ease-in-out infinite reverse;
}
.hero-orb3 {
  position: absolute; width: 120px; height: 120px; border-radius: 50%;
  background: rgba(255,255,255,0.1);
  top: 20%; right: 30%;
  animation: orb-float 6s ease-in-out infinite 1s;
}
@keyframes orb-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33%      { transform: translate(15px, -20px) scale(1.08); }
  66%      { transform: translate(-10px, 12px) scale(0.95); }
}
.hero-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  opacity: 0.85;
  margin-bottom: 0.9rem;
  display: flex; align-items: center; gap: 0.5rem;
}
.hero-eyebrow::before {
  content: ''; display: inline-block;
  width: 24px; height: 2px;
  background: rgba(255,255,255,0.6);
  border-radius: 2px;
}
.hero-title {
  font-family: 'Outfit', sans-serif;
  font-size: 4.5rem;
  font-weight: 900;
  line-height: 1.0;
  letter-spacing: -0.035em;
  margin: 0 0 0.8rem 0;
  text-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
.hero-sub {
  font-size: 1.05rem;
  line-height: 1.7;
  max-width: 620px;
  opacity: 0.9;
  font-weight: 400;
}
.hero-chips {
  display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 1.6rem;
}
.chip {
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.3);
  color: #fff !important;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; font-weight: 500;
  padding: 0.4rem 1rem;
  border-radius: 100px;
  letter-spacing: 0.04em;
  backdrop-filter: blur(8px);
  transition: all 0.2s;
}
.chip:hover { background: rgba(255,255,255,0.28); transform: translateY(-1px); }
.chip.orange, .chip.green, .chip.purple { background: rgba(255,255,255,0.18); }

/* ── TICKER TAPE ─────────────────────────────────────────────────── */
.ticker-wrap {
  overflow: hidden;
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 0.55rem 0;
  margin-bottom: 1.8rem;
  box-shadow: var(--shadow-sm);
  white-space: nowrap;
}
.ticker-inner {
  display: inline-block;
  animation: ticker-scroll 35s linear infinite;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  color: var(--txt3);
}
.ticker-inner span.sym { color: var(--primary); font-weight: 700; margin: 0 0.25rem; }
@keyframes ticker-scroll {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* ── KPI CARDS ────────────────────────────────────────────────────── */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.2rem;
  margin-bottom: 2rem;
}
.kpi {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.6rem 1.8rem 1.5rem;
  position: relative;
  overflow: hidden;
  cursor: default;
  box-shadow: var(--shadow);
  transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.kpi:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: var(--shadow-xl);
  border-color: var(--border2);
}
.kpi-stripe {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
  border-radius: var(--radius) var(--radius) 0 0;
}
.kpi-stripe.orange { background: linear-gradient(90deg, var(--orange), var(--yellow)); }
.kpi-stripe.green  { background: linear-gradient(90deg, var(--green), var(--accent)); }
.kpi-stripe.purple { background: linear-gradient(90deg, var(--purple), var(--pink)); }
.kpi-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--txt3);
  margin-bottom: 0.6rem;
  font-weight: 600;
}
.kpi-val {
  font-family: 'Outfit', sans-serif;
  font-size: 2.3rem;
  font-weight: 800;
  line-height: 1.0;
  color: var(--primary) !important;
  letter-spacing: -0.03em;
}
.kpi-val.orange { color: var(--orange) !important; }
.kpi-val.green  { color: var(--green)  !important; }
.kpi-val.purple { color: var(--purple) !important; }
.kpi-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.66rem;
  color: var(--txt3);
  margin-top: 0.5rem;
}
.kpi-icon {
  position: absolute;
  right: 1.5rem; bottom: 1.3rem;
  font-size: 2.5rem;
  opacity: 0.08;
}
.kpi-badge {
  position: absolute;
  top: 1.1rem; right: 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.06em;
  padding: 0.22rem 0.7rem;
  border-radius: 100px;
  font-weight: 700;
}
.up   { background: rgba(16,185,129,0.12); color: var(--green) !important; border: 1px solid rgba(16,185,129,0.25); }
.down { background: rgba(239,68,68,0.10);  color: var(--red)   !important; border: 1px solid rgba(239,68,68,0.2);  }
.flat { background: rgba(245,158,11,0.10); color: var(--yellow) !important; border: 1px solid rgba(245,158,11,0.2); }

/* ── SECTION HEADERS ─────────────────────────────────────────────── */
.sec {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 2.5rem 0 1.4rem 0;
}
.sec-title {
  font-family: 'Outfit', sans-serif;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  white-space: nowrap;
  color: var(--txt);
}
.sec-line {
  flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--border2), transparent);
}
.sec-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.58rem;
  color: var(--white) !important;
  letter-spacing: 0.08em;
  white-space: nowrap;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  padding: 0.28rem 0.8rem;
  border-radius: 100px;
  font-weight: 600;
}

/* ── CHART CARD ───────────────────────────────────────────────────── */
.chart-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.4rem 1.4rem 0.8rem;
  margin-bottom: 1.2rem;
  box-shadow: var(--shadow-sm);
}

/* ── RANK ROWS ────────────────────────────────────────────────────── */
.rank-row {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  margin-bottom: 0.35rem;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}
.rank-row:hover { border-color: var(--border); background: var(--surface); box-shadow: var(--shadow-sm); }
.rank-num { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 800; color: var(--txt4); width: 1.5rem; text-align: center; }
.rank-name { font-weight: 600; font-size: 0.88rem; flex: 1; color: var(--txt); }
.rank-val { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: var(--primary); font-weight: 600; }

/* ── TABS ──────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  gap: 0.35rem;
  background: transparent;
  border-bottom: 2px solid var(--border);
  padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 3px solid transparent !important;
  border-radius: 0 !important;
  color: var(--txt3) !important;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.7rem 1.3rem !important;
  transition: all 0.2s;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--primary) !important; }
.stTabs [aria-selected="true"] {
  color: var(--primary) !important;
  border-bottom-color: var(--primary) !important;
  background: transparent !important;
}

/* ── LIVE PULSE DOT ──────────────────────────────────────────────── */
.live {
  display: inline-block;
  width: 8px; height: 8px;
  background: #34d399;
  border-radius: 50%;
  margin-right: 6px;
  vertical-align: middle;
  box-shadow: 0 0 0 3px rgba(52,211,153,0.3);
  animation: pulse-ring 2s ease infinite;
}
@keyframes pulse-ring {
  0%   { box-shadow: 0 0 0 0 rgba(52,211,153,0.5); }
  70%  { box-shadow: 0 0 0 8px rgba(52,211,153,0); }
  100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); }
}

/* ── INSIGHT CARDS ───────────────────────────────────────────────── */
.insight-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem 2rem;
  margin-bottom: 1rem;
  border-left: 4px solid var(--primary);
  box-shadow: var(--shadow);
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  overflow: hidden;
}
.insight-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; bottom: 0; width: 120px;
  background: linear-gradient(90deg, rgba(79,70,229,0.04), transparent);
  pointer-events: none;
}
.insight-card:hover { transform: translateX(6px); box-shadow: var(--shadow-lg); }
.insight-title { font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 700; color: var(--txt); margin-bottom: 0.5rem; }
.insight-body { font-size: 0.88rem; color: var(--txt2); line-height: 1.8; }

/* ── GLASS PANEL ─────────────────────────────────────────────────── */
.glass-panel {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem 1.8rem;
  box-shadow: var(--shadow);
  position: relative;
}

/* ── PAGE TITLE ──────────────────────────────────────────────────── */
.page-title {
  font-family: 'Outfit', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 60%, var(--green) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.6rem;
}

/* ── SCROLLBAR ───────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--txt4); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--txt3); }

/* ── DATAFRAME ───────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow-sm);
}

/* ── METRICS ─────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.1rem 1.3rem;
  box-shadow: var(--shadow-sm);
}
[data-testid="stMetricLabel"] {
  font-size: 0.65rem !important; text-transform: uppercase;
  letter-spacing: 0.1em; color: var(--txt3) !important; font-weight: 600;
}
[data-testid="stMetricValue"] {
  font-family: 'Outfit', sans-serif !important;
  color: var(--primary) !important;
  font-weight: 700;
}

/* ── SIDEBAR LOGO ────────────────────────────────────────────────── */
.logo-wrap { padding: 1.6rem 0 1.2rem; }
.logo-text {
  font-family: 'Outfit', sans-serif;
  font-size: 1.6rem;
  font-weight: 900;
  color: #fff !important;
  letter-spacing: -0.03em;
}
.logo-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.55rem;
  color: rgba(255,255,255,0.55) !important;
  letter-spacing: 0.16em;
  margin-top: 0.25rem;
}
.logo-badge {
  display: inline-flex; align-items: center; gap: 0.45rem;
  margin-top: 1rem;
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 100px;
  padding: 0.35rem 0.85rem;
  backdrop-filter: blur(8px);
}
.logo-badge-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: #fff !important;
  letter-spacing: 0.06em;
}

/* ── DIVIDERS ────────────────────────────────────────────────────── */
.h-divider {
  height: 1px;
  background: rgba(255,255,255,0.15);
  margin: 0.8rem 0;
}

/* ── ANIMATIONS ──────────────────────────────────────────────────── */
@keyframes slide-up {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: slide-up 0.5s ease forwards; }
</style>
""", unsafe_allow_html=True)

# ── PLOTLY LAYOUT (LIGHT THEME) ───────────────────────────────────────────────
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#475569", size=11),
    xaxis=dict(gridcolor="rgba(0,0,0,0.04)", zerolinecolor="rgba(0,0,0,0.07)",
               linecolor="rgba(0,0,0,0.06)"),
    yaxis=dict(gridcolor="rgba(0,0,0,0.04)", zerolinecolor="rgba(0,0,0,0.07)",
               linecolor="rgba(0,0,0,0.06)"),
    margin=dict(l=10, r=10, t=44, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0.06)",
                borderwidth=1, font=dict(size=10, color="#64748b"), orientation='h', y=1.1),
)
COLORS = {
    'Apple':     '#1d1d1f',
    'Microsoft': '#0078d4',
    'Google':    '#ea4335',
    'Amazon':    '#ff9900',
    'Meta':      '#0668e1',
    'NVIDIA':    '#76b900',
    'Tesla':     '#cc0000',
    'Netflix':   '#e50914',
}
ALL_COMPANIES = list(COLORS.keys())

def hex_to_rgba(h, a=0.15):
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{a})'

def sf(fig, h=360, legend=True):
    kw = dict(**PL, height=h)
    if not legend: kw['showlegend'] = False
    fig.update_layout(**kw)
    return fig

def sec(title, tag=""):
    t = f'<div class="sec-tag">{tag}</div>' if tag else ''
    st.markdown(
        f'<div class="sec"><div class="sec-title">{title}</div>'
        f'<div class="sec-line"></div>{t}</div>',
        unsafe_allow_html=True)

# ── LIVE DATA ─────────────────────────────────────────────────────────────────
try:
    from live_data import (
        get_live_price, get_intraday_data, get_multi_live_prices,
        get_all_fundamentals, get_all_price_history,
        get_all_quarterly, get_all_annual, merge_with_csv,
        COMPANIES as LIVE_COMPANIES, COMPANY_COLORS, NAME_TO_TICKER
    )
    _live_ok = True
except ImportError:
    _live_ok = False

try:
    from streamlit_autorefresh import st_autorefresh
    _autorefresh_ok = True
except ImportError:
    _autorefresh_ok = False

# ── CSV LOADING ───────────────────────────────────────────────────────────────
@st.cache_data
def load_csv():
    base = Path(__file__).parent
    q = pd.read_csv(base / "quarterly_revenue.csv", parse_dates=["Quarter"])
    a = pd.read_csv(base / "annual_metrics.csv")
    p = pd.read_csv(base / "stock_prices.csv", parse_dates=["Date"])
    return q, a, p

@st.cache_data(ttl=43200)
def load_live_annual():
    if not _live_ok: return pd.DataFrame()
    try: return get_all_annual()
    except: return pd.DataFrame()

@st.cache_data(ttl=43200)
def load_live_quarterly():
    if not _live_ok: return pd.DataFrame()
    try: return get_all_quarterly()
    except: return pd.DataFrame()

@st.cache_data(ttl=86400)
def load_live_prices():
    if not _live_ok: return pd.DataFrame()
    try: return get_all_price_history(period="5y")
    except: return pd.DataFrame()

@st.cache_data(ttl=60)
def load_live_fundamentals():
    if not _live_ok: return pd.DataFrame()
    try: return get_all_fundamentals()
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def build_merged_data():
    q_csv, ann_csv, price_csv = load_csv()
    live_ann = load_live_annual()
    live_q   = load_live_quarterly()
    live_p   = load_live_prices()

    if _live_ok and not live_ann.empty:
        ann_df = merge_with_csv(live_ann, ann_csv, ['Company', 'Year'])
    else:
        ann_df = ann_csv.copy()

    if _live_ok and not live_q.empty:
        live_q2 = live_q.copy()
        live_q2['Quarter'] = pd.to_datetime(live_q2['Quarter'])
        q_csv2 = q_csv.copy()
        q_csv2['Quarter'] = pd.to_datetime(q_csv2['Quarter'])
        q_df = merge_with_csv(live_q2, q_csv2, ['Company', 'Quarter'])
    else:
        q_df = q_csv.copy()

    if _live_ok and not live_p.empty:
        live_p2 = live_p.copy()
        live_p2['Date'] = pd.to_datetime(live_p2['Date'])
        p2 = price_csv.copy()
        p2['Date'] = pd.to_datetime(p2['Date'])
        price_df = merge_with_csv(live_p2, p2, ['Company', 'Date'])
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

def best_common_year(df, all_cos=ALL_COMPANIES):
    year_counts = df[df.Company.isin(all_cos)].groupby('Year')['Company'].nunique()
    if year_counts.empty: return int(df['Year'].max())
    half  = max(1, len(all_cos) // 2)
    valid = year_counts[year_counts >= half]
    return int(valid.index.max()) if not valid.empty else int(year_counts.index.max())

COMMON_LATEST_YEAR = best_common_year(ann_df)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:

    # ── LOGO ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="logo-wrap">
      <div style="font-size:2rem;margin-bottom:0.35rem;">🚀</div>
      <div class="logo-text">MARKET NEXUS</div>
      <div class="logo-sub">BIG TECH INTELLIGENCE · v6.0</div>
      <div class="logo-badge">
        <span class="live"></span>
        <span class="logo-badge-text">LIVE · 8 COMPANIES</span>
      </div>
    </div>
    <div class="h-divider"></div>
    """, unsafe_allow_html=True)

    # ── FILTERS FIRST (top of sidebar) ────────────────────────────────────────
    st.markdown('<div style="font-size:0.6rem;text-transform:uppercase;letter-spacing:0.14em;opacity:0.55;margin-bottom:0.5rem;">🏢 Companies</div>', unsafe_allow_html=True)
    sel_companies = st.multiselect("", ALL_COMPANIES, default=ALL_COMPANIES, label_visibility="hidden")
    if not sel_companies:
        sel_companies = ALL_COMPANIES

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.6rem;text-transform:uppercase;letter-spacing:0.14em;opacity:0.55;margin-bottom:0.5rem;">📅 Year Range</div>', unsafe_allow_html=True)
    slider_min = int(ann_df['Year'].min()) if not ann_df.empty else 2020
    slider_max = COMMON_LATEST_YEAR
    year_range = st.slider("", slider_min, slider_max, (slider_min, slider_max), label_visibility="hidden")

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)

    # ── PAGE NAVIGATION (below filters) ───────────────────────────────────────
    st.markdown('<div style="font-size:0.6rem;text-transform:uppercase;letter-spacing:0.14em;opacity:0.55;margin-bottom:0.5rem;">🗂 Navigation</div>', unsafe_allow_html=True)
    page = st.selectbox("", [
        "🏠  Command Center",
        "📈  Stock Performance",
        "💰  Revenue & Earnings",
        "🏆  Competitive Analysis",
        "🔬  Deep Analytics",
        "🤖  AI Insight Engine",
        "📡  Live Dashboard",
    ], label_visibility="hidden")

    # ── STATUS INFO ────────────────────────────────────────────────────────────
    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    data_src = "yfinance LIVE" if (_live_ok and not ann_df.empty) else "CSV Fallback"
    companies_in_latest = ann_df[ann_df.Year == COMMON_LATEST_YEAR]['Company'].nunique()
    price_latest_date = price_df['Date'].max().strftime("%Y-%m-%d") if not price_df.empty else "—"
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;opacity:0.45;line-height:2.2;">
      🕐 {datetime.now().strftime("%H:%M:%S")}<br>
      📡 {data_src}<br>
      📅 {COMMON_LATEST_YEAR} ({companies_in_latest}/8)<br>
      📈 Prices to: {price_latest_date}<br>
      🗂 {len(q_df)+len(ann_df)+len(price_df):,} records
    </div>
    """, unsafe_allow_html=True)

# ── FILTERED DATA ─────────────────────────────────────────────────────────────
ann_f = ann_df[(ann_df.Company.isin(sel_companies)) & (ann_df.Year.between(*year_range))]
q_f   = q_df[(q_df.Company.isin(sel_companies)) & (q_df.Quarter.dt.year.between(*year_range))]
p_f   = price_df[(price_df.Company.isin(sel_companies)) & (price_df.Date.dt.year.between(*year_range))]

def get_latest_slice(df, companies, fallback_year=None):
    sub = df[df.Company.isin(companies)]
    yr  = best_common_year(sub, companies) if fallback_year is None else fallback_year
    return sub[sub.Year == yr].copy(), yr

# ── TICKER TAPE ───────────────────────────────────────────────────────────────
ticker_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "NFLX"]
ticker_display = " &nbsp;·&nbsp; ".join([f'<span class="sym">{s}</span>' for s in ticker_symbols * 2])
st.markdown(f"""
<div class="ticker-wrap">
  <div class="ticker-inner">{ticker_display} &nbsp;&nbsp;&nbsp; {ticker_display}</div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: COMMAND CENTER
# ════════════════════════════════════════════════════════════════════════════
if "Command Center" in page:

    st.markdown("""
    <div class="hero animate-in">
      <div class="hero-orb1"></div>
      <div class="hero-orb2"></div>
      <div class="hero-orb3"></div>
      <div style="position:relative;z-index:1;">
        <div class="hero-eyebrow">⚡ Live Big Tech Intelligence Platform</div>
        <p class="hero-title">MARKET<br>NEXUS</p>
        <p class="hero-sub">
          Real-time financial intelligence across
          <strong>Apple · Microsoft · Google · Amazon · Meta · NVIDIA · Tesla · Netflix</strong> —
          powered by yfinance live feeds & competitive benchmarks.
        </p>
        <div class="hero-chips">
          <span class="chip">📊 Live Earnings</span>
          <span class="chip">📈 Real Stock History</span>
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
        top_row_idx = latest_sl.MarketCap_B.idxmax()
        top_mcap_co = latest_sl.loc[top_row_idx, 'Company']
        top_mcap    = latest_sl.loc[top_row_idx, 'MarketCap_B']
        nvda_sl     = latest_sl[latest_sl.Company == 'NVIDIA']
        nvda_ni     = nvda_sl['NetIncome_B'].values[0] if not nvda_sl.empty else 0
        data_label  = f"CSV · {lyr}"

    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi animate-in"><div class="kpi-stripe"></div><div class="kpi-icon">💰</div>
        <div class="kpi-label">Combined Revenue (TTM)</div>
        <div class="kpi-val">${total_rev/1000:.2f}T</div>
        <div class="kpi-sub">{len(sel_companies)} companies · {data_label}</div>
        <div class="kpi-badge up">↑ LIVE</div></div>
      <div class="kpi animate-in"><div class="kpi-stripe orange"></div><div class="kpi-icon">🏦</div>
        <div class="kpi-label">Combined Market Cap</div>
        <div class="kpi-val orange">${total_mcap/1000:.1f}T</div>
        <div class="kpi-sub">{data_label}</div>
        <div class="kpi-badge up">↑ LIVE</div></div>
      <div class="kpi animate-in"><div class="kpi-stripe green"></div><div class="kpi-icon">🥇</div>
        <div class="kpi-label">Largest by Market Cap</div>
        <div class="kpi-val green">{top_mcap_co}</div>
        <div class="kpi-sub">${top_mcap:,.0f}B cap</div>
        <div class="kpi-badge flat">LIVE</div></div>
      <div class="kpi animate-in"><div class="kpi-stripe purple"></div><div class="kpi-icon">⚡</div>
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
        sf(fig, 350).update_layout(title=dict(text="Quarterly Revenue ($B)", font=dict(size=13, color='#334155')),
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
        sf(fig, 350).update_layout(title=dict(text="Market Cap by Year ($B)", font=dict(size=13, color='#334155')),
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
        sf(fig, 340).update_layout(title=dict(text="Normalised Stock Performance (Base=100)", font=dict(size=13, color='#334155')),
            yaxis_title="Indexed Return")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        margin_sl, m_yr = get_latest_slice(ann_df, sel_companies)
        margin_sl['Margin'] = (margin_sl.NetIncome_B / margin_sl.Revenue_B * 100).round(1)
        margin_sl = margin_sl.sort_values('Margin')
        fig = go.Figure(go.Bar(x=margin_sl.Margin, y=margin_sl.Company, orientation='h',
            marker=dict(color=margin_sl.Margin,
                colorscale=[[0,'#ef4444'],[0.4,'#f97316'],[1,'#10b981']], line=dict(width=0)),
            text=[f"{v:.1f}%" for v in margin_sl.Margin],
            textposition='outside', textfont=dict(size=10, color='#64748b'),
            hovertemplate='<b>%{y}</b><br>Margin: %{x:.1f}%<extra></extra>'))
        sf(fig, 340, legend=False).update_layout(title=dict(text=f"Net Profit Margin {m_yr}", font=dict(size=13, color='#334155')),
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
            fig.update_layout(**PL, height=330, title=dict(text=f"Revenue Treemap {t_yr}", font=dict(size=13, color='#334155')),
                coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        emp_sl, e_yr = get_latest_slice(ann_df, sel_companies)
        emp_sl = emp_sl.copy()
        emp_sl['RevPerEmp'] = (emp_sl.Revenue_B * 1e9 / (emp_sl.Employees_K * 1e3) / 1e6).round(2)
        emp_sl = emp_sl.sort_values('RevPerEmp')
        fig = go.Figure(go.Bar(x=emp_sl.RevPerEmp, y=emp_sl.Company, orientation='h',
            marker=dict(color=[COLORS[c] for c in emp_sl.Company], line=dict(width=0)),
            text=[f"${v:.2f}M" for v in emp_sl.RevPerEmp],
            textposition='outside', textfont=dict(size=10, color='#64748b'),
            hovertemplate='<b>%{y}</b><br>$%{x:.2f}M per employee<extra></extra>'))
        sf(fig, 330, legend=False).update_layout(title=dict(text=f"Revenue per Employee {e_yr} ($M)", font=dict(size=13, color='#334155')),
            xaxis_title="$M per Employee")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════════════
# PAGE: STOCK PERFORMANCE
# ════════════════════════════════════════════════════════════════════════════
elif "Stock Performance" in page:
    st.markdown('<p class="page-title">📈 Stock Performance</p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊  Price History", "📉  Volatility & Risk", "🎯  Return Analysis"])

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
            hovertemplate='<b>'+co1+'</b><br>%{x|%b %d,%Y}<br>$%{y:.2f}<extra></extra>'))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.MA50, name='MA50',
            line=dict(color='#f59e0b', width=1.5, dash='dot')))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.MA200, name='MA200',
            line=dict(color='#8b5cf6', width=1.5, dash='dash')))
        sf(fig, 420).update_layout(title=dict(text=f"{co1} — Price + Bollinger Bands + MAs", font=dict(size=13, color='#334155')),
            yaxis_title="Price (USD)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        fig2 = go.Figure(go.Bar(x=sub.Date, y=sub.Volume_M, marker_color=COLORS[co1], opacity=0.35, name='Volume'))
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
        sf(fig, 340).update_layout(title=dict(text="30-Day Rolling Volatility", font=dict(size=13, color='#334155')),
            yaxis_title="Volatility (%)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        stats = p_f.groupby('Company').agg(Avg_Return=('Daily_Return','mean'), Volatility=('Daily_Return','std')).reset_index()
        total_return = p_f.groupby('Company').apply(
            lambda g: (g.sort_values('Date').Price.iloc[-1] / g.sort_values('Date').Price.iloc[0] - 1) * 100
        ).reset_index(name='Total_Return_Pct')
        stats = stats.merge(total_return, on='Company')
        fig2 = go.Figure()
        for _, row in stats.iterrows():
            fig2.add_trace(go.Scatter(x=[row.Volatility], y=[row.Total_Return_Pct], mode='markers+text',
                name=row.Company, text=[row.Company], textposition='top center',
                textfont=dict(size=10, color=COLORS[row.Company]),
                marker=dict(size=20, color=COLORS[row.Company],
                    line=dict(width=2, color='rgba(255,255,255,0.8)')),
                hovertemplate=f'<b>{row.Company}</b><br>Vol:{row.Volatility:.2f}%<br>Return:{row.Total_Return_Pct:.0f}%<extra></extra>'))
        fig2.add_hline(y=0, line_dash='dot', line_color='rgba(0,0,0,0.08)')
        fig2.add_vline(x=stats.Volatility.mean(), line_dash='dot', line_color='rgba(0,0,0,0.08)')
        sf(fig2, 340).update_layout(title=dict(text="Risk vs Total Return", font=dict(size=13, color='#334155')),
            xaxis_title="Daily Volatility (Std Dev %)", yaxis_title="Total Return %", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        p_f2 = p_f.copy(); p_f2['Year'] = p_f2.Date.dt.year
        annual_ret = p_f2.groupby(['Company','Year']).apply(
            lambda g: (g.sort_values('Date').Price.iloc[-1] / g.sort_values('Date').Price.iloc[0] - 1) * 100
        ).reset_index(name='Annual_Return')
        pivot = annual_ret.pivot(index='Company', columns='Year', values='Annual_Return')
        fig = go.Figure(go.Heatmap(z=pivot.values, x=[str(c) for c in pivot.columns], y=list(pivot.index),
            colorscale=[[0,'#ef4444'],[0.45,'#f8fafc'],[1,'#10b981']], zmid=0,
            text=[[f"{v:.0f}%" if not np.isnan(v) else "" for v in row] for row in pivot.values],
            texttemplate='%{text}', textfont=dict(size=11, color='#334155'),
            hovertemplate='<b>%{y}</b> %{x}<br>Return: %{z:.1f}%<extra></extra>'))
        sf(fig, 360, legend=False).update_layout(title=dict(text="Annual Stock Return %", font=dict(size=13, color='#334155')))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        fig2 = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f.Company == co]
            if sub.empty: continue
            fig2.add_trace(go.Violin(x=[co]*len(sub), y=sub.Daily_Return, name=co,
                box_visible=True, meanline_visible=True,
                fillcolor=hex_to_rgba(COLORS[co], 0.2), line_color=COLORS[co], opacity=0.85,
                hovertemplate=f'<b>{co}</b><br>%{{y:.3f}}%<extra></extra>'))
        sf(fig2, 340).update_layout(title=dict(text="Daily Return Distribution", font=dict(size=13, color='#334155')),
            yaxis_title="Daily Return %")
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════════════
# PAGE: REVENUE & EARNINGS
# ════════════════════════════════════════════════════════════════════════════
elif "Revenue" in page:
    st.markdown('<p class="page-title">💰 Revenue & Earnings</p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊  Quarterly Deep-Dive", "📈  Growth Trends", "💎  Profitability"])

    with tab1:
        co2 = st.selectbox("Company", sel_companies, key='re1')
        sub = q_f[q_f.Company == co2].sort_values('Quarter').copy()
        sub['YoY'] = sub.Revenue_B.pct_change(4) * 100
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.65, 0.35], vertical_spacing=0.08)
        fig.add_trace(go.Bar(x=sub.Quarter, y=sub.Revenue_B, name='Revenue ($B)',
            marker_color=COLORS[co2], opacity=0.85,
            hovertemplate='%{x|%b %Y}<br>$%{y:.1f}B<extra></extra>'), row=1, col=1)
        fig.add_trace(go.Scatter(x=sub.Quarter, y=sub.Revenue_B.rolling(4).mean(), name='4Q Avg',
            line=dict(color='#f59e0b', width=2, dash='dot')), row=1, col=1)
        fig.add_trace(go.Bar(x=sub.Quarter, y=sub.YoY, name='YoY %',
            marker_color=['#10b981' if v >= 0 else '#ef4444' for v in sub.YoY.fillna(0)],
            hovertemplate='%{x|%b %Y}<br>YoY: %{y:.1f}%<extra></extra>'), row=2, col=1)
        sf(fig, 440).update_layout(title=dict(text=f"{co2} — Quarterly Revenue + YoY Growth", font=dict(size=13, color='#334155')))
        fig.update_yaxes(title_text="Revenue ($B)", row=1, col=1)
        fig.update_yaxes(title_text="YoY %", row=2, col=1)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with tab2:
        yr_min = int(ann_df.Year.min()); yr_max = COMMON_LATEST_YEAR
        cagr_rows = []
        for co in sel_companies:
            sub = ann_df[(ann_df.Company == co) & (ann_df.Year.isin([yr_min, yr_max]))].sort_values('Year')
            if len(sub) == 2:
                r0, r1 = sub.Revenue_B.iloc[0], sub.Revenue_B.iloc[1]
                n = yr_max - yr_min
                cagr = ((r1/r0)**(1/n) - 1) * 100 if n > 0 else 0
                cagr_rows.append({'Company': co, 'CAGR': round(cagr, 1)})
        cagr_df = pd.DataFrame(cagr_rows).sort_values('CAGR')
        c1, c2 = st.columns(2)
        with c1:
            if not cagr_df.empty:
                fig = go.Figure(go.Bar(x=cagr_df.CAGR, y=cagr_df.Company, orientation='h',
                    marker=dict(color=[COLORS[c] for c in cagr_df.Company], line=dict(width=0)),
                    text=[f"{v:.1f}%" for v in cagr_df.CAGR],
                    textposition='outside', textfont=dict(size=11, color='#64748b'),
                    hovertemplate='<b>%{y}</b><br>CAGR: %{x:.1f}%<extra></extra>'))
                sf(fig, 340, legend=False).update_layout(title=dict(text=f"Revenue CAGR {yr_min}–{yr_max}", font=dict(size=13, color='#334155')), xaxis_title="CAGR %")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with c2:
            fig2 = go.Figure()
            for co in sel_companies:
                sub2 = ann_f[ann_f.Company == co].sort_values('Year')
                if sub2.empty: continue
                fig2.add_trace(go.Scatter(x=sub2.Year, y=sub2.Revenue_B, name=co, mode='lines+markers',
                    stackgroup='one', fillcolor=hex_to_rgba(COLORS[co], 0.3),
                    line=dict(color=COLORS[co], width=1.5),
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:.1f}}B<extra></extra>'))
            sf(fig2, 340).update_layout(title=dict(text="Stacked Annual Revenue ($B)", font=dict(size=13, color='#334155')), yaxis_title="Revenue ($B)")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        ni_data = ann_f.pivot(index='Year', columns='Company', values='NetIncome_B').fillna(0)
        fig = go.Figure()
        for co in [c for c in sel_companies if c in ni_data.columns]:
            fig.add_trace(go.Scatter(x=ni_data.index, y=ni_data[co], name=co, mode='lines+markers',
                line=dict(color=COLORS[co], width=2.5),
                marker=dict(size=8, color=COLORS[co], line=dict(width=2, color='#fff')),
                hovertemplate=f'<b>{co}</b> %{{x}}<br>Net Income: $%{{y:.1f}}B<extra></extra>'))
        fig.add_hline(y=0, line_dash='dot', line_color='rgba(0,0,0,0.08)')
        sf(fig, 360).update_layout(title=dict(text="Net Income — All Companies", font=dict(size=13, color='#334155')), yaxis_title="Net Income ($B)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        c1, c2 = st.columns(2)
        with c1:
            avail_years = sorted(ann_df[ann_df.Company.isin(sel_companies)]['Year'].unique().tolist(), reverse=True)
            yr = st.selectbox("Year", avail_years, key='yr_ni')
            sub3 = ann_df[(ann_df.Year == yr) & (ann_df.Company.isin(sel_companies))]
            fig2 = go.Figure()
            for _, row in sub3.iterrows():
                fig2.add_trace(go.Scatter(x=[row.Revenue_B], y=[row.NetIncome_B], mode='markers+text',
                    name=row.Company, text=[row.Company], textposition='top center',
                    textfont=dict(size=10, color=COLORS[row.Company]),
                    marker=dict(size=16, color=COLORS[row.Company], line=dict(width=2, color='#fff')),
                    showlegend=False))
            sf(fig2, 320, legend=False).update_layout(title=dict(text=f"Revenue vs Net Income {yr}", font=dict(size=13, color='#334155')),
                xaxis_title="Revenue ($B)", yaxis_title="Net Income ($B)")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        with c2:
            ni_ch = ann_df[ann_df.Company.isin(sel_companies)].sort_values(['Company','Year']).copy()
            ni_ch['NI_Change'] = ni_ch.groupby('Company')['NetIncome_B'].diff()
            ni_latest_sl, ni_yr = get_latest_slice(ni_ch, sel_companies)
            ni_latest_sl = ni_latest_sl.sort_values('NI_Change')
            fig3 = go.Figure(go.Bar(x=ni_latest_sl.NI_Change, y=ni_latest_sl.Company, orientation='h',
                marker=dict(color=['#10b981' if v >= 0 else '#ef4444' for v in ni_latest_sl.NI_Change.fillna(0)], line=dict(width=0)),
                text=[f"${v:+.1f}B" for v in ni_latest_sl.NI_Change.fillna(0)],
                textposition='outside', textfont=dict(size=10, color='#64748b'),
                hovertemplate='<b>%{y}</b><br>Change: $%{x:+.1f}B<extra></extra>'))
            sf(fig3, 320, legend=False).update_layout(title=dict(text=f"Net Income YoY Change {ni_yr}", font=dict(size=13, color='#334155')))
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════════════
# PAGE: COMPETITIVE ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif "Competitive" in page:
    st.markdown('<p class="page-title">🏆 Competitive Analysis</p>', unsafe_allow_html=True)

    sec("Multi-Dimensional Competitive Radar", "LIVE BENCHMARKS")
    ann_latest, latest_yr = get_latest_slice(ann_df, sel_companies)
    ann_latest = ann_latest.copy()
    ann_latest['Margin']    = (ann_latest.NetIncome_B / ann_latest.Revenue_B * 100).round(1)
    ann_latest['RevPerEmp'] = (ann_latest.Revenue_B * 1e9 / (ann_latest.Employees_K * 1e3) / 1e6).round(2)

    if not fund_df.empty:
        for _, fr in fund_df.iterrows():
            mask = ann_latest.Company == fr['Company']
            if mask.any(): ann_latest.loc[mask, 'MarketCap_B'] = fr['marketCap_B']

    metrics = ['Revenue_B','NetIncome_B','MarketCap_B','Margin','RevPerEmp']
    labels  = ['Revenue ($B)','Net Income ($B)','Market Cap ($B)','Net Margin %','Rev/Emp $M']
    norm = ann_latest.set_index('Company')[metrics].copy()
    for col in metrics:
        norm[col] = (norm[col] - norm[col].min()) / (norm[col].max() - norm[col].min() + 1e-9) * 10

    fig = go.Figure()
    for co in sel_companies:
        if co not in norm.index: continue
        vals = list(norm.loc[co].values) + [norm.loc[co].values[0]]
        fig.add_trace(go.Scatterpolar(r=vals, theta=labels + [labels[0]], name=co, fill='toself',
            fillcolor=hex_to_rgba(COLORS[co], 0.12), line=dict(color=COLORS[co], width=2.5),
            hovertemplate=f'<b>{co}</b><br>%{{theta}}: %{{r:.1f}}/10<extra></extra>'))
    fig.update_layout(**PL, height=480,
        polar=dict(bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0,10], gridcolor='rgba(0,0,0,0.06)', tickfont=dict(size=8, color='#94a3b8')),
            angularaxis=dict(gridcolor='rgba(0,0,0,0.06)', tickfont=dict(size=10, color='#475569'))),
        title=dict(text=f"Competitive Radar {latest_yr} — 5 Dimensions", font=dict(size=13, color='#334155')))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    c1, c2 = st.columns(2)
    with c1:
        sec("Rankings Board", f"{latest_yr} LIVE")
        ann_rs = ann_latest.sort_values('MarketCap_B', ascending=False)
        medals = ['🥇','🥈','🥉','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣']
        html = ""
        for i, (_, row) in enumerate(ann_rs.iterrows()):
            html += (f'<div class="rank-row"><div class="rank-num">{medals[i] if i < len(medals) else i+1}</div>'
                     f'<div style="width:12px;height:12px;border-radius:50%;background:{COLORS[row.Company]};flex-shrink:0;"></div>'
                     f'<div class="rank-name">{row.Company}</div><div class="rank-val">${row.MarketCap_B:,.0f}B</div></div>')
        st.markdown(f'<div class="glass-panel"><div style="font-family:\'JetBrains Mono\',monospace;font-size:0.6rem;color:var(--txt3);letter-spacing:0.1em;margin-bottom:0.8rem;">RANKED BY MARKET CAP · {latest_yr}</div>{html}</div>', unsafe_allow_html=True)

    with c2:
        sec("Price/Sales Ratio", "LIVE P/S")
        ann_ps = ann_latest.copy()
        ann_ps['PS_Ratio'] = ann_ps.MarketCap_B / ann_ps.Revenue_B
        ann_ps = ann_ps.sort_values('PS_Ratio')
        fig = go.Figure(go.Bar(x=ann_ps.PS_Ratio, y=ann_ps.Company, orientation='h',
            marker=dict(color=[COLORS[c] for c in ann_ps.Company], line=dict(width=0)),
            text=[f"{v:.1f}x" for v in ann_ps.PS_Ratio],
            textposition='outside', textfont=dict(size=11, color='#64748b'),
            hovertemplate='<b>%{y}</b><br>P/S: %{x:.1f}x<extra></extra>'))
        sf(fig, 330, legend=False).update_layout(title=dict(text=f"Price/Sales Ratio {latest_yr}", font=dict(size=13, color='#334155')), xaxis_title="P/S Ratio")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    sec("Employees vs Revenue — Efficiency Matrix", "ANIMATED")
    ann_all = ann_f.copy()
    ann_all['RevPerEmp'] = (ann_all.Revenue_B * 1e9 / (ann_all.Employees_K * 1e3) / 1e6).round(2)
    if not ann_all.empty:
        fig = px.scatter(ann_all, x='Employees_K', y='Revenue_B', color='Company',
            size='MarketCap_B', animation_frame='Year', color_discrete_map=COLORS, size_max=60,
            hover_data={'NetIncome_B':':.1f','RevPerEmp':':.2f'})
        fig.update_layout(**PL, height=400, title=dict(text="Employees vs Revenue (bubble=Market Cap)", font=dict(size=13, color='#334155')),
            xaxis_title="Employees (K)", yaxis_title="Revenue ($B)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════════════
# PAGE: DEEP ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
elif "Deep Analytics" in page:
    st.markdown('<p class="page-title">🔬 Deep Analytics</p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🔗  Correlation Lab", "📐  Statistical Tests", "🌊  Market Cycles"])

    with tab1:
        sec("Stock Price Correlation Matrix", "LIVE DAILY RETURNS")
        price_pivot = price_df[price_df.Company.isin(sel_companies)].pivot(index='Date', columns='Company', values='Daily_Return').dropna()
        corr = price_pivot.corr()
        fig = go.Figure(go.Heatmap(z=corr.values, x=list(corr.columns), y=list(corr.index),
            colorscale=[[0,'#ef4444'],[0.5,'#f8fafc'],[1,'#4f46e5']], zmid=0, zmin=-1, zmax=1,
            text=np.round(corr.values, 2), texttemplate='%{text}', textfont_size=11,
            hovertemplate='<b>%{y} × %{x}</b><br>Correlation: %{z:.2f}<extra></extra>'))
        sf(fig, 420, legend=False).update_layout(title=dict(text="Daily Return Correlation", font=dict(size=13, color='#334155')))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        c1, c2 = st.columns(2)
        with c1: co_a = st.selectbox("Company A", sel_companies, index=0, key='ca')
        with c2: co_b = st.selectbox("Company B", sel_companies, index=min(1, len(sel_companies)-1), key='cb')
        if co_a != co_b and co_a in price_pivot.columns and co_b in price_pivot.columns:
            pair = price_pivot[[co_a, co_b]].dropna()
            corr_val = pair[co_a].corr(pair[co_b])
            slope, intercept, r, p, se = scipy_stats.linregress(pair[co_a], pair[co_b])
            x_range = np.linspace(pair[co_a].min(), pair[co_a].max(), 100)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=pair[co_a], y=pair[co_b], mode='markers',
                marker=dict(size=3, color='rgba(79,70,229,0.3)'),
                hovertemplate=f'{co_a}: %{{x:.2f}}%<br>{co_b}: %{{y:.2f}}%<extra></extra>', name='Daily Returns'))
            fig2.add_trace(go.Scatter(x=x_range, y=slope*x_range+intercept, mode='lines',
                line=dict(color='#f97316', width=2, dash='dash'), name=f'Fit (r={corr_val:.2f})'))
            sf(fig2, 340).update_layout(title=dict(text=f"{co_a} vs {co_b} — r={corr_val:.3f} | p={p:.2e}", font=dict(size=13, color='#334155')),
                xaxis_title=f"{co_a} Daily Return %", yaxis_title=f"{co_b} Daily Return %")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab2:
        sec("Normality Tests & Distribution Stats", "LIVE DATA")
        stats_rows = []
        for co in sel_companies:
            rets = price_df[price_df.Company == co]['Daily_Return'].dropna()
            if len(rets) < 10: continue
            stat, p_sh = scipy_stats.shapiro(rets.sample(min(5000, len(rets)), random_state=42))
            stats_rows.append({'Company': co, 'Mean (%)': round(rets.mean(), 4), 'Std Dev (%)': round(rets.std(), 4),
                'Skewness': round(scipy_stats.skew(rets), 3), 'Kurtosis': round(scipy_stats.kurtosis(rets), 3),
                'Shapiro-Wilk p': f'{p_sh:.4f}', 'Normal?': '✅ Yes' if p_sh > 0.05 else '❌ No',
                'Min (%)': round(rets.min(), 3), 'Max (%)': round(rets.max(), 3)})
        if stats_rows:
            st.dataframe(pd.DataFrame(stats_rows).set_index('Company'), use_container_width=True)

        co_qq = st.selectbox("Q-Q Plot for:", sel_companies, key='qq')
        rets_qq = price_df[price_df.Company == co_qq]['Daily_Return'].dropna()
        theo = scipy_stats.norm.ppf(np.linspace(0.01, 0.99, len(rets_qq)))
        sample_q = np.sort(rets_qq.values)[:len(theo)]; theo = theo[:len(sample_q)]
        mu, sig = rets_qq.mean(), rets_qq.std()
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=theo, y=sample_q, mode='markers', marker=dict(size=3, color=COLORS[co_qq], opacity=0.5), name='Q-Q'))
            fig.add_trace(go.Scatter(x=[theo.min(), theo.max()], y=[theo.min()*sig+mu, theo.max()*sig+mu],
                mode='lines', line=dict(color='#f97316', width=2, dash='dash'), name='Normal'))
            sf(fig, 300).update_layout(title=dict(text=f"{co_qq} — Q-Q Plot", font=dict(size=13, color='#334155')), xaxis_title="Theoretical", yaxis_title="Sample")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with c2:
            fig2 = go.Figure()
            fig2.add_trace(go.Histogram(x=rets_qq, nbinsx=80, name='Returns',
                marker=dict(color=hex_to_rgba(COLORS[co_qq], 0.5), line=dict(color=COLORS[co_qq], width=0.5))))
            x_n = np.linspace(rets_qq.min(), rets_qq.max(), 200)
            fig2.add_trace(go.Scatter(x=x_n, y=scipy_stats.norm.pdf(x_n, mu, sig)*len(rets_qq)*(rets_qq.max()-rets_qq.min())/80,
                mode='lines', line=dict(color='#f97316', width=2, dash='dot'), name='Normal Fit'))
            sf(fig2, 300).update_layout(title=dict(text=f"{co_qq} Return Distribution", font=dict(size=13, color='#334155')), yaxis_title="Count")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        sec("Drawdown Analysis — Peak-to-Trough", "LIVE DATA")
        fig = go.Figure()
        for co in sel_companies:
            sub = price_df[price_df.Company == co].sort_values('Date')
            if sub.empty: continue
            roll_max = sub.Price.cummax()
            drawdown = (sub.Price - roll_max) / roll_max * 100
            fig.add_trace(go.Scatter(x=sub.Date, y=drawdown, name=co, line=dict(color=COLORS[co], width=1.5),
                hovertemplate=f'<b>{co}</b> %{{x|%b %Y}}<br>Drawdown: %{{y:.1f}}%<extra></extra>'))
        sf(fig, 380).update_layout(title=dict(text="Maximum Drawdown from Peak", font=dict(size=13, color='#334155')), yaxis_title="Drawdown %")
        fig.add_hrect(y0=-100, y1=-30, fillcolor="rgba(239,68,68,0.04)", line_width=0)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════════════
# PAGE: AI INSIGHT ENGINE
# ════════════════════════════════════════════════════════════════════════════
elif "AI Insight" in page:
    st.markdown('<p class="page-title">🤖 AI Insight Engine</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-panel" style="border-left:4px solid var(--primary);margin-bottom:1.8rem;">
      <div style="font-family:'Outfit',sans-serif;font-size:1.15rem;font-weight:700;color:var(--primary);margin-bottom:0.6rem;">
        ⚡ Auto-Generated Insights from Live Data
      </div>
      <div style="color:var(--txt2);font-size:0.92rem;line-height:1.8;">
        Insights computed directly from live yfinance earnings & stock data across all 8 companies.
        Updated automatically every session.
      </div>
    </div>
    """, unsafe_allow_html=True)

    ai_latest, ai_yr = get_latest_slice(ann_df, ALL_COMPANIES)
    ai_first, ai_fy  = get_latest_slice(ann_df[ann_df.Year == ann_df.Year.min()], ALL_COMPANIES, fallback_year=int(ann_df.Year.min()))
    ai_idx   = ai_latest.set_index('Company')

    insights = []
    for co, color, label in [
        ('NVIDIA',    '#76b900', '🚀 NVIDIA AI Supercycle'),
        ('Meta',      '#0668e1', '💎 Meta Efficiency Era'),
        ('Apple',     '#1d1d1f', '🍎 Apple Revenue Machine'),
        ('Amazon',    '#ff9900', '📦 Amazon Profit Inflection'),
        ('Microsoft', '#0078d4', '☁️ Microsoft Cloud Dominance'),
    ]:
        try:
            row = ai_idx.loc[co]
            mgn = row.NetIncome_B / row.Revenue_B * 100
            insights.append((label, color,
                f"<b style='color:{color};'>{co}</b> — Revenue: <b style='color:{color};'>${row.Revenue_B:.1f}B</b> · "
                f"Net Income: <b style='color:{color};'>${row.NetIncome_B:.1f}B</b> · "
                f"Net Margin: <b style='color:{color};'>{mgn:.1f}%</b> ({ai_yr})"))
        except: pass

    try:
        tsla_vol = price_df[price_df.Company == 'Tesla']['Daily_Return'].std()
        insights.append(('⚡ Tesla: Highest Volatility', '#cc0000',
            f"Tesla daily return std dev: <b style='color:#cc0000;'>{tsla_vol:.2f}%</b> — highest among all 8 companies."))
    except: pass

    for title, color, body in insights:
        st.markdown(f"""
        <div class="insight-card" style="border-left-color:{color};">
          <div class="insight-title">{title}</div>
          <div class="insight-body">{body}</div>
        </div>""", unsafe_allow_html=True)

    sec(f"Full Company Scorecard — {ai_yr}", "LIVE METRICS")
    score = ai_latest[ai_latest.Company.isin(sel_companies)].copy()
    score['Net_Margin_%']  = (score.NetIncome_B / score.Revenue_B * 100).round(1)
    score['Rev_per_Emp_M'] = (score.Revenue_B * 1e9 / (score.Employees_K * 1e3) / 1e6).round(2)
    score['PS_Ratio']      = (score.MarketCap_B / score.Revenue_B).round(1)
    if not fund_df.empty:
        for _, fr in fund_df.iterrows():
            mask = score.Company == fr['Company']
            if mask.any(): score.loc[mask, 'MarketCap_B'] = fr['marketCap_B']
    disp = score[['Company','Sector','Revenue_B','NetIncome_B','MarketCap_B','Employees_K','Net_Margin_%','Rev_per_Emp_M','PS_Ratio']].sort_values('MarketCap_B', ascending=False)
    disp.columns = ['Company','Sector','Revenue ($B)','Net Income ($B)','Market Cap ($B)','Employees (K)','Net Margin %','Rev/Employee ($M)','P/S Ratio']
    st.dataframe(disp.set_index('Company'), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: LIVE DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
elif "Live Dashboard" in page:
    if not _live_ok:
        st.error("⚠️ `live_data.py` not found."); st.stop()

    st.markdown("""
    <div class="hero" style="padding:2.4rem 3rem;margin-bottom:1.5rem;">
      <div class="hero-orb1"></div>
      <div class="hero-orb2"></div>
      <div style="position:relative;z-index:1;">
        <div class="hero-eyebrow">📡 yfinance · auto-refresh · intraday data</div>
        <p class="hero-title" style="font-size:3rem;">Live Dashboard</p>
        <p class="hero-sub">Real-time intraday prices for all 8 Big Tech companies — auto-refreshes every 60 seconds.</p>
        <div class="hero-chips">
          <span class="chip">🟢 Live Prices</span>
          <span class="chip">⏱ 60s Auto-Refresh</span>
          <span class="chip">📈 5-min Intraday</span>
          <span class="chip">🆓 No API Key</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if _autorefresh_ok:
        st_autorefresh(interval=60000, limit=None, key="live_refresh")
    else:
        st.warning("⚠️ `streamlit-autorefresh` not installed — manual refresh only.")
        if st.button("🔄 Refresh Now"): st.rerun()

    st.markdown(
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.68rem;color:var(--txt3);margin-bottom:1.2rem;">'
        f'<span class="live"></span> Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} · Data via yfinance</div>',
        unsafe_allow_html=True)

    @st.cache_data(ttl=30)
    def fetch_live_price(ticker): return get_live_price(ticker)

    @st.cache_data(ttl=300)
    def fetch_intraday(ticker, period="1d", interval="5m"):
        return get_intraday_data(ticker, period=period, interval=interval)

    ticker_map = {"Apple":"AAPL","Microsoft":"MSFT","Google":"GOOGL","Amazon":"AMZN",
                  "Meta":"META","NVIDIA":"NVDA","Tesla":"TSLA","Netflix":"NFLX"}

    sec("Live Price Snapshot", "ALL 8 COMPANIES · 60s REFRESH")
    cols = st.columns(4)
    for idx, (name, ticker) in enumerate(ticker_map.items()):
        price, change, vol = fetch_live_price(ticker)
        col = cols[idx % 4]
        if price is not None:
            direction = "up" if change >= 0 else "down"
            arrow = "↑" if change >= 0 else "↓"
            color = "#10b981" if change >= 0 else "#ef4444"
            vol_str = f"{vol/1e6:.1f}M" if vol and vol >= 1e6 else (f"{vol/1e3:.0f}K" if vol else "—")
            col.markdown(f"""
            <div class="kpi" style="margin-bottom:0.8rem;">
              <div class="kpi-stripe" style="background:linear-gradient(90deg,{color},{COLORS.get(name,'#4f46e5')});"></div>
              <div style="display:flex;justify-content:space-between;align-items:f