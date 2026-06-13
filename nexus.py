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
                title=dict(text="Stacked Annual Revenue ($B)", font=dict(size=12, color='#7a92bb')),
                yaxis_title="Revenue ($B)")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        ni_data = ann_f.pivot(index='Year', columns='Company', values='NetIncome_B').fillna(0)
        fig = go.Figure()
        for co in [c for c in sel_companies if c in ni_data.columns]:
            fig.add_trace(go.Scatter(
                x=ni_data.index, y=ni_data[co], name=co, mode='lines+markers',
                line=dict(color=COLORS[co], width=2.5),
                marker=dict(size=8, color=COLORS[co], line=dict(width=2, color='rgba(0,0,0,0.4)')),
                hovertemplate=f'<b>{co}</b> %{{x}}<br>Net Income: $%{{y:.1f}}B<extra></extra>'))
        fig.add_hline(y=0, line_dash='dot', line_color='rgba(255,255,255,0.1)')
        sf(fig, 360).update_layout(
            title=dict(text="Net Income — All Companies", font=dict(size=12, color='#7a92bb')),
            yaxis_title="Net Income ($B)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        c1, c2 = st.columns(2)
        with c1:
            avail_years = sorted(ann_df[ann_df.Company.isin(sel_companies)]['Year'].unique().tolist(), reverse=True)
            yr = st.selectbox("Year", avail_years, key='yr_ni')
            sub3 = ann_df[(ann_df.Year == yr) & (ann_df.Company.isin(sel_companies))]
            fig2 = go.Figure()
            for _, row in sub3.iterrows():
                fig2.add_trace(go.Scatter(
                    x=[row.Revenue_B], y=[row.NetIncome_B],
                    mode='markers+text', name=row.Company,
                    text=[row.Company], textposition='top center',
                    textfont=dict(size=10, color=COLORS[row.Company]),
                    marker=dict(size=16, color=COLORS[row.Company],
                                line=dict(width=2, color='rgba(255,255,255,0.15)')),
                    showlegend=False))
            sf(fig2, 320, legend=False).update_layout(
                title=dict(text=f"Revenue vs Net Income {yr}", font=dict(size=12, color='#7a92bb')),
                xaxis_title="Revenue ($B)", yaxis_title="Net Income ($B)")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        with c2:
            ni_ch = ann_df[ann_df.Company.isin(sel_companies)].sort_values(['Company', 'Year']).copy()
            ni_ch['NI_Change'] = ni_ch.groupby('Company')['NetIncome_B'].diff()
            ni_latest_sl, ni_yr = get_latest_slice(ni_ch, sel_companies)
            ni_latest_sl = ni_latest_sl.sort_values('NI_Change')
            fig3 = go.Figure(go.Bar(
                x=ni_latest_sl.NI_Change, y=ni_latest_sl.Company, orientation='h',
                marker=dict(
                    color=['#00ff9d' if v >= 0 else '#ff3366' for v in ni_latest_sl.NI_Change.fillna(0)],
                    line=dict(width=0)),
                text=[f"${v:+.1f}B" for v in ni_latest_sl.NI_Change.fillna(0)],
                textposition='outside', textfont=dict(size=10, color='#7a92bb'),
                hovertemplate='<b>%{y}</b><br>Change: $%{x:+.1f}B<extra></extra>'))
            sf(fig3, 320, legend=False).update_layout(
                title=dict(text=f"Net Income YoY Change {ni_yr}", font=dict(size=12, color='#7a92bb')))
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

    metrics = ['Revenue_B', 'NetIncome_B', 'MarketCap_B', 'Margin', 'RevPerEmp']
    labels  = ['Revenue ($B)', 'Net Income ($B)', 'Market Cap ($B)', 'Net Margin %', 'Rev/Emp $M']
    norm = ann_latest.set_index('Company')[metrics].copy()
    for col in metrics:
        norm[col] = (norm[col] - norm[col].min()) / (norm[col].max() - norm[col].min() + 1e-9) * 10

    fig = go.Figure()
    for co in sel_companies:
        if co not in norm.index: continue
        vals = list(norm.loc[co].values) + [norm.loc[co].values[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=labels + [labels[0]], name=co, fill='toself',
            fillcolor=hex_to_rgba(COLORS[co], 0.15),
            line=dict(color=COLORS[co], width=2),
            hovertemplate=f'<b>{co}</b><br>%{{theta}}: %{{r:.1f}}/10<extra></extra>'))
    fig.update_layout(
        **PL, height=480,
        polar=dict(bgcolor='rgba(0,0,0,0)',
                   radialaxis=dict(visible=True, range=[0, 10],
                                   gridcolor='rgba(255,255,255,0.06)',
                                   tickfont=dict(size=8, color='#2d3f5a')),
                   angularaxis=dict(gridcolor='rgba(255,255,255,0.06)',
                                    tickfont=dict(size=10, color='#7a92bb'))),
        title=dict(text=f"Competitive Radar {latest_yr} — 5 Dimensions (0–10)",
                   font=dict(size=12, color='#7a92bb')))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    c1, c2 = st.columns(2)
    with c1:
        sec("Rankings Board", f"{latest_yr} LIVE")
        ann_rs = ann_latest.sort_values('MarketCap_B', ascending=False)
        medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
        html = ""
        for i, (_, row) in enumerate(ann_rs.iterrows()):
            html += (
                f'<div class="rank-row">'
                f'<div class="rank-num">{medals[i] if i < len(medals) else i+1}</div>'
                f'<div style="width:12px;height:12px;border-radius:50%;background:{COLORS[row.Company]};flex-shrink:0;"></div>'
                f'<div class="rank-name">{row.Company}</div>'
                f'<div class="rank-val">${row.MarketCap_B:,.0f}B</div>'
                f'</div>'
            )
        st.markdown(
            f'<div class="glass-panel">'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.6rem;color:var(--txt3);letter-spacing:0.1em;margin-bottom:0.8rem;">RANKED BY MARKET CAP · {latest_yr}</div>'
            f'{html}</div>',
            unsafe_allow_html=True)

    with c2:
        sec("Price/Sales Ratio", "LIVE P/S")
        ann_ps = ann_latest.copy()
        ann_ps['PS_Ratio'] = ann_ps.MarketCap_B / ann_ps.Revenue_B
        ann_ps = ann_ps.sort_values('PS_Ratio')
        fig = go.Figure(go.Bar(
            x=ann_ps.PS_Ratio, y=ann_ps.Company, orientation='h',
            marker=dict(color=[COLORS[c] for c in ann_ps.Company], line=dict(width=0)),
            text=[f"{v:.1f}x" for v in ann_ps.PS_Ratio],
            textposition='outside', textfont=dict(size=11, color='#7a92bb'),
            hovertemplate='<b>%{y}</b><br>P/S: %{x:.1f}x<extra></extra>'))
        sf(fig, 330, legend=False).update_layout(
            title=dict(text=f"Price/Sales Ratio {latest_yr}", font=dict(size=12, color='#7a92bb')),
            xaxis_title="P/S Ratio")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    sec("Employees vs Revenue — Efficiency Matrix", "ANIMATED")
    ann_all = ann_f.copy()
    ann_all['RevPerEmp'] = (ann_all.Revenue_B * 1e9 / (ann_all.Employees_K * 1e3) / 1e6).round(2)
    if not ann_all.empty:
        fig = px.scatter(
            ann_all, x='Employees_K', y='Revenue_B', color='Company',
            size='MarketCap_B', animation_frame='Year',
            color_discrete_map=COLORS, size_max=60,
            hover_data={'NetIncome_B': ':.1f', 'RevPerEmp': ':.2f'})
        fig.update_layout(
            **PL, height=400,
            title=dict(text="Employees vs Revenue (bubble=Market Cap) — Animated",
                       font=dict(size=12, color='#7a92bb')),
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
        price_pivot = price_df[price_df.Company.isin(sel_companies)].pivot(
            index='Date', columns='Company', values='Daily_Return').dropna()
        corr = price_pivot.corr()
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=list(corr.columns), y=list(corr.index),
            colorscale=[[0, '#ff3366'], [0.5, '#0a0d22'], [1, '#00d4ff']],
            zmid=0, zmin=-1, zmax=1,
            text=np.round(corr.values, 2), texttemplate='%{text}', textfont_size=11,
            hovertemplate='<b>%{y} × %{x}</b><br>Correlation: %{z:.2f}<extra></extra>'))
        sf(fig, 420, legend=False).update_layout(
            title=dict(text="Daily Return Correlation", font=dict(size=12, color='#7a92bb')))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        c1, c2 = st.columns(2)
        with c1: co_a = st.selectbox("Company A", sel_companies, index=0, key='ca')
        with c2: co_b = st.selectbox("Company B", sel_companies, index=min(1, len(sel_companies) - 1), key='cb')
        if co_a != co_b and co_a in price_pivot.columns and co_b in price_pivot.columns:
            pair = price_pivot[[co_a, co_b]].dropna()
            corr_val = pair[co_a].corr(pair[co_b])
            slope, intercept, r, p, se = scipy_stats.linregress(pair[co_a], pair[co_b])
            x_range = np.linspace(pair[co_a].min(), pair[co_a].max(), 100)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=pair[co_a], y=pair[co_b], mode='markers',
                marker=dict(size=3, color='rgba(0,212,255,0.35)'),
                hovertemplate=f'{co_a}: %{{x:.2f}}%<br>{co_b}: %{{y:.2f}}%<extra></extra>',
                name='Daily Returns'))
            fig2.add_trace(go.Scatter(
                x=x_range, y=slope * x_range + intercept, mode='lines',
                line=dict(color='#ff6b35', width=2, dash='dash'),
                name=f'Fit (r={corr_val:.2f})'))
            sf(fig2, 340).update_layout(
                title=dict(text=f"{co_a} vs {co_b} — r={corr_val:.3f} | p={p:.2e}",
                           font=dict(size=12, color='#7a92bb')),
                xaxis_title=f"{co_a} Daily Return %", yaxis_title=f"{co_b} Daily Return %")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab2:
        sec("Normality Tests & Distribution Stats", "LIVE DATA")
        stats_rows = []
        for co in sel_companies:
            rets = price_df[price_df.Company == co]['Daily_Return'].dropna()
            if len(rets) < 10: continue
            stat, p_sh = scipy_stats.shapiro(rets.sample(min(5000, len(rets)), random_state=42))
            stats_rows.append({
                'Company': co, 'Mean (%)': round(rets.mean(), 4),
                'Std Dev (%)': round(rets.std(), 4),
                'Skewness': round(scipy_stats.skew(rets), 3),
                'Kurtosis': round(scipy_stats.kurtosis(rets), 3),
                'Shapiro-Wilk p': f'{p_sh:.4f}',
                'Normal?': '✅ Yes' if p_sh > 0.05 else '❌ No',
                'Min (%)': round(rets.min(), 3), 'Max (%)': round(rets.max(), 3)})
        if stats_rows:
            st.dataframe(pd.DataFrame(stats_rows).set_index('Company'), use_container_width=True)

        co_qq = st.selectbox("Q-Q Plot for:", sel_companies, key='qq')
        rets_qq = price_df[price_df.Company == co_qq]['Daily_Return'].dropna()
        theo = scipy_stats.norm.ppf(np.linspace(0.01, 0.99, len(rets_qq)))
        sample_q = np.sort(rets_qq.values)[:len(theo)]
        theo = theo[:len(sample_q)]
        mu, sig = rets_qq.mean(), rets_qq.std()
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=theo, y=sample_q, mode='markers',
                marker=dict(size=3, color=COLORS[co_qq], opacity=0.5), name='Q-Q'))
            fig.add_trace(go.Scatter(
                x=[theo.min(), theo.max()],
                y=[theo.min() * sig + mu, theo.max() * sig + mu],
                mode='lines', line=dict(color='#ff6b35', width=2, dash='dash'), name='Normal'))
            sf(fig, 300).update_layout(
                title=dict(text=f"{co_qq} — Q-Q Plot", font=dict(size=12, color='#7a92bb')),
                xaxis_title="Theoretical", yaxis_title="Sample")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with c2:
            fig2 = go.Figure()
            fig2.add_trace(go.Histogram(
                x=rets_qq, nbinsx=80, name='Returns',
                marker=dict(color=hex_to_rgba(COLORS[co_qq], 0.5),
                            line=dict(color=COLORS[co_qq], width=0.5))))
            x_n = np.linspace(rets_qq.min(), rets_qq.max(), 200)
            fig2.add_trace(go.Scatter(
                x=x_n,
                y=scipy_stats.norm.pdf(x_n, mu, sig) * len(rets_qq) * (rets_qq.max() - rets_qq.min()) / 80,
                mode='lines', line=dict(color='#ff6b35', width=2, dash='dot'), name='Normal Fit'))
            sf(fig2, 300).update_layout(
                title=dict(text=f"{co_qq} Return Distribution", font=dict(size=12, color='#7a92bb')),
                yaxis_title="Count")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        sec("Drawdown Analysis — Peak-to-Trough", "LIVE DATA")
        fig = go.Figure()
        for co in sel_companies:
            sub = price_df[price_df.Company == co].sort_values('Date')
            if sub.empty: continue
            roll_max = sub.Price.cummax()
            drawdown = (sub.Price - roll_max) / roll_max * 100
            fig.add_trace(go.Scatter(
                x=sub.Date, y=drawdown, name=co,
                line=dict(color=COLORS[co], width=1.5),
                hovertemplate=f'<b>{co}</b> %{{x|%b %Y}}<br>Drawdown: %{{y:.1f}}%<extra></extra>'))
        sf(fig, 380).update_layout(
            title=dict(text="Maximum Drawdown from Peak", font=dict(size=12, color='#7a92bb')),
            yaxis_title="Drawdown %")
        fig.add_hrect(y0=-100, y1=-30, fillcolor="rgba(255,51,102,0.04)", line_width=0)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════════════
