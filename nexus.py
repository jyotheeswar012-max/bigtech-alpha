"""
╔══════════════════════════════════════════════════════════════════╗
║  BIGTECH ALPHA — Big Tech Intelligence Platform  v6.2           ║
║  Live data: Apple · Microsoft · Google · Amazon · Meta          ║
║             NVIDIA · Tesla · Netflix                             ║
║  Run: streamlit run nexus.py                                     ║
╚══════════════════════════════════════════════════════════════════╝

Architecture
────────────
nexus.py                      ← this file: config, data loading, sidebar, router
pages/
  page_command_center.py      ← Page 1
  page_stock_performance.py   ← Page 2
  page_revenue_earnings.py    ← Page 3
  page_competitive_analysis.py← Page 4
  page_deep_analytics.py      ← Page 5
  page_ai_insights.py         ← Page 6
nexus_ld_page.py              ← Page 7  (Live Dashboard)
live_data.py                  ← yfinance data layer
constants.py                  ← single source of truth: companies, colours, TTLs
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path

# ── SINGLE SOURCE OF TRUTH: all company / colour constants ──────────────────
from constants import (
    COLORS,          # company-name → hex  (used by every chart)
    ALL_COMPANIES,   # ordered list of display names
    COMPANIES,       # ticker → name  (re-exported for page modules that need it)
    COMPANY_COLORS,  # ticker → hex   (used by live dashboard / intraday charts)
    NAME_TO_TICKER,  # name → ticker
    DATA_TTL,        # cache TTL values
)

st.set_page_config(
    page_title="BIGTECH ALPHA", page_icon="🚀",
    layout="wide", initial_sidebar_state="expanded"
)

# ── GLOBAL CSS (shared across all pages) ─────────────────────────────────────
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
[data-testid="stSidebar"] [data-baseweb="tag"]{background:rgba(255,255,255,0.2)!important;border:1px solid rgba(255,255,255,0.35)!important;border-radius:6px!important;}
[data-testid="stSidebar"] [data-baseweb="tag"] span{color:#fff!important;}
[data-testid="stSidebar"] [data-baseweb="tag"] button svg{fill:#fff!important;}
[data-testid="stSidebar"] .stButton>button{width:100%!important;background:rgba(255,255,255,0.10)!important;border:1px solid rgba(255,255,255,0.18)!important;border-radius:12px!important;color:#fff!important;font-size:0.82rem!important;font-weight:500!important;padding:0.55rem 1rem!important;text-align:left!important;margin-bottom:0.25rem!important;transition:all 0.2s!important;}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,0.22)!important;border-color:rgba(255,255,255,0.4)!important;transform:translateX(4px)!important;}
[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:rgba(255,255,255,0.30)!important;border-color:rgba(255,255,255,0.6)!important;font-weight:700!important;box-shadow:0 2px 12px rgba(0,0,0,0.15)!important;}
[data-testid="stSlider"] div[role="slider"]{background:#ffffff!important;border:2px solid rgba(255,255,255,0.8)!important;box-shadow:0 0 0 4px rgba(255,255,255,0.15)!important;width:16px!important;height:16px!important;border-radius:50%!important;}
[data-testid="stSlider"] [class*="Track"],[data-testid="stSlider"] [class*="track"]{background:rgba(255,255,255,0.2)!important;height:4px!important;border-radius:2px!important;}
[data-testid="stSlider"] [class*="Track"] div,[data-testid="stSlider"] [class*="track"] div{background:rgba(255,255,255,0.2)!important;}
[data-baseweb="slider"] div[class*="Track"]>div:nth-child(2){background:#ffffff!important;}
[data-baseweb="slider"] [data-testid="stSlider"] div[role="slider"]{background:#ffffff!important;border:2px solid rgba(255,255,255,0.9)!important;}
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
.closed-badge{background:rgba(100,116,139,0.18);color:#94a3b8!important;border:1px solid rgba(100,116,139,0.35);}
.sec{display:flex;align-items:center;gap:1rem;margin:2.5rem 0 1.4rem 0;}
.sec-title{font-family:'Outfit',sans-serif;font-size:0.9rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--txt);}
.sec-line{flex:1;height:1px;background:linear-gradient(90deg,var(--border2),transparent);}
.sec-tag{font-size:0.58rem;color:#fff!important;background:linear-gradient(135deg,var(--primary),var(--accent));padding:0.28rem 0.8rem;border-radius:100px;font-weight:600;}
.sec-tag.closed{background:linear-gradient(135deg,#475569,#64748b)!important;}
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
.dead{display:inline-block;width:8px;height:8px;background:#64748b;border-radius:50%;margin-right:6px;vertical-align:middle;}
@keyframes pulse-ring{0%{box-shadow:0 0 0 0 rgba(52,211,153,0.5);}70%{box-shadow:0 0 0 8px rgba(52,211,153,0);}100%{box-shadow:0 0 0 0 rgba(52,211,153,0);}}
.price-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:2rem;}
.price-card{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:1.2rem 1.4rem 1rem;position:relative;overflow:hidden;box-shadow:var(--shadow);transition:all 0.25s;}
.price-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg);}
.price-card-bar{position:absolute;top:0;left:0;right:0;height:3px;}
.price-card-ticker{font-family:'JetBrains Mono',monospace;font-size:0.6rem;font-weight:700;letter-spacing:0.14em;color:var(--txt3);margin-bottom:0.25rem;text-transform:uppercase;}
.price-card-co{font-size:0.82rem;font-weight:700;color:var(--txt);margin-bottom:0.7rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.price-card-price{font-family:'Outfit',sans-serif;font-size:1.75rem;font-weight:800;line-height:1.0;margin-bottom:0.4rem;}
.price-card-chg{font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;}
.price-card-vol{font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:var(--txt3);margin-top:0.35rem;}
.price-card-badge{position:absolute;top:0.9rem;right:0.9rem;font-size:0.52rem;padding:0.18rem 0.6rem;border-radius:100px;font-weight:700;}
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
.cmp-co{font-weight:600;color:var(--txt);}
.badge-up{color:#34d399;font-weight:700;}
.badge-dn{color:#f87171;font-weight:700;}
.badge-fl{color:#fbbf24;font-weight:700;}
.logo-wrap{padding:1.6rem 0 1.2rem;}
.logo-text{font-family:'Outfit',sans-serif;font-size:1.6rem;font-weight:900;color:#fff!important;}
.logo-sub{font-size:0.55rem;color:rgba(255,255,255,0.55)!important;letter-spacing:0.16em;margin-top:0.25rem;}
.h-divider{height:1px;background:rgba(255,255,255,0.15);margin:0.8rem 0;}
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

# ── PAGE INDEX CONSTANTS ─────────────────────────────────────────────────────────
PAGE_NAMES = [
    "🏠  Command Center", "📈  Stock Performance", "💰  Revenue & Earnings",
    "🏆  Competitive Analysis", "🔬  Deep Analytics",
    "🤖  AI Insight Engine", "📡  Live Dashboard",
]
PAGE_CC, PAGE_SP, PAGE_RE, PAGE_CA, PAGE_DA, PAGE_AI, PAGE_LD = range(7)

if "page_idx" not in st.session_state:
    st.session_state.page_idx = 0


# ── SHARED HELPERS ────────────────────────────────────────────────────────────
def hex_to_rgba(h, a=0.15):
    """Convert a CSS hex colour to rgba() string with the given alpha."""
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{a})'


def sf(fig, h=360, legend=True):
    """Apply the shared dark Plotly theme to a figure and set its height."""
    kw = dict(**PL, height=h)
    if not legend:
        kw['showlegend'] = False
    fig.update_layout(**kw)
    return fig


def sec(title, tag="", closed=False):
    """Render a styled horizontal section divider with an optional tag pill."""
    tag_cls = 'sec-tag closed' if closed else 'sec-tag'
    t = f'<div class="{tag_cls}">{tag}</div>' if tag else ''
    st.markdown(
        f'<div class="sec"><div class="sec-title">{title}</div>'
        f'<div class="sec-line"></div>{t}</div>',
        unsafe_allow_html=True)


def nav_to(idx):
    """Navigate to a page by index and trigger a Streamlit rerun."""
    st.session_state.page_idx = idx


# ── OPTIONAL LIVE IMPORTS ─────────────────────────────────────────────────────
try:
    from live_data import (
        get_live_price, get_intraday_data, get_multi_live_prices,
        get_all_fundamentals, get_all_price_history,
        get_all_quarterly, get_all_annual, merge_with_csv,
        is_market_open,
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
    """Load the three bundled CSV datasets from the repo root."""
    from constants import CSV_FILES
    base = Path(__file__).parent
    q = pd.read_csv(base / CSV_FILES["quarterly"], parse_dates=["Quarter"])
    a = pd.read_csv(base / CSV_FILES["annual"])
    p = pd.read_csv(base / CSV_FILES["prices"], parse_dates=["Date"])
    return q, a, p


@st.cache_data(ttl=DATA_TTL["annual"], show_spinner=False)
def load_live_annual():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_annual()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=DATA_TTL["quarterly"], show_spinner=False)
def load_live_quarterly():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_quarterly()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=DATA_TTL["price_history"], show_spinner=False)
def load_live_prices():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_price_history(period="5y")
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=DATA_TTL["fundamentals"], show_spinner=False)
def load_live_fundamentals():
    if not _live_ok:
        return pd.DataFrame()
    try:
        return get_all_fundamentals()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=DATA_TTL["merged_pipeline"], show_spinner=False)
def build_merged_data():
    """Merge live yfinance data with bundled CSVs; live data wins on overlap."""
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
                csv_patch, on=['Company', 'Year'], how='left', suffixes=('', '_csv')
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
    """Return the latest year for which >= 50% of the selected companies have data."""
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
    """Return (slice_df, year) for the best common year in the given companies."""
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


# ── SHARED HELPER BUNDLE (passed into every page module) ─────────────────────
_HELPERS = dict(
    sec=sec, sf=sf, hex_to_rgba=hex_to_rgba,
    get_latest_slice=get_latest_slice,
    best_common_year=best_common_year,
)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <div style="font-size:2rem;margin-bottom:0.35rem;">🚀</div>
      <div class="logo-text">BIGTECH ALPHA</div>
      <div class="logo-sub">BIG TECH INTELLIGENCE · v6.2</div>
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
    data_src     = "Live Data" if (_live_ok and not ann_df.empty) else "CSV Fallback"
    price_latest = price_df['Date'].max().strftime("%Y-%m-%d") if not price_df.empty else "—"
    st.markdown(
        f"<div style='font-size:0.6rem;opacity:0.5;line-height:2;'>"
        f"🕐 {datetime.now().strftime('%H:%M:%S')}<br>"
        f"📡 {data_src}<br>"
        f"📅 Latest year: {COMMON_LATEST_YEAR}<br>"
        f"📈 Prices to: {price_latest}<br>"
        f"🗂 {len(q_df)+len(ann_df)+len(price_df):,} records"
        f"</div>",
        unsafe_allow_html=True,
    )

page_idx = st.session_state.page_idx


# ── PAGE HEADER HELPERS ───────────────────────────────────────────────────────
def page_header_range(title_html, key_suffix):
    """Render a page title + year-range slider; returns (start_year, end_year)."""
    title_col, _, yr_col = st.columns([5, 0.5, 2.5])
    with title_col:
        st.markdown(f'<p class="page-title">{title_html}</p>', unsafe_allow_html=True)
    with yr_col:
        st.markdown(
            '<div class="yr-card"><div class="yr-card-label">'
            '<span class="yr-icon">📅</span> Year Range</div>',
            unsafe_allow_html=True)
        yr = st.slider(
            "Year Range", SLIDER_MIN, SLIDER_MAX, (SLIDER_MIN, SLIDER_MAX),
            label_visibility="collapsed", key=f"yr_range_{key_suffix}",
        )
        st.markdown(
            f'<div style="display:flex;justify-content:flex-end;margin-top:0.1rem;">'
            f'<span class="yr-badge">{yr[0]} – {yr[1]}</span></div></div>',
            unsafe_allow_html=True)
    return yr


def page_header_single(title_html, key_suffix):
    """Render a page title + single-year selector; returns the selected year."""
    title_col, _, yr_col = st.columns([5, 0.5, 2.5])
    with title_col:
        st.markdown(f'<p class="page-title">{title_html}</p>', unsafe_allow_html=True)
    with yr_col:
        st.markdown(
            '<div class="yr-card"><div class="yr-card-label">'
            '<span class="yr-icon">📅</span> Select Year</div>',
            unsafe_allow_html=True)
        yr = st.selectbox(
            "Year", options=ALL_YEARS, index=len(ALL_YEARS) - 1,
            label_visibility="collapsed", key=f"yr_single_{key_suffix}",
        )
        st.markdown(
            f'<div style="display:flex;justify-content:flex-end;margin-top:0.1rem;">'
            f'<span class="yr-badge">FY {yr}</span></div></div>',
            unsafe_allow_html=True)
    return yr


# ── TICKER TAPE ───────────────────────────────────────────────────────────────
from constants import TICKERS as _TICKERS
ticker_html = " &nbsp;·&nbsp; ".join([f'<span class="sym">{s}</span>' for s in _TICKERS * 2])
st.markdown(
    f'<div class="ticker-wrap"><div class="ticker-inner">{ticker_html} &nbsp;&nbsp; {ticker_html}</div></div>',
    unsafe_allow_html=True,
)


# ════════════════════════════════════════════════════════════════════
# PAGE ROUTER — each branch is a single function call
# ════════════════════════════════════════════════════════════════════
if page_idx == PAGE_CC:
    from pages.page_command_center import render_cc
    year_range = page_header_range("🏠 Command Center", "cc")
    render_cc(
        ann_df, q_df, price_df, fund_df,
        sel_companies, year_range,
        COMMON_LATEST_YEAR, COLORS, PL,
        **_HELPERS,
    )

elif page_idx == PAGE_SP:
    from pages.page_stock_performance import render_sp
    year_range = page_header_range("📈 Stock Performance", "sp")
    render_sp(price_df, ann_df, sel_companies, year_range, COLORS, PL, sec, sf)

elif page_idx == PAGE_RE:
    from pages.page_revenue_earnings import render_re
    year_range = page_header_range("💰 Revenue & Earnings", "re")
    render_re(ann_df, q_df, sel_companies, year_range, COLORS, PL, sec, sf, hex_to_rgba)

elif page_idx == PAGE_CA:
    from pages.page_competitive_analysis import render_ca
    sel_year = page_header_single("🏆 Competitive Analysis", "ca")
    render_ca(ann_df, sel_companies, sel_year, COLORS, PL, sec, sf, hex_to_rgba)

elif page_idx == PAGE_DA:
    from pages.page_deep_analytics import render_da
    year_range = page_header_range("🔬 Deep Analytics", "da")
    render_da(ann_df, price_df, sel_companies, year_range, COLORS, PL, sec, sf)

elif page_idx == PAGE_AI:
    from pages.page_ai_insights import render_ai
    sel_year = page_header_single("🤖 AI Insight Engine", "ai")
    render_ai(ann_df, sel_companies, sel_year, COLORS, PL, sec, sf)

elif page_idx == PAGE_LD:
    from nexus_ld_page import render_ld
    render_ld(sel_companies, _live_ok, _autorefresh_ok)
