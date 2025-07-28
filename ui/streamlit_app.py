# ui/streamlit_app.py

import streamlit as st
import requests

# Config
BACKEND_HOST = "http://localhost:8000"
ASK_API = f"{BACKEND_HOST}/ask"
METRICS_API = f"{BACKEND_HOST}/metrics"

st.set_page_config(page_title="Enterprise RAG Dashboard", layout="wide")
st.title("🚀 Enterprise RAG Agent Interface")

# Sidebar - API Key
st.sidebar.header("🔐 Authentication")
api_key = st.sidebar.text_input("Enter API Key", type="password")
headers = {"X-API-Key": api_key} if api_key else {}

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "📊 System Metrics", "🔍 Health Check"])

# --- Tab 1: Chat Assistant ---
with tab1:
    st.subheader("Ask your enterprise knowledge assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    question = st.text_input("Your Question:")

    if st.button("Submit", key="submit_qa") and question and api_key:
        with st.spinner("Generating answer..."):
            try:
                response = requests.post(ASK_API, json={"question": question}, headers=headers)
                response.raise_for_status()
                answer = response.json().get("final_answer", "No answer returned.")
                st.session_state.chat_history.append(("You", question))
                st.session_state.chat_history.append(("AI", answer))
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("🗂️ Chat History")
        for sender, message in st.session_state.chat_history:
            st.markdown(f"**{sender}:** {message}")

# --- Tab 2: System Metrics ---
with tab2:
    st.subheader("📈 Prometheus-style Metrics")

    if st.button("Refresh Metrics"):
        with st.spinner("Fetching metrics..."):
            try:
                response = requests.get(METRICS_API)
                response.raise_for_status()
                metrics_text = response.text
                st.code(metrics_text, language="yaml")
            except Exception as e:
                st.error(f"Failed to fetch metrics: {e}")

# --- Tab 3: Health Check ---
with tab3:
    st.subheader("🔎 Service Status")

    try:
        ping_response = requests.get(f"{BACKEND_HOST}/docs")
        if ping_response.status_code == 200:
            st.success("✅ Backend is UP and reachable!")
        else:
            st.warning("⚠️ Backend responded but with non-200 status.")
    except Exception:
        st.error("❌ Backend is not reachable.")
