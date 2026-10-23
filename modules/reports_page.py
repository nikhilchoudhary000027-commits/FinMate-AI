"""Reports page: monthly report, CSV export and import (UI only)."""

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.csv_tools import export_csv, import_csv
from modules.financial_calculations import (
    category_spending, format_rupees, monthly_summary,
)
from modules.transactions import list_transactions


def show_reports_page(user):
    st.title("📑 Reports")
    uid = user["id"]
    txns = list_transactions(uid)

    st.subheader("Monthly report")
    if not txns:
        st.info("No transactions yet.")
    else:
        summary = monthly_summary(txns)
        df = pd.DataFrame([
            {"Month": m, "Income": format_rupees(v["income"]),
             "Expenses": format_rupees(v["expense"]),
             "Savings": format_rupees(v["savings"])}
            for m, v in summary.items()
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)

        month = st.selectbox("Category breakdown for", list(summary.keys())[::-1])
        spending = category_spending([t for t in txns if t["txn_date"].startswith(month)])
        if spending:
            cdf = pd.DataFrame({"Category": list(spending.keys()),
                                "Amount (Rs.)": [v / 100 for v in spending.values()]})
            fig = px.bar(cdf, x="Category", y="Amount (Rs.)")
            fig.update_xaxes(type="category")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No expenses in this month.")

    st.subheader("Export")
    st.download_button("Download my transactions (CSV)", export_csv(uid),
                       file_name="finmate_transactions.csv", mime="text/csv")

    st.subheader("Import")
    st.caption("Columns required: date, amount, type, description, category. "
               "Duplicates are skipped and invalid rows are reported.")
    uploaded = st.file_uploader("Upload CSV", type="csv")
    if uploaded is not None and st.button("Import file"):
        try:
            text = uploaded.getvalue().decode("utf-8-sig")
        except UnicodeDecodeError:
            st.error("File must be UTF-8 text.")
            return
        result = import_csv(uid, text)
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(f"Added {result['added']}, skipped {result['duplicates']} duplicates, "
                       f"rejected {len(result['invalid'])} invalid rows.")
            for msg in result["invalid"]:
                st.warning(msg)