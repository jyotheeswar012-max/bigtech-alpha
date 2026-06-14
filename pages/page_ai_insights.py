"""
Page 6 — AI Insight Engine
Auto-generates plain-English insight cards from the latest year's
annual data plus a financial snapshot table.

Public API:
    render_ai(ann_df, sel_companies, sel_year, COLORS, PL, sec, sf)
"""

import streamlit as st
import pandas as pd


def render_ai(ann_df, sel_companies, sel_year, COLORS, PL, sec, sf):
    """Render the AI Insight Engine page.

    Args:
        ann_df (pd.DataFrame): Annual financial metrics.
        sel_companies (list[str]): Active company filter.
        sel_year (int): Single year selected via the header picker.
        COLORS (dict): Company-name → hex colour (unused here, kept for API parity).
        PL (dict): Shared Plotly dark-theme layout kwargs (kept for API parity).
        sec, sf: Helpers injected from nexus.py.
    """
    ann_f = ann_df[
        (ann_df['Company'].isin(sel_companies)) &
        (ann_df['Year'] == sel_year)
    ]

    sec("Auto-Generated Insights", str(sel_year))

    if ann_f.empty:
        st.info(f"No data available for {sel_year}. Try selecting a different year.")
        return

    # Revenue leader
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

    # Market cap leader
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

    # Most profitable
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
    display_cols = [
        c for c in ['Company', 'Revenue_B', 'NetIncome_B', 'MarketCap_B', 'Employees_K']
        if c in ann_f.columns
    ]
    if len(display_cols) > 1:
        st.dataframe(
            ann_f[display_cols].set_index('Company').style.format("{:.2f}"),
            use_container_width=True,
        )
