from __future__ import annotations

from datetime import date
from typing import Tuple

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

import database as db
from ui.dashboard import render_dashboard
from ui.expense_page import render_expense_page
from ui.income_page import render_income_page
from ui.upload_page import render_upload_page
from utils import ai_insights


load_dotenv()
db.init_db()

st.set_page_config(page_title="Sempreviva Dashboard", layout="wide")


@st.cache_data
def _get_date_defaults() -> Tuple[date, date]:
    min_date_str, max_date_str = db.get_date_bounds()
    today = date.today()
    start = pd.to_datetime(min_date_str).date() if min_date_str else today.replace(month=1, day=1)
    end = pd.to_datetime(max_date_str).date() if max_date_str else today
    return start, end


def _date_range_selector() -> Tuple[str, str]:
    default_start, default_end = _get_date_defaults()
    start_date, end_date = st.sidebar.date_input(
        "Rango de fechas",
        value=(default_start, default_end),
    )

    if isinstance(start_date, tuple):
        start_date, end_date = start_date

    if start_date > end_date:
        st.sidebar.error("La fecha inicial no puede ser posterior a la final.")
    return start_date.isoformat(), end_date.isoformat()


def _load_datasets(start: str, end: str):
    transactions = db.fetch_transactions_df(start, end)
    income_df = transactions[transactions["type"] == "INCOME"].copy()
    expense_df = transactions[transactions["type"] == "EXPENSE"].copy()

    totals = db.get_totals(start, end)
    trend_df = db.get_monthly_totals(start, end)
    income_channel_breakdown = db.get_breakdown("INCOME", "subcategory", start, end)
    income_category_breakdown = db.get_breakdown("INCOME", "category", start, end)
    expense_category_breakdown = db.get_breakdown("EXPENSE", "category", start, end)
    expense_group_breakdown = db.get_breakdown("EXPENSE", "subcategory", start, end)

    return {
        "transactions": transactions,
        "income_df": income_df,
        "expense_df": expense_df,
        "totals": totals,
        "trend_df": trend_df,
        "income_channel_breakdown": income_channel_breakdown,
        "income_category_breakdown": income_category_breakdown,
        "expense_category_breakdown": expense_category_breakdown,
        "expense_group_breakdown": expense_group_breakdown,
    }


def main():
    st.sidebar.title("Sempreviva")
    st.sidebar.markdown("Navegación")
    start, end = _date_range_selector()

    page = st.sidebar.radio("", ["Dashboard", "Ingresos", "Gastos", "Subir archivo"])

    data = _load_datasets(start, end)

    insight_text = None
    if not data["transactions"].empty:
        stats = {
            "totals": data["totals"],
            "monthly_trend": data["trend_df"].tail(6).to_dict("records"),
            "top_income": data["income_category_breakdown"].head(3).to_dict("records"),
            "top_expenses": data["expense_category_breakdown"].head(3).to_dict("records"),
        }
        insight_text = ai_insights.generate_insights(stats)

    if page == "Dashboard":
        render_dashboard(
            data["totals"],
            data["trend_df"],
            data["income_channel_breakdown"],
            data["expense_category_breakdown"],
            ai_text=insight_text,
        )
    elif page == "Ingresos":
        render_income_page(
            data["income_df"],
            data["income_category_breakdown"],
            data["income_channel_breakdown"],
        )
    elif page == "Gastos":
        render_expense_page(
            data["expense_df"],
            data["expense_category_breakdown"],
            data["expense_group_breakdown"],
        )
    else:
        render_upload_page()


if __name__ == "__main__":
    main()

