from __future__ import annotations

import streamlit as st

from utils import charts


def render_income_page(transactions_df, category_breakdown_df, channel_breakdown_df):
    st.header("Ingresos")

    total_income = transactions_df["amount"].sum() if not transactions_df.empty else 0
    st.metric("Total ingresos", f"€{total_income:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Por categoría")
        cat_fig = charts.bar_chart(category_breakdown_df, x="label", y="total", title="Ingresos por categoría")
        if cat_fig:
            st.plotly_chart(cat_fig, use_container_width=True)
        else:
            st.caption("Sin datos de categorías.")
    with col2:
        st.subheader("Por canal")
        chan_fig = charts.donut_chart(channel_breakdown_df["label"], channel_breakdown_df["total"], "Canales de venta")
        if chan_fig:
            st.plotly_chart(chan_fig, use_container_width=True)
        else:
            st.caption("Sin datos de canales.")

    st.subheader("Detalle de transacciones")
    if transactions_df.empty:
        st.caption("No hay ingresos en el rango seleccionado.")
    else:
        st.dataframe(transactions_df)

