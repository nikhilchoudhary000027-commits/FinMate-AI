"""Forecast page for FinMate AI (UI only)."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from modules.financial_calculations import format_rupees, monthly_summary
from modules.forecasting import (
    MIN_MONTHS_FOR_BASELINE, MIN_MONTHS_FOR_MODEL, evaluate, forecast_next,
)
from modules.transactions import list_transactions


def show_forecast_page(user):
    st.title("📈 Expense Forecast")
    st.caption("Estimates from past spending patterns. Not financial advice, "
               "not a guarantee, and not a stock or investment prediction.")

    source = st.radio("Data source", ["My recorded transactions",
                                       "Synthetic sample data (demo)"], horizontal=True)

    if source.startswith("Synthetic"):
        st.warning("This is SYNTHETIC sample data used only to demonstrate the method.")
        df = pd.read_csv("data/synthetic_monthly_expenses.csv")
        series = pd.Series(df["expense_rupees"].values, index=df["month"])
        factor = 1          # rupees
    else:
        summary = monthly_summary(list_transactions(user["id"]))
        months = [m for m, v in summary.items() if v["expense"] > 0]
        series = pd.Series([summary[m]["expense"] / 100 for m in months], index=months)
        factor = 1

    n = len(series)
    st.write(f"Months of expense history available: **{n}**")

    if n < MIN_MONTHS_FOR_BASELINE:
        st.info(f"Forecast unavailable: at least {MIN_MONTHS_FOR_BASELINE} months of "
                "expense history are needed.")
        return

    value, method = forecast_next(series)
    label = "Preliminary" if n < MIN_MONTHS_FOR_MODEL else "Estimated"
    st.metric(f"{label} next-month expense ({method})", f"Rs. {value:,.0f}")
    if n < MIN_MONTHS_FOR_MODEL:
        st.warning(f"Fewer than {MIN_MONTHS_FOR_MODEL} months of data: only a simple "
                   "moving average is shown, and it is preliminary.")
        return

    result = evaluate(series)
    st.subheader("Held-out test months (chronological split)")
    fig = go.Figure()
    fig.add_scatter(x=result["test_index"], y=result["actual"], name="Actual", mode="lines+markers")
    fig.add_scatter(x=result["test_index"], y=result["baseline_pred"], name="Baseline (3-mo avg)", mode="lines+markers")
    fig.add_scatter(x=result["test_index"], y=result["model_pred"], name="Linear Regression", mode="lines+markers")
    fig.update_layout(yaxis_title="Rs.", xaxis_type="category")
    st.plotly_chart(fig, use_container_width=True)

    m1, m2 = st.columns(2)
    m1.metric("Baseline MAE / RMSE", f"{result['baseline_mae']:.0f} / {result['baseline_rmse']:.0f}")
    m2.metric("Model MAE / RMSE", f"{result['model_mae']:.0f} / {result['model_rmse']:.0f}")
    st.caption(f"Trained on {result['train_months']} months, tested on "
               f"{result['test_months']} months. Small test sets give noisy metrics.")