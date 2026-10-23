"""Budgets and Savings Goals pages for FinMate AI (UI only)."""

from datetime import date, timedelta

import streamlit as st

from modules.budget_planner import OVERALL, budget_status, set_budget
from modules.financial_calculations import format_rupees
from modules.savings_planner import (
    add_goal, delete_goal, list_goals, update_saved_amount,
)
from modules.transactions import CATEGORIES


def show_budgets_page(user):
    st.title("🎯 Budgets")
    uid = user["id"]
    st.caption("Budget alerts are in-app alerts based on your recorded transactions, "
               "not bank notifications.")

    month = st.text_input("Month (YYYY-MM)", value=date.today().strftime("%Y-%m"))

    with st.form("budget_form"):
        c1, c2 = st.columns(2)
        category = c1.selectbox("Category", [OVERALL] + CATEGORIES)
        limit = c2.text_input("Limit (Rs.)", placeholder="e.g. 5000")
        saved = st.form_submit_button("Save budget")
    if saved:
        ok, msg = set_budget(uid, month, category, limit)
        (st.success if ok else st.error)(msg)

    st.subheader(f"Budget status for {month}")
    statuses = budget_status(uid, month)
    if not statuses:
        st.info("No budgets set for this month.")
        return
    for s in statuses:
        label = (f"{s['category']}: {format_rupees(s['spent_paise'])} of "
                 f"{format_rupees(s['limit_paise'])} ({s['percent_used']}%)")
        st.progress(min(s["percent_used"] / 100, 1.0), text=label)
        if s["status"] == "exceeded":
            st.error(f"{s['category']} exceeded by {format_rupees(-s['remaining_paise'])}.")
        elif s["status"] == "warning":
            st.warning(f"{s['category']}: {format_rupees(s['remaining_paise'])} remaining.")


def show_goals_page(user):
    st.title("🏦 Savings Goals")
    uid = user["id"]
    st.caption("Estimates assume equal monthly savings and no investment returns. "
               "They are not guarantees.")

    with st.expander("➕ Add a goal"):
        with st.form("goal_form", clear_on_submit=True):
            name = st.text_input("Goal name", placeholder="e.g. Laptop")
            c1, c2 = st.columns(2)
            target = c1.text_input("Target amount (Rs.)")
            saved = c2.text_input("Already saved (Rs.)", value="0")
            target_date = st.date_input(
                "Target date", value=date.today() + timedelta(days=180),
                min_value=date.today() + timedelta(days=1))
            submit = st.form_submit_button("Save goal")
        if submit:
            ok, msg = add_goal(uid, name, target, saved, target_date.isoformat())
            (st.success if ok else st.error)(msg)

    goals = list_goals(uid)
    if not goals:
        st.info("No savings goals yet.")
        return

    for g in goals:
        st.subheader(g["goal_name"])
        st.progress(g["percent"] / 100,
                    text=f"{g['percent']}% of {format_rupees(g['target_paise'])}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Remaining", format_rupees(g["remaining_paise"]))
        m2.metric("Months left", g["months_remaining"])
        if g["monthly_required_paise"] is None:
            m3.metric("Required per month", "n/a")
        else:
            m3.metric("Required per month", format_rupees(g["monthly_required_paise"]))
        if g["status"] == "achieved":
            st.success("Goal achieved.")
        elif g["status"] == "overdue":
            st.warning("Target date has passed.")

        u1, u2 = st.columns([3, 1])
        new_saved = u1.text_input("Update saved amount (Rs.)",
                                  value=f"{g['saved_paise'] / 100:.2f}",
                                  key=f"saved_{g['id']}")
        if u2.button("Update", key=f"upd_{g['id']}"):
            ok, msg = update_saved_amount(uid, g["id"], new_saved)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()
        if st.button("Delete goal", key=f"del_{g['id']}"):
            ok, msg = delete_goal(uid, g["id"])
            if ok:
                st.rerun()
            st.error(msg)
        st.divider()