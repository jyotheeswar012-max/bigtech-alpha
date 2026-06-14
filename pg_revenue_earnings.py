"""
Page 3 — Revenue & Earnings
Two tabs: Revenue Trends (annual + quarterly combined + per-company),
Earnings & Margins.

Public API:
    render_re(ann_df, q_df, sel_companies, year_range, COLORS, PL, sec, sf, hex_to_rgba)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats as scipy_stats


def render_re(ann_df, q_df, sel_companies, year_range, COLORS, PL, sec, sf, hex_to_rgba):
    ann_f = ann_df[
        (ann_df['Company'].isin(sel_companies)) &
        (ann_df['Year'].between(*year_range))
    ]
    q_f = q_df[
        (q_df['Company'].isin(sel_companies)) &
        (q_df['Quarter'].dt.year.between(*year_range))
    ]

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
                hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:.1f}}B<extra></extra>',
            ))
        sf(fig, 380).update_layout(
            title=dict(text="Annual Revenue ($B) — All Companies", font=dict(size=13, color='#94a3b8')),
            yaxis_title="Revenue ($B)",
        )
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
                hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>${{y:.1f}}B<extra></extra>',
            ))
        fig2.update_layout(barmode='group')
        sf(fig2, 340).update_layout(
            title=dict(text="Quarterly Revenue ($B) — All Companies", font=dict(size=13, color='#94a3b8')),
            yaxis_title="Revenue ($B)",
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

        sec("Quarterly Revenue — Per Company", f"{year_range[0]}–{year_range[1]}")
        active_cos = [co for co in sel_companies if not q_f[q_f['Company'] == co].empty]
        if active_cos:
            pairs = [active_cos[i:i+2] for i in range(0, len(active_cos), 2)]
            for pair in pairs:
                cols = st.columns(len(pair))
                for col, co in zip(cols, pair):
                    with col:
                        sub   = q_f[q_f['Company'] == co].sort_values('Quarter').copy()
                        color = COLORS.get(co, '#818cf8')
                        fill  = hex_to_rgba(color, 0.12)
                        fig   = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=sub['Quarter'], y=sub['Revenue_B'],
                            name=co, mode='lines+markers',
                            line=dict(color=color, width=2.5),
                            marker=dict(size=7, color=color, line=dict(color='#0f1117', width=1.5)),
                            fill='tozeroy', fillcolor=fill,
                            hovertemplate=f'<b>{co}</b><br>%{{x|%b %Y}}<br>${{y:.1f}}B<extra></extra>',
                        ))
                        if len(sub) >= 3:
                            x_num = np.arange(len(sub))
                            slope, intercept, *_ = scipy_stats.linregress(x_num, sub['Revenue_B'].values)
                            trend = slope * x_num + intercept
                            fig.add_trace(go.Scatter(
                                x=sub['Quarter'], y=trend, mode='lines', name='Trend',
                                line=dict(color='rgba(255,255,255,0.18)', width=1.5, dash='dot'),
                                showlegend=False,
                            ))
                        sf(fig, 280, legend=False).update_layout(
                            title=dict(text=f"{co} — Quarterly Revenue",
                                       font=dict(size=12, color=color)),
                            yaxis_title="$B", margin=dict(l=10, r=10, t=40, b=10),
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
                    hovertemplate=f'<b>{co}</b> %{{x}}<br>${{y:.1f}}B<extra></extra>',
                ))
            sf(fig, 340).update_layout(
                title=dict(text="Net Income ($B)", font=dict(size=13, color='#94a3b8')),
                yaxis_title="Net Income ($B)",
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with c2:
            margin_data = []
            for co in sel_companies:
                sub = ann_f[ann_f['Company'] == co].sort_values('Year').copy()
                if sub.empty:
                    continue
                sub['Margin'] = (
                    sub['NetIncome_B'] / sub['Revenue_B'].replace(0, np.nan) * 100
                ).round(1)
                for _, row in sub.iterrows():
                    margin_data.append({'Company': co, 'Year': row['Year'], 'Margin': row['Margin']})
            if margin_data:
                mdf = pd.DataFrame(margin_data)
                fig  = go.Figure()
                for co in sel_companies:
                    sub = mdf[mdf['Company'] == co]
                    if sub.empty:
                        continue
                    fig.add_trace(go.Scatter(
                        x=sub['Year'], y=sub['Margin'], name=co, mode='lines+markers',
                        line=dict(color=COLORS.get(co, '#818cf8'), width=2),
                        hovertemplate=f'<b>{co}</b> %{{x}}<br>Margin: %{{y:.1f}}%<extra></extra>',
                    ))
                sf(fig, 340).update_layout(
                    title=dict(text="Net Profit Margin (%)", font=dict(size=13, color='#94a3b8')),
                    yaxis_title="Net Margin %",
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No margin data available for the selected filters.")
