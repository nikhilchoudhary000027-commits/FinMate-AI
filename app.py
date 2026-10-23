"""FinMate AI - main Streamlit application."""

import streamlit as st

from database.db import init_db
from modules.authentication import login_user, register_user
from modules.dashboard import show_dashboard
from modules.transactions_page import show_transactions_page
from modules.planning_pages import show_budgets_page, show_goals_page
from modules.chat_page import show_chat_page
from modules.simulator_page import show_simulator_page
from modules.forecast_page import show_forecast_page
from modules.reports_page import show_reports_page
from modules.ui_theme import apply_theme

st.set_page_config(page_title="FinMate AI", page_icon="💰", layout="wide")
init_db()
apply_theme()

def show_auth_page():
    st.title("💰 FinMate AI")
    st.caption("An intelligent personal finance assistant by Team ArthX")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in")
        if submitted:
            user = login_user(username, password)
            if user:
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("Wrong username or password.")

    with register_tab:
        with st.form("register_form"):
            name = st.text_input("Full name")
            email = st.text_input("Email")
            new_username = st.text_input("Choose a username")
            new_password = st.text_input("Choose a password", type="password")
            registered = st.form_submit_button("Create account")
        if registered:
            ok, message = register_user(name, email, new_username, new_password)
            if ok:
                st.success(message)
            else:
                st.error(message)


def show_main_app(user):
    st.sidebar.title("💰 FinMate AI")
    st.sidebar.write(f"Logged in as **{user['name']}**")

    page = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "Transactions", "Budgets", "Savings Goals", "What-if Simulator", "Forecast", "AI Assistant", "Reports"],
    )

    if st.sidebar.button("Log out"):
        del st.session_state["user"]
        st.rerun()

    if page == "Dashboard":
        show_dashboard(user)
    elif page == "Transactions":
        show_transactions_page(user)
    elif page == "Budgets":
        show_budgets_page(user)
    elif page == "Savings Goals":
        show_goals_page(user)
    elif page == "AI Assistant":
        show_chat_page(user)
    elif page == "What-if Simulator":
        show_simulator_page(user)
    elif page == "Forecast":
        show_forecast_page(user)
    elif page == "Reports":
        show_reports_page(user)
    else:
        st.title(page)
        st.info(f"{page} page coming soon.")


user = st.session_state.get("user")
if user is None:
    show_auth_page()
else:
    show_main_app(user)