# PAGE: AI INSIGHT ENGINE
# ════════════════════════════════════════════════════════════════════════════
elif "AI Insight" in page:
    st.markdown('<p class="page-title">🤖 AI Insight Engine</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-panel" style="border-left:3px solid var(--cyan);margin-bottom:1.5rem;">
      <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;
                  color:var(--cyan);margin-bottom:0.6rem;">⚡ Auto-Generated Insights from Live Data</div>
      <div style="color:var(--txt2);font-size:0.9rem;line-height:1.75;">
        Insights computed directly from live yfinance earnings & stock data across all 8 companies.
        Updated automatically every session with fresh market data.
      </div>
    </div>
    """, unsafe_allow_html=True)

    ai_latest, ai_yr = get_latest_slice(ann_df, ALL_COMPANIES)
    ai_first, ai_fy  = get_latest_slice(
        ann_df[ann_df.Year == ann_df.Year.min()], ALL_COMPANIES,
        fallback_year=int(ann_df.Year.min()))
    ai_idx   = ai_latest.set_index('Company')
    ai_f_idx = ai_first.set_index('Company')

    insights = []
    for co, color, label in [
        ('NVIDIA',    '#86efac', '🚀 NVIDIA AI Supercycle'),
        ('Meta',      '#818cf8', '💎 Meta Efficiency Era'),
        ('Apple',     '#e2e8f0', '🍎 Apple Revenue Machine'),
        ('Amazon',    '#fb923c', '📦 Amazon Profit Inflection'),
        ('Microsoft', '#38bdf8', '☁️ Microsoft Cloud Dominance'),
    ]:
        try:
            row = ai_idx.loc[co]
            mgn = row.NetIncome_B / row.Revenue_B * 100
            insights.append((
                label, color,
                f"<b style='color:{color};'>{co}</b> — Revenue: <b style='color:{color};'>${row.Revenue_B:.1f}B</b> · "
                f"Net Income: <b style='color:{color};'>${row.NetIncome_B:.1f}B</b> · "
                f"Net Margin: <b style='color:{color};'>{mgn:.1f}%</b> ({ai_yr})"
            ))
        except: pass

    try:
        tsla_vol = price_df[price_df.Company == 'Tesla']['Daily_Return'].std()
        insights.append((
            '⚡ Tesla: Highest Volatility', '#f87171',
            f"Tesla daily return std dev: <b style='color:#f87171;'>{tsla_vol:.2f}%</b> — highest among all 8 companies."
        ))
    except: pass

    for title, color, body in insights:
        st.markdown(f"""
        <div class="insight-card" style="border-left-color:{color};">
          <div class="insight-title">{title}</div>
          <div class="insight-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)

    sec(f"Full Company Scorecard — {ai_yr}", "LIVE METRICS")
    score = ai_latest[ai_latest.Company.isin(sel_companies)].copy()
    score['Net_Margin_%']  = (score.NetIncome_B / score.Revenue_B * 100).round(1)
    score['Rev_per_Emp_M'] = (score.Revenue_B * 1e9 / (score.Employees_K * 1e3) / 1e6).round(2)
    score['PS_Ratio']      = (score.MarketCap_B / score.Revenue_B).round(1)
    if not fund_df.empty:
        for _, fr in fund_df.iterrows():
            mask = score.Company == fr['Company']
            if mask.any(): score.loc[mask, 'MarketCap_B'] = fr['marketCap_B']
    disp = score[['Company', 'Sector', 'Revenue_B', 'NetIncome_B', 'MarketCap_B',
                  'Employees_K', 'Net_Margin_%', 'Rev_per_Emp_M', 'PS_Ratio']].sort_values('MarketCap_B', ascending=False)
    disp.columns = ['Company', 'Sector', 'Revenue ($B)', 'Net Income ($B)', 'Market Cap ($B)',
                    'Employees (K)', 'Net Margin %', 'Rev/Employee ($M)', 'P/S Ratio']
    st.dataframe(disp.set_index('Company'), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: LIVE DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
elif "Live Dashboard" in page:
    if not _live_ok:
        st.error("⚠️ `live_data.py` not found.")
        st.stop()

    st.markdown("""
    <div class="hero" style="padding:2.2rem 2.8rem;margin-bottom:1.5rem;">
      <div class="hero-glow1"></div>
      <div class="hero-glow2"></div>
      <div style="position:relative;z-index:1;">
        <div class="hero-eyebrow">📡 yfinance · auto-refresh · intraday data</div>
        <p class="hero-title" style="font-size:2.8rem;">Live Dashboard</p>
        <p class="hero-sub">Real-time intraday prices for all 8 Big Tech companies — auto-refreshes every 60 seconds.</p>
        <div class="hero-chips">
          <span class="chip green">🟢 Live Prices</span>
          <span class="chip">⏱ 60s Auto-Refresh</span>
          <span class="chip orange">📈 5-min Intraday</span>
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
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;color:var(--txt3);margin-bottom:1.2rem;">'
        f'<span class="live"></span> Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} · Data via yfinance (15-min delayed)</div>',
        unsafe_allow_html=True)

    @st.cache_data(ttl=30)
    def fetch_live_price(ticker): return get_live_price(ticker)

    @st.cache_data(ttl=300)
    def fetch_intraday(ticker, period="1d", interval="5m"):
        return get_intraday_data(ticker, period=period, interval=interval)

    ticker_map = {
        "Apple": "AAPL", "Microsoft": "MSFT", "Google": "GOOGL", "Amazon": "AMZN",
        "Meta": "META", "NVIDIA": "NVDA", "Tesla": "TSLA", "Netflix": "NFLX"
    }

    sec("Live Price Snapshot", "ALL 8 COMPANIES · 60s REFRESH")
    cols = st.columns(4)
    for idx, (name, ticker) in enumerate(ticker_map.items()):
        price, change, vol = fetch_live_price(ticker)
        col = cols[idx % 4]
        if price is not None:
            direction = "up" if change >= 0 else "down"
            arrow = "↑" if change >= 0 else "↓"
            color = "#00ff9d" if change >= 0 else "#ff3366"
            vol_str = (f"{vol/1e6:.1f}M" if vol and vol >= 1e6 else
                       (f"{vol/1e3:.0f}K" if vol else "—"))
            col.markdown(f"""
            <div class="kpi" style="margin-bottom:0.8rem;">
              <div class="kpi-stripe" style="background:linear-gradient(180deg,{color},transparent);"></div>
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <div class="kpi-label">{name}</div>
                  <div class="kpi-val" style="font-size:1.65rem;color:{color} !important;">${price:,.2f}</div>
                </div>
                <div style="text-align:right;">
                  <div class="kpi-badge {direction}">{arrow} {abs(change):.2f}%</div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:0.56rem;color:var(--txt3);margin-top:0.8rem;">{ticker}</div>
                </div>
              </div>
              <div class="kpi-sub">Vol: {vol_str}</div>
            </div>""", unsafe_allow_html=True)
        else:
            col.markdown(
                f'<div class="kpi" style="margin-bottom:0.8rem;">'
                f'<div class="kpi-stripe"></div>'
                f'<div class="kpi-label">{name} ({ticker})</div>'
                f'<div class="kpi-val" style="font-size:1.2rem;color:var(--txt3) !important;">—</div>'
                f'<div class="kpi-sub">Market closed or unavailable</div></div>',
                unsafe_allow_html=True)

    sec("Intraday Price Chart", "CANDLESTICK · TODAY")
    live_col1, live_col2 = st.columns([3, 1])
    with live_col2:
        selected_name   = st.selectbox("Company", list(ticker_map.keys()), key="live_co")
        interval_choice = st.selectbox("Interval", ["1m", "5m", "15m", "30m", "1h"], index=1, key="live_int")
        period_choice   = st.selectbox("Period", ["1d", "5d", "1mo"], index=0, key="live_per")

    selected_ticker = ticker_map[selected_name]
    df_intraday = fetch_intraday(selected_ticker, period=period_choice, interval=interval_choice)

    with live_col1:
        if df_intraday is not None and not df_intraday.empty:
            ticker_color = COMPANY_COLORS.get(selected_ticker, "#00d4ff")
            fig = go.Figure()
            if len(df_intraday) >= 10:
                fig.add_trace(go.Candlestick(
                    x=df_intraday.index,
                    open=df_intraday['Open'], high=df_intraday['High'],
                    low=df_intraday['Low'], close=df_intraday['Close'], name="OHLC",
                    increasing=dict(line=dict(color='#00ff9d'), fillcolor='rgba(0,255,157,0.3)'),
                    decreasing=dict(line=dict(color='#ff3366'), fillcolor='rgba(255,51,102,0.3)')))
            else:
                fig.add_trace(go.Scatter(
                    x=df_intraday.index, y=df_intraday['Close'],
                    mode='lines', line=dict(color=ticker_color, width=2.5)))
            sf(fig, 420).update_layout(
                title=dict(text=f"{selected_name} ({selected_ticker}) — {interval_choice} · {period_choice}",
                           font=dict(size=12, color='#7a92bb')),
                xaxis_title="Time", yaxis_title="Price (USD)", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            fig_vol = go.Figure(go.Bar(
                x=df_intraday.index, y=df_intraday['Volume'],
                marker_color=ticker_color, opacity=0.4))
            sf(fig_vol, 110, legend=False).update_layout(yaxis_title="Volume", margin=dict(t=4))
            st.plotly_chart(fig_vol, use_container_width=True, config={'displayModeBar': False})

            lp = df_intraday['Close'].iloc[-1]; op = df_intraday['Open'].iloc[0]
            dh = df_intraday['High'].max();     dl = df_intraday['Low'].min()
            dc = (lp - op) / op * 100;         tv = df_intraday['Volume'].sum()
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Last Price", f"${lp:.2f}", delta=f"{dc:+.2f}%")
            m2.metric("Day High", f"${dh:.2f}")
            m3.metric("Day Low", f"${dl:.2f}")
            m4.metric("Total Volume", f"{tv/1e6:.1f}M" if tv >= 1e6 else f"{tv/1e3:.0f}K")
        else:
            st.markdown("""
            <div class="glass-panel" style="text-align:center;border-color:rgba(255,107,53,0.3);">
              <div style="font-size:2.5rem;margin-bottom:0.5rem;">🌙</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:var(--orange);">
                Market Closed / No Intraday Data
              </div>
              <div style="color:var(--txt2);font-size:0.87rem;margin-top:0.5rem;">
                US markets open Mon–Fri 9:30am–4:00pm ET.<br>Try switching Period to "5d".
              </div>
            </div>""", unsafe_allow_html=True)

    sec("Live Price Comparison Table", "ALL COMPANIES")

    @st.cache_data(ttl=60)
    def fetch_all_prices():
        rows = []
        for name, ticker in ticker_map.items():
            price, change, vol = get_live_price(ticker)
            rows.append({
                "Company": name, "Ticker": ticker,
                "Price (USD)": f"${price:,.2f}" if price else "—",
                "Change %": f"{change:+.2f}%" if change is not None else "—",
                "Volume": (f"{vol/1e6:.1f}M" if vol and vol >= 1e6 else
                           (f"{vol/1e3:.0f}K" if vol else "—")),
                "Direction": "🟢" if (change or 0) >= 0 else "🔴"
            })
        return pd.DataFrame(rows)

    st.dataframe(fetch_all_prices().set_index("Company"), use_container_width=True, height=320)
    st.markdown(
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.58rem;color:var(--txt3);'
        'margin-top:1rem;border-top:1px solid var(--border);padding-top:0.8rem;">'
        '📡 Live data powered by yfinance · Prices delayed up to 15 minutes during market hours</div>',
        unsafe_allow_html=True)


# ── PREMIUM FOOTER ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="
  border-top: 1px solid var(--border);
  margin-top: 4rem;
  padding-top: 1.5rem;
  text-align: center;
">
  <div style="
    font-family:'Syne',sans-serif;
    font-size:1.1rem;
    font-weight:700;
    background:linear-gradient(110deg,#00d4ff,#ff6b35);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    margin-bottom:0.5rem;
  ">MARKET NEXUS</div>
  <div style="
    font-family:'JetBrains Mono',monospace;
    font-size:0.58rem;
    color:var(--txt3);
    letter-spacing:0.1em;
    line-height:2;
  ">
    Built by Jyotheeswar Gudipalli &nbsp;·&nbsp; Manipal University Jaipur · B.Tech Data Science 2027
    <br>Data: yfinance Live Feed · Public Earnings Reports · SEC Filings
    <br>
    <span style="color:var(--border2);">v5.0 &nbsp;·&nbsp; Powered by Streamlit &amp; Plotly</span>
  </div>
</div>
""", unsafe_allow_html=True)
