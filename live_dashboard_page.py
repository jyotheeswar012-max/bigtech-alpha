"""
live_dashboard_page.py
——————————————————————
Drop-in replacement for the PAGE_LD block inside nexus.py.
Call render_live_dashboard(sel_companies) from nexus.py.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

try:
    from live_data import (
        get_multi_live_prices, get_intraday_data,
        get_all_fundamentals, is_market_open,
        NAME_TO_TICKER, COMPANY_COLORS,
    )
    _live_ok = True
except ImportError:
    _live_ok = False

try:
    from streamlit_autorefresh import st_autorefresh
    _autorefresh_ok = True
except ImportError:
    _autorefresh_ok = False

PL = dict(
    paper_bgcolor="#1a1d27", plot_bgcolor="#13161f",
    font=dict(family="Inter", color="#94a3b8", size=11),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)", color="#64748b"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)", color="#64748b"),
    margin=dict(l=10, r=10, t=44, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=1,
                font=dict(size=10, color="#94a3b8"), orientation='h', y=1.12),
)


def _safe(val, fmt):
    try:
        return fmt(float(val)) if val is not None and not pd.isna(val) else "—"
    except Exception:
        return "—"


def render_live_dashboard(sel_companies):
    st.markdown('<p class="page-title">📡 Live Dashboard</p>', unsafe_allow_html=True)

    if not _live_ok:
        st.error("❌ `live_data.py` not found. Please ensure it is present in the project folder.")
        return

    # ── Auto-refresh every 30 s when market is open ────────────────────────────
    if _autorefresh_ok:
        st_autorefresh(interval=30_000, key="live_refresh")

    # ── Market status ──────────────────────────────────────────────────────────
    try:
        market_open = is_market_open()
    except Exception:
        market_open = False

    now_str = datetime.now().strftime("%H:%M:%S")
    if market_open:
        dot_html    = '<span class="live"></span>'
        badge_label = "🟢 MARKET OPEN"
        badge_note  = f"Real-time prices · auto-refresh 30 s · {now_str} ET"
        badge_cls   = "up"
    else:
        dot_html    = '<span class="dead"></span>'
        badge_label = "⚫ MARKET CLOSED"
        badge_note  = f"Showing last available prices · {now_str}"
        badge_cls   = "closed-badge"

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:1.5rem;">'
        f'<span class="kpi-badge {badge_cls}" style="position:static;font-size:0.65rem;'
        f'padding:0.3rem 0.9rem;">'
        f'{dot_html}{badge_label}</span>'
        f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:0.7rem;'
        f'color:#64748b;">{badge_note}</span></div>',
        unsafe_allow_html=True
    )

    # ── Fetch live prices ──────────────────────────────────────────────────────
    with st.spinner("Fetching live prices…"):
        try:
            all_prices = get_multi_live_prices()
        except Exception as e:
            st.error(f"Could not fetch prices: {e}")
            all_prices = {}

    prices = {co: d for co, d in all_prices.items() if co in sel_companies}

    if not prices:
        st.warning("No live price data available.")
        return

    # ── Fundamentals ───────────────────────────────────────────────────────────
    @st.cache_data(ttl=300, show_spinner=False)
    def _fund():
        return get_all_fundamentals()

    fund_df = _fund()

    # ── Build enriched list ────────────────────────────────────────────────────
    rows = []
    for co, d in sorted(prices.items(), key=lambda x: x[1].get("price", 0), reverse=True):
        ticker = NAME_TO_TICKER.get(co, "") if isinstance(NAME_TO_TICKER, dict) else ""
        color  = COMPANY_COLORS.get(ticker, "#818cf8") if isinstance(COMPANY_COLORS, dict) else "#818cf8"
        price  = d.get("price", 0) or 0
        chg    = d.get("change_pct", 0) or 0
        vol    = d.get("volume", 0) or 0

        vol_str = (
            f"{vol/1_000_000:.1f}M" if vol >= 1_000_000
            else f"{vol/1_000:.0f}K" if vol >= 1_000
            else str(int(vol)) if vol else "—"
        )

        # Fundamentals lookup
        fr = None
        if not fund_df.empty:
            frow = fund_df[fund_df["Company"] == co]
            if not frow.empty:
                fr = frow.iloc[0]

        w52h   = _safe(fr["52w_high"]    if fr is not None and "52w_high"    in fr.index else None, lambda v: f"${v:,.2f}")
        w52l   = _safe(fr["52w_low"]     if fr is not None and "52w_low"     in fr.index else None, lambda v: f"${v:,.2f}")
        mktcap = _safe(fr["marketCap_B"] if fr is not None and "marketCap_B" in fr.index else None, lambda v: f"${v:,.0f}B")
        pe     = _safe(fr["peRatio"]     if fr is not None and "peRatio"     in fr.index else None, lambda v: f"{v:.1f}x")
        beta   = _safe(fr["beta"]        if fr is not None and "beta"        in fr.index else None, lambda v: f"{v:.2f}")
        eps    = _safe(fr["eps"]         if fr is not None and "eps"         in fr.index else None, lambda v: f"${v:.2f}")
        ni     = _safe(fr["netIncome_B"] if fr is not None and "netIncome_B" in fr.index else None, lambda v: f"${v:.2f}B")
        margin = _safe(fr["net_margin"]  if fr is not None and "net_margin"  in fr.index else None, lambda v: f"{v:.1f}%")

        rows.append(dict(
            co=co, ticker=ticker, color=color,
            price=price, chg=chg, vol_str=vol_str,
            w52h=w52h, w52l=w52l, mktcap=mktcap,
            pe=pe, beta=beta, eps=eps, ni=ni, margin=margin,
        ))

    # ══════════════════════════════════════════════════════════
    # SECTION A — LIVE PRICE CARDS
    # ══════════════════════════════════════════════════════════
    st.markdown(
        '<div class="sec">'
        '<div class="sec-title">LIVE PRICES</div>'
        '<div class="sec-line"></div>'
        f'<div class="sec-tag{\" closed\" if not market_open else \"\"}">'
        f'{"LAST CLOSE" if not market_open else "REAL-TIME"}'
        '</div></div>',
        unsafe_allow_html=True
    )

    CARD_COLORS = [
        "linear-gradient(135deg,#6366f1,#818cf8)",
        "linear-gradient(135deg,#0284c7,#38bdf8)",
        "linear-gradient(135deg,#dc2626,#f87171)",
        "linear-gradient(135deg,#d97706,#fbbf24)",
        "linear-gradient(135deg,#ea580c,#fb923c)",
        "linear-gradient(135deg,#16a34a,#86efac)",
        "linear-gradient(135deg,#9f1239,#fb7185)",
        "linear-gradient(135deg,#7e22ce,#f472b6)",
    ]

    # 4 per row
    for row_start in range(0, len(rows), 4):
        chunk = rows[row_start:row_start + 4]
        cols  = st.columns(len(chunk))
        for col, r in zip(cols, chunk):
            ci    = rows.index(r)
            grad  = CARD_COLORS[ci % len(CARD_COLORS)]
            arrow = "▲" if r["chg"] >= 0 else "▼"
            clr   = "#34d399" if r["chg"] >= 0 else "#f87171"
            badge = ("🟢 LIVE" if market_open else "⚫ LAST CLOSE")
            with col:
                st.markdown(f"""
