"""
Page 5 — Deep Analytics
Three tabs: Correlation matrix, Revenue vs MCap regression,
YoY revenue growth factor analysis.

Public API:
    render_da(ann_df, price_df, sel_companies, year_range, COLORS, PL, sec, sf)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats as scipy_stats


def render_da(ann_df, price_df, sel_companies, year_range, COLORS, PL, sec, sf):
    ann_f = ann_df[
        (ann_df['Company'].isin(sel_companies)) &
        (ann_df['Year'].between(*year_range))
    ]
    p_f = price_df[
        (price_df['Company'].isin(sel_companies)) &
        (price_df['Date'].dt.year.between(*year_range))
    ]

    tab1, tab2, tab3 = st.tabs(["📈 Correlation", "📉 Regression", "🔍 Factor Analysis"])

    with tab1:
        sec("Price Return Correlation Matrix", f"{year_range[0]}–{year_range[1]}")
        pivot = price_df[price_df['Company'].isin(sel_companies)].pivot_table(
            index='Date', columns='Company', values='Price')
        pivot = pivot.ffill().dropna()
        if len(pivot) > 5:
            corr = pivot.pct_change().dropna().corr()
            fig  = go.Figure(go.Heatmap(
                z=corr.values,
                x=corr.columns.tolist(),
                y=corr.index.tolist(),
                colorscale=[[0, '#f87171'], [0.5, '#1e293b'], [1, '#34d399']],
                zmin=-1, zmax=1,
                text=corr.round(2).values,
                texttemplate='%{text}',
                hovertemplate='%{y} × %{x}<br>r = %{z:.3f}<extra></extra>',
            ))
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
                        text=sub['Year'].astype(str), textposition='top center',
                        marker=dict(color=COLORS.get(co, '#818cf8'), size=10),
                        hovertemplate=f'<b>{co}</b><br>Rev: $%{{x:.1f}}B<br>MCap: $%{{y:.1f}}B<extra></extra>',
                    ))
                fig.add_trace(go.Scatter(
                    x=x_line, y=y_line, mode='lines',
                    name=f'Fit (R²={r**2:.2f})',
                    line=dict(color='rgba(129,140,248,0.5)', width=2, dash='dash'),
                ))
                sf(fig, 400).update_layout(
                    title=dict(
                        text=f"Revenue vs Market Cap | R²={r**2:.3f} p={p_val:.3f}",
                        font=dict(size=13, color='#94a3b8'),
                    ),
                    xaxis_title="Revenue ($B)", yaxis_title="Market Cap ($B)",
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Insufficient data for regression (need ≥3 data points with MarketCap).")

    with tab3:
        sec("YoY Revenue Growth Rates", f"{year_range[0]}–{year_range[1]}")
        growth_rows = []
        for co in sel_companies:
            sub = ann_df[ann_df['Company'] == co].sort_values('Year').copy()
            if len(sub) < 2:
                continue
            sub['YoY_Growth'] = sub['Revenue_B'].pct_change() * 100
            for _, row in sub.iterrows():
                if pd.notna(row['YoY_Growth']) and year_range[0] <= row['Year'] <= year_range[1]:
                    growth_rows.append({
                        'Company':    co,
                        'Year':       int(row['Year']),
                        'YoY_Growth': round(row['YoY_Growth'], 1),
                    })
        if growth_rows:
            gdf = pd.DataFrame(growth_rows)
            fig = go.Figure()
            for co in sel_companies:
                sub = gdf[gdf['Company'] == co]
                if sub.empty:
                    continue
                fig.add_trace(go.Bar(
                    x=sub['Year'], y=sub['YoY_Growth'], name=co,
                    marker_color=COLORS.get(co, '#818cf8'), opacity=0.85,
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>Growth: %{{y:.1f}}%<extra></extra>',
                ))
            fig.update_layout(barmode='group')
            sf(fig, 360).update_layout(
                title=dict(text="YoY Revenue Growth (%)", font=dict(size=13, color='#94a3b8')),
                yaxis_title="Growth %",
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Not enough data for YoY growth analysis.")
