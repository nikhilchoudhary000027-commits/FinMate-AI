"""Global CSS for a dark, card-based FinMate look (inspired by modern fintech UIs)."""

import streamlit as st

CSS = """
<style>
.stApp {
    background: radial-gradient(circle at 20% 0%, #1a1440 0%, #0B1120 45%);
}
section[data-testid="stSidebar"] {
    background: #0d1326;
    border-right: 1px solid #1f2747;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid #232b4d;
    border-radius: 18px;
    padding: 6px;
}
div[data-testid="stMetric"] {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid #232b4d;
    border-radius: 16px;
    padding: 14px 16px;
}
div[data-testid="stMetricValue"] { font-size: 1.6rem; }
.stButton > button {
    border-radius: 999px;
    border: 1px solid #3b3f73;
    background: #151b36;
}
.stButton > button:hover { border-color: #8B5CF6; color: #c4b5fd; }
h1, h2, h3 { letter-spacing: -0.01em; }
.fm-chip-label { color: #9ca3af; font-size: 0.8rem; }
.fm-amount-neg { color: #f87171; font-weight: 600; }
.fm-amount-pos { color: #34d399; font-weight: 600; }
</style>
"""


def apply_theme():
    st.markdown(CSS, unsafe_allow_html=True)