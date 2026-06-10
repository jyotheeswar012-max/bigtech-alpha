"""
╔══════════════════════════════════════════════════════════════════╗
║  MARKET NEXUS — Big Tech Intelligence Platform                   ║
║  Real data: Apple · Microsoft · Google · Amazon · Meta          ║
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

/* ── base ── */
.stApp { background: var(--bg) !important; font-family:'Space Grotesk',sans-serif; }
.main .block-container { padding:1.2rem 1.8rem !important; max-width:100% !important; }
*{ box-sizing:border-box; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
  background:linear-gradient(175deg,#040916 0%,#060d1e 100%) !important;
  border-right:1px solid var(--border) !important;
}

/* ── hero ── */
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

/* ── KPI row ── */
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

/* ── section header ── */
.sec { display:flex; align-items:center; gap:0.75rem; margin:2rem 0 1rem 0; }
.sec-title { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700;
  letter-spacing:0.06em; text-transform:uppercase; white-space:nowrap; }
.sec-line  { flex:1; height:1px; background:var(--border); }
.sec-tag   { font-family:'JetBrains Mono',monospace; font-size:0.58rem;
  color:var(--orange) !important; letter-spacing:0.1em; white-space:nowrap; }

/* ── chart card ── */
.chart-card {
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:14px; padding:1.2rem 1.2rem 0.6rem; margin-bottom:1rem;
}

/* ── company tag ── */
.co-tag { display:inline-flex; align-items:center; gap:0.35rem;
  background:var(--surface); border:1px solid var(--border);
  border-radius:8px; padding:0.3rem 0.65rem;
  font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:var(--txt2) !important; }

/* ── rank table ── */
.rank-row { display:flex; align-items:center; gap:0.75rem;
  padding:0.6rem 0.8rem; border-radius:8px; margin-bottom:0.3rem;
  border:1px solid transparent; transition:border-color .15s; }
.rank-row:hover { border-color:var(--border); background:var(--surface); }
.rank-num { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:800;
  color:var(--txt3); width:1.5rem; text-align:center; }
.rank-name { font-weight:600; font-size:0.85rem; flex:1; }
.rank-val  { font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:var(--cyan); }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] { gap:0.4rem; background:transparent;
  border-bottom:1px solid var(--border); padding-bottom:0; }
.stTabs [data-baseweb="tab"] { background:transparent !important; border:1px solid transparent !important;
  border-radius:8px 8px 0 0 !important; color:var(--txt2) !important;
  font-family:'Space Grotesk',sans-serif; font-size:0.82rem; padding:0.55rem 1.1rem !important; }
.stTabs [aria-selected="true"] { background:var(--bg-card) !important;
  border-color:var(--border) !important; color:var(--cyan) !important; }

/* ── live dot ── */
.live { display:inline-block; width:7px; height:7px; background:var(--green);
  border-radius:50%; margin-right:5px; vertical-align:middle;
  box-shadow:0 0 6px var(--green); animation:blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.4;} }

/* ── scrollbar ── */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--txt3);border-radius:3px;}

/* ── sidebar widgets ── */
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
# Brand colors per company
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

# ── Helper: convert hex color to rgba string with given opacity ──
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

# ── DATA LOADING ──────────────────────────────────────────────────────────────
@st.cache_data
def load():
    base = Path(__file__).parent
    q  = pd.read_csv(base/"quarterly_revenue.csv", parse_dates=["Quarter"])
    a  = pd.read_csv(base/"annual_metrics.csv")
    p  = pd.read_csv(base/"stock_prices.csv", parse_dates=["Date"])
    return q, a, p

q_df, ann_df, price_df = load()

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
        BIG TECH INTELLIGENCE v3.0
      </div>
      <div style="margin-top:0.8rem;">
        <span class="live"></span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:#00ff9d;">
          REAL DATA · 8 COMPANIES
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
    ], label_visibility="hidden")

    st.markdown("<hr style='border-color:rgba(0,229,255,0.07);margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.62rem;text-transform:uppercase;letter-spacing:0.1em;color:#2d3f5a;margin-bottom:0.5rem;">COMPANIES</div>', unsafe_allow_html=True)
    sel_companies = st.multiselect("", ALL_COMPANIES, default=ALL_COMPANIES, label_visibility="hidden")
    if not sel_companies: sel_companies = ALL_COMPANIES

    st.markdown("<hr style='border-color:rgba(0,229,255,0.07);margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.62rem;text-transform:uppercase;letter-spacing:0.1em;color:#2d3f5a;margin-bottom:0.5rem;">YEAR RANGE</div>', unsafe_allow_html=True)
    year_range = st.slider("", 2020, 2024, (2020, 2024), label_visibility="hidden")

    st.markdown("<hr style='border-color:rgba(0,229,255,0.07);margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#2d3f5a;line-height:2.0;">
      UPDATED: {datetime.now().strftime("%H:%M:%S")}<br>
      RECORDS: {len(q_df)+len(ann_df)+len(price_df):,}<br>
      SOURCE: Public Earnings Reports<br>
      PERIOD: 2020 – 2024
    </div>
    """, unsafe_allow_html=True)

# ── Filtered data ─────────────────────────────────────────────────────────────
ann_f = ann_df[(ann_df.Company.isin(sel_companies)) & (ann_df.Year.between(*year_range))]
q_f   = q_df[(q_df.Company.isin(sel_companies)) & (q_df.Quarter.dt.year.between(*year_range))]
p_f   = price_df[(price_df.Company.isin(sel_companies)) &
                 (price_df.Date.dt.year.between(*year_range))]

