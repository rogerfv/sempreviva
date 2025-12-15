from __future__ import annotations

import streamlit as st

from database import insert_transactions, record_processed_file, recent_files
from processing import expenses, income


def render_upload_page():
    st.header("Subida y procesamiento")
    st.write("Arrastra y suelta un Excel para procesar ingresos o gastos. Los datos se almacenarán automáticamente en SQLite.")

    txn_type = st.radio("Tipo de transacción", ["Ingresos", "Gastos"], horizontal=True)
    uploaded_file = st.file_uploader("Archivo Excel", type=["xlsx", "xls"])

    if uploaded_file and st.button("Procesar archivo"):
        try:
            if txn_type == "Ingresos":
                df, rows = income.process_income(uploaded_file, uploaded_file.name)
            else:
                df, rows = expenses.process_expenses(uploaded_file, uploaded_file.name)

            inserted = insert_transactions(rows)
            record_processed_file(uploaded_file.name, inserted)

            st.success(f"Procesado completado: {inserted} filas insertadas.")
            st.dataframe(df.head())
        except Exception as exc:
            st.error(f"No se pudo procesar el archivo: {exc}")

    st.subheader("Archivos procesados recientemente")
    files = recent_files()
    if not files:
        st.caption("Aún no se han cargado archivos.")
    else:
        for file in files:
            st.write(f"• {file['filename']} ({file['row_count']} filas) - {file['upload_date']}")

