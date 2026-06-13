
"""
╔══════════════════════════════════════════════════════════════════╗
║  MARKET NEXUS — Big Tech Intelligence Platform  v5.0            ║
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

# ── PREMIUM CSS — glassmorphism, aurora, animations ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;700&family=Syne:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ── DESIGN TOKENS ─────────────────────────────────────────────── */
:root {
  --bg:        #020510;
  --bg-card:   #07091a;
  --surface:   #0a0d22;
  --glass:     rgba(10,14,40,0.75);
  --glass2:    rgba(255,255,255,0.04);
  --cyan:      #00d4ff;
  --cyan2:     #00f5ff;
  --orange:    #ff6b35;
  --green:     #00ff9d;
  --purple:    #b06ef3;
  --yellow:    #ffd60a;
  --pink:      #ff3366;
  --gold:      #f5a623;
  --txt:       #e8f0ff;
  --txt2:      #7a92bb;
  --txt3:      #2d3f5a;
  --border:    rgba(0,212,255,0.08);
  --border2:   rgba(0,212,255,0.20);
  --border3:   rgba(0,212,255,0.35);
  --glow-c:    rgba(0,212,255,0.15);
  --glow-o:    rgba(255,107,53,0.12);
  --glow-g:    rgba(0,255,157,0.12);
}

/* ── GLOBAL ────────────────────────────────────────────────────── */
* { box-sizing: border-box; }
.stApp {
  background: var(--bg) !important;
  font-family: 'Plus Jakarta Sans', 'Space Grotesk', sans-serif;
  min-height: 100vh;
}
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 10% 20%, rgba(0,100,200,0.06) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 90% 80%, rgba(100,0,200,0.05) 0%, transparent 60%),
    radial-gradient(ellipse 50% 60% at 50% 50%, rgba(0,200,150,0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}
.main .block-container {
  padding: 1.2rem 2rem !important;
  max-width: 100% !important;
  position: relative;
  z-index: 1;
}

/* ── SIDEBAR ────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #050815 0%, #07091f 100%) !important;
  border-right: 1px solid var(--border2) !important;
  backdrop-filter: blur(20px);
}
[data-testid="stSidebar"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 200px;
  background: radial-gradient(ellipse at top, rgba(0,150,255,0.1) 0%, transparent 70%);
  pointer-events: none;
}

/* ── TICKER TAPE ─────────────────────────────────────────────────── */
.ticker-wrap {
  overflow: hidden;
  background: linear-gradient(90deg, rgba(0,212,255,0.05) 0%, rgba(0,212,255,0.03) 100%);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 0.45rem 0;
  margin-bottom: 1.5rem;
  white-space: nowrap;
}
.ticker-inner {
  display: inline-block;
  animation: ticker-scroll 30s linear infinite;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.06em;
  color: var(--txt2);
}
.ticker-inner span.up   { color: var(--green);  }
.ticker-inner span.down { color: var(--pink);   }
.ticker-inner span.sym  { color: var(--cyan); font-weight: 700; margin: 0 0.3rem; }
@keyframes ticker-scroll {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* ── HERO SECTION ───────────────────────────────────────────────── */
.hero {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #040918 0%, #070d20 50%, #040918 100%);
  border: 1px solid var(--border2);
  border-radius: 24px;
  padding: 3rem 3.5rem 2.6rem;
  margin-bottom: 1.8rem;
  backdrop-filter: blur(12px);
}
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.035;
  background-image:
    linear-gradient(rgba(0,212,255,0.6) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,0.6) 1px, transparent 1px);
  background-size: 44px 44px;
}
.hero-glow1 {
  position: absolute;
  width: 600px; height: 350px;
  border-radius: 50%;
  background: radial-gradient(ellipse, rgba(0,150,255,0.12), transparent 70%);
  top: -100px; left: -150px;
  animation: float 8s ease-in-out infinite;
}
.hero-glow2 {
  position: absolute;
  width: 450px; height: 280px;
  border-radius: 50%;
  background: radial-gradient(ellipse, rgba(150,0,255,0.08), transparent 70%);
  bottom: -80px; right: -100px;
  animation: float 10s ease-in-out infinite reverse;
}
.hero-glow3 {
  position: absolute;
  width: 300px; height: 200px;
  border-radius: 50%;
  background: radial-gradient(ellipse, rgba(0,255,157,0.06), transparent 70%);
  top: 30%; right: 20%;
  animation: float 12s ease-in-out infinite 2s;
}
@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33%       { transform: translate(20px, -15px) scale(1.05); }
  66%       { transform: translate(-10px, 10px) scale(0.97); }
}
.hero-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.22em;
  color: var(--cyan);
  text-transform: uppercase;
  margin-bottom: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.hero-eyebrow::before {
  content: '';
  display: inline-block;
  width: 20px; height: 1px;
  background: var(--cyan);
}
.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: 4.2rem;
  font-weight: 800;
  line-height: 1.0;
  background: linear-gradient(120deg, #00d4ff 0%, #60a5fa 40%, #ff6b35 80%, #ff3366 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 0.7rem 0;
  letter-spacing: -0.02em;
}
.hero-sub {
  font-size: 0.98rem;
  color: var(--txt2);
  line-height: 1.75;
  max-width: 640px;
}
.hero-chips {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 1.4rem;
}
.chip {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(0,212,255,0.07);
  border: 1px solid rgba(0,212,255,0.22);
  color: var(--cyan) !important;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem;
  padding: 0.32rem 0.85rem;
  border-radius: 100px;
  letter-spacing: 0.06em;
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
}
.chip:hover { background: rgba(0,212,255,0.14); transform: translateY(-1px); }
.chip.orange { background: rgba(255,107,53,0.08); border-color: rgba(255,107,53,0.25); color: var(--orange) !important; }
.chip.green  { background: rgba(0,255,157,0.08); border-color: rgba(0,255,157,0.25); color: var(--green) !important;  }
.chip.purple { background: rgba(176,110,243,0.08); border-color: rgba(176,110,243,0.25); color: var(--purple) !important; }

/* ── KPI CARDS ───────────────────────────────────────────────────── */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.1rem;
  margin-bottom: 1.8rem;
}
.kpi {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.6rem 1.6rem 1.4rem;
  position: relative;
  overflow: hidden;
  cursor: default;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  backdrop-filter: blur(16px);
}
.kpi::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, transparent 60%);
  border-radius: inherit;
}
.kpi:hover {
  border-color: var(--border3);
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 30px var(--glow-c);
}
.kpi-stripe {
  position: absolute;
  inset: 0 auto 0 0;
  width: 3px;
  background: linear-gradient(180deg, var(--cyan), transparent);
  border-radius: 18px 0 0 18px;
}
.kpi-stripe.orange { background: linear-gradient(180deg, var(--orange), transparent); }
.kpi-stripe.green  { background: linear-gradient(180deg, var(--green), transparent);  }
.kpi-stripe.purple { background: linear-gradient(180deg, var(--purple), transparent); }
.kpi-stripe.gold   { background: linear-gradient(180deg, var(--gold), transparent);   }
.kpi-label {
  font-size: 0.63rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--txt3);
  margin-bottom: 0.5rem;
  font-weight: 600;
}
.kpi-val {
  font-family: 'Syne', sans-serif;
  font-size: 2.2rem;
  font-weight: 800;
  line-height: 1.0;
  color: var(--cyan) !important;
  letter-spacing: -0.02em;
}
.kpi-val.orange { color: var(--orange) !important; }
.kpi-val.green  { color: var(--green)  !important; }
.kpi-val.purple { color: var(--purple) !important; }
.kpi-val.gold   { color: var(--gold)   !important; }
.kpi-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.66rem;
  color: var(--txt3);
  margin-top: 0.4rem;
}
.kpi-icon {
  position: absolute;
  right: 1.4rem;
  bottom: 1.2rem;
  font-size: 2.2rem;
  opacity: 0.06;
}
.kpi-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.55rem;
  letter-spacing: 0.08em;
  padding: 0.2rem 0.6rem;
  border-radius: 100px;
  font-weight: 700;
}
.up   { background: rgba(0,255,157,0.12);  color: var(--green)  !important; border: 1px solid rgba(0,255,157,0.3);  }
.down { background: rgba(255,51,102,0.12); color: var(--pink)   !important; border: 1px solid rgba(255,51,102,0.3); }
.flat { background: rgba(255,214,10,0.12); color: var(--yellow) !important; border: 1px solid rgba(255,214,10,0.3); }

/* ── SECTION HEADERS ─────────────────────────────────────────────── */
.sec {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin: 2.2rem 0 1.2rem 0;
}
.sec-title {
  font-family: 'Syne', sans-serif;
  font-size: 0.88rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  white-space: nowrap;
  color: var(--txt);
}
.sec-line { flex: 1; height: 1px; background: linear-gradient(90deg, var(--border2), transparent); }
.sec-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.56rem;
  color: var(--orange) !important;
  letter-spacing: 0.12em;
  white-space: nowrap;
  background: rgba(255,107,53,0.08);
  border: 1px solid rgba(255,107,53,0.2);
  padding: 0.2rem 0.6rem;
  border-radius: 100px;
}

/* ── CHART CARD ───────────────────────────────────────────────────── */
.chart-card {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.4rem 1.4rem 0.8rem;
  margin-bottom: 1.1rem;
  backdrop-filter: blur(16px);
  transition: border-color 0.3s;
}
.chart-card:hover { border-color: var(--border2); }

/* ── RANK ROWS ────────────────────────────────────────────────────── */
.rank-row {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.7rem 1rem;
  border-radius: 10px;
  margin-bottom: 0.35rem;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}
.rank-row:hover { border-color: var(--border); background: rgba(255,255,255,0.03); }
.rank-num { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 800; color: var(--txt3); width: 1.5rem; text-align: center; }
.rank-name { font-weight: 600; font-size: 0.87rem; flex: 1; color: var(--txt); }
.rank-val { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--cyan); }

/* ── TABS ──────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  gap: 0.3rem;
  background: transparent;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: 10px 10px 0 0 !important;
  color: var(--txt2) !important;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 0.83rem;
  font-weight: 500;
  padding: 0.6rem 1.2rem !important;
  transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
  background: var(--glass) !important;
  border-color: var(--border2) !important;
  color: var(--cyan) !important;
  backdrop-filter: blur(12px);
}

/* ── LIVE PULSE DOT ──────────────────────────────────────────────── */
.live {
  display: inline-block;
  width: 7px; height: 7px;
  background: var(--green);
  border-radius: 50%;
  margin-right: 5px;
  vertical-align: middle;
  box-shadow: 0 0 8px var(--green);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; box-shadow: 0 0 8px var(--green); }
  50%       { opacity: 0.4; box-shadow: 0 0 3px var(--green); }
}

/* ── INSIGHT CARDS ───────────────────────────────────────────────── */
.insight-card {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.4rem 1.8rem;
  margin-bottom: 1rem;
  border-left: 3px solid var(--cyan);
  backdrop-filter: blur(16px);
  transition: all 0.25s;
  position: relative;
  overflow: hidden;
}
.insight-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0,212,255,0.04) 0%, transparent 50%);
  pointer-events: none;
}
.insight-card:hover { border-color: var(--border2); transform: translateX(4px); }
.insight-title { font-family: 'Syne', sans-serif; font-size: 0.92rem; font-weight: 700; color: var(--txt); margin-bottom: 0.5rem; }
.insight-body { font-size: 0.87rem; color: var(--txt2); line-height: 1.75; }

/* ── GLASS PANEL ─────────────────────────────────────────────────── */
.glass-panel {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.4rem 1.6rem;
  backdrop-filter: blur(20px);
  position: relative;
  overflow: hidden;
}
.glass-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent);
}

/* ── SCROLLBAR ───────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--txt3); border-radius: 3px; }

/* ── SIDEBAR LABELS ──────────────────────────────────────────────── */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
  font-size: 0.63rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--txt3) !important;
}

/* ── NAV ITEM ─────────────────────────────────────────────────────── */
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 0.8rem;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--txt2);
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 0.15rem;
}
.nav-item:hover { background: rgba(0,212,255,0.07); color: var(--txt); }
.nav-item.active { background: rgba(0,212,255,0.1); color: var(--cyan); border: 1px solid var(--border2); }

/* ── PAGE TITLE ──────────────────────────────────────────────────── */
.page-title {
  font-family: 'Syne', sans-serif;
  font-size: 2.4rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(120deg, var(--cyan), #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.6rem;
  position: relative;
  display: inline-block;
}

/* ── STAT BADGE ──────────────────────────────────────────────────── */
.stat-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem;
  padding: 0.22rem 0.7rem;
  border-radius: 100px;
  font-weight: 700;
}

/* ── DATAFRAME STYLING ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid var(--border) !important;
}

/* ── METRIC STYLING ──────────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1rem 1.2rem;
  backdrop-filter: blur(12px);
}
[data-testid="stMetricLabel"] { font-size: 0.65rem !important; text-transform: uppercase; letter-spacing: 0.1em; color: var(--txt3) !important; }
[data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; color: var(--cyan) !important; }

/* ── ANIMATIONS ──────────────────────────────────────────────────── */
@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: slide-up 0.5s ease forwards; }

/* ── SIDEBAR LOGO ────────────────────────────────────────────────── */
.logo-wrap {
  padding: 1.4rem 0 1.6rem;
  position: relative;
}
.logo-text {
  font-family: 'Syne', sans-serif;
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(110deg, #00d4ff, #ff6b35);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}
.logo-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.55rem;
  color: var(--txt3);
  letter-spacing: 0.15em;
  margin-top: 0.2rem;
}
.logo-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.9rem;
  background: rgba(0,255,157,0.08);
  border: 1px solid rgba(0,255,157,0.2);
  border-radius: 100px;
  padding: 0.3rem 0.75rem;
}
.logo-badge-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: var(--green) !important;
  letter-spacing: 0.06em;
}

/* ── SECTION DIVIDER ─────────────────────────────────────────────── */
.h-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border2), transparent);
  margin: 0.8rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY LAYOUT DEFAULTS ────────────────────────────────────────────────────
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans", color="#7a92bb", size=11),
    xaxis=dict(gridcolor="rgba(255,255,255,0.03)", zerolinecolor="rgba(255,255,255,0.05)",
               linecolor="rgba(255,255,255,0.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.03)", zerolinecolor="rgba(255,255,255,0.05)",
               linecolor="rgba(255,255,255,0.04)"),
    margin=dict(l=8, r=8, t=40, b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.07)",
                borderwidth=1, font=dict(size=10), orientation='h', y=1.1),
)
COLORS = {
    'Apple':     '#e2e8f0',
    'Microsoft': '#38bdf8',
    'Google':    '#fbbf24',
    'Amazon':    '#fb923c',
    'Meta':      '#818cf8',
    'NVIDIA':    '#86efac',
    'Tesla':     '#f87171',
    'Netflix':   '#fb7185',
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
        unsafe_allow_html=True
    )

def glass_card(html, padding="1.4rem 1.6rem"):
    st.markdown(
        f'<div class="glass-panel" style="padding:{padding};">{html}</div>',
        unsafe_allow_html=True
    )

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
    st.markdown("""
    <div class="logo-wrap">
      <div style="font-size:1.8rem;margin-bottom:0.3rem;">🚀</div>
      <div class="logo-text">MARKET NEXUS</div>
      <div class="logo-sub">BIG TECH INTELLIGENCE · v5.0</div>
      <div class="logo-badge">
        <span class="live"></span>
        <span class="logo-badge-text">LIVE · 8 COMPANIES · yfinance</span>
      </div>
    </div>
    <div class="h-divider"></div>
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

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.6rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--txt3);margin-bottom:0.5rem;padding:0 0.2rem;">Companies</div>', unsafe_allow_html=True)
    sel_companies = st.multiselect("", ALL_COMPANIES, default=ALL_COMPANIES, label_visibility="hidden")
    if not sel_companies: sel_companies = ALL_COMPANIES

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.6rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--txt3);margin-bottom:0.5rem;padding:0 0.2rem;">Year Range</div>', unsafe_allow_html=True)
    slider_min = int(ann_df['Year'].min()) if not ann_df.empty else 2020
    slider_max = COMMON_LATEST_YEAR
    year_range = st.slider("", slider_min, slider_max, (slider_min, slider_max), label_visibility="hidden")

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    data_src = "yfinance LIVE" if (_live_ok and not ann_df.empty) else "CSV Fallback"
    companies_in_latest = ann_df[ann_df.Year == COMMON_LATEST_YEAR]['Company'].nunique()
    price_latest_date = price_df['Date'].max().strftime("%Y-%m-%d") if not price_df.empty else "—"
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:var(--txt3);line-height:2.2;padding:0 0.2rem;">
      <div>🕐 {datetime.now().strftime("%H:%M:%S")}</div>
      <div>📡 {data_src}</div>
      <div>📅 YEAR: {COMMON_LATEST_YEAR} ({companies_in_latest}/8)</div>
      <div>📈 PRICES TO: {price_latest_date}</div>
      <div>🗂 RECORDS: {len(q_df)+len(ann_df)+len(price_df):,}</div>
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
ticker_display = " &nbsp;·&nbsp; ".join([
    f'<span class="sym">{s}</span>'
    for s in ticker_symbols * 2
])
st.markdown(f"""
<div class="ticker-wrap">
  <div class="ticker-inner">
    {ticker_display} &nbsp;&nbsp;&nbsp; {ticker_display}
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: COMMAND CENTER
# ════════════════════════════════════════════════════════════════════════════
if "Command Center" in page:

    st.markdown("""
    <div class="hero animate-in">
      <div class="hero-glow1"></div>
      <div class="hero-glow2"></div>
      <div class="hero-glow3"></div>
      <div style="position:relative;z-index:1;">
        <div class="hero-eyebrow">⚡ Live Big Tech Intelligence Platform</div>
        <p class="hero-title">MARKET NEXUS</p>
        <p class="hero-sub">
          Real-time financial intelligence across
          <strong style="color:#00d4ff;">Apple · Microsoft · Google ·
          Amazon · Meta · NVIDIA · Tesla · Netflix</strong> —
          powered by yfinance live feeds, real earnings & competitive benchmarks.
        </p>
        <div class="hero-chips">
          <span class="chip">📊 Live Earnings</span>
          <span class="chip orange">📈 Real Stock History</span>
          <span class="chip green">🏆 Competitive Intel</span>
          <span class="chip purple">💡 AI Insights</span>
          <span class="chip green">📡 Live Prices</span>
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
      <div class="kpi animate-in">
        <div class="kpi-stripe"></div>
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Combined Revenue (TTM)</div>
        <div class="kpi-val">${total_rev/1000:.2f}T</div>
        <div class="kpi-sub">{len(sel_companies)} companies · {data_label}</div>
        <div class="kpi-badge up">↑ LIVE</div>
      </div>
      <div class="kpi animate-in">
        <div class="kpi-stripe orange"></div>
        <div class="kpi-icon">🏦</div>
        <div class="kpi-label">Combined Market Cap</div>
        <div class="kpi-val orange">${total_mcap/1000:.1f}T</div>
        <div class="kpi-sub">{data_label}</div>
        <div class="kpi-badge up">↑ LIVE</div>
      </div>
      <div class="kpi animate-in">
        <div class="kpi-stripe green"></div>
        <div class="kpi-icon">🥇</div>
        <div class="kpi-label">Largest by Market Cap</div>
        <div class="kpi-val green">{top_mcap_co}</div>
        <div class="kpi-sub">${top_mcap:,.0f}B cap</div>
        <div class="kpi-badge flat">LIVE</div>
      </div>
      <div class="kpi animate-in">
        <div class="kpi-stripe purple"></div>
        <div class="kpi-icon">⚡</div>
        <div class="kpi-label">NVIDIA Net Income (TTM)</div>
        <div class="kpi-val purple">${nvda_ni:.1f}B</div>
        <div class="kpi-sub">AI boom · {data_label}</div>
        <div class="kpi-badge up">↑ LIVE</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    sec("Revenue Race & Market Cap", "LIVE yfinance DATA")
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        for co in sel_companies:
            sub = q_f[q_f.Company == co].sort_values('Quarter')
            if sub.empty: continue
            fig.add_trace(go.Scatter(
                x=sub.Quarter, y=sub.Revenue_B, name=co, mode='lines',
                line=dict(color=COLORS[co], width=2.5),
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>${{y:.1f}}B<extra></extra>'))
        sf(fig, 350).update_layout(
            title=dict(text="Quarterly Revenue ($B) — Live Earnings", font=dict(size=12, color='#7a92bb')),
            yaxis_title="Revenue ($B)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        mc_data = ann_f.pivot(index='Year', columns='Company', values='MarketCap_B').fillna(0)
        fig = go.Figure()
        for co in [c for c in sel_companies if c in mc_data.columns]:
            fig.add_trace(go.Bar(
                x=mc_data.index, y=mc_data[co], name=co,
                marker_color=COLORS[co], opacity=0.85,
                hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:,.0f}}B<extra></extra>'))
        fig.update_layout(barmode='group')
        sf(fig, 350).update_layout(
            title=dict(text="Market Capitalization by Year ($B)", font=dict(size=12, color='#7a92bb')),
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
            fig.add_trace(go.Scatter(
                x=sub.Date, y=sub.Price / base * 100, name=co, mode='lines',
                line=dict(color=COLORS[co], width=2),
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>%{{y:.0f}}<extra></extra>'))
        fig.add_hline(y=100, line_dash='dot', line_color='rgba(255,255,255,0.1)')
        sf(fig, 340).update_layout(
            title=dict(text="Normalised Stock Performance (Base=100)", font=dict(size=12, color='#7a92bb')),
            yaxis_title="Indexed Return")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        margin_sl, m_yr = get_latest_slice(ann_df, sel_companies)
        margin_sl['Margin'] = (margin_sl.NetIncome_B / margin_sl.Revenue_B * 100).round(1)
        margin_sl = margin_sl.sort_values('Margin')
        fig = go.Figure(go.Bar(
            x=margin_sl.Margin, y=margin_sl.Company, orientation='h',
            marker=dict(color=margin_sl.Margin,
                        colorscale=[[0, '#ff3366'], [0.4, '#ff6b35'], [1, '#00ff9d']],
                        line=dict(width=0)),
            text=[f"{v:.1f}%" for v in margin_sl.Margin],
            textposition='outside', textfont=dict(size=10, color='#7a92bb'),
            hovertemplate='<b>%{y}</b><br>Margin: %{x:.1f}%<extra></extra>'))
        sf(fig, 340, legend=False).update_layout(
            title=dict(text=f"Net Profit Margin {m_yr}", font=dict(size=12, color='#7a92bb')),
            xaxis_title="Net Margin %")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    sec("Revenue Distribution & Headcount", "STRUCTURAL VIEW")
    c1, c2 = st.columns(2)
    with c1:
        treemap_sl, t_yr = get_latest_slice(ann_df, sel_companies)
        if not treemap_sl.empty:
            fig = px.treemap(
                treemap_sl, path=['Sector', 'Company'], values='Revenue_B',
                color='NetIncome_B',
                color_continuous_scale=[[0, '#ff3366'], [0.5, '#0a0d22'], [1, '#00ff9d']],
                hover_data={'Revenue_B': ':.1f', 'NetIncome_B': ':.1f'})
            fig.update_traces(
                textfont_size=13, textfont_color='white',
                hovertemplate='<b>%{label}</b><br>Revenue: $%{value:.1f}B<extra></extra>')
            fig.update_layout(
                **PL, height=330,
                title=dict(text=f"Revenue Treemap {t_yr} — Color=Net Income", font=dict(size=12, color='#7a92bb')),
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
            text=[f"${v:.2f}M" for v in emp_sl.RevPerEmp],
            textposition='outside', textfont=dict(size=10, color='#7a92bb'),
            hovertemplate='<b>%{y}</b><br>$%{x:.2f}M per employee<extra></extra>'))
        sf(fig, 330, legend=False).update_layout(
            title=dict(text=f"Revenue per Employee {e_yr} ($M)", font=dict(size=12, color='#7a92bb')),
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
                                 line=dict(color='rgba(0,212,255,0.2)', width=1, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.Lower, name='BB Lower',
                                 fill='tonexty', fillcolor='rgba(0,212,255,0.04)',
                                 line=dict(color='rgba(0,212,255,0.2)', width=1, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.Price, name='Price',
                                 line=dict(color=COLORS[co1], width=2.5),
                                 hovertemplate='<b>' + co1 + '</b><br>%{x|%b %d,%Y}<br>$%{y:.2f}<extra></extra>'))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.MA50, name='MA50',
                                 line=dict(color='#fbbf24', width=1.5, dash='dot')))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.MA200, name='MA200',
                                 line=dict(color='#b06ef3', width=1.5, dash='dash')))
        sf(fig, 420).update_layout(
            title=dict(text=f"{co1} — Price + Bollinger Bands + MAs", font=dict(size=12, color='#7a92bb')),
            yaxis_title="Price (USD)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        fig2 = go.Figure(go.Bar(x=sub.Date, y=sub.Volume_M, marker_color=COLORS[co1], opacity=0.4, name='Volume'))
        sf(fig2, 120, legend=False).update_layout(yaxis_title="Volume (M)", margin=dict(t=10))
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab2:
        fig = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f.Company == co].sort_values('Date')
            if sub.empty: continue
            vol = sub.Daily_Return.rolling(30).std()
            fig.add_trace(go.Scatter(
                x=sub.Date, y=vol, name=co, mode='lines',
                line=dict(color=COLORS[co], width=1.8),
                hovertemplate=f'<b>{co}</b> %{{x|%b %Y}}<br>Vol: %{{y:.2f}}%<extra></extra>'))
        sf(fig, 340).update_layout(
            title=dict(text="30-Day Rolling Volatility", font=dict(size=12, color='#7a92bb')),
            yaxis_title="Volatility (%)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        stats = p_f.groupby('Company').agg(
            Avg_Return=('Daily_Return', 'mean'),
            Volatility=('Daily_Return', 'std')).reset_index()
        total_return = p_f.groupby('Company').apply(
            lambda g: (g.sort_values('Date').Price.iloc[-1] / g.sort_values('Date').Price.iloc[0] - 1) * 100
        ).reset_index(name='Total_Return_Pct')
        stats = stats.merge(total_return, on='Company')
        fig2 = go.Figure()
        for _, row in stats.iterrows():
            fig2.add_trace(go.Scatter(
                x=[row.Volatility], y=[row.Total_Return_Pct], mode='markers+text',
                name=row.Company, text=[row.Company],
                textposition='top center', textfont=dict(size=10, color=COLORS[row.Company]),
                marker=dict(size=18, color=COLORS[row.Company],
                            line=dict(width=2, color='rgba(255,255,255,0.2)')),
                hovertemplate=f'<b>{row.Company}</b><br>Vol:{row.Volatility:.2f}%<br>Return:{row.Total_Return_Pct:.0f}%<extra></extra>'))
        fig2.add_hline(y=0, line_dash='dot', line_color='rgba(255,255,255,0.08)')
        fig2.add_vline(x=stats.Volatility.mean(), line_dash='dot', line_color='rgba(255,255,255,0.08)')
        sf(fig2, 340).update_layout(
            title=dict(text="Risk vs Total Return", font=dict(size=12, color='#7a92bb')),
            xaxis_title="Daily Volatility (Std Dev %)", yaxis_title="Total Return %", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        p_f2 = p_f.copy(); p_f2['Year'] = p_f2.Date.dt.year
        annual_ret = p_f2.groupby(['Company', 'Year']).apply(
            lambda g: (g.sort_values('Date').Price.iloc[-1] / g.sort_values('Date').Price.iloc[0] - 1) * 100
        ).reset_index(name='Annual_Return')
        pivot = annual_ret.pivot(index='Company', columns='Year', values='Annual_Return')
        fig = go.Figure(go.Heatmap(
            z=pivot.values, x=[str(c) for c in pivot.columns], y=list(pivot.index),
            colorscale=[[0, '#ff3366'], [0.45, '#0a0d22'], [1, '#00ff9d']], zmid=0,
            text=[[f"{v:.0f}%" if not np.isnan(v) else "" for v in row] for row in pivot.values],
            texttemplate='%{text}', textfont=dict(size=11),
            hovertemplate='<b>%{y}</b> %{x}<br>Return: %{z:.1f}%<extra></extra>'))
        sf(fig, 360, legend=False).update_layout(
            title=dict(text="Annual Stock Return % — All Companies", font=dict(size=12, color='#7a92bb')))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        fig2 = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f.Company == co]
            if sub.empty: continue
            fig2.add_trace(go.Violin(
                x=[co] * len(sub), y=sub.Daily_Return, name=co,
                box_visible=True, meanline_visible=True,
                fillcolor=hex_to_rgba(COLORS[co], 0.19),
                line_color=COLORS[co], opacity=0.85,
                hovertemplate=f'<b>{co}</b><br>%{{y:.3f}}%<extra></extra>'))
        sf(fig2, 340).update_layout(
            title=dict(text="Daily Return Distribution", font=dict(size=12, color='#7a92bb')),
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
        fig.add_trace(go.Bar(
            x=sub.Quarter, y=sub.Revenue_B, name='Revenue ($B)',
            marker_color=COLORS[co2], opacity=0.85,
            hovertemplate='%{x|%b %Y}<br>$%{y:.1f}B<extra></extra>'), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=sub.Quarter, y=sub.Revenue_B.rolling(4).mean(), name='4Q Avg',
            line=dict(color='#fbbf24', width=2, dash='dot')), row=1, col=1)
        fig.add_trace(go.Bar(
            x=sub.Quarter, y=sub.YoY, name='YoY %',
            marker_color=['#00ff9d' if v >= 0 else '#ff3366' for v in sub.YoY.fillna(0)],
            hovertemplate='%{x|%b %Y}<br>YoY: %{y:.1f}%<extra></extra>'), row=2, col=1)
        sf(fig, 440).update_layout(
            title=dict(text=f"{co2} — Quarterly Revenue + YoY Growth", font=dict(size=12, color='#7a92bb')))
        fig.update_yaxes(title_text="Revenue ($B)", row=1, col=1)
        fig.update_yaxes(title_text="YoY %", row=2, col=1)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with tab2:
        yr_min = int(ann_df.Year.min())
        yr_max = COMMON_LATEST_YEAR
        cagr_rows = []
        for co in sel_companies:
            sub = ann_df[(ann_df.Company == co) & (ann_df.Year.isin([yr_min, yr_max]))].sort_values('Year')
            if len(sub) == 2:
                r0, r1 = sub.Revenue_B.iloc[0], sub.Revenue_B.iloc[1]
                n = yr_max - yr_min
                cagr = ((r1 / r0) ** (1 / n) - 1) * 100 if n > 0 else 0
                cagr_rows.append({'Company': co, 'CAGR': round(cagr, 1)})
        cagr_df = pd.DataFrame(cagr_rows).sort_values('CAGR')
        c1, c2 = st.columns(2)
        with c1:
            if not cagr_df.empty:
                fig = go.Figure(go.Bar(
                    x=cagr_df.CAGR, y=cagr_df.Company, orientation='h',
                    marker=dict(color=[COLORS[c] for c in cagr_df.Company], line=dict(width=0)),
                    text=[f"{v:.1f}%" for v in cagr_df.CAGR],
                    textposition='outside', textfont=dict(size=11, color='#7a92bb'),
                    hovertemplate='<b>%{y}</b><br>CAGR: %{x:.1f}%<extra></extra>'))
                sf(fig, 340, legend=False).update_layout(
                    title=dict(text=f"Revenue CAGR {yr_min}–{yr_max}", font=dict(size=12, color='#7a92bb')),
                    xaxis_title="CAGR %")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with c2:
            fig2 = go.Figure()
            for co in sel_companies:
                sub2 = ann_f[ann_f.Company == co].sort_values('Year')
                if sub2.empty: continue
                fig2.add_trace(go.Scatter(
                    x=sub2.Year, y=sub2.Revenue_B, name=co,
                    mode='lines+markers', stackgroup='one',
                    fillcolor=hex_to_rgba(COLORS[co], 0.33),
                    line=dict(color=COLORS[co], width=1.5),
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:.1f}}B<extra></extra>'))
            sf(fig2, 340).update_layout(
         