<div class="price-card">
  <div class="price-card-bar" style="background:{grad};"></div>
  <div class="price-card-badge {'up' if r['chg']>=0 else 'down'}">{badge}</div>
  <div class="price-card-ticker">{r['ticker']}</div>
  <div class="price-card-co">{r['co']}</div>
  <div class="price-card-price" style="color:{r['color']};">
    ${r['price']:,.2f}
  </div>
  <div class="price-card-chg" style="color:{clr};">
    {arrow} {r['chg']:+.2f}%
  </div>
  <div class="price-card-vol">Vol {r['vol_str']} &nbsp;·&nbsp; MCap {r['mktcap']}</div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # SECTION B — LIVE COMPARISON TABLE
    # ══════════════════════════════════════════════════════════
    st.markdown(
        '<div class="sec" style="margin-top:2rem;">'
        '<div class="sec-title">LIVE COMPARISON TABLE</div>'
        '<div class="sec-line"></div>'
        f'<div class="sec-tag{\" closed\" if not market_open else \"\"}">'
        f'{"LAST PRICES" if not market_open else "REAL-TIME"}</div></div>',
        unsafe_allow_html=True
    )

    # Build HTML table
    thead = """
<thead><tr>
  <th>Company</th>
  <th>Ticker</th>
  <th>Price</th>
  <th>Change %</th>
  <th>Market Cap</th>
  <th>PE Ratio</th>
  <th>EPS</th>
  <th>Beta</th>
  <th>Net Income</th>
  <th>Net Margin</th>
  <th>52W High</th>
  <th>52W Low</th>
  <th>Volume</th>
</tr></thead>
"""

    tbody = "<tbody>"
    for r in rows:
        arrow = "▲" if r["chg"] >= 0 else "▼"
        chg_cls = "badge-up" if r["chg"] >= 0 else "badge-dn"
        tbody += f"""
<tr>
  <td><span class="cmp-dot" style="background:{r['color']};"></span>
      <span class="cmp-co">{r['co']}</span></td>
  <td><span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;
                   color:#818cf8;font-weight:700;">{r['ticker']}</span></td>
  <td><strong style="color:{r['color']};">${r['price']:,.2f}</strong></td>
  <td class="{chg_cls}">{arrow} {r['chg']:+.2f}%</td>
  <td>{r['mktcap']}</td>
  <td>{r['pe']}</td>
  <td>{r['eps']}</td>
  <td>{r['beta']}</td>
  <td>{r['ni']}</td>
  <td>{r['margin']}</td>
  <td>{r['w52h']}</td>
  <td>{r['w52l']}</td>
  <td style="color:#64748b;">{r['vol_str']}</td>
</tr>"""
    tbody += "</tbody>"

    st.markdown(
        f'<div class="cmp-wrap"><table class="cmp-table">{thead}{tbody}</table></div>',
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════════════════════════
    # SECTION C — INTRADAY CHARTS
    # ══════════════════════════════════════════════════════════
    st.markdown(
        '<div class="sec" style="margin-top:2rem;">'
        '<div class="sec-title">INTRADAY CHARTS</div>'
        '<div class="sec-line"></div>'
        f'<div class="sec-tag{\" closed\" if not market_open else \"\"}">'
        f'{"5-DAY" if not market_open else "TODAY"}</div></div>',
        unsafe_allow_html=True
    )

    period   = "1d" if market_open else "5d"
    interval = "5m" if market_open else "1h"

    active = [r for r in rows]  # all selected
    for row_start in range(0, len(active), 2):
        chunk = active[row_start:row_start + 2]
        cols  = st.columns(len(chunk))
        for col, r in zip(cols, chunk):
            with col:
                with st.spinner(f"Loading {r['co']} intraday…"):
                    try:
                        idf = get_intraday_data(r["ticker"], period=period, interval=interval)
                    except Exception:
                        idf = pd.DataFrame()

                if idf.empty:
                    st.info(f"No intraday data for {r['co']}")
                    continue

                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    row_heights=[0.75, 0.25],
                    vertical_spacing=0.03,
                )

                # Price line
                fig.add_trace(
                    go.Scatter(
                        x=idf.index, y=idf["Close"],
                        name="Price",
                        line=dict(color=r["color"], width=2),
                        fill="tozeroy",
                        fillcolor=f"rgba({','.join(str(int(r['color'].lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.08)",
                        hovertemplate="%{x}<br>$%{y:,.2f}<extra></extra>",
                    ),
                    row=1, col=1
                )

                # Volume bars
                if "Volume" in idf.columns:
                    fig.add_trace(
                        go.Bar(
                            x=idf.index, y=idf["Volume"] / 1e6,
                            name="Vol (M)",
                            marker_color=r["color"],
                            opacity=0.35,
                            hovertemplate="%{x}<br>%{y:.2f}M<extra></extra>",
                        ),
                        row=2, col=1
                    )

                fig.update_layout(
                    **PL,
                    height=300,
                    title=dict(
                        text=f"{r['co']}  ·  ${r['price']:,.2f}  "
                             f"<span style='color:{'#34d399' if r['chg']>=0 else '#f87171'};'>" 
                             f"{'▲' if r['chg']>=0 else '▼'} {r['chg']:+.2f}%</span>",
                        font=dict(size=12, color="#e2e8f0")
                    ),
                    showlegend=False,
                    xaxis2=dict(
                        gridcolor="rgba(255,255,255,0.04)",
                        color="#64748b",
                        zerolinecolor="rgba(255,255,255,0.06)"
                    ),
                    yaxis2=dict(
                        gridcolor="rgba(255,255,255,0.04)",
                        color="#64748b",
                        zerolinecolor="rgba(255,255,255,0.06)"
                    ),
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Footer note ────────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;'
        f'color:#334155;margin-top:1.5rem;text-align:center;">'
        f'⚡ Data via yfinance · refreshed {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} · '
        f'{"Market open — live prices" if market_open else "Market closed — last available prices"}'
        f'</div>',
        unsafe_allow_html=True
    )
