from __future__ import annotations

import streamlit as st

from utils import charts


def render_dashboard(totals, trend_df, income_breakdown_df, expense_breakdown_df, ai_text: str | None = None):
    st.header("Panel general")

    if ai_text:
        st.info(ai_text)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ingresos", f"€{totals['income']:.2f}")
    col2.metric("Gastos", f"€{totals['expenses']:.2f}")
    col3.metric("Beneficio", f"€{totals['net']:.2f}")
    col4.metric("Margen", f"{totals['margin']:.1f}%")

    st.subheader("Tendencia mensual")
    trend_fig = charts.monthly_trend_chart(trend_df)
    if trend_fig:
        st.plotly_chart(trend_fig, use_container_width=True)
    else:
        st.caption("No hay datos suficientes para la tendencia.")

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### Canales de ingreso")
        income_fig = charts.bar_chart(income_breakdown_df, x="label", y="total", title="Ingresos por canal")
        if income_fig:
            st.plotly_chart(income_fig, use_container_width=True)
        else:
            st.caption("No hay ingresos registrados en el periodo.")
    with col_right:
        st.markdown("### Distribución de gastos")
        expense_fig = charts.donut_chart(expense_breakdown_df["label"], expense_breakdown_df["total"], "Gastos por categoría")
        if expense_fig:
            st.plotly_chart(expense_fig, use_container_width=True)
        else:
            st.caption("No hay gastos registrados en el periodo.")

