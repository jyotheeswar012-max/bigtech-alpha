"""
╔══════════════════════════════════════════════════════════════════╗
║  MARKET NEXUS — Big Tech Intelligence Platform  v6.1            ║
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;700&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
:root{
  --bg:#0f1117;--white:#1a1d27;--surface:#13161f;
  --primary:#818cf8;--accent:#22d3ee;--orange:#fb923c;
  --green:#34d399;--red:#f87171;--purple:#a78bfa;
  --pink:#f472b6;--yellow:#fbbf24;
  --txt:#e2e8f0;--txt2:#94a3b8;--txt3:#64748b;--txt4:#334155;
  --border:rgba(129,140,248,0.15);--border2:rgba(129,140,248,0.28);
  --shadow:0 4px 16px rgba(0,0,0,0.4);
  --shadow-lg:0 12px 40px rgba(0,0,0,0.5);
  --shadow-xl:0 24px 60px rgba(0,0,0,0.6);
  --radius:16px;--radius-xl:32px;
}
*{box-sizing:border-box;}
.stApp{background:var(--bg)!important;font-family:'Inter',sans-serif;color:var(--txt);}
.main .block-container{background:var(--bg)!important;padding:1.4rem 2.2rem!important;max-width:100%!important;}
.main{background:var(--bg)!important;}
[data-testid="stAppViewContainer"]>section.main{background:var(--bg)!important;}
.stTabs [data-baseweb="tab-list"]{gap:0.35rem;background:transparent;border-bottom:2px solid var(--border);}
.stTabs [data-baseweb="tab"]{background:transparent!important;border:none!important;border-bottom:3px solid transparent!important;border-radius:0!important;color:var(--txt3)!important;font-size:0.85rem;font-weight:600;padding:0.7rem 1.3rem!important;transition:all 0.2s;}
.stTabs [data-baseweb="tab"]:hover{color:var(--primary)!important;}
.stTabs [aria-selected="true"]{color:var(--primary)!important;border-bottom-color:var(--primary)!important;background:transparent!important;}
.main .stSelectbox>div>div{background:var(--white)!important;border:1px solid var(--border)!important;border-radius:12px!important;color:var(--txt)!important;}
.main .stSelectbox label,.main .stMultiSelect label,.main .stSlider label{color:var(--txt2)!important;font-size:0.75rem!important;}
[data-testid="stMetric"]{background:var(--white)!important;border:1px solid var(--border)!important;border-radius:14px;padding:1.1rem 1.3rem;}
[data-testid="stMetricValue"]{font-family:'Outfit',sans-serif!important;color:var(--primary)!important;font-weight:700;}
[data-testid="stMetricLabel"]{color:var(--txt2)!important;}
.main [data-testid="stDataFrame"]{background:var(--white)!important;border:1px solid var(--border)!important;border-radius:12px!important;}
.main .stInfo,.main .stWarning{background:var(--surface)!important;border-color:var(--border)!important;color:var(--txt)!important;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}
[data-testid="collapsedControl"]{display:none!important;}
[data-testid="stSidebarCollapseButton"]{display:none!important;}
button[aria-label="Close sidebar"]{display:none!important;}
button[aria-label="Collapse sidebar"]{display:none!important;}
section[data-testid="stSidebar"]{min-width:240px!important;max-width:280px!important;transform:none!important;visibility:visible!important;display:block!important;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#4f46e5 0%,#6366f1 40%,#818cf8 100%)!important;border-right:none!important;box-shadow:4px 0 24px rgba(79,70,229,0.15);}
[data-testid="stSidebar"] *{color:#fff!important;}
[data-testid="stSidebar"] .stSelectbox>div>div,[data-testid="stSidebar"] .stMultiSelect>div>div{background:rgba(255,255,255,0.15)!important;border:1px solid rgba(255,255,255,0.25)!important;border-radius:12px!important;color:#fff!important;}
/* ── Sidebar multiselect tags — white text & border ───────────── */
[data-testid="stSidebar"] [data-baseweb="tag"]{background:rgba(255,255,255,0.2)!important;border:1px solid rgba(255,255,255,0.35)!important;border-radius:6px!important;}
[data-testid="stSidebar"] [data-baseweb="tag"] span{color:#fff!important;}
[data-testid="stSidebar"] [data-baseweb="tag"] button svg{fill:#fff!important;}
[data-testid="stSidebar"] .stButton>button{width:100%!important;background:rgba(255,255,255,0.10)!important;border:1px solid rgba(255,255,255,0.18)!important;border-radius:12px!important;color:#fff!important;font-size:0.82rem!important;font-weight:500!important;padding:0.55rem 1rem!important;text-align:left!important;margin-bottom:0.25rem!important;transition:all 0.2s!important;}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,0.22)!important;border-color:rgba(255,255,255,0.4)!important;transform:translateX(4px)!important;}
[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:rgba(255,255,255,0.30)!important;border-color:rgba(255,255,255,0.6)!important;font-weight:700!important;box-shadow:0 2px 12px rgba(0,0,0,0.15)!important;}
/* ── SLIDER — white theme ─────────────────────────────────────── */
[data-testid="stSlider"] div[role="slider"]{background:#ffffff!important;border:2px solid rgba(255,255,255,0.8)!important;box-shadow:0 0 0 4px rgba(255,255,255,0.15)!important;width:16px!important;height:16px!important;border-radius:50%!important;}
[data-testid="stSlider"] [class*="Track"],[data-testid="stSlider"] [class*="track"]{background:rgba(255,255,255,0.2)!important;height:4px!important;border-radius:2px!important;}
[data-testid="stSlider"] [class*="Track"] div,[data-testid="stSlider"] [class*="track"] div{background:rgba(255,255,255,0.2)!important;}
[data-baseweb="slider"] div[class*="Track"]>div:nth-child(2){background:#ffffff!important;}
[data-baseweb="slider"] [data-testid="stSlider"] div[role="slider"]{background:#ffffff!important;border:2px solid rgba(255,255,255,0.9)!important;}
/* ── YR-CARD — white label text, tight alignment ─────────────── */
.hero{position:relative;overflow:hidden;background:linear-gradient(135deg,#312e81 0%,#4c1d95 30%,#0e7490 70%,#065f46 100%);border-radius:var(--radius-xl);padding:3.2rem 3.8rem 3rem;margin-bottom:2rem;box-shadow:var(--shadow-xl);color:#fff;}
.hero-title{font-family:'Outfit',sans-serif;font-size:4.5rem;font-weight:900;line-height:1.0;letter-spacing:-0.035em;margin:0 0 0.8rem 0;}
.hero-sub{font-size:1.05rem;line-height:1.7;max-width:620px;opacity:0.9;}
.hero-chips{display:flex;gap:0.6rem;flex-wrap:wrap;margin-top:1.6rem;}
.chip{display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.22);color:#fff!important;font-size:0.65rem;font-weight:500;padding:0.4rem 1rem;border-radius:100px;}
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
.kpi-icon{position:absolute;right:1.5rem;bottom:1.3rem;font-size:2.5rem;opacity:0.06;}
.kpi-badge{position:absolute;top:1.1rem;right:1rem;font-size:0.58rem;padding:0.22rem 0.7rem;border-radius:100px;font-weight:700;}
.up{background:rgba(52,211,153,0.15);color:var(--green)!important;border:1px solid rgba(52,211,153,0.3);}
.down{background:rgba(248,113,113,0.12);color:var(--red)!important;border:1px solid rgba(248,113,113,0.25);}
.flat{background:rgba(251,191,36,0.12);color:var(--yellow)!important;border:1px solid rgba(251,191,36,0.25);}
.sec{display:flex;align-items:center;gap:1rem;margin:2.5rem 0 1.4rem 0;}
.sec-title{font-family:'Outfit',sans-serif;font-size:0.9rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--txt);}
.sec-line{flex:1;height:1px;background:linear-gradient(90deg,var(--border2),transparent);}
.sec-tag{font-size:0.58rem;color:#fff!important;background:linear-gradient(135deg,var(--primary),var(--accent));padding:0.28rem 0.8rem;border-radius:100px;font-weight:600;}
.page-title{font-family:'Outfit',sans-serif;font-size:2.5rem;font-weight:800;letter-spacing:-0.03em;background:linear-gradient(135deg,var(--primary) 0%,var(--accent) 60%,var(--green) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:0.3rem;}
.yr-card{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:0.7rem 1rem 0.5rem;}
.yr-card-label{font-size:0.58rem;text-transform:uppercase;letter-spacing:0.12em;color:#e2e8f0;font-weight:600;margin-bottom:0.25rem;display:flex;align-items:center;gap:0.35rem;line-height:1.2;}
.yr-card-label .yr-icon{font-size:0.7rem;}
.yr-badge{display:inline-block;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff!important;font-family:'JetBrains Mono',monospace;font-size:0.62rem;font-weight:700;padding:0.2rem 0.65rem;border-radius:100px;margin-left:auto;}
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
/* ── COMPARISON TABLE ─────────────────────────────────────────── */
.cmp-wrap{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;margin-bottom:2rem;box-shadow:var(--shadow);}
.cmp-table{width:100%;border-collapse:collapse;font-size:0.82rem;}
.cmp-table thead tr{background:rgba(129,140,248,0.08);border-bottom:1px solid var(--border2);}
.cmp-table thead th{padding:0.75rem 1.1rem;text-align:left;font-size:0.62rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--txt3);font-weight:600;white-space:nowrap;}
.cmp-table thead th:not(:first-child){text-align:right;}
.cmp-table tbody tr{border-bottom:1px solid rgba(129,140,248,0.06);transition:background 0.15s;}
.cmp-table tbody tr:hover{background:rgba(129,140,248,0.05);}
.cmp-table tbody tr:last-child{border-bottom:none;}
.cmp-table td{padding:0.72rem 1.1rem;color:var(--txt);font-family:'Inter',sans-serif;}
.cmp-table td:not(:first-child){text-align:right;font-family:'JetBrains Mono',monospace;font-size:0.78rem;}
.cmp-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px;vertical-align:middle;}
.cmp-co{font-weight:600;color:var(--txt);display:flex;align-items:center;gap:0;}
.badge-up{color:#34d399;font-weight:700;}
.badge-dn{color:#f87171;font-weight:700;}
.badge-fl{color:#fbbf24;font-weight:700;}
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--txt4);border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY DARK DEFAULTS ──────────────────────────────────────────────────────
PL = dict(
    paper_bgcolor="#1a1d27", plot_bgcolor="#13161f",
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
    'Amazon': '#fbbf24', 'Meta': '#f97316', 'NVIDIA': '#86efac',
    'Tesla': '#fb7185', 'Netflix': '#f472b6',
}
ALL_COMPANIES = list(COLORS.keys())

PAGE_NAMES = [
    "🏠  Command Center", "📈  Stock Performance", "💰  Revenue & Earnings",
    "🏆  Competitive Analysis", "🔬  Deep Analytics",
    "🤖  AI Insight Engine", "📡  Live Dashboard",
]
PAGE_CC, PAGE_SP, PAGE_RE, PAGE_CA, PAGE_DA, PAGE_AI, PAGE_LD = range(7)

if "page_idx" not in st.session_state:
    st.session_state.page_idx = 0


# ── HELPERS ───────────────────────────────────────────────────────────────────
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
@st.cache_data(show_spinner=False)
def load_csv():
    base = Path(__file__).parent
    q = pd.read_csv(base / "quarterly_revenue.csv", parse_dates=["Quarter"])
    a = pd.read_csv(base / "annual_metrics.csv")
    p = pd.read_csv(base / "stock_prices.csv", parse_dates=["Date"])
    return q, a, p


@st.cache_data(ttl=43200, show_spinner=False)
def load_live_annual():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_annual()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=43200, show_spinner=False)
def load_live_quarterly():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_quarterly()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=86400, show_spinner=False)
def load_live_prices():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_price_history(period="5y")
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=300, show_spinner=False)
def load_live_fundamentals():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_fundamentals()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def build_merged_data():
    q_csv, ann_csv, price_csv = load_csv()
    live_ann = load_live_annual()
    live_q   = load_live_quarterly()
    live_p   = load_live_prices()

    if _live_ok and not live_ann.empty:
        ann_df = merge_with_csv(live_ann, ann_csv, ['Company', 'Year'])
        ann_df['Year']        = ann_df['Year'].astype(int)
        ann_csv_typed         = ann_csv.copy()
        ann_csv_typed['Year'] = ann_csv_typed['Year'].astype(int)

        ghost_cols = [
            c for c in ann_csv_typed.columns
            if c not in ('Company', 'Year')
            and c in ann_df.columns
            and ann_df[c].isna().any()
            and ann_csv_typed[c].notna().any()
        ]

        if ghost_cols:
            csv_patch = ann_csv_typed[['Company', 'Year'] + ghost_cols].copy()
            ann_df = ann_df.merge(
                csv_patch,
                on=['Company', 'Year'],
                how='left',
                suffixes=('', '_csv')
            )
            for col in ghost_cols:
                csv_col = f'{col}_csv'
                if csv_col in ann_df.columns:
                    ann_df[col] = ann_df[col].fillna(ann_df[csv_col])
                    ann_df.drop(columns=[csv_col], inplace=True)
    else:
        ann_df = ann_csv.copy()

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
    _dt = pd.to_datetime(price_df['Date'])
    price_df['Date'] = _dt.dt.tz_convert(None) if _dt.dt.tz is not None else _dt
    ann_df['Year']   = ann_df['Year'].astype(int)
    return ann_df, q_df, price_df


ann_df, q_df, price_df = build_merged_data()
fund_df = load_live_fundamentals()


def best_common_year(df, all_cos=None):
    if all_cos is None:
        all_cos = ALL_COMPANIES
    sub = df[df['Company'].isin(all_cos)]
    if sub.empty:
        return int(df['Year'].max()) if not df.empty else 2025
    yc = sub.groupby('Year')['Company'].nunique()
    if yc.empty:
        return int(df['Year'].max())
    valid = yc[yc >= max(1, len(all_cos) // 2)]
    return int(valid.index.max()) if not valid.empty else int(yc.index.max())


def get_latest_slice(df, companies, fallback_year=None):
    if df.empty:
        return pd.DataFrame(), fallback_year or 2025
    sub = df[df['Company'].isin(companies)]
    if sub.empty:
        return pd.DataFrame(), fallback_year or 2025
    yr = best_common_year(sub, companies) if fallback_year is None else fallback_year
    return sub[sub['Year'] == yr].copy(), yr


COMMON_LATEST_YEAR = best_common_year(ann_df)
SLIDER_MIN = int(ann_df['Year'].min()) if not ann_df.empty else 2020
SLIDER_MAX = COMMON_LATEST_YEAR
if SLIDER_MIN >= SLIDER_MAX:
    SLIDER_MAX = SLIDER_MIN + 1
ALL_YEARS = list(range(SLIDER_MIN, SLIDER_MAX + 1))


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <div style="font-size:2rem;margin-bottom:0.35rem;">🚀</div>
      <div class="logo-text">MARKET NEXUS</div>
      <div class="logo-sub">BIG TECH INTELLIGENCE · v6.1</div>
    </div>
    <div class="h-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.6rem;letter-spacing:0.12em;text-transform:uppercase;color:#fff;font-weight:600;margin-bottom:0.5rem;'>Navigation</div>", unsafe_allow_html=True)
    for i, label in enumerate(PAGE_NAMES):
        is_active = (st.session_state.page_idx == i)
        if st.button(label, key=f"nav_{i}", type="primary" if is_active else "secondary"):
            nav_to(i)
            st.rerun()

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.6rem;letter-spacing:0.12em;text-transform:uppercase;color:#fff;font-weight:600;margin-bottom:0.5rem;'>Filter Companies</div>", unsafe_allow_html=True)
    sel_companies = st.multiselect("Companies", ALL_COMPANIES, default=ALL_COMPANIES, label_visibility="collapsed")
    if not sel_companies:
        sel_companies = ALL_COMPANIES

    st.markdown("<div class='h-divider'></div>", unsafe_allow_html=True)
    data_src = "Live Data" if (_live_ok and not ann_df.empty) else "CSV Fallback"
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


# ── PAGE HEADER HELPERS ───────────────────────────────────────────────────────
def page_header_range(title_html, key_suffix):
    title_col, spacer, yr_col = st.columns([5, 0.5, 2.5])
    with title_col:
        st.markdown(f'<p class="page-title">{title_html}</p>', unsafe_allow_html=True)
    with yr_col:
        st.markdown(
            '<div class="yr-card">'
            '<div class="yr-card-label">'
            '<span class="yr-icon">📅</span> Year Range'
            '</div>',
            unsafe_allow_html=True)
        yr = st.slider(
            "Year Range",
            SLIDER_MIN, SLIDER_MAX,
            (SLIDER_MIN, SLIDER_MAX),
            label_visibility="collapsed",
            key=f"yr_range_{key_suffix}",
        )
        st.markdown(
            f'<div style="display:flex;justify-content:flex-end;margin-top:0.1rem;">'
            f'<span class="yr-badge">{yr[0]} – {yr[1]}</span></div></div>',
            unsafe_allow_html=True)
    return yr


def page_header_single(title_html, key_suffix):
    title_col, spacer, yr_col = st.columns([5, 0.5, 2.5])
    with title_col:
        st.markdown(f'<p class="page-title">{title_html}</p>', unsafe_allow_html=True)
    with yr_col:
        st.markdown(
            '<div class="yr-card">'
            '<div class="yr-card-label">'
            '<span class="yr-icon">📅</span> Select Year'
            '</div>',
            unsafe_allow_html=True)
        yr = st.selectbox(
            "Year",
            options=ALL_YEARS,
            index=len(ALL_YEARS) - 1,
            label_visibility="collapsed",
            key=f"yr_single_{key_suffix}",
        )
        st.markdown(
            f'<div style="display:flex;justify-content:flex-end;margin-top:0.1rem;">'
            f'<span class="yr-badge">FY {yr}</span></div></div>',
            unsafe_allow_html=True)
    return yr


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
    year_range = page_header_range("🏠 Command Center", "cc")

    ann_f  = ann_df[(ann_df['Company'].isin(sel_companies)) & (ann_df['Year'].between(*year_range))]
    q_f    = q_df[(q_df['Company'].isin(sel_companies)) & (q_df['Quarter'].dt.year.between(*year_range))]
    p_f    = price_df[(price_df['Company'].isin(sel_companies)) & (price_df['Date'].dt.year.between(*year_range))]
    FILTERED_LATEST_YEAR = best_common_year(ann_f, sel_companies) if not ann_f.empty else year_range[1]

    st.markdown("""
    <div class="hero">
      <div style="position:relative;z-index:1;">
        <div style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;opacity:0.8;margin-bottom:0.8rem;">⚡ Live Big Tech Intelligence Platform</div>
        <p class="hero-title">MARKET<br>NEXUS</p>
        <p class="hero-sub">
          Real-time financial intelligence across
          <strong>Apple · Microsoft · Google · Amazon · Meta · NVIDIA · Tesla · Netflix</strong>.
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

    if not fund_df.empty and not fund_df[fund_df['Company'].isin(sel_companies)].empty:
        kpi_cos     = fund_df[fund_df['Company'].isin(sel_companies)]
        total_rev   = kpi_cos['revenue_B'].sum()
        total_mcap  = kpi_cos['marketCap_B'].sum()
        top_row     = kpi_cos.loc[kpi_cos['marketCap_B'].idxmax()]
        top_mcap_co = top_row['Company']
        top_mcap    = top_row['marketCap_B']
        nvda_row    = kpi_cos[kpi_cos['Company'] == 'NVIDIA']
        nvda_ni     = nvda_row['netIncome_B'].values[0] if not nvda_row.empty else 0
        data_label  = "Live Data"
    else:
        latest_sl, lyr = get_latest_slice(ann_f, sel_companies)
        if latest_sl.empty:
            total_rev, total_mcap, top_mcap_co, top_mcap, nvda_ni = 0, 0, "N/A", 0, 0
            data_label = "No data"
        else:
            total_rev   = latest_sl['Revenue_B'].sum()
            total_mcap  = latest_sl['MarketCap_B'].sum()
            top_idx     = latest_sl['MarketCap_B'].idxmax()
            top_mcap_co = latest_sl.loc[top_idx, 'Company']
            top_mcap    = latest_sl.loc[top_idx, 'MarketCap_B']
            nvda_sl     = latest_sl[latest_sl['Company'] == 'NVIDIA']
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

    sec("Revenue Race & Market Cap", f"{year_range[0]}–{year_range[1]}")
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        for co in sel_companies:
            sub = q_f[q_f['Company'] == co].sort_values('Quarter')
            if sub.empty:
                continue
            fig.add_trace(go.Scatter(x=sub['Quarter'], y=sub['Revenue_B'], name=co, mode='lines',
                line=dict(color=COLORS.get(co, '#818cf8'), width=2.5),
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>${{y:.1f}}B<extra></extra>'))
        sf(fig, 350).update_layout(
            title=dict(text="Quarterly Revenue ($B)", font=dict(size=13, color='#94a3b8')),
            yaxis_title="Revenue ($B)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        if not ann_f.empty:
            mc_data = ann_f.pivot_table(index='Year', columns='Company', values='MarketCap_B', aggfunc='first').fillna(0)
            fig = go.Figure()
            for co in [c for c in sel_companies if c in mc_data.columns]:
                fig.add_trace(go.Bar(x=mc_data.index, y=mc_data[co], name=co,
                    marker_color=COLORS.get(co, '#818cf8'), opacity=0.88,
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:,.0f}}B<extra></extra>'))
            fig.update_layout(barmode='group')
            sf(fig, 350).update_layout(
                title=dict(text="Market Cap by Year ($B)", font=dict(size=13, color='#94a3b8')),
                yaxis_title="Market Cap ($B)")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No annual data available for the selected filters.")

    sec("Stock Returns & Profitability", f"{year_range[0]}–{year_range[1]}")
    c1, c2 = st.columns([3, 2])
    with c1:
        fig = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f['Company'] == co].sort_values('Date')
            if sub.empty or sub['Price'].iloc[0] == 0:
                continue
            base = sub['Price'].iloc[0]
            fig.add_trace(go.Scatter(x=sub['Date'], y=sub['Price'] / base * 100, name=co, mode='lines',
                line=dict(color=COLORS.get(co, '#818cf8'), width=2),
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>%{{y:.0f}}<extra></extra>'))
        fig.add_hline(y=100, line_dash='dot', line_color='rgba(255,255,255,0.1)')
        sf(fig, 340).update_layout(
            title=dict(text="Normalised Stock Performance (Base=100)", font=dict(size=13, color='#94a3b8')),
            yaxis_title="Indexed Return")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        margin_sl, m_yr = get_latest_slice(ann_f, sel_companies)
        if not margin_sl.empty:
            margin_sl = margin_sl.copy()
            margin_sl['Margin'] = (margin_sl['NetIncome_B'] / margin_sl['Revenue_B'].replace(0, np.nan) * 100).round(1).fillna(0)
            margin_sl = margin_sl.sort_values('Margin')
            fig = go.Figure(go.Bar(
                x=margin_sl['Margin'], y=margin_sl['Company'], orientation='h',
                marker=dict(color=margin_sl['Margin'],
                    colorscale=[[0, '#f87171'], [0.4, '#fb923c'], [1, '#34d399']], line=dict(width=0)),
                text=[f"{v:.1f}%" for v in margin_sl['Margin']], textposition='outside',
                hovertemplate='<b>%{y}</b><br>Margin: %{x:.1f}%<extra></extra>'))
            sf(fig, 340, legend=False).update_layout(
                title=dict(text=f"Net Profit Margin {m_yr}", font=dict(size=13, color='#94a3b8')),
                xaxis_title="Net Margin %")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No margin data available for the selected filters.")

    sec("Revenue Distribution & Headcount", f"{year_range[0]}–{year_range[1]}")
    c1, c2 = st.columns(2)
    with c1:
        treemap_sl, t_yr = get_latest_slice(ann_f, sel_companies)
        if not treemap_sl.empty and 'Sector' in treemap_sl.columns:
            fig = px.treemap(treemap_sl, path=['Sector', 'Company'], values='Revenue_B',
                color='NetIncome_B',
                color_continuous_scale=[[0, '#f87171'], [0.5, '#1e293b'], [1, '#34d399']],
                hover_data={'Revenue_B': ':.1f', 'NetIncome_B': ':.1f'})
            fig.update_traces(textfont_size=13, textfont_color='#e2e8f0',
                hovertemplate='<b>%{label}</b><br>Revenue: $%{value:.1f}B<extra></extra>')
            fig.update_layout(**PL, height=330,
                title=dict(text=f"Revenue Treemap {t_yr}", font=dict(size=13, color='#94a3b8')),
                coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Sector data not available in current dataset.")
    with c2:
        emp_sl, e_yr = get_latest_slice(ann_f, sel_companies)
        if not emp_sl.empty:
            emp_sl = emp_sl.copy()
            emp_sl['RevPerEmp'] = (emp_sl['Revenue_B'] * 1e9 / (emp_sl['Employees_K'].replace(0, np.nan) * 1e3) / 1e6).round(2).fillna(0)
            emp_sl = emp_sl.sort_values('RevPerEmp')
            fig = go.Figure(go.Bar(
                x=emp_sl['RevPerEmp'], y=emp_sl['Company'], orientation='h',
                marker=dict(color=[COLORS.get(c, '#818cf8') for c in emp_sl['Company']], line=dict(width=0)),
                text=[f"${v:.2f}M" for v in emp_sl['RevPerEmp']], textposition='outside',
                hovertemplate='<b>%{y}</b><br>$%{x:.2f}M per employee<extra></extra>'))
            sf(fig, 330, legend=False).update_layout(
                title=dict(text=f"Revenue per Employee {e_yr} ($M)", font=dict(size=13, color='#94a3b8')),
                xaxis_title="$M per Employee")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No employee data available for the selected filters.")


# ════════════════════════════════════════════════════════════════════
# PAGE 2 — STOCK PERFORMANCE
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_SP:
    year_range = page_header_range("📈 Stock Performance", "sp")
    ann_f  = ann_df[(ann_df['Company'].isin(sel_companies)) & (ann_df['Year'].between(*year_range))]
    q_f    = q_df[(q_df['Company'].isin(sel_companies)) & (q_df['Quarter'].dt.year.between(*year_range))]
    p_f    = price_df[(price_df['Company'].isin(sel_companies)) & (price_df['Date'].dt.year.between(*year_range))]

    if 'Daily_Return' not in p_f.columns and not p_f.empty:
        p_f = p_f.copy()
        p_f['Daily_Return'] = (
            p_f.sort_values('Date')
               .groupby('Company')['Price']
               .pct_change() * 100
        )

    tab1, tab2, tab3 = st.tabs(["📊 Price History", "📉 Volatility & Risk", "🎯 Return Analysis"])

    with tab1:
        if sel_companies:
            co1 = st.selectbox("Company", sel_companies, key='sp1')
            sub = p_f[p_f['Company'] == co1].sort_values('Date').copy()
            if not sub.empty:
                sub['MA50']  = sub['Price'].rolling(50).mean()
                sub['MA200'] = sub['Price'].rolling(200).mean()
                sub['Upper'] = sub['Price'].rolling(20).mean() + 2 * sub['Price'].rolling(20).std()
                sub['Lower'] = sub['Price'].rolling(20).mean() - 2 * sub['Price'].rolling(20).std()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=sub['Date'], y=sub['Upper'], name='BB Upper',
                    line=dict(color='rgba(129,140,248,0.2)', width=1, dash='dot'), showlegend=False))
                fig.add_trace(go.Scatter(x=sub['Date'], y=sub['Lower'], name='BB Lower', fill='tonexty',
                    fillcolor='rgba(129,140,248,0.06)',
                    line=dict(color='rgba(129,140,248,0.2)', width=1, dash='dot'), showlegend=False))
                fig.add_trace(go.Scatter(x=sub['Date'], y=sub['Price'], name='Price',
                    line=dict(color=COLORS.get(co1, '#818cf8'), width=2.5),
                    hovertemplate='<b>' + co1 + '</b><br>%{x|%b %d, %Y}<br>$%{y:.2f}<extra></extra>'))
                fig.add_trace(go.Scatter(x=sub['Date'], y=sub['MA50'], name='MA50',
                    line=dict(color='#fbbf24', width=1.5, dash='dot')))
                fig.add_trace(go.Scatter(x=sub['Date'], y=sub['MA200'], name='MA200',
                    line=dict(color='#a78bfa', width=1.5, dash='dash')))
                sf(fig, 420).update_layout(
                    title=dict(text=f"{co1} — Price + Bollinger Bands + MAs", font=dict(size=13, color='#94a3b8')),
                    yaxis_title="Price (USD)")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                if 'Volume_M' in sub.columns:
                    fig2 = go.Figure(go.Bar(x=sub['Date'], y=sub['Volume_M'],
                        marker_color=COLORS.get(co1, '#818cf8'), opacity=0.35, name='Volume'))
                    sf(fig2, 120, legend=False).update_layout(yaxis_title="Volume (M)", margin=dict(t=10))
                    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No price data available for the selected filters.")

    with tab2:
        if 'Daily_Return' in p_f.columns and not p_f.empty:
            fig = go.Figure()
            for co in sel_companies:
                sub = p_f[p_f['Company'] == co].sort_values('Date')
                if sub.empty:
                    continue
                vol = sub['Daily_Return'].rolling(30).std()
                fig.add_trace(go.Scatter(x=sub['Date'], y=vol, name=co, mode='lines',
                    line=dict(color=COLORS.get(co, '#818cf8'), width=1.8),
                    hovertemplate=f'<b>{co}</b> %{{x|%b %Y}}<br>Vol: %{{y:.2f}}%<extra></extra>'))
            sf(fig, 340).update_layout(
                title=dict(text="30-Day Rolling Volatility", font=dict(size=13, color='#94a3b8')),
                yaxis_title="Volatility (%)")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            stats_rows = []
            for co in sel_companies:
                sub = p_f[p_f['Company'] == co].sort_values('Date')
                if len(sub) < 2:
                    continue
                ret = sub['Daily_Return'].dropna()
                if ret.empty:
                    continue
                stats_rows.append({
                    'Company': co,
                    'Ann. Return %': round(ret.mean() * 252, 2),
                    'Ann. Volatility %': round(ret.std() * np.sqrt(252), 2),
                    'Sharpe (rf=0)': round(ret.mean() / ret.std() * np.sqrt(252), 2) if ret.std() > 0 else 0,
                    'Max Drawdown %': round((sub['Price'] / sub['Price'].cummax() - 1).min() * 100, 2),
                    'Skewness': round(float(scipy_stats.skew(ret)), 3),
                    'Kurtosis': round(float(scipy_stats.kurtosis(ret)), 3),
                })
            if stats_rows:
                st.dataframe(pd.DataFrame(stats_rows).set_index('Company'), use_container_width=True)
            else:
                st.info("Not enough price data to compute risk statistics.")
        else:
            st.info("No price data available for the selected filters.")

    with tab3:
        fig = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f['Company'] == co].sort_values('Date')
            if sub.empty or sub['Price'].iloc[0] == 0:
                continue
            total_ret = (sub['Price'].iloc[-1] / sub['Price'].iloc[0] - 1) * 100
            fig.add_trace(go.Bar(
                x=[co], y=[total_ret], name=co,
                marker_color=COLORS.get(co, '#818cf8'),
                text=[f"{total_ret:.1f}%"], textposition='outside',
                hovertemplate=f'<b>{co}</b><br>Return: %{{y:.1f}}%<extra></extra>'))
        sf(fig, 340, legend=False).update_layout(
            title=dict(text=f"Total Return {year_range[0]}–{year_range[1]}", font=dict(size=13, color='#94a3b8')),
            yaxis_title="Total Return (%)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ════════════════════════════════════════════════════════════════════
# PAGE 3 — REVENUE & EARNINGS
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_RE:
    year_range = page_header_range("💰 Revenue & Earnings", "re")
    ann_f = ann_df[(ann_df['Company'].isin(sel_companies)) & (ann_df['Year'].between(*year_range))]
    q_f   = q_df[(q_df['Company'].isin(sel_companies)) & (q_df['Quarter'].dt.year.between(*year_range))]

    tab1, tab2 = st.tabs(["📊 Revenue Trends", "💵 Earnings & Margins"])

    with tab1:
        sec("Annual Revenue Growth", f"{year_range[0]}–{year_range[1]}")
        fig = go.Figure()
        for co in sel_companies:
            sub = ann_f[ann_f['Company'] == co].sort_values('Year')
            if sub.empty:
                continue
            fig.add_trace(go.Scatter(
                x=sub['Year'], y=sub['Revenue_B'], name=co, mode='lines+markers',
                line=dict(color=COLORS.get(co, '#818cf8'), width=2.5),
                marker=dict(size=7),
                hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:.1f}}B<extra></extra>'))
        sf(fig, 380).update_layout(
            title=dict(text="Annual Revenue ($B) — All Companies", font=dict(size=13, color='#94a3b8')),
            yaxis_title="Revenue ($B)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        sec("Quarterly Revenue — Combined", f"{year_range[0]}–{year_range[1]}")
        fig2 = go.Figure()
        for co in sel_companies:
            sub = q_f[q_f['Company'] == co].sort_values('Quarter')
            if sub.empty:
                continue
            fig2.add_trace(go.Bar(
                x=sub['Quarter'], y=sub['Revenue_B'], name=co,
                marker_color=COLORS.get(co, '#818cf8'), opacity=0.85,
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>${{y:.1f}}B<extra></extra>'))
        fig2.update_layout(barmode='group')
        sf(fig2, 340).update_layout(
            title=dict(text="Quarterly Revenue ($B) — All Companies", font=dict(size=13, color='#94a3b8')),
            yaxis_title="Revenue ($B)")
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

        sec("Quarterly Revenue — Per Company", f"{year_range[0]}–{year_range[1]}")
        active_cos = [co for co in sel_companies if not q_f[q_f['Company'] == co].empty]
        if active_cos:
            pairs = [active_cos[i:i+2] for i in range(0, len(active_cos), 2)]
            for pair in pairs:
                cols = st.columns(len(pair))
                for col, co in zip(cols, pair):
                    with col:
                        sub = q_f[q_f['Company'] == co].sort_values('Quarter').copy()
                        color = COLORS.get(co, '#818cf8')
                        fill_color = hex_to_rgba(color, 0.12)
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=sub['Quarter'], y=sub['Revenue_B'],
                            name=co, mode='lines+markers',
                            line=dict(color=color, width=2.5),
                            marker=dict(size=7, color=color, line=dict(color='#0f1117', width=1.5)),
                            fill='tozeroy', fillcolor=fill_color,
                            hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>${{y:.1f}}B<extra></extra>'
                        ))
                        if len(sub) >= 3:
                            x_num = np.arange(len(sub))
                            slope, intercept, *_ = scipy_stats.linregress(x_num, sub['Revenue_B'].values)
                            trend = slope * x_num + intercept
                            fig.add_trace(go.Scatter(
                                x=sub['Quarter'], y=trend, mode='lines', name='Trend',
                                line=dict(color='rgba(255,255,255,0.18)', width=1.5, dash='dot'),
                                showlegend=False
                            ))
                        sf(fig, 280, legend=False).update_layout(
                            title=dict(text=f"{co} — Quarterly Revenue", font=dict(size=12, color=color)),
                            yaxis_title="$B", margin=dict(l=10, r=10, t=40, b=10)
                        )
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No quarterly data available for the selected filters.")

    with tab2:
        sec("Net Income vs Revenue", f"{year_range[0]}–{year_range[1]}")
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            for co in sel_companies:
                sub = ann_f[ann_f['Company'] == co].sort_values('Year')
                if sub.empty:
                    continue
                fig.add_trace(go.Scatter(
                    x=sub['Year'], y=sub['NetIncome_B'], name=co, mode='lines+markers',
                    line=dict(color=COLORS.get(co, '#818cf8'), width=2),
                    marker=dict(size=6),
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:.1f}}B<extra></extra>'))
            sf(fig, 340).update_layout(
                title=dict(text="Net Income ($B)", font=dict(size=13, color='#94a3b8')),
                yaxis_title="Net Income ($B)")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with c2:
            margin_data = []
            for co in sel_companies:
                sub = ann_f[ann_f['Company'] == co].sort_values('Year')
                if sub.empty:
                    continue
                sub = sub.copy()
                sub['Margin'] = (sub['NetIncome_B'] / sub['Revenue_B'].replace(0, np.nan) * 100).round(1)
                for _, row in sub.iterrows():
                    margin_data.append({'Company': co, 'Year': row['Year'], 'Margin': row['Margin']})
            if margin_data:
                mdf = pd.DataFrame(margin_data)
                fig = go.Figure()
                for co in sel_companies:
                    sub = mdf[mdf['Company'] == co]
                    if sub.empty:
                        continue
                    fig.add_trace(go.Scatter(
                        x=sub['Year'], y=sub['Margin'], name=co, mode='lines+markers',
                        line=dict(color=COLORS.get(co, '#818cf8'), width=2),
                        hovertemplate=f'<b>{co}</b> %{{x}}<br>Margin: %{{y:.1f}}%<extra></extra>'))
                sf(fig, 340).update_layout(
                    title=dict(text="Net Profit Margin (%)", font=dict(size=13, color='#94a3b8')),
                    yaxis_title="Net Margin %")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No margin data available for the selected filters.")


# ════════════════════════════════════════════════════════════════════
# PAGE 4 — COMPETITIVE ANALYSIS
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_CA:
    sel_year = page_header_single("🏆 Competitive Analysis", "ca")
    ann_f = ann_df[(ann_df['Company'].isin(sel_companies)) & (ann_df['Year'] == sel_year)]

    tab1, tab2, tab3 = st.tabs(["🥊 Head-to-Head", "📊 Market Share", "⚡ Efficiency"])

    with tab1:
        sec("Key Metrics Comparison", str(sel_year))
        if not ann_f.empty:
            display_cols = [c for c in ['Company', 'Revenue_B', 'NetIncome_B', 'MarketCap_B',
                                         'Employees_K', 'PE_Ratio', 'EPS'] if c in ann_f.columns]
            st.dataframe(
                ann_f[display_cols].set_index('Company').style.format("{:.2f}"),
                use_container_width=True)

            sec("Radar Chart", str(sel_year))
            metrics = [c for c in ['Revenue_B', 'NetIncome_B', 'MarketCap_B'] if c in ann_f.columns]
            if metrics:
                fig = go.Figure()
                for _, row in ann_f.iterrows():
                    vals = [row.get(m, 0) for m in metrics]
                    max_vals = [ann_f[m].max() for m in metrics]
                    norm = [v / mx * 100 if mx > 0 else 0 for v, mx in zip(vals, max_vals)]
                    fig.add_trace(go.Scatterpolar(
                        r=norm + [norm[0]], theta=metrics + [metrics[0]],
                        fill='toself', name=row['Company'],
                        line=dict(color=COLORS.get(row['Company'], '#818cf8')),
                        fillcolor=hex_to_rgba(COLORS.get(row['Company'], '#818cf8'), 0.1)))
                sf(fig, 420).update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100],
                               gridcolor='rgba(255,255,255,0.08)', color='#64748b')),
                    title=dict(text=f"Normalised Metrics Radar {sel_year}", font=dict(size=13, color='#94a3b8')))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info(f"No data available for {sel_year}.")

    with tab2:
        sec("Revenue & Market Cap Share", str(sel_year))
        if not ann_f.empty:
            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure(go.Pie(
                    labels=ann_f['Company'], values=ann_f['Revenue_B'],
                    hole=0.45, textinfo='label+percent',
                    marker=dict(colors=[COLORS.get(c, '#818cf8') for c in ann_f['Company']],
                                line=dict(color='#0f1117', width=2))))
                sf(fig, 340, legend=False).update_layout(
                    title=dict(text=f"Revenue Share {sel_year}", font=dict(size=13, color='#94a3b8')))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            with c2:
                if 'MarketCap_B' in ann_f.columns:
                    fig = go.Figure(go.Pie(
                        labels=ann_f['Company'], values=ann_f['MarketCap_B'],
                        hole=0.45, textinfo='label+percent',
                        marker=dict(colors=[COLORS.get(c, '#818cf8') for c in ann_f['Company']],
                                    line=dict(color='#0f1117', width=2))))
                    sf(fig, 340, legend=False).update_layout(
                        title=dict(text=f"Market Cap Share {sel_year}", font=dict(size=13, color='#94a3b8')))
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Market cap data not available for the selected year.")
        else:
            st.info(f"No data for {sel_year}.")

    with tab3:
        sec("Efficiency Metrics", str(sel_year))
        if not ann_f.empty:
            eff = ann_f.copy()
            if 'Employees_K' in eff.columns:
                eff['RevPerEmp'] = (eff['Revenue_B'] * 1e9 / (eff['Employees_K'].replace(0, np.nan) * 1e3) / 1e6).round(2).fillna(0)
            eff['NetMargin'] = (eff['NetIncome_B'] / eff['Revenue_B'].replace(0, np.nan) * 100).round(1).fillna(0)
            c1, c2 = st.columns(2)
            with c1:
                eff_s = eff.sort_values('NetMargin')
                fig = go.Figure(go.Bar(
                    x=eff_s['NetMargin'], y=eff_s['Company'], orientation='h',
                    marker=dict(color=[COLORS.get(c, '#818cf8') for c in eff_s['Company']], line=dict(width=0)),
                    text=[f"{v:.1f}%" for v in eff_s['NetMargin']], textposition='outside',
                    hovertemplate='<b>%{y}</b><br>%{x:.1f}%<extra></extra>'))
                sf(fig, 320, legend=False).update_layout(
                    title=dict(text=f"Net Margin {sel_year}", font=dict(size=13, color='#94a3b8')),
                    xaxis_title="Net Margin %")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            with c2:
                if 'RevPerEmp' in eff.columns:
                    eff_s2 = eff.sort_values('RevPerEmp')
                    fig = go.Figure(go.Bar(
                        x=eff_s2['RevPerEmp'], y=eff_s2['Company'], orientation='h',
                        marker=dict(color=[COLORS.get(c, '#818cf8') for c in eff_s2['Company']], line=dict(width=0)),
                        text=[f"${v:.2f}M" for v in eff_s2['RevPerEmp']], textposition='outside',
                        hovertemplate='<b>%{y}</b><br>$%{x:.2f}M/emp<extra></extra>'))
                    sf(fig, 320, legend=False).update_layout(
                        title=dict(text=f"Revenue/Employee {sel_year}", font=dict(size=13, color='#94a3b8')),
                        xaxis_title="$M per Employee")
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Employee data not available for the selected year.")
        else:
            st.info(f"No data for {sel_year}.")


