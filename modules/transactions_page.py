"""Transactions page for FinMate AI (UI only; logic lives in transactions.py)."""

from datetime import date

import pandas as pd
import streamlit as st

from modules.financial_calculations import format_rupees
from modules.transactions import (
    CATEGORIES, TXN_TYPES, add_transaction, delete_transaction,
    list_transactions, update_transaction,
)
from modules.categorization import predict_category
PAYMENT_METHODS = ["", "Cash", "UPI", "Card", "Net Banking", "Other"]


def show_transactions_page(user):
    st.title("💸 Transactions")
    uid = user["id"]

       # ---------- Add form ----------
    with st.expander("➕ Add a transaction", expanded=False):
        description = st.text_input("Description", key="add_desc",
                                    placeholder="e.g. Uber ride to office")

        suggested, confidence, source = predict_category(description)
        if description.strip():
            if source == "model":
                st.caption(f"💡 Suggested category: **{suggested}** "
                           f"(model confidence {confidence:.0%})")
            else:
                st.caption(f"💡 Suggested category: **{suggested}** "
                           "(low model confidence, rule-based fallback). Please check.")
        default_index = CATEGORIES.index(suggested) if suggested in CATEGORIES else CATEGORIES.index("Other")

        with st.form("add_txn_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            txn_date = c1.date_input("Date", value=date.today(), max_value=date.today())
            amount = c2.text_input("Amount (Rs.)", placeholder="e.g. 180.50")
            c3, c4 = st.columns(2)
            txn_type = c3.selectbox("Type", TXN_TYPES, index=1)
            category = c4.selectbox("Category", CATEGORIES, index=default_index)
            c5, c6 = st.columns(2)
            payment = c5.selectbox("Payment method (optional)", PAYMENT_METHODS)
            notes = c6.text_input("Notes (optional)")
            submitted = st.form_submit_button("Save transaction")
        if submitted:
            ok, msg = add_transaction(
                uid, txn_date.isoformat(), amount, txn_type, description,
                category, payment or None, notes or None)
            (st.success if ok else st.error)(msg)
    # ---------- Filters ----------
    st.subheader("Your transactions")
    f1, f2, f3, f4 = st.columns(4)
    start = f1.date_input("From", value=None, key="f_start")
    end = f2.date_input("To", value=None, key="f_end")
    cat = f3.selectbox("Category", ["All"] + CATEGORIES, key="f_cat")
    search = f4.text_input("Search description", key="f_search")

    rows = list_transactions(
        uid,
        start_date=start.isoformat() if start else None,
        end_date=end.isoformat() if end else None,
        category=None if cat == "All" else cat,
        search_text=search or None,
    )

    if not rows:
        st.info("No transactions match these filters.")
        return

    df = pd.DataFrame(rows)
    df["Amount"] = df["amount_paise"].apply(format_rupees)
    st.dataframe(
        df[["id", "txn_date", "txn_type", "description", "category", "Amount"]],
        use_container_width=True, hide_index=True,
    )
    st.caption(f"{len(rows)} transaction(s) shown.")

    # ---------- Edit / delete ----------
    st.subheader("Edit or delete")
    options = {
        f"#{r['id']} | {r['txn_date']} | {r['description']} | {format_rupees(r['amount_paise'])}": r
        for r in rows
    }
    chosen = st.selectbox("Select a transaction", list(options.keys()))
    row = options[chosen]

    with st.form("edit_txn_form"):
        e1, e2 = st.columns(2)
        e_date = e1.date_input(
            "Date", value=date.fromisoformat(row["txn_date"]), max_value=date.today())
        e_amount = e2.text_input("Amount (Rs.)", value=f"{row['amount_paise'] / 100:.2f}")
        e3, e4 = st.columns(2)
        e_type = e3.selectbox("Type", TXN_TYPES, index=TXN_TYPES.index(row["txn_type"]))
        e_cat = e4.selectbox("Category", CATEGORIES, index=CATEGORIES.index(row["category"]))
        e_desc = st.text_input("Description", value=row["description"])
        save = st.form_submit_button("Update")
    if save:
        ok, msg = update_transaction(
            uid, row["id"], e_date.isoformat(), e_amount, e_type, e_desc, e_cat,
            row["payment_method"], row["notes"])
        (st.success if ok else st.error)(msg)
        if ok:
            st.rerun()

    confirm = st.checkbox("I understand this delete cannot be undone")
    if st.button("Delete selected transaction", disabled=not confirm):
        ok, msg = delete_transaction(uid, row["id"])
        (st.success if ok else st.error)(msg)
        if ok:
            st.rerun()