"""Dashboard page for FinMate AI."""

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.budget_planner import budget_status
from modules.financial_calculations import (
    calculate_balance, category_spending, format_rupees,
    monthly_summary, total_by_type,
)
from modules.savings_planner import list_goals
from modules.transactions import list_transactions
from modules.anomaly_detection import find_unusual

def show_dashboard(user):
    st.title("📊 Dashboard")
    st.caption(
        "All figures are calculated from the transactions you recorded. "
        "The balance is NOT a bank-confirmed balance."
    )

    transactions = list_transactions(user["id"])
    if not transactions:
        st.info("No transactions yet. Add some on the Transactions page.")
        return

    this_month = date.today().strftime("%Y-%m")
    month_txns = [t for t in transactions if t["txn_date"].startswith(this_month)]

    income = total_by_type(transactions, "income")
    expense = total_by_type(transactions, "expense")
    month_income = total_by_type(month_txns, "income")
    month_expense = total_by_type(month_txns, "expense")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total income", format_rupees(income))
    c2.metric("Total expenses", format_rupees(expense))
    c3.metric("Calculated balance", format_rupees(calculate_balance(transactions)))
    c4.metric(f"Savings ({this_month})", format_rupees(month_income - month_expense))

    left, right = st.columns(2)

    with left:
        st.subheader("Spending by category")
        spending = category_spending(transactions)
        if spending:
            df = pd.DataFrame({
                "Category": list(spending.keys()),
                "Amount (Rs.)": [v / 100 for v in spending.values()],
            })
            fig = px.pie(df, names="Category", values="Amount (Rs.)", hole=0.55)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No expenses recorded yet.")

    with right:
        st.subheader("Monthly income vs expense")
        summary = monthly_summary(transactions)
        df = pd.DataFrame([
            {"Month": m, "Income": v["income"] / 100, "Expense": v["expense"] / 100}
            for m, v in summary.items()
        ])
        df["Month"] = df["Month"].astype(str)
        fig = px.bar(df, x="Month", y=["Income", "Expense"], barmode="group")
        fig.update_xaxes(type="category")
        fig.update_layout(yaxis_title="Rs.", legend_title="")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Budget utilisation ({this_month})")
    statuses = budget_status(user["id"], this_month)
    if statuses:
        for s in statuses:
            label = (f"{s['category']}: {format_rupees(s['spent_paise'])} of "
                     f"{format_rupees(s['limit_paise'])} ({s['percent_used']}%)")
            st.progress(min(s["percent_used"] / 100, 1.0), text=label)
            if s["status"] == "exceeded":
                st.error(f"{s['category']} budget exceeded.")
            elif s["status"] == "warning":
                st.warning(f"{s['category']} is above 80% of its budget.")
        st.caption("These are in-app alerts based on recorded transactions, not bank notifications.")
    else:
        st.write("No budgets set for this month.")

    st.subheader("Savings goals")
    goals = list_goals(user["id"])
    if goals:
        for g in goals:
            st.progress(g["percent"] / 100,
                        text=f"{g['goal_name']}: {g['percent']}% of {format_rupees(g['target_paise'])}")
    else:
        st.write("No savings goals yet.")

    st.subheader("Transactions worth a second look")
    unusual = find_unusual(transactions)
    if unusual:
        for u in unusual[:5]:
            st.warning(
                f"{u['txn_date']} | {u['category']} | {u['description']} | "
                f"{format_rupees(u['amount_paise'])} is much higher than your typical "
                f"{format_rupees(u['typical_paise'])} for this category."
            )
        st.caption("These are only statistical flags. An unusual expense is not proof "
                   "of fraud or a mistake; it may be a genuine one-off purchase.")
    else:
        st.write("Nothing unusual found (needs at least 5 expenses in a category).")

    st.subheader("Recent transactions")
    recent = pd.DataFrame(transactions[:10])
    recent["Amount (Rs.)"] = recent["amount_paise"] / 100
    st.dataframe(
        recent[["txn_date", "txn_type", "description", "category", "Amount (Rs.)"]],
        use_container_width=True, hide_index=True,
    )