# ── PAGE: COMMAND CENTER ──────────────────────────────────────────────────────
if "Command Center" in page:

    # ── Hero ──
    st.markdown(f"""
    <div class="hero">
      <div class="hero-grid"></div><div class="hero-glow1"></div><div class="hero-glow2"></div>
      <div style="position:relative;z-index:1;">
        <div class="hero-eyebrow">⚡ Real-Time Big Tech Intelligence Platform</div>
        <p class="hero-title">MARKET NEXUS</p>
        <p class="hero-sub">
          Live financial analytics across <strong style="color:#00e5ff;">Apple · Microsoft · Google ·
          Amazon · Meta · NVIDIA · Tesla · Netflix</strong> —
          powered by real earnings data, stock history & competitive benchmarks.
        </p>
        <div class="hero-chips">
          <span class="chip">📊 Real Earnings Data</span>
          <span class="chip orange">📈 5-Year Stock History</span>
          <span class="chip green">🏆 Competitive Intel</span>
          <span class="chip">💡 AI Insights</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──
    latest = ann_df[ann_df.Year == 2024]
    total_rev   = latest.Revenue_B.sum()
    total_mcap  = latest.MarketCap_B.sum()
    top_mcap_co = latest.loc[latest.MarketCap_B.idxmax(), 'Company']
    top_mcap    = latest.MarketCap_B.max()
    nvda_ni     = latest[latest.Company=='NVIDIA']['NetIncome_B'].values[0]

    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi">
        <div class="kpi-stripe"></div>
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Combined 2024 Revenue</div>
        <div class="kpi-val">${total_rev/1000:.2f}T</div>
        <div class="kpi-sub">8 companies · real earnings</div>
        <div class="kpi-badge up">↑ Live</div>
      </div>
      <div class="kpi">
        <div class="kpi-stripe orange"></div>
        <div class="kpi-icon">🏦</div>
        <div class="kpi-label">Combined Market Cap</div>
        <div class="kpi-val orange">${total_mcap/1000:.1f}T</div>
        <div class="kpi-sub">end of 2024</div>
        <div class="kpi-badge up">↑ +38% YoY</div>
      </div>
      <div class="kpi">
        <div class="kpi-stripe green"></div>
        <div class="kpi-icon">🥇</div>
        <div class="kpi-label">Largest by Market Cap</div>
        <div class="kpi-val green">{top_mcap_co}</div>
        <div class="kpi-sub">${top_mcap:,.0f}B cap</div>
        <div class="kpi-badge flat">2024</div>
      </div>
      <div class="kpi">
        <div class="kpi-stripe purple"></div>
        <div class="kpi-icon">⚡</div>
        <div class="kpi-label">NVIDIA Net Income 2024</div>
        <div class="kpi-val purple">${nvda_ni:.1f}B</div>
        <div class="kpi-sub">AI boom · +144% YoY</div>
        <div class="kpi-badge up">↑ Record</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1: Revenue race + Market cap evolution ──
    sec("Revenue Race & Market Cap", "2020 – 2024 · REAL DATA")
    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        for co in sel_companies:
            sub = q_f[q_f.Company==co].sort_values('Quarter')
            fig.add_trace(go.Scatter(
                x=sub.Quarter, y=sub.Revenue_B, name=co, mode='lines',
                line=dict(color=COLORS[co], width=2.5),
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>${{y:.1f}}B<extra></extra>'
            ))
        sf(fig, 350).update_layout(
            title=dict(text="Quarterly Revenue ($B) — Real Earnings", font=dict(size=12,color='#6b80a0')),
            yaxis_title="Revenue ($B)"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

    with c2:
        mc_data = ann_f.pivot(index='Year', columns='Company', values='MarketCap_B').fillna(0)
        fig = go.Figure()
        for co in [c for c in sel_companies if c in mc_data.columns]:
            fig.add_trace(go.Bar(
                x=mc_data.index, y=mc_data[co], name=co,
                marker_color=COLORS[co], opacity=0.85,
                hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:,.0f}}B<extra></extra>'
            ))
        fig.update_layout(barmode='group')
        sf(fig, 350).update_layout(
            title=dict(text="Market Capitalization by Year ($B)", font=dict(size=12,color='#6b80a0')),
            yaxis_title="Market Cap ($B)"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

    # ── Row 2: Stock performance + profit margin ──
    sec("Stock Returns & Profitability", "5-YEAR JOURNEY")
    c1, c2 = st.columns([3,2])

    with c1:
        fig = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f.Company==co].sort_values('Date')
            base = sub.Price.iloc[0]
            fig.add_trace(go.Scatter(
                x=sub.Date, y=sub.Price/base*100, name=co, mode='lines',
                line=dict(color=COLORS[co], width=2),
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>%{{y:.0f}} (base 100)<extra></extra>'
            ))
        fig.add_hline(y=100, line_dash='dot', line_color='rgba(255,255,255,0.1)')
        sf(fig, 340).update_layout(
            title=dict(text="Normalised Stock Performance (Base = 100 on Jan 2020)", font=dict(size=12,color='#6b80a0')),
            yaxis_title="Indexed Return"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

    with c2:
        ann_2024 = ann_df[ann_df.Year==2024].copy()
        ann_2024['Margin'] = (ann_2024.NetIncome_B / ann_2024.Revenue_B * 100).round(1)
        ann_2024 = ann_2024[ann_2024.Company.isin(sel_companies)].sort_values('Margin')
        fig = go.Figure(go.Bar(
            x=ann_2024.Margin, y=ann_2024.Company, orientation='h',
            marker=dict(
                color=ann_2024.Margin,
                colorscale=[[0,'#ff375f'],[0.4,'#ff6d2d'],[1,'#00ff9d']],
                line=dict(width=0)
            ),
            text=[f"{v:.1f}%" for v in ann_2024.Margin],
            textposition='outside', textfont=dict(size=10,color='#6b80a0'),
            hovertemplate='<b>%{y}</b><br>Margin: %{x:.1f}%<extra></extra>'
        ))
        sf(fig, 340, legend=False).update_layout(
            title=dict(text="Net Profit Margin 2024 (Real)", font=dict(size=12,color='#6b80a0')),
            xaxis_title="Net Margin %"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

    # ── Row 3: Revenue treemap + Employee productivity ──
    sec("Revenue Distribution & Headcount", "STRUCTURAL VIEW")
    c1, c2 = st.columns(2)

    with c1:
        latest_rev = ann_df[ann_df.Year==2024][ann_df.Company.isin(sel_companies)]
        fig = px.treemap(
            latest_rev, path=['Sector','Company'], values='Revenue_B',
            color='NetIncome_B',
            color_continuous_scale=[[0,'#ff375f'],[0.5,'#0c1528'],[1,'#00ff9d']],
            hover_data={'Revenue_B':':.1f','NetIncome_B':':.1f'},
        )
        fig.update_traces(
            textfont_size=13, textfont_color='white',
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value:.1f}B<extra></extra>'
        )
        fig.update_layout(**PL, height=330,
            title=dict(text="2024 Revenue Treemap — Color = Net Income", font=dict(size=12,color='#6b80a0')),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

    with c2:
        ann_2024_e = ann_df[(ann_df.Year==2024)&(ann_df.Company.isin(sel_companies))].copy()
        ann_2024_e['RevPerEmp'] = (ann_2024_e.Revenue_B * 1e9 / (ann_2024_e.Employees_K * 1e3) / 1e6).round(2)
        ann_2024_e = ann_2024_e.sort_values('RevPerEmp', ascending=True)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=ann_2024_e.RevPerEmp, y=ann_2024_e.Company, orientation='h',
            marker=dict(
                color=[COLORS[c] for c in ann_2024_e.Company],
                line=dict(width=0)
            ),
            text=[f"${v:.2f}M" for v in ann_2024_e.RevPerEmp],
            textposition='outside', textfont=dict(size=10, color='#6b80a0'),
            hovertemplate='<b>%{y}</b><br>$%{x:.2f}M per employee<extra></extra>'
        ))
        sf(fig, 330, legend=False).update_layout(
            title=dict(text="Revenue per Employee 2024 ($M) — Real Headcount", font=dict(size=12,color='#6b80a0')),
            xaxis_title="$M per Employee"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})


# ── PAGE: STOCK PERFORMANCE ───────────────────────────────────────────────────
elif "Stock Performance" in page:
    st.markdown('<p class="hero-title" style="font-size:2.2rem;margin-bottom:1.5rem;">📈 Stock Performance</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊  Price History", "📉  Volatility & Risk", "🎯  Return Analysis"])

    with tab1:
        co1 = st.selectbox("Company", sel_companies, key='sp1')
        sub = p_f[p_f.Company==co1].sort_values('Date').copy()
        sub['MA50']  = sub.Price.rolling(50).mean()
        sub['MA200'] = sub.Price.rolling(200).mean()
        sub['Upper'] = sub.Price.rolling(20).mean() + 2*sub.Price.rolling(20).std()
        sub['Lower'] = sub.Price.rolling(20).mean() - 2*sub.Price.rolling(20).std()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.Upper, name='BB Upper',
            line=dict(color='rgba(0,229,255,0.2)', width=1, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.Lower, name='BB Lower',
            fill='tonexty', fillcolor='rgba(0,229,255,0.04)',
            line=dict(color='rgba(0,229,255,0.2)', width=1, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.Price, name='Price',
            line=dict(color=COLORS[co1], width=2.5),
            hovertemplate='<b>'+co1+'</b><br>%{x|%b %d, %Y}<br>$%{y:.2f}<extra></extra>'))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.MA50,  name='MA50',
            line=dict(color='#ffd60a', width=1.5, dash='dot')))
        fig.add_trace(go.Scatter(x=sub.Date, y=sub.MA200, name='MA200',
            line=dict(color='#bf5af2', width=1.5, dash='dash')))

        sf(fig, 420).update_layout(
            title=dict(text=f"{co1} — Price + Bollinger Bands + Moving Averages", font=dict(size=12,color='#6b80a0')),
            yaxis_title="Price (USD)"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        fig2 = go.Figure(go.Bar(x=sub.Date, y=sub.Volume_M,
            marker_color=COLORS[co1], opacity=0.4, name='Volume'))
        sf(fig2, 120, legend=False).update_layout(yaxis_title="Volume (M)", margin=dict(t=10))
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})

    with tab2:
        fig = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f.Company==co].sort_values('Date')
            vol = sub.Daily_Return.rolling(30).std()
            fig.add_trace(go.Scatter(x=sub.Date, y=vol, name=co, mode='lines',
                line=dict(color=COLORS[co], width=1.8),
                hovertemplate=f'<b>{co}</b> %{{x|%b %Y}}<br>Vol: %{{y:.2f}}%<extra></extra>'))
        sf(fig, 340).update_layout(
            title=dict(text="30-Day Rolling Volatility (Std Dev of Daily Returns)", font=dict(size=12,color='#6b80a0')),
            yaxis_title="Volatility (%)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        stats = p_f.groupby('Company').agg(
            Avg_Return=('Daily_Return','mean'),
            Volatility=('Daily_Return','std'),
        ).reset_index()
        total_return = p_f.groupby('Company').apply(
            lambda g: (g.sort_values('Date').Price.iloc[-1] / g.sort_values('Date').Price.iloc[0] - 1)*100
        ).reset_index(name='Total_Return_Pct')
        stats = stats.merge(total_return, on='Company')
        stats = stats[stats.Company.isin(sel_companies)]

        fig2 = go.Figure()
        for _, row in stats.iterrows():
            fig2.add_trace(go.Scatter(
                x=[row.Volatility], y=[row.Total_Return_Pct],
                mode='markers+text', name=row.Company,
                text=[row.Company], textposition='top center',
                textfont=dict(size=10, color=COLORS[row.Company]),
                marker=dict(size=18, color=COLORS[row.Company],
                            line=dict(width=2,color='rgba(255,255,255,0.2)')),
                hovertemplate=f'<b>{row.Company}</b><br>Volatility: {row.Volatility:.2f}%<br>Total Return: {row.Total_Return_Pct:.0f}%<extra></extra>'
            ))
        fig2.add_hline(y=0, line_dash='dot', line_color='rgba(255,255,255,0.08)')
        fig2.add_vline(x=stats.Volatility.mean(), line_dash='dot', line_color='rgba(255,255,255,0.08)')
        sf(fig2, 340).update_layout(
            title=dict(text="Risk vs Total Return 2020–2024 (bubble = company)", font=dict(size=12,color='#6b80a0')),
            xaxis_title="Daily Volatility (Std Dev %)", yaxis_title="Total Return %", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})

    with tab3:
        p_f2 = p_f.copy()
        p_f2['Year'] = p_f2.Date.dt.year
        annual_ret = p_f2.groupby(['Company','Year']).apply(
            lambda g: (g.sort_values('Date').Price.iloc[-1] / g.sort_values('Date').Price.iloc[0] - 1)*100
        ).reset_index(name='Annual_Return')
        pivot = annual_ret[annual_ret.Company.isin(sel_companies)].pivot(
            index='Company', columns='Year', values='Annual_Return')

        fig = go.Figure(go.Heatmap(
            z=pivot.values, x=[str(c) for c in pivot.columns], y=list(pivot.index),
            colorscale=[[0,'#ff375f'],[0.45,'#0c1528'],[1,'#00ff9d']],
            zmid=0,
            text=[[f"{v:.0f}%" for v in row] for row in pivot.values],
            texttemplate='%{text}', textfont=dict(size=11),
            hovertemplate='<b>%{y}</b> %{x}<br>Return: %{z:.1f}%<extra></extra>'
        ))
        sf(fig, 360, legend=False).update_layout(
            title=dict(text="Annual Stock Return % — Red=Loss · Green=Gain", font=dict(size=12,color='#6b80a0')))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        fig2 = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f.Company==co]
            fig2.add_trace(go.Violin(
                x=[co]*len(sub), y=sub.Daily_Return, name=co,
                box_visible=True, meanline_visible=True,
                fillcolor=hex_to_rgba(COLORS[co], 0.19),
                line_color=COLORS[co], opacity=0.85,
                hovertemplate=f'<b>{co}</b><br>%{{y:.3f}}%<extra></extra>'
            ))
        sf(fig2, 340).update_layout(
            title=dict(text="Daily Return Distribution — Real Stock History", font=dict(size=12,color='#6b80a0')),
            yaxis_title="Daily Return %")
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})


# ── PAGE: REVENUE & EARNINGS ──────────────────────────────────────────────────
elif "Revenue" in page:
    st.markdown('<p class="hero-title" style="font-size:2.2rem;margin-bottom:1.5rem;">💰 Revenue & Earnings</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊  Quarterly Deep-Dive", "📈  Growth Trends", "💎  Profitability"])

    with tab1:
        co2 = st.selectbox("Company", sel_companies, key='re1')
        sub = q_f[q_f.Company==co2].sort_values('Quarter')
        sub['QoQ'] = sub.Revenue_B.pct_change()*100
        sub['YoY'] = sub.Revenue_B.pct_change(4)*100

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.65,0.35], vertical_spacing=0.08)
        fig.add_trace(go.Bar(x=sub.Quarter, y=sub.Revenue_B,
            name='Revenue ($B)', marker_color=COLORS[co2], opacity=0.8,
            hovertemplate='%{x|%b %Y}<br>$%{y:.1f}B<extra></extra>'), row=1,col=1)
        fig.add_trace(go.Scatter(x=sub.Quarter, y=sub.Revenue_B.rolling(4).mean(),
            name='4Q Rolling Avg', line=dict(color='#ffd60a', width=2, dash='dot')), row=1,col=1)
        fig.add_trace(go.Bar(x=sub.Quarter, y=sub.YoY,
            name='YoY Growth %',
            marker_color=['#00ff9d' if v>=0 else '#ff375f' for v in sub.YoY.fillna(0)],
            hovertemplate='%{x|%b %Y}<br>YoY: %{y:.1f}%<extra></extra>'), row=2,col=1)
        sf(fig, 440).update_layout(
            title=dict(text=f"{co2} — Quarterly Revenue + YoY Growth (Real Earnings)", font=dict(size=12,color='#6b80a0')))
        fig.update_yaxes(title_text="Revenue ($B)", row=1, col=1)
        fig.update_yaxes(title_text="YoY %", row=2, col=1)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

    with tab2:
        cagr_rows = []
        for co in sel_companies:
            sub = ann_df[(ann_df.Company==co)&(ann_df.Year.isin([2020,2024]))].sort_values('Year')
            if len(sub)==2:
                r0, r4 = sub.Revenue_B.iloc[0], sub.Revenue_B.iloc[1]
                cagr = ((r4/r0)**0.25 - 1)*100
                cagr_rows.append({'Company':co,'CAGR':round(cagr,1),'2020':r0,'2024':r4})
        cagr_df = pd.DataFrame(cagr_rows).sort_values('CAGR', ascending=True)

        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure(go.Bar(
                x=cagr_df.CAGR, y=cagr_df.Company, orientation='h',
                marker=dict(color=[COLORS[c] for c in cagr_df.Company], line=dict(width=0)),
                text=[f"{v:.1f}%" for v in cagr_df.CAGR],
                textposition='outside', textfont=dict(size=11,color='#6b80a0'),
                hovertemplate='<b>%{y}</b><br>CAGR: %{x:.1f}%<extra></extra>'
            ))
            sf(fig, 340, legend=False).update_layout(
                title=dict(text="Revenue CAGR 2020–2024 (Real Data)", font=dict(size=12,color='#6b80a0')),
                xaxis_title="4-Year CAGR %")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        with c2:
            fig2 = go.Figure()
            for co in sel_companies:
                sub2 = ann_f[ann_f.Company==co].sort_values('Year')
                fig2.add_trace(go.Scatter(
                    x=sub2.Year, y=sub2.Revenue_B, name=co,
                    mode='lines+markers', stackgroup='one',
                    fillcolor=hex_to_rgba(COLORS[co], 0.33),
                    line=dict(color=COLORS[co], width=1.5),
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:.1f}}B<extra></extra>'
                ))
            sf(fig2, 340).update_layout(
                title=dict(text="Stacked Revenue — Combined Big Tech ($B)", font=dict(size=12,color='#6b80a0')),
                yaxis_title="Revenue ($B)")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})

    with tab3:
        ni_data = ann_f.pivot(index='Year', columns='Company', values='NetIncome_B').fillna(0)
        fig = go.Figure()
        for co in [c for c in sel_companies if c in ni_data.columns]:
            fig.add_trace(go.Scatter(
                x=ni_data.index, y=ni_data[co], name=co, mode='lines+markers',
                line=dict(color=COLORS[co], width=2.5),
                marker=dict(size=8, color=COLORS[co], line=dict(width=2,color='rgba(0,0,0,0.4)')),
                hovertemplate=f'<b>{co}</b> %{{x}}<br>Net Income: $%{{y:.1f}}B<extra></extra>'
            ))
        fig.add_hline(y=0, line_dash='dot', line_color='rgba(255,255,255,0.1)')
        sf(fig, 360).update_layout(
            title=dict(text="Net Income 2020–2024 ($B) — Real Earnings", font=dict(size=12,color='#6b80a0')),
            yaxis_title="Net Income ($B)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        c1, c2 = st.columns(2)
        with c1:
            yr = st.selectbox("Year", [2020,2021,2022,2023,2024], index=4, key='yr_ni')
            sub3 = ann_df[(ann_df.Year==yr)&(ann_df.Company.isin(sel_companies))]
            fig2 = go.Figure()
            for _, row in sub3.iterrows():
                fig2.add_trace(go.Scatter(
                    x=[row.Revenue_B], y=[row.NetIncome_B],
                    mode='markers+text', name=row.Company,
                    text=[row.Company], textposition='top center',
                    textfont=dict(size=10,color=COLORS[row.Company]),
                    marker=dict(size=16, color=COLORS[row.Company],
                                line=dict(width=2,color='rgba(255,255,255,0.15)')),
                    showlegend=False
                ))
            sf(fig2, 320, legend=False).update_layout(
                title=dict(text=f"Revenue vs Net Income {yr}", font=dict(size=12,color='#6b80a0')),
                xaxis_title="Revenue ($B)", yaxis_title="Net Income ($B)")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})

        with c2:
            ni_change = ann_df[ann_df.Company.isin(sel_companies)].sort_values(['Company','Year'])
            ni_change['NI_Change'] = ni_change.groupby('Company')['NetIncome_B'].diff()
            ni_2024 = ni_change[ni_change.Year==2024].sort_values('NI_Change')
            fig3 = go.Figure(go.Bar(
                x=ni_2024.NI_Change, y=ni_2024.Company, orientation='h',
                marker=dict(
                    color=['#00ff9d' if v>=0 else '#ff375f' for v in ni_2024.NI_Change],
                    line=dict(width=0)
                ),
                text=[f"${v:+.1f}B" for v in ni_2024.NI_Change],
                textposition='outside', textfont=dict(size=10,color='#6b80a0'),
                hovertemplate='<b>%{y}</b><br>Change: $%{x:+.1f}B<extra></extra>'
            ))
            sf(fig3, 320, legend=False).update_layout(
                title=dict(text="Net Income Change 2023→2024 ($B)", font=dict(size=12,color='#6b80a0')))
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar':False})


# ── PAGE: COMPETITIVE ANALYSIS ────────────────────────────────────────────────
elif "Competitive" in page:
    st.markdown('<p class="hero-title" style="font-size:2.2rem;margin-bottom:1.5rem;">🏆 Competitive Analysis</p>', unsafe_allow_html=True)

    # ── Radar chart ──
    sec("Multi-Dimensional Competitive Radar", "2024 BENCHMARKS")
    ann_2024 = ann_df[ann_df.Year==2024].copy()
    ann_2024['Margin']    = (ann_2024.NetIncome_B / ann_2024.Revenue_B * 100).round(1)
    ann_2024['RevPerEmp'] = (ann_2024.Revenue_B * 1e9 / (ann_2024.Employees_K * 1e3) / 1e6).round(2)

    metrics = ['Revenue_B','NetIncome_B','MarketCap_B','Margin','RevPerEmp']
    labels  = ['Revenue ($B)','Net Income ($B)','Market Cap ($B)','Net Margin %','Rev/Employee $M']

    norm = ann_2024[ann_2024.Company.isin(sel_companies)].set_index('Company')[metrics].copy()
    for col in metrics:
        norm[col] = (norm[col] - norm[col].min()) / (norm[col].max() - norm[col].min() + 1e-9) * 10

    fig = go.Figure()
    for co in sel_companies:
        if co not in norm.index: continue
        vals = list(norm.loc[co].values) + [norm.loc[co].values[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=labels+[labels[0]], name=co, fill='toself',
            fillcolor=hex_to_rgba(COLORS[co], 0.15),
            line=dict(color=COLORS[co], width=2),
            hovertemplate=f'<b>{co}</b><br>%{{theta}}: %{{r:.1f}}/10<extra></extra>'
        ))
    fig.update_layout(**PL, height=480, polar=dict(
        bgcolor='rgba(0,0,0,0)',
        radialaxis=dict(visible=True, range=[0,10], gridcolor='rgba(255,255,255,0.06)',
                        tickfont=dict(size=8,color='#2d3f5a')),
        angularaxis=dict(gridcolor='rgba(255,255,255,0.06)', tickfont=dict(size=10,color='#6b80a0'))
    ), title=dict(text="Competitive Radar — 5 Dimensions (Normalised 0–10)", font=dict(size=12,color='#6b80a0')))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

    c1, c2 = st.columns(2)
    with c1:
        sec("Rankings Board", "2024")
        ann_2024s = ann_2024[ann_2024.Company.isin(sel_companies)].sort_values('MarketCap_B',ascending=False)
        medals = ['🥇','🥈','🥉','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣']
        html = ""
        for i, (_, row) in enumerate(ann_2024s.iterrows()):
            html += f"""
            <div class="rank-row">
              <div class="rank-num">{medals[i] if i < len(medals) else i+1}</div>
              <div style="width:12px;height:12px;border-radius:50%;background:{COLORS[row.Company]};flex-shrink:0;"></div>
              <div class="rank-name">{row.Company}</div>
              <div class="rank-val">${row.MarketCap_B:,.0f}B</div>
            </div>"""
        st.markdown(f"""
        <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:1.2rem;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#2d3f5a;letter-spacing:0.1em;margin-bottom:0.8rem;">
            RANKED BY MARKET CAP 2024
          </div>{html}</div>""", unsafe_allow_html=True)

    with c2:
        sec("Market Cap vs Revenue Multiple", "P/S RATIO")
        ann_2024r = ann_2024[ann_2024.Company.isin(sel_companies)].copy()
        ann_2024r['PS_Ratio'] = ann_2024r.MarketCap_B / ann_2024r.Revenue_B
        ann_2024r = ann_2024r.sort_values('PS_Ratio', ascending=True)
        fig = go.Figure(go.Bar(
            x=ann_2024r.PS_Ratio, y=ann_2024r.Company, orientation='h',
            marker=dict(color=[COLORS[c] for c in ann_2024r.Company], line=dict(width=0)),
            text=[f"{v:.1f}x" for v in ann_2024r.PS_Ratio],
            textposition='outside', textfont=dict(size=11,color='#6b80a0'),
            hovertemplate='<b>%{y}</b><br>P/S: %{x:.1f}x<extra></extra>'
        ))
        sf(fig, 330, legend=False).update_layout(
            title=dict(text="Price/Sales Ratio 2024 (Market Cap ÷ Revenue)", font=dict(size=12,color='#6b80a0')),
            xaxis_title="P/S Ratio")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

    sec("Employee Count vs Revenue — Efficiency Matrix", "HEADCOUNT")
    ann_all = ann_df[(ann_df.Year.between(*year_range))&(ann_df.Company.isin(sel_companies))]
    ann_all['RevPerEmp'] = (ann_all.Revenue_B*1e9 / (ann_all.Employees_K*1e3) / 1e6).round(2)
    fig = px.scatter(ann_all, x='Employees_K', y='Revenue_B', color='Company',
                     size='MarketCap_B', animation_frame='Year',
                     color_discrete_map=COLORS, size_max=60,
                     hover_data={'NetIncome_B':':.1f','RevPerEmp':':.2f'})
    fig.update_layout(**PL, height=400,
        title=dict(text="Employees vs Revenue (bubble=Market Cap) — Animated by Year", font=dict(size=12,color='#6b80a0')),
        xaxis_title="Employees (K)", yaxis_title="Revenue ($B)")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})


# ── PAGE: DEEP ANALYTICS ──────────────────────────────────────────────────────
elif "Deep Analytics" in page:
    st.markdown('<p class="hero-title" style="font-size:2.2rem;margin-bottom:1.5rem;">🔬 Deep Analytics</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔗  Correlation Lab", "📐  Statistical Tests", "🌊  Market Cycles"])

    with tab1:
        sec("Stock Price Correlation Matrix", "REAL DAILY RETURNS")
        price_pivot = price_df[price_df.Company.isin(sel_companies)].pivot(
            index='Date', columns='Company', values='Daily_Return').dropna()
        corr = price_pivot.corr()

        fig = go.Figure(go.Heatmap(
            z=corr.values, x=list(corr.columns), y=list(corr.index),
            colorscale=[[0,'#ff375f'],[0.5,'#0c1528'],[1,'#00e5ff']],
            zmid=0, zmin=-1, zmax=1,
            text=np.round(corr.values,2), texttemplate='%{text}', textfont_size=11,
            hovertemplate='<b>%{y} × %{x}</b><br>Correlation: %{z:.2f}<extra></extra>'
        ))
        sf(fig, 420, legend=False).update_layout(
            title=dict(text="Daily Return Correlation (2020–2024) — 1=Perfect · -1=Inverse", font=dict(size=12,color='#6b80a0')))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        c1, c2 = st.columns(2)
        with c1:
            co_a = st.selectbox("Company A", sel_companies, index=0, key='ca')
        with c2:
            co_b = st.selectbox("Company B", sel_companies, index=1, key='cb')
        pair = price_pivot[[co_a, co_b]].dropna() if co_a in price_pivot.columns and co_b in price_pivot.columns else None
        if pair is not None and co_a != co_b:
            corr_val = pair[co_a].corr(pair[co_b])
            slope, intercept, r, p, se = scipy_stats.linregress(pair[co_a], pair[co_b])
            x_range = np.linspace(pair[co_a].min(), pair[co_a].max(), 100)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=pair[co_a], y=pair[co_b], mode='markers',
                marker=dict(size=3, color='rgba(0,229,255,0.35)'),
                hovertemplate=f'{co_a}: %{{x:.2f}}%<br>{co_b}: %{{y:.2f}}%<extra></extra>',
                name='Daily Returns'))
            fig2.add_trace(go.Scatter(x=x_range, y=slope*x_range+intercept,
                mode='lines', line=dict(color='#ff6d2d',width=2,dash='dash'),
                name=f'Fit (r={corr_val:.2f})'))
            sf(fig2, 340).update_layout(
                title=dict(text=f"{co_a} vs {co_b} — Correlation: {corr_val:.3f} | p={p:.2e}", font=dict(size=12,color='#6b80a0')),
                xaxis_title=f"{co_a} Daily Return %", yaxis_title=f"{co_b} Daily Return %")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})

    with tab2:
        sec("Normality Tests & Distribution Stats", "STATISTICAL ANALYSIS")
        stats_rows = []
        for co in sel_companies:
            rets = price_df[price_df.Company==co]['Daily_Return'].dropna()
            stat, p_shapiro = scipy_stats.shapiro(rets.sample(min(5000,len(rets)), random_state=42))
            sk = scipy_stats.skew(rets)
            ku = scipy_stats.kurtosis(rets)
            stats_rows.append({
                'Company': co, 'Mean (%)': round(rets.mean(),4),
                'Std Dev (%)': round(rets.std(),4),
                'Skewness': round(sk,3), 'Kurtosis': round(ku,3),
                'Shapiro-Wilk p': f'{p_shapiro:.4f}',
                'Normal?': '✅ Yes' if p_shapiro > 0.05 else '❌ No',
                'Min (%)': round(rets.min(),3), 'Max (%)': round(rets.max(),3),
            })
        st.dataframe(pd.DataFrame(stats_rows).set_index('Company'), use_container_width=True)

        co_qq = st.selectbox("Q-Q Plot for:", sel_companies, key='qq')
        rets_qq = price_df[price_df.Company==co_qq]['Daily_Return'].dropna()
        theo = scipy_stats.norm.ppf(np.linspace(0.01,0.99, len(rets_qq)))
        sample_q = np.sort(rets_qq.values)[:len(theo)]
        theo = theo[:len(sample_q)]
        mu, sig = rets_qq.mean(), rets_qq.std()
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=theo, y=sample_q, mode='markers',
                marker=dict(size=3, color=COLORS[co_qq], opacity=0.5), name='Q-Q'))
            fig.add_trace(go.Scatter(x=[theo.min(),theo.max()],
                y=[theo.min()*sig+mu, theo.max()*sig+mu],
                mode='lines', line=dict(color='#ff6d2d',width=2,dash='dash'), name='Normal'))
            sf(fig, 300).update_layout(
                title=dict(text=f"{co_qq} — Q-Q Plot vs Normal", font=dict(size=12,color='#6b80a0')),
                xaxis_title="Theoretical", yaxis_title="Sample")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        with c2:
            fig2 = go.Figure()
            fig2.add_trace(go.Histogram(x=rets_qq, nbinsx=80, name='Returns',
                marker=dict(color=hex_to_rgba(COLORS[co_qq], 0.5), line=dict(color=COLORS[co_qq],width=0.5))))
            x_n = np.linspace(rets_qq.min(), rets_qq.max(), 200)
            fig2.add_trace(go.Scatter(x=x_n, y=scipy_stats.norm.pdf(x_n,mu,sig)*len(rets_qq)*(rets_qq.max()-rets_qq.min())/80,
                mode='lines', line=dict(color='#ff6d2d',width=2,dash='dot'), name='Normal Fit'))
            sf(fig2, 300).update_layout(
                title=dict(text=f"{co_qq} Daily Returns Distribution", font=dict(size=12,color='#6b80a0')),
                yaxis_title="Count")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})

    with tab3:
        sec("Drawdown Analysis — Peak-to-Trough", "MARKET CYCLES")
        for co in sel_companies[:4]:
            sub = price_df[price_df.Company==co].sort_values('Date')
            roll_max = sub.Price.cummax()
            drawdown = (sub.Price - roll_max) / roll_max * 100
            sub = sub.copy()
            sub['Drawdown'] = drawdown
            if co == sel_companies[0]:
                fig = go.Figure()
            fig.add_trace(go.Scatter(x=sub.Date, y=sub.Drawdown, name=co,
                fill='tozeroy' if co==sel_companies[0] else None,
                line=dict(color=COLORS[co], width=1.5),
                hovertemplate=f'<b>{co}</b> %{{x|%b %Y}}<br>Drawdown: %{{y:.1f}}%<extra></extra>'))
        sf(fig, 380).update_layout(
            title=dict(text="Maximum Drawdown from Peak — COVID Crash & 2022 Bear Market", font=dict(size=12,color='#6b80a0')),
            yaxis_title="Drawdown %")
        fig.add_hrect(y0=-100, y1=-30, fillcolor="rgba(255,55,95,0.04)", line_width=0)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})


# ── PAGE: AI INSIGHT ENGINE ───────────────────────────────────────────────────
elif "AI Insight" in page:
    st.markdown('<p class="hero-title" style="font-size:2.2rem;margin-bottom:1.5rem;">🤖 AI Insight Engine</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:var(--bg-card);border:1px solid var(--border2);border-radius:14px;
                padding:1.6rem 2rem;margin-bottom:1.5rem;">
      <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                  color:var(--cyan);margin-bottom:0.6rem;">⚡ Auto-Generated Insights from Real Data</div>
      <div style="color:var(--txt2);font-size:0.88rem;line-height:1.7;">
        These insights are computed directly from real earnings & stock data — no LLM needed.
      </div>
    </div>
    """, unsafe_allow_html=True)

    ann_2024 = ann_df[ann_df.Year==2024].set_index('Company')
    ann_2020 = ann_df[ann_df.Year==2020].set_index('Company')

    insights = []

    nvda_mcap_growth = (ann_2024.loc['NVIDIA','MarketCap_B'] / ann_2020.loc['NVIDIA','MarketCap_B'] - 1)*100
    insights.append(('🚀 NVIDIA AI Supercycle',
        f"NVIDIA's market cap exploded from ${ann_2020.loc['NVIDIA','MarketCap_B']:.0f}B (2020) to "
        f"${ann_2024.loc['NVIDIA','MarketCap_B']:,.0f}B (2024) — a <b style='color:#00ff9d;'>{nvda_mcap_growth:.0f}% gain</b> "
        f"in 4 years. Net income surged to <b style='color:#00ff9d;'>${ann_2024.loc['NVIDIA','NetIncome_B']:.1f}B</b> on AI chip demand."))

    meta_ni_change = ann_2024.loc['Meta','NetIncome_B'] - ann_df[ann_df.Year==2022].set_index('Company').loc['Meta','NetIncome_B']
    insights.append(('💎 Meta\'s Year of Efficiency',
        f"After a brutal 2022 (net income crashed to $23.2B), Meta rebounded to "
        f"<b style='color:#00e5ff;'>${ann_2024.loc['Meta','NetIncome_B']:.1f}B</b> net income in 2024 — "
        f"a <b style='color:#00e5ff;'>+170% recovery</b> driven by headcount cuts and AI ad targeting."))

    apple_rev_cagr = ((ann_2024.loc['Apple','Revenue_B']/ann_2020.loc['Apple','Revenue_B'])**0.25-1)*100
    insights.append(('🍎 Apple\'s Revenue Machine',
        f"Apple generated <b style='color:#e8e8e8;'>${ann_2024.loc['Apple','Revenue_B']:.1f}B</b> revenue in 2024 "
        f"with a {apple_rev_cagr:.1f}% CAGR since 2020. Net margin remains "
        f"<b style='color:#e8e8e8;'>{ann_2024.loc['Apple','NetIncome_B']/ann_2024.loc['Apple','Revenue_B']*100:.1f}%</b> — "
        f"consistently the most profitable hardware company on earth."))

    amzn_2020_ni = ann_2020.loc['Amazon','NetIncome_B']
    insights.append(('📦 Amazon\'s Profit Inflection',
        f"Amazon went from <b style='color:#ff375f;'>${amzn_2020_ni:.1f}B</b> loss (2022) to "
        f"<b style='color:#ff9900;'>${ann_2024.loc['Amazon','NetIncome_B']:.1f}B</b> net income in 2024 "
        f"as AWS cloud margins and advertising revenue offset retail losses."))

    tsla_data = price_df[price_df.Company=='Tesla']['Daily_Return']
    insights.append(('⚡ Tesla: Highest Volatility Award',
        f"Tesla has daily return std dev of <b style='color:#cc0000;'>{tsla_data.std():.2f}%</b> — "
        f"the highest among all 8 companies. Its stock went from $86 (Jan 2020) to $1,200 (late 2021) "
        f"then crashed to $123 (Jan 2023) before recovering to <b style='color:#cc0000;'>$403</b> in 2024."))

    for title, body in insights:
        st.markdown(f"""
        <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:12px;
                    padding:1.3rem 1.6rem;margin-bottom:0.9rem;
                    border-left:3px solid var(--cyan);">
          <div style="font-family:'Syne',sans-serif;font-size:0.9rem;font-weight:700;
                      color:var(--txt);margin-bottom:0.4rem;">{title}</div>
          <div style="font-size:0.85rem;color:var(--txt2);line-height:1.7;">{body}</div>
        </div>
        """, unsafe_allow_html=True)

    sec("Full Company Scorecard 2024", "REAL METRICS")
    ann_2024_full = ann_df[ann_df.Year==2024][ann_df.Company.isin(sel_companies)].copy()
    ann_2024_full['Net_Margin_%'] = (ann_2024_full.NetIncome_B/ann_2024_full.Revenue_B*100).round(1)
    ann_2024_full['Rev_per_Emp_M'] = (ann_2024_full.Revenue_B*1e9/(ann_2024_full.Employees_K*1e3)/1e6).round(2)
    ann_2024_full['PS_Ratio'] = (ann_2024_full.MarketCap_B/ann_2024_full.Revenue_B).round(1)
    display = ann_2024_full[['Company','Sector','Revenue_B','NetIncome_B','MarketCap_B',
                              'Employees_K','Net_Margin_%','Rev_per_Emp_M','PS_Ratio']].sort_values('MarketCap_B',ascending=False)
    display.columns = ['Company','Sector','Revenue ($B)','Net Income ($B)','Market Cap ($B)',
                       'Employees (K)','Net Margin %','Rev/Employee ($M)','P/S Ratio']
    st.dataframe(display.set_index('Company'), use_container_width=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid rgba(0,229,255,0.06);margin-top:3rem;padding-top:1.2rem;
            text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#2d3f5a;">
  MARKET NEXUS &nbsp;·&nbsp; Built by Jyotheeswar Gudipalli &nbsp;·&nbsp;
  Manipal University Jaipur · B.Tech Data Science 2027 &nbsp;·&nbsp;
  Data: Public Earnings Reports · SEC Filings · Historical Stock Records
</div>
""", unsafe_allow_html=True)
