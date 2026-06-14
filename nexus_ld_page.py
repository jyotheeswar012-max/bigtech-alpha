# nexus_ld_page.py  —  place next to nexus.py
#
# In nexus.py replace the entire  elif page_idx == PAGE_LD:  block with:
#
#   elif page_idx == PAGE_LD:
#       from nexus_ld_page import render_ld
#       render_ld(sel_companies, _live_ok, _autorefresh_ok)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# ── Plotly dark theme ────────────────────────────────────────────────────────
_PL = dict(
    paper_bgcolor="#1a1d27", plot_bgcolor="#13161f",
    font=dict(family="Inter", color="#94a3b8", size=11),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)",
               zerolinecolor="rgba(255,255,255,0.08)", color="#64748b"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)",
               zerolinecolor="rgba(255,255,255,0.08)", color="#64748b"),
    margin=dict(l=10, r=10, t=44, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=1,
                font=dict(size=10, color="#94a3b8"), orientation="h", y=1.12),
)

_CARD_GRADS = [
    "linear-gradient(135deg,#6366f1,#818cf8)",
    "linear-gradient(135deg,#0284c7,#38bdf8)",
    "linear-gradient(135deg,#dc2626,#f87171)",
    "linear-gradient(135deg,#d97706,#fbbf24)",
    "linear-gradient(135deg,#ea580c,#fb923c)",
    "linear-gradient(135deg,#16a34a,#86efac)",
    "linear-gradient(135deg,#9f1239,#fb7185)",
    "linear-gradient(135deg,#7e22ce,#f472b6)",
]


# ── Module-level safe formatter (avoids closure / late-binding bugs) ──────────
def _fmt_val(fr, col, fmt_str):
    """Pull `col` from pandas Series `fr` and format with `fmt_str`.
    Returns em-dash string on any error or NaN.
    """
    try:
        if fr is None or col not in fr.index:
            return "\u2014"
        v = float(fr[col])
        if pd.isna(v):
            return "\u2014"
        return fmt_str.format(v)
    except Exception:
        return "\u2014"


@st.cache_data(ttl=300, show_spinner=False)
def _get_fund():
    from live_data import get_all_fundamentals
    return get_all_fundamentals()


# ── Hex → RGB string helper ───────────────────────────────────────────────────
def _hex_rgb(hex_color):
    hx = hex_color.lstrip("#")
    try:
        return f"{int(hx[0:2],16)},{int(hx[2:4],16)},{int(hx[4:6],16)}"
    except Exception:
        return "129,140,248"


