"""
Page 1 — Command Center
Renders the hero banner, KPI tiles, and four overview charts.

Public API:
    render_cc(ann_df, q_df, price_df, fund_df, sel_companies,
              year_range, COMMON_LATEST_YEAR, COLORS, PL, helpers)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


def render_cc(
    ann_df, q_df, price_df, fund_df,
    sel_companies, year_range,
    COMMON_LATEST_YEAR, COLORS, PL,
    sec, sf, hex_to_rgba, get_latest_slice, best_common_year,
):
    """Render the Command Center overview page.

    Args:
        ann_df, q_df, price_df, fund_df: DataFrames built by nexus.py.
        sel_companies (list[str]): Companies selected in the sidebar.
        year_range (tuple[int,int]): (start_year, end_year) from the slider.
        COMMON_LATEST_YEAR (int): Best fully-covered year across all companies.
        COLORS (dict): Company-name → hex colour mapping.
        PL (dict): Shared Plotly dark-theme layout kwargs.
        sec, sf, hex_to_rgba, get_latest_slice, best_common_year: Helpers
            injected from nexus.py so this module stays import-free of st config.
    """
    from scipy import stats as scipy_stats

    ann_f = ann_df[
        (ann_df['Company'].isin(sel_companies)) &
        (ann_df['Year'].between(*year_range))
    ]
    q_f = q_df[
        (q_df['Company'].isin(sel_companies)) &
        (q_df['Quarter'].dt.year.between(*year_range))
    ]
    p_f = price_df[
        (price_df['Company'].isin(sel_companies)) &
        (price_df['Date'].dt.year.between(*year_range))
    ]

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

    # ── KPI tiles ──────────────────────────────────────────────────
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

    # ── Section 1: Revenue Race & Market Cap ──────────────────────
    sec("Revenue Race & Market Cap", f"{year_range[0]}–{year_range[1]}")
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        for co in sel_companies:
            sub = q_f[q_f['Company'] == co].sort_values('Quarter')
            if sub.empty:
                continue
            fig.add_trace(go.Scatter(
                x=sub['Quarter'], y=sub['Revenue_B'], name=co, mode='lines',
                line=dict(color=COLORS.get(co, '#818cf8'), width=2.5),
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>${{y:.1f}}B<extra></extra>',
            ))
        sf(fig, 350).update_layout(
            title=dict(text="Quarterly Revenue ($B)", font=dict(size=13, color='#94a3b8')),
            yaxis_title="Revenue ($B)",
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        if not ann_f.empty:
            mc_data = ann_f.pivot_table(
                index='Year', columns='Company', values='MarketCap_B', aggfunc='first'
            ).fillna(0)
            fig = go.Figure()
            for co in [c for c in sel_companies if c in mc_data.columns]:
                fig.add_trace(go.Bar(
                    x=mc_data.index, y=mc_data[co], name=co,
                    marker_color=COLORS.get(co, '#818cf8'), opacity=0.88,
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:,.0f}}B<extra></extra>',
                ))
            fig.update_layout(barmode='group')
            sf(fig, 350).update_layout(
                title=dict(text="Market Cap by Year ($B)", font=dict(size=13, color='#94a3b8')),
                yaxis_title="Market Cap ($B)",
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No annual data available for the selected filters.")

    # ── Section 2: Stock Returns & Profitability ───────────────────
    sec("Stock Returns & Profitability", f"{year_range[0]}–{year_range[1]}")
    c1, c2 = st.columns([3, 2])
    with c1:
        fig = go.Figure()
        for co in sel_companies:
            sub = p_f[p_f['Company'] == co].sort_values('Date')
            if sub.empty or sub['Price'].iloc[0] == 0:
                continue
            base = sub['Price'].iloc[0]
            fig.add_trace(go.Scatter(
                x=sub['Date'], y=sub['Price'] / base * 100, name=co, mode='lines',
                line=dict(color=COLORS.get(co, '#818cf8'), width=2),
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>%{{y:.0f}}<extra></extra>',
            ))
        fig.add_hline(y=100, line_dash='dot', line_color='rgba(255,255,255,0.1)')
        sf(fig, 340).update_layout(
            title=dict(text="Normalised Stock Performance (Base=100)", font=dict(size=13, color='#94a3b8')),
            yaxis_title="Indexed Return",
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        margin_sl, m_yr = get_latest_slice(ann_f, sel_companies)
        if not margin_sl.empty:
            margin_sl = margin_sl.copy()
            margin_sl['Margin'] = (
                margin_sl['NetIncome_B'] /
                margin_sl['Revenue_B'].replace(0, np.nan) * 100
            ).round(1).fillna(0)
            margin_sl = margin_sl.sort_values('Margin')
            fig = go.Figure(go.Bar(
                x=margin_sl['Margin'], y=margin_sl['Company'], orientation='h',
                marker=dict(
                    color=margin_sl['Margin'],
                    colorscale=[[0, '#f87171'], [0.4, '#fb923c'], [1, '#34d399']],
                    line=dict(width=0),
                ),
                text=[f"{v:.1f}%" for v in margin_sl['Margin']], textposition='outside',
                hovertemplate='<b>%{y}</b><br>Margin: %{x:.1f}%<extra></extra>',
            ))
            sf(fig, 340, legend=False).update_layout(
                title=dict(text=f"Net Profit Margin {m_yr}", font=dict(size=13, color='#94a3b8')),
                xaxis_title="Net Margin %",
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No margin data available for the selected filters.")

    # ── Section 3: Revenue Distribution & Headcount ───────────────
    sec("Revenue Distribution & Headcount", f"{year_range[0]}–{year_range[1]}")
    c1, c2 = st.columns(2)
    with c1:
        treemap_sl, t_yr = get_latest_slice(ann_f, sel_companies)
        if not treemap_sl.empty and 'Sector' in treemap_sl.columns:
            fig = px.treemap(
                treemap_sl, path=['Sector', 'Company'], values='Revenue_B',
                color='NetIncome_B',
                color_continuous_scale=[[0, '#f87171'], [0.5, '#1e293b'], [1, '#34d399']],
                hover_data={'Revenue_B': ':.1f', 'NetIncome_B': ':.1f'},
            )
            fig.update_traces(
                textfont_size=13, textfont_color='#e2e8f0',
                hovertemplate='<b>%{label}</b><br>Revenue: $%{value:.1f}B<extra></extra>',
            )
            fig.update_layout(
                **PL, height=330,
                title=dict(text=f"Revenue Treemap {t_yr}", font=dict(size=13, color='#94a3b8')),
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Sector data not available in current dataset.")
    with c2:
        emp_sl, e_yr = get_latest_slice(ann_f, sel_companies)
        if not emp_sl.empty:
            emp_sl = emp_sl.copy()
            emp_sl['RevPerEmp'] = (
                emp_sl['Revenue_B'] * 1e9 /
                (emp_sl['Employees_K'].replace(0, np.nan) * 1e3) / 1e6
            ).round(2).fillna(0)
            emp_sl = emp_sl.sort_values('RevPerEmp')
            fig = go.Figure(go.Bar(
                x=emp_sl['RevPerEmp'], y=emp_sl['Company'], orientation='h',
                marker=dict(
                    color=[COLORS.get(c, '#818cf8') for c in emp_sl['Company']],
                    line=dict(width=0),
                ),
                text=[f"${v:.2f}M" for v in emp_sl['RevPerEmp']], textposition='outside',
                hovertemplate='<b>%{y}</b><br>$%{x:.2f}M per employee<extra></extra>',
            ))
            sf(fig, 330, legend=False).update_layout(
                title=dict(text=f"Revenue per Employee {e_yr} ($M)", font=dict(size=13, color='#94a3b8')),
                xaxis_title="$M per Employee",
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No employee data available for the selected filters.")