# ════════════════════════════════════════════════════════════════════
# PAGE 5 — DEEP ANALYTICS
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_DA:
    year_range = page_header_range("🔬 Deep Analytics", "da")
    ann_f   = ann_df[(ann_df['Company'].isin(sel_companies)) & (ann_df['Year'].between(*year_range))]
    p_f     = price_df[(price_df['Company'].isin(sel_companies)) & (price_df['Date'].dt.year.between(*year_range))]

    tab1, tab2, tab3 = st.tabs(["📈 Correlation", "📉 Regression", "🔍 Factor Analysis"])

    with tab1:
        sec("Price Return Correlation Matrix", f"{year_range[0]}–{year_range[1]}")
        pivot = price_df[price_df['Company'].isin(sel_companies)].pivot_table(
            index='Date', columns='Company', values='Price')
        pivot = pivot.ffill().dropna()
        if len(pivot) > 5:
            corr = pivot.pct_change().dropna().corr()
            fig = go.Figure(go.Heatmap(
                z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
                colorscale=[[0, '#f87171'], [0.5, '#1e293b'], [1, '#34d399']],
                zmin=-1, zmax=1,
                text=corr.round(2).values,
                texttemplate='%{text}',
                hovertemplate='%{y} × %{x}<br>r = %{z:.3f}<extra></extra>'))
            sf(fig, 420, legend=False).update_layout(
                title=dict(text="Daily Return Correlation", font=dict(size=13, color='#94a3b8')))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Not enough price data for correlation analysis.")

    with tab2:
        sec("Revenue vs Market Cap Regression", f"{year_range[0]}–{year_range[1]}")
        if not ann_f.empty and len(ann_f) >= 3 and 'MarketCap_B' in ann_f.columns:
            x = ann_f['Revenue_B'].values
            y = ann_f['MarketCap_B'].values
            if len(x) >= 3:
                slope, intercept, r, p_val, _ = scipy_stats.linregress(x, y)
                x_line = np.linspace(x.min(), x.max(), 100)
                y_line = slope * x_line + intercept
                fig = go.Figure()
                for co in sel_companies:
                    sub = ann_f[ann_f['Company'] == co]
                    if sub.empty:
                        continue
                    fig.add_trace(go.Scatter(
                        x=sub['Revenue_B'], y=sub['MarketCap_B'],
                        mode='markers+text', name=co,
                        text=sub['Year'].astype(str),
                        textposition='top center',
                        marker=dict(color=COLORS.get(co, '#818cf8'), size=10),
                        hovertemplate=f'<b>{co}</b><br>Rev: $%{{x:.1f}}B<br>MCap: $%{{y:.1f}}B<extra></extra>'))
                fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name=f'Fit (R²={r**2:.2f})',
                    line=dict(color='rgba(129,140,248,0.5)', width=2, dash='dash')))
                sf(fig, 400).update_layout(
                    title=dict(text=f"Revenue vs Market Cap | R²={r**2:.3f} p={p_val:.3f}", font=dict(size=13, color='#94a3b8')),
                    xaxis_title="Revenue ($B)", yaxis_title="Market Cap ($B)")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Insufficient data for regression (need ≥3 data points with MarketCap).")

    with tab3:
        sec("YoY Revenue Growth Rates", f"{year_range[0]}–{year_range[1]}")
        growth_rows = []
        for co in sel_companies:
            sub = ann_df[ann_df['Company'] == co].sort_values('Year')
            if len(sub) < 2:
                continue
            sub = sub.copy()
            sub['YoY_Growth'] = sub['Revenue_B'].pct_change() * 100
            for _, row in sub.iterrows():
                if pd.notna(row['YoY_Growth']) and year_range[0] <= row['Year'] <= year_range[1]:
                    growth_rows.append({'Company': co, 'Year': int(row['Year']), 'YoY_Growth': round(row['YoY_Growth'], 1)})
        if growth_rows:
            gdf = pd.DataFrame(growth_rows)
            fig = go.Figure()
            for co in sel_companies:
                sub = gdf[gdf['Company'] == co]
                if sub.empty:
                    continue
                fig.add_trace(go.Bar(x=sub['Year'], y=sub['YoY_Growth'], name=co,
                    marker_color=COLORS.get(co, '#818cf8'), opacity=0.85,
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>Growth: %{{y:.1f}}%<extra></extra>'))
            fig.update_layout(barmode='group')
            sf(fig, 360).update_layout(
                title=dict(text="YoY Revenue Growth (%)", font=dict(size=13, color='#94a3b8')),
                yaxis_title="Growth %")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Not enough data for YoY growth analysis.")


# ════════════════════════════════════════════════════════════════════
# PAGE 6 — AI INSIGHT ENGINE
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_AI:
    sel_year = page_header_single("🤖 AI Insight Engine", "ai")
    ann_f = ann_df[(ann_df['Company'].isin(sel_companies)) & (ann_df['Year'] == sel_year)]

    sec("Auto-Generated Insights", str(sel_year))

    if ann_f.empty:
        st.info(f"No data available for {sel_year}. Try selecting a different year.")
    else:
        top_rev = ann_f.loc[ann_f['Revenue_B'].idxmax()]
        st.markdown(f"""
        <div class="insight-card">
          <div class="insight-title">💰 Revenue Leader — {top_rev['Company']}</div>
          <div class="insight-body">
            {top_rev['Company']} led all tracked companies in {sel_year} with
            <strong>${top_rev['Revenue_B']:.1f}B</strong> in annual revenue,
            representing exceptional scale in the Big Tech landscape.
          </div>
        </div>""", unsafe_allow_html=True)

        if 'MarketCap_B' in ann_f.columns:
            top_mc = ann_f.loc[ann_f['MarketCap_B'].idxmax()]
            st.markdown(f"""
            <div class="insight-card" style="border-left-color:#22d3ee;">
              <div class="insight-title">🏦 Market Cap Leader — {top_mc['Company']}</div>
              <div class="insight-body">
                {top_mc['Company']} commanded the highest market capitalisation at
                <strong>${top_mc['MarketCap_B']:,.0f}B</strong> in {sel_year}.
              </div>
            </div>""", unsafe_allow_html=True)

        if 'NetIncome_B' in ann_f.columns:
            top_ni = ann_f.loc[ann_f['NetIncome_B'].idxmax()]
            margin = top_ni['NetIncome_B'] / top_ni['Revenue_B'] * 100 if top_ni['Revenue_B'] > 0 else 0
            st.markdown(f"""
            <div class="insight-card" style="border-left-color:#34d399;">
              <div class="insight-title">📈 Most Profitable — {top_ni['Company']}</div>
              <div class="insight-body">
                {top_ni['Company']} achieved the highest net income of
                <strong>${top_ni['NetIncome_B']:.1f}B</strong> with a
                <strong>{margin:.1f}%</strong> net profit margin in {sel_year}.
              </div>
            </div>""", unsafe_allow_html=True)

        sec("Financial Snapshot", str(sel_year))
        display_cols = [c for c in ['Company', 'Revenue_B', 'NetIncome_B', 'MarketCap_B',
                                     'Employees_K'] if c in ann_f.columns]
        if len(display_cols) > 1:
            st.dataframe(
                ann_f[display_cols].set_index('Company').style.format("{:.2f}"),
                use_container_width=True)


# ════════════════════════════════════════════════════════════════════
# PAGE 7 — LIVE DASHBOARD
# ════════════════════════════════════════════════════════════════════
elif page_idx == PAGE_LD:
    st.markdown('<p class="page-title">📡 Live Dashboard</p>', unsafe_allow_html=True)

    if not _live_ok:
        st.error("Live data module (`live_data.py`) not found. Please ensure it is present.")
    else:
        if _autorefresh_ok:
            st_autorefresh(interval=30000, key="live_refresh")

        sec("Live Prices", "REAL-TIME")
        try:
            prices = get_multi_live_prices()
            if prices:
                filtered_prices = {co: d for co, d in prices.items() if co in sel_companies}
                fund_live = load_live_fundamentals()

                # ── Build table rows ──────────────────────────────────────
                table_rows = []
                for company, data in sorted(
                    filtered_prices.items(),
                    key=lambda x: x[1].get('price', 0), reverse=True
                ):
                    ticker  = NAME_TO_TICKER.get(company, '') if isinstance(NAME_TO_TICKER, dict) else ''
                    price   = data.get('price', 0) or 0
                    change  = data.get('change_pct', 0) or 0
                    volume  = data.get('volume', 0) or 0

                    # Volume formatting
                    if volume >= 1_000_000:
                        vol_str = f"{volume / 1_000_000:.1f}M"
                    elif volume >= 1_000:
                        vol_str = f"{volume / 1_000:.0f}K"
                    else:
                        vol_str = str(int(volume)) if volume else "—"

                    # Change arrow
                    if change > 0:
                        chg_str = f"▲ {change:.2f}%"
                    elif change < 0:
                        chg_str = f"▼ {abs(change):.2f}%"
                    else:
                        chg_str = f"— {change:.2f}%"

                    # Fundamentals
                    w52_high = w52_low = mktcap = pe = "—"
                    if not fund_live.empty:
                        frow = fund_live[fund_live['Company'] == company]
                        if not frow.empty:
                            fr = frow.iloc[0]

                            def _safe(col, fmt):
                                try:
                                    v = fr[col] if col in fr.index else None
                                    return fmt(float(v)) if v is not None and not pd.isna(v) else "—"
                                except (TypeError, ValueError):
                                    return "—"

                            w52_high = _safe('52w_high',    lambda v: f"${v:,.2f}")
                            w52_low  = _safe('52w_low',     lambda v: f"${v:,.2f}")
                            mktcap   = _safe('marketCap_B', lambda v: f"${v:,.0f}B")
                            pe       = _safe('trailingPE',  lambda v: f"{v:.1f}x")

                    table_rows.append({
                        "Company":    f"{company} ({ticker})" if ticker else company,
                        "Price (USD)": f"${price:,.2f}",
                        "Change %":   chg_str,
                        "Volume":     vol_str,
                        "52W High":   w52_high,
                        "52W Low":    w52_low,
                        "Mkt Cap":    mktcap,
                        "P/E":        pe,
                    })

                if table_rows:
                    live_df = pd.DataFrame(table_rows)

                    # Colour-code Change % column
                    def colour_change(val):
                        if val.startswith("▲"):
                            return "color: #34d399; font-weight: 700"
                        elif val.startswith("▼"):
                            return "color: #f87171; font-weight: 700"
                        return "color: #fbbf24; font-weight: 700"

                    styled = (
                        live_df.style
                        .applymap(colour_change, subset=["Change %"])
                        .set_properties(**{
                            "background-color": "#1a1d27",
                            "color": "#e2e8f0",
                            "font-family": "JetBrains Mono, monospace",
                            "font-size": "0.82rem",
                        })
                        .set_table_styles([
                            {"selector": "thead th", "props": [
                                ("background-color", "#13161f"),
                                ("color", "#64748b"),
                                ("font-size", "0.65rem"),
                                ("text-transform", "uppercase"),
                                ("letter-spacing", "0.1em"),
                                ("border-bottom", "1px solid rgba(129,140,248,0.28)"),
                            ]},
                            {"selector": "tbody tr:hover td", "props": [
                                ("background-color", "rgba(129,140,248,0.07)"),
                            ]},
                            {"selector": "td", "props": [
                                ("border-bottom", "1px solid rgba(129,140,248,0.06)"),
                                ("padding", "0.65rem 1rem"),
                            ]},
                        ])
                    )
                    st.dataframe(styled, use_container_width=True, hide_index=True)

            else:
                st.info("No live price data returned. Please check your live_data.py connection.")

        except Exception as e:
            st.warning(f"Could not fetch live prices: {e}")

        sec("Intraday Chart", "LIVE")
        try:
            co_live = st.selectbox("Select Company", sel_companies, key='ld_co')
            ticker  = NAME_TO_TICKER.get(co_live, 'AAPL') if isinstance(NAME_TO_TICKER, dict) else 'AAPL'
            intra   = get_intraday_data(ticker, period="1d", interval="5m")
            if not intra.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=intra.index, y=intra['Close'], mode='lines',
                    line=dict(color=COLORS.get(co_live, '#818cf8'), width=2),
                    name=co_live,
                    hovertemplate='%{x|%H:%M}<br>$%{y:.2f}<extra></extra>'
                ))
                sf(fig, 360, legend=False).update_layout(
                    title=dict(text=f"{co_live} — Intraday (5-min)", font=dict(size=13, color='#94a3b8')),
                    yaxis_title="Price (USD)"
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No intraday data available at this time.")
        except Exception as e:
            st.warning(f"Could not load intraday chart: {e}")
