"""
Page 4 — Competitive Analysis
Three tabs: Head-to-Head (table + radar), Market Share (pie charts),
Efficiency (margin + rev/employee).

Public API:
    render_ca(ann_df, sel_companies, sel_year, COLORS, PL, sec, sf, hex_to_rgba)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def render_ca(ann_df, sel_companies, sel_year, COLORS, PL, sec, sf, hex_to_rgba):
    ann_f = ann_df[
        (ann_df['Company'].isin(sel_companies)) &
        (ann_df['Year'] == sel_year)
    ]

    tab1, tab2, tab3 = st.tabs(["🥊 Head-to-Head", "📊 Market Share", "⚡ Efficiency"])

    with tab1:
        sec("Key Metrics Comparison", str(sel_year))
        if not ann_f.empty:
            display_cols = [
                c for c in ['Company', 'Revenue_B', 'NetIncome_B', 'MarketCap_B',
                             'Employees_K', 'PE_Ratio', 'EPS']
                if c in ann_f.columns
            ]
            st.dataframe(
                ann_f[display_cols].set_index('Company').style.format("{:.2f}"),
                use_container_width=True,
            )

            sec("Radar Chart", str(sel_year))
            metrics = [c for c in ['Revenue_B', 'NetIncome_B', 'MarketCap_B'] if c in ann_f.columns]
            if metrics:
                fig = go.Figure()
                for _, row in ann_f.iterrows():
                    vals     = [row.get(m, 0) for m in metrics]
                    max_vals = [ann_f[m].max() for m in metrics]
                    norm     = [v / mx * 100 if mx > 0 else 0 for v, mx in zip(vals, max_vals)]
                    fig.add_trace(go.Scatterpolar(
                        r=norm + [norm[0]], theta=metrics + [metrics[0]],
                        fill='toself', name=row['Company'],
                        line=dict(color=COLORS.get(row['Company'], '#818cf8')),
                        fillcolor=hex_to_rgba(COLORS.get(row['Company'], '#818cf8'), 0.1),
                    ))
                sf(fig, 420).update_layout(
                    polar=dict(radialaxis=dict(
                        visible=True, range=[0, 100],
                        gridcolor='rgba(255,255,255,0.08)', color='#64748b',
                    )),
                    title=dict(text=f"Normalised Metrics Radar {sel_year}",
                               font=dict(size=13, color='#94a3b8')),
                )
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
                    marker=dict(
                        colors=[COLORS.get(c, '#818cf8') for c in ann_f['Company']],
                        line=dict(color='#0f1117', width=2),
                    ),
                ))
                sf(fig, 340, legend=False).update_layout(
                    title=dict(text=f"Revenue Share {sel_year}", font=dict(size=13, color='#94a3b8')))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            with c2:
                if 'MarketCap_B' in ann_f.columns:
                    fig = go.Figure(go.Pie(
                        labels=ann_f['Company'], values=ann_f['MarketCap_B'],
                        hole=0.45, textinfo='label+percent',
                        marker=dict(
                            colors=[COLORS.get(c, '#818cf8') for c in ann_f['Company']],
                            line=dict(color='#0f1117', width=2),
                        ),
                    ))
                    sf(fig, 340, legend=False).update_layout(
                        title=dict(text=f"Market Cap Share {sel_year}",
                                   font=dict(size=13, color='#94a3b8')))
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
                eff['RevPerEmp'] = (
                    eff['Revenue_B'] * 1e9 /
                    (eff['Employees_K'].replace(0, np.nan) * 1e3) / 1e6
                ).round(2).fillna(0)
            eff['NetMargin'] = (
                eff['NetIncome_B'] / eff['Revenue_B'].replace(0, np.nan) * 100
            ).round(1).fillna(0)

            c1, c2 = st.columns(2)
            with c1:
                eff_s = eff.sort_values('NetMargin')
                fig   = go.Figure(go.Bar(
                    x=eff_s['NetMargin'], y=eff_s['Company'], orientation='h',
                    marker=dict(
                        color=[COLORS.get(c, '#818cf8') for c in eff_s['Company']],
                        line=dict(width=0),
                    ),
                    text=[f"{v:.1f}%" for v in eff_s['NetMargin']], textposition='outside',
                    hovertemplate='<b>%{y}</b><br>%{x:.1f}%<extra></extra>',
                ))
                sf(fig, 320, legend=False).update_layout(
                    title=dict(text=f"Net Margin {sel_year}", font=dict(size=13, color='#94a3b8')),
                    xaxis_title="Net Margin %",
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            with c2:
                if 'RevPerEmp' in eff.columns:
                    eff_s2 = eff.sort_values('RevPerEmp')
                    fig    = go.Figure(go.Bar(
                        x=eff_s2['RevPerEmp'], y=eff_s2['Company'], orientation='h',
                        marker=dict(
                            color=[COLORS.get(c, '#818cf8') for c in eff_s2['Company']],
                            line=dict(width=0),
                        ),
                        text=[f"${v:.2f}M" for v in eff_s2['RevPerEmp']], textposition='outside',
                        hovertemplate='<b>%{y}</b><br>$%{x:.2f}M/emp<extra></extra>',
                    ))
                    sf(fig, 320, legend=False).update_layout(
                        title=dict(text=f"Revenue/Employee {sel_year}",
                                   font=dict(size=13, color='#94a3b8')),
                        xaxis_title="$M per Employee",
                    )
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Employee data not available for the selected year.")
        else:
            st.info(f"No data for {sel_year}.")