# ── Main renderer ─────────────────────────────────────────────────────────────
def render_ld(sel_companies, _live_ok, _autorefresh_ok):
    """Render the full Live Dashboard page."""

    st.markdown('<p class="page-title">\U0001f4e1 Live Dashboard</p>',
                unsafe_allow_html=True)

    if not _live_ok:
        st.error("Live data module (`live_data.py`) not found. "
                 "Make sure live_data.py is present in the same folder.")
        return

    # ── imports from live_data ────────────────────────────────────────────────
    from live_data import (
        get_multi_live_prices, get_intraday_data,
        is_market_open, NAME_TO_TICKER, COMPANY_COLORS,
    )

    # ── auto-refresh ──────────────────────────────────────────────────────────
    if _autorefresh_ok:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=30_000, key="live_refresh")

    # ── market status ─────────────────────────────────────────────────────────
    try:
        market_open = is_market_open()
    except Exception:
        market_open = False

    now_str = datetime.now().strftime("%H:%M:%S")
    if market_open:
        dot     = '<span class="live"></span>'
        s_label = "REAL-TIME"
        s_cls   = "up"
        s_note  = f"\U0001f7e2 Market Open \u00b7 auto-refresh 30 s \u00b7 {now_str} ET"
    else:
        dot     = '<span class="dead"></span>'
        s_label = "LAST CLOSE"
        s_cls   = "closed-badge"
        s_note  = (f"\u26ab Market Closed \u00b7 "
                   f"showing last available prices \u00b7 {now_str}")

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:.8rem;margin-bottom:1.5rem;">'
        f'<span class="kpi-badge {s_cls}" '
        f'style="position:static;font-size:.65rem;padding:.3rem .9rem;">'
        f'{dot}{s_label}</span>'
        f'<span style="font-family:\'JetBrains Mono\',monospace;'
        f'font-size:.7rem;color:#64748b;">{s_note}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── fetch live prices ─────────────────────────────────────────────────────
    with st.spinner("Fetching live prices\u2026"):
        try:
            all_prices = get_multi_live_prices()
        except Exception as exc:
            st.error(f"Could not fetch prices: {exc}")
            all_prices = {}

    prices = {co: d for co, d in all_prices.items() if co in sel_companies}
    if not prices:
        st.warning("No live price data available for the selected companies.")
        return

    # ── fundamentals ─────────────────────────────────────────────────────────
    try:
        fund_df = _get_fund()
    except Exception:
        fund_df = pd.DataFrame()

    # ── build enriched rows (NO inner def / lambda closure) ───────────────────
    rows = []
    for co, d in sorted(
        prices.items(), key=lambda x: x[1].get("price", 0), reverse=True
    ):
        ticker = (NAME_TO_TICKER.get(co, "")
                  if isinstance(NAME_TO_TICKER, dict) else "")
        color  = (COMPANY_COLORS.get(ticker, "#818cf8")
                  if isinstance(COMPANY_COLORS, dict) else "#818cf8")
        price  = d.get("price", 0) or 0
        chg    = d.get("change_pct", 0) or 0
        vol    = d.get("volume", 0) or 0

        vol_str = (
            f"{vol/1e6:.1f}M" if vol >= 1_000_000
            else f"{vol/1e3:.0f}K" if vol >= 1_000
            else str(int(vol)) if vol else "\u2014"
        )

        # Grab the fundamentals row once — avoids repeated DataFrame lookups
        fr = None
        if not fund_df.empty:
            frow = fund_df[fund_df["Company"] == co]
            if not frow.empty:
                fr = frow.iloc[0]

        # Use module-level _fmt_val to avoid closure bugs
        rows.append(dict(
            co=co, ticker=ticker, color=color,
            price=price, chg=chg, vol_str=vol_str,
            mktcap = _fmt_val(fr, "marketCap_B", "${:.0f}B"),
            pe     = _fmt_val(fr, "peRatio",     "{:.1f}x"),
            eps    = _fmt_val(fr, "eps",         "${:.2f}"),
            beta   = _fmt_val(fr, "beta",        "{:.2f}"),
            ni     = _fmt_val(fr, "netIncome_B", "${:.2f}B"),
            margin = _fmt_val(fr, "net_margin",  "{:.1f}%"),
            w52h   = _fmt_val(fr, "52w_high",    "${:,.2f}"),
            w52l   = _fmt_val(fr, "52w_low",     "${:,.2f}"),
        ))

    closed_tag = " closed" if not market_open else ""
    rt_tag     = "LAST CLOSE" if not market_open else "REAL-TIME"

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION A — LIVE PRICE CARDS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown(
        f'<div class="sec"><div class="sec-title">LIVE PRICES</div>'
        f'<div class="sec-line"></div>'
        f'<div class="sec-tag{closed_tag}">{rt_tag}</div></div>',
        unsafe_allow_html=True,
    )

    for row_start in range(0, len(rows), 4):
        chunk = rows[row_start:row_start + 4]
        cols  = st.columns(len(chunk))
        for idx, (col, r) in enumerate(zip(cols, chunk)):
            grad    = _CARD_GRADS[(row_start + idx) % len(_CARD_GRADS)]
            arrow   = "\u25b2" if r["chg"] >= 0 else "\u25bc"
            clr     = "#34d399" if r["chg"] >= 0 else "#f87171"
            chg_cls = "up" if r["chg"] >= 0 else "down"
            badge   = "\U0001f7e2 LIVE" if market_open else "\u26ab LAST CLOSE"
            with col:
                st.markdown(
                    f'<div class="price-card">'
                    f'<div class="price-card-bar" style="background:{grad};"></div>'
                    f'<div class="price-card-badge {chg_cls}">{badge}</div>'
                    f'<div class="price-card-ticker">{r["ticker"]}</div>'
                    f'<div class="price-card-co">{r["co"]}</div>'
                    f'<div class="price-card-price" style="color:{r["color"]};">${r["price"]:,.2f}</div>'
                    f'<div class="price-card-chg" style="color:{clr};">{arrow} {r["chg"]:+.2f}%</div>'
                    f'<div class="price-card-vol">'
                    f'Vol {r["vol_str"]} &nbsp;\u00b7&nbsp; MCap {r["mktcap"]}'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION B — LIVE COMPARISON TABLE
    # ══════════════════════════════════════════════════════════════════════════
    tbl_tag = "LAST PRICES" if not market_open else "REAL-TIME"
    st.markdown(
        f'<div class="sec" style="margin-top:2rem;">'
        f'<div class="sec-title">LIVE COMPARISON TABLE</div>'
        f'<div class="sec-line"></div>'
        f'<div class="sec-tag{closed_tag}">{tbl_tag}</div></div>',
        unsafe_allow_html=True,
    )

    thead = (
        "<thead><tr>"
        "<th>Company</th><th>Ticker</th>"
        "<th>Price</th><th>Change&nbsp;%</th>"
        "<th>Mkt&nbsp;Cap</th><th>P/E</th><th>EPS</th><th>Beta</th>"
        "<th>Net&nbsp;Income</th><th>Net&nbsp;Margin</th>"
        "<th>52W&nbsp;High</th><th>52W&nbsp;Low</th><th>Volume</th>"
        "</tr></thead>"
    )

    tbody_parts = ["<tbody>"]
    for r in rows:
        arrow   = "\u25b2" if r["chg"] >= 0 else "\u25bc"
        chg_cls = "badge-up" if r["chg"] >= 0 else "badge-dn"
        tbody_parts.append(
            f"<tr>"
            f"<td><span class='cmp-dot' style='background:{r['color']};'></span>"
            f"<span class='cmp-co'>{r['co']}</span></td>"
            f"<td><span style='font-family:\"JetBrains Mono\",monospace;"
            f"font-size:.7rem;color:#818cf8;font-weight:700;'>{r['ticker']}</span></td>"
            f"<td><strong style='color:{r['color']};'>${r['price']:,.2f}</strong></td>"
            f"<td class='{chg_cls}'>{arrow}&nbsp;{r['chg']:+.2f}%</td>"
            f"<td>{r['mktcap']}</td>"
            f"<td>{r['pe']}</td>"
            f"<td>{r['eps']}</td>"
            f"<td>{r['beta']}</td>"
            f"<td>{r['ni']}</td>"
            f"<td>{r['margin']}</td>"
            f"<td>{r['w52h']}</td>"
            f"<td>{r['w52l']}</td>"
            f"<td style='color:#64748b;'>{r['vol_str']}</td>"
            f"</tr>"
        )
    tbody_parts.append("</tbody>")
    tbody = "".join(tbody_parts)

    st.markdown(
        f'<div class="cmp-wrap">'
        f'<table class="cmp-table">{thead}{tbody}</table>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION C — INTRADAY CHARTS
    # ══════════════════════════════════════════════════════════════════════════
    chart_tag = "5-DAY" if not market_open else "TODAY"
    st.markdown(
        f'<div class="sec" style="margin-top:2rem;">'
        f'<div class="sec-title">INTRADAY CHARTS</div>'
        f'<div class="sec-line"></div>'
        f'<div class="sec-tag{closed_tag}">{chart_tag}</div></div>',
        unsafe_allow_html=True,
    )

    period   = "1d" if market_open else "5d"
    interval = "5m" if market_open else "1h"

    for row_start in range(0, len(rows), 2):
        chunk = rows[row_start:row_start + 2]
        cols  = st.columns(len(chunk))
        for col, r in zip(cols, chunk):
            with col:
                with st.spinner(f"Loading {r['co']}\u2026"):
                    try:
                        idf = get_intraday_data(
                            r["ticker"], period=period, interval=interval
                        )
                    except Exception:
                        idf = pd.DataFrame()

                if idf.empty:
                    st.info(f"No intraday data available for {r['co']}")
                    continue

                fill_clr = f"rgba({_hex_rgb(r['color'])},0.08)"

                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    row_heights=[0.75, 0.25],
                    vertical_spacing=0.03,
                )

                # Price line
                fig.add_trace(
                    go.Scatter(
                        x=idf.index,
                        y=idf["Close"],
                        name="Price",
                        line=dict(color=r["color"], width=2),
                        fill="tozeroy",
                        fillcolor=fill_clr,
                        hovertemplate="%{x}<br>$%{y:,.2f}<extra></extra>",
                    ),
                    row=1, col=1,
                )

                # Volume bars
                if "Volume" in idf.columns:
                    fig.add_trace(
                        go.Bar(
                            x=idf.index,
                            y=idf["Volume"] / 1e6,
                            name="Vol (M)",
                            marker_color=r["color"],
                            opacity=0.35,
                            hovertemplate="%{x}<br>%{y:.2f}M<extra></extra>",
                        ),
                        row=2, col=1,
                    )

                arrow2    = "\u25b2" if r["chg"] >= 0 else "\u25bc"
                chg_color = "#34d399" if r["chg"] >= 0 else "#f87171"

                fig.update_layout(
                    **_PL,
                    height=300,
                    showlegend=False,
                    title=dict(
                        text=(
                            f"{r['co']} \u00b7 "
                            f"${r['price']:,.2f} "
                            f"<span style='color:{chg_color};'>"
                            f"{arrow2} {r['chg']:+.2f}%</span>"
                        ),
                        font=dict(size=12, color="#e2e8f0"),
                    ),
                    xaxis2=dict(
                        gridcolor="rgba(255,255,255,0.04)",
                        color="#64748b",
                        zerolinecolor="rgba(255,255,255,0.06)",
                    ),
                    yaxis2=dict(
                        gridcolor="rgba(255,255,255,0.04)",
                        color="#64748b",
                        zerolinecolor="rgba(255,255,255,0.06)",
                    ),
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

    # ── footer ────────────────────────────────────────────────────────────────
    mkt_note = (
        "Market open \u2014 live prices"
        if market_open
        else "Market closed \u2014 last available prices"
    )
    st.markdown(
        f'<div style="font-family:\'JetBrains Mono\',monospace;'
        f'font-size:.65rem;color:#334155;margin-top:1.5rem;text-align:center;">'
        f'\u26a1 Data via yfinance \u00b7 '
        f'refreshed {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \u00b7 '
        f'{mkt_note}'
        f'</div>',
        unsafe_allow_html=True,
    )
