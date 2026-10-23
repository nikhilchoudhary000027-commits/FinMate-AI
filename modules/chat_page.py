"""AI Assistant page for FinMate AI (chat UI only)."""

import streamlit as st

from modules.chatbot import handle_message

WELCOME = ("Hi! I can answer questions about your recorded spending, categories, "
           "budget and savings, run what-if reductions, and add expenses "
           "(I always ask before saving).")


def show_chat_page(user):
    st.title("🤖 AI Assistant")
    st.caption("Answers come from your own records using deterministic calculations. "
               "This is not financial advice.")

    # Keep history per user so one login never sees another user's chat.
    key = f"chat_{user['id']}"
    if key not in st.session_state:
        st.session_state[key] = [{"role": "assistant", "content": WELCOME}]
    pending_key = f"pending_{user['id']}"

    for message in st.session_state[key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    text = st.chat_input("Ask about your finances...")
    if text:
        st.session_state[key].append({"role": "user", "content": text})
        reply, pending = handle_message(
            user["id"], text, st.session_state.get(pending_key))
        st.session_state[pending_key] = pending
        st.session_state[key].append({"role": "assistant", "content": reply})
        st.rerun()