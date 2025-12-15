from __future__ import annotations

import pandas as pd
import plotly.express as px


def monthly_trend_chart(df: pd.DataFrame):
    if df.empty:
        return None
    melted = df.melt(id_vars="month", value_vars=["income", "expenses"], var_name="type", value_name="amount")
    fig = px.line(melted, x="month", y="amount", color="type", markers=True, title="Ingresos vs Gastos por mes")
    fig.update_layout(legend_title_text="Tipo")
    return fig


def donut_chart(labels, values, title: str):
    if not len(values):
        return None
    fig = px.pie(names=labels, values=values, hole=0.5, title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str):
    if df.empty:
        return None
    fig = px.bar(df, x=x, y=y, title=title)
    fig.update_layout(xaxis_title="", yaxis_title="Monto")
    return fig

