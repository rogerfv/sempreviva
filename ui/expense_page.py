from __future__ import annotations

import streamlit as st

from utils import charts


def render_expense_page(transactions_df, category_breakdown_df, group_breakdown_df):
    st.header("Gastos")

    total_expense = transactions_df["amount"].sum() if not transactions_df.empty else 0
    st.metric("Total gastos", f"€{total_expense:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Por categoría")
        cat_fig = charts.bar_chart(category_breakdown_df, x="label", y="total", title="Gastos por categoría")
        if cat_fig:
            st.plotly_chart(cat_fig, use_container_width=True)
        else:
            st.caption("Sin datos de categorías.")
    with col2:
        st.subheader("Fijo vs Variable")
        group_fig = charts.donut_chart(group_breakdown_df["label"], group_breakdown_df["total"], "Tipo de gasto")
        if group_fig:
            st.plotly_chart(group_fig, use_container_width=True)
        else:
            st.caption("Sin datos de grupos.")

    st.subheader("Detalle de transacciones")
    if transactions_df.empty:
        st.caption("No hay gastos en el rango seleccionado.")
    else:
        st.dataframe(transactions_df)

