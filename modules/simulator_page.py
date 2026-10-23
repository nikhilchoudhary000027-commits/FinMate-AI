"""What-if Simulator page for FinMate AI (UI only)."""

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.financial_calculations import format_rupees, rupees_to_paise
from modules.simulator import monthly_baseline, simulate
from modules.transactions import CATEGORIES, list_transactions


def show_simulator_page(user):
    st.title("🧮 What-if Simulator")
    st.caption(
        "Hypothetical estimates only. Nothing here is saved as a transaction, "
        "and results are not guarantees."
    )

    month = st.text_input("Base month (YYYY-MM)", value=date.today().strftime("%Y-%m"))
    txns = list_transactions(user["id"], start_date=f"{month}-01", end_date=f"{month}-31")
    if not txns:
        st.info("No transactions found for this month, so there is nothing to simulate.")
        return

    base = monthly_baseline(txns)
    st.subheader("Current (recorded) figures")
    c1, c2, c3 = st.columns(3)
    c1.metric("Income", format_rupees(base["income"]))
    c2.metric("Expenses", format_rupees(base["expense"]))
    c3.metric("Savings", format_rupees(base["savings"]))

    st.subheader("Scenario")
    col1, col2 = st.columns(2)
    category = col1.selectbox("Reduce spending on", ["None"] + CATEGORIES)
    percent = col1.slider("Reduce by (%)", 0, 100, 0)
    extra_text = col2.text_input("Extra saving per month (Rs.)", value="0")
    income_change = col2.slider("Income change (%)", -50, 50, 0)
    months = st.slider("Months to project", 1, 24, 6)

    extra_text = extra_text.strip()
    extra = 0 if extra_text in ("", "0") else rupees_to_paise(extra_text)
    if extra is None:
        st.error("Extra saving must be 0 or a positive number.")
        return

    result = simulate(
        base,
        reduce_category=None if category == "None" else category,
        reduce_percent=percent,
        extra_saving_paise=extra,
        income_change_percent=income_change,
        months=months,
    )

    s1, s2, s3 = st.columns(3)
    s1.metric("Scenario monthly savings", format_rupees(result["scenario_savings"]),
              delta=format_rupees(result["monthly_difference"]))
    s2.metric(f"Baseline over {months} months", format_rupees(result["baseline_total"]))
    s3.metric(f"Scenario over {months} months", format_rupees(result["scenario_total"]))

    df = pd.DataFrame({
        "Case": ["Current", "Scenario"],
        "Monthly savings (Rs.)": [result["baseline_savings"] / 100,
                                  result["scenario_savings"] / 100],
    })
    st.plotly_chart(px.bar(df, x="Case", y="Monthly savings (Rs.)"),
                    use_container_width=True)

    st.caption(
        "Assumptions: this month's recorded figures repeat every month; no investment "
        "returns or inflation; extra saving is added on top; estimates only."
    )