# frontend/app.py

import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Medicine Info Assistant", page_icon="💊")

st.title("💊 Medicine Info Assistant")
st.caption("Answers from official leaflets only. This is NOT medical advice.")

if "history" not in st.session_state:
    st.session_state["history"] = []

medicine_name_input = st.text_input("Ilac adini yaz",width=200)
user_input = st.text_input("Ask about a medicine (e.g., dosage, side effects, usage):")

if st.button("Ask") and user_input.strip():
    with st.spinner("Thinking..."):
        resp = requests.post(BACKEND_URL, json={"question": user_input})
        if resp.status_code == 200:
            data = resp.json()
            answer = data["answer"]
            sources = data["sources"]

            st.session_state["history"].append({
                "question": user_input,
                "answer": answer,
                "sources": sources,
            })
        else:
            st.error(f"Error from backend: {resp.status_code}")

# Show chat history
for turn in reversed(st.session_state["history"]):
    st.markdown(f"**You:** {turn['question']}")
    st.markdown(f"**Assistant:** {turn['answer']}")
    if turn["sources"]:
        st.markdown(f"_Sources: {', '.join(turn['sources'])}_")
    st.markdown("---")

st.markdown("⚠️ **Disclaimer:** This tool only summarizes leaflet information and is **not** medical advice.")

