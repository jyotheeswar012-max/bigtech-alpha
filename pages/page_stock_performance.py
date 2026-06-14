"""
Page 2 — Stock Performance
Three tabs: Price History (candlestick + MAs + BBands),
Volatility & Risk, Return Analysis.

Public API:
    render_sp(price_df, ann_df, sel_companies, year_range, COLORS, PL, sec, sf)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats as scipy_stats


def render_sp(price_df, ann_df, sel_companies, year_range, COLORS, PL, sec, sf):
    """Render the Stock Performance page.

    Args:
        price_df (pd.DataFrame): Full price history (all companies).
        ann_df   (pd.DataFrame): Annual metrics (used for context).
        sel_companies (list[str]): Active company filter from the sidebar.
        year_range (tuple[int,int]): (start_year, end_year).
        COLORS (dict): Company-name → hex colour.
        PL (dict): Shared Plotly dark-theme layout kwargs.
        sec: Section-header helper from nexus.py.
        sf:  Figure-style helper from nexus.py.
    """
    p_f = price_df[
        (price_df['Company'].isin(sel_companies)) &
        (price_df['Date'].dt.year.between(*year_range))
    ]

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
                fig.add_trace(go.Scatter(
                    x=sub['Date'], y=sub['Upper'], name='BB Upper',
                    line=dict(color='rgba(129,140,248,0.2)', width=1, dash='dot'), showlegend=False))
                fig.add_trace(go.Scatter(
                    x=sub['Date'], y=sub['Lower'], name='BB Lower', fill='tonexty',
                    fillcolor='rgba(129,140,248,0.06)',
                    line=dict(color='rgba(129,140,248,0.2)', width=1, dash='dot'), showlegend=False))
                fig.add_trace(go.Scatter(
                    x=sub['Date'], y=sub['Price'], name='Price',
                    line=dict(color=COLORS.get(co1, '#818cf8'), width=2.5),
                    hovertemplate='<b>' + co1 + '</b><br>%{x|%b %d, %Y}<br>$%{y:.2f}<extra></extra>'))
                fig.add_trace(go.Scatter(
                    x=sub['Date'], y=sub['MA50'], name='MA50',
                    line=dict(color='#fbbf24', width=1.5, dash='dot')))
                fig.add_trace(go.Scatter(
                    x=sub['Date'], y=sub['MA200'], name='MA200',
                    line=dict(color='#a78bfa', width=1.5, dash='dash')))
                sf(fig, 420).update_layout(
                    title=dict(text=f"{co1} — Price + Bollinger Bands + MAs",
                               font=dict(size=13, color='#94a3b8')),
                    yaxis_title="Price (USD)",
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                if 'Volume_M' in sub.columns:
                    fig2 = go.Figure(go.Bar(
                        x=sub['Date'], y=sub['Volume_M'],
                        marker_color=COLORS.get(co1, '#818cf8'), opacity=0.35, name='Volume'))
                    sf(fig2, 120, legend=False).update_layout(
                        yaxis_title="Volume (M)", margin=dict(t=10))
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
                fig.add_trace(go.Scatter(
                    x=sub['Date'], y=vol, name=co, mode='lines',
                    line=dict(color=COLORS.get(co, '#818cf8'), width=1.8),
                    hovertemplate=f'<b>{co}</b> %{{x|%b %Y}}<br>Vol: %{{y:.2f}}%<extra></extra>'))
            sf(fig, 340).update_layout(
                title=dict(text="30-Day Rolling Volatility", font=dict(size=13, color='#94a3b8')),
                yaxis_title="Volatility (%)",
            )
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
                    'Ann. Return %':     round(ret.mean() * 252, 2),
                    'Ann. Volatility %': round(ret.std() * np.sqrt(252), 2),
                    'Sharpe (rf=0)':     round(ret.mean() / ret.std() * np.sqrt(252), 2) if ret.std() > 0 else 0,
                    'Max Drawdown %':    round((sub['Price'] / sub['Price'].cummax() - 1).min() * 100, 2),
                    'Skewness':          round(float(scipy_stats.skew(ret)), 3),
                    'Kurtosis':          round(float(scipy_stats.kurtosis(ret)), 3),
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
                hovertemplate=f'<b>{co}</b><br>Return: %{{y:.1f}}%<extra></extra>',
            ))
        sf(fig, 340, legend=False).update_layout(
            title=dict(text=f"Total Return {year_range[0]}–{year_range[1]}",
                       font=dict(size=13, color='#94a3b8')),
            yaxis_title="Total Return (%)",
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
