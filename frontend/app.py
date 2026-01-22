## İLAÇ ASİSTANI -- Frontend kodu
## Oğuz Demirtaş

import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="İLAÇ ASİSTANI", page_icon="💊")

st.title("💊 İLAÇ ASİSTANI")
st.caption("Kullandığınız ilaçla ilgili neyi merak ediyorsunuz? İlacın prospektüsünden bakıp hemen söyleyelim.\n\n(Tıbbi bilgi değildir. Mutlaka doktorunuza danışın.)")

if "history" not in st.session_state:
    st.session_state["history"] = []

medicine_name_input = st.text_input("Hangi ilacı kullanıyorsunuz?",width=200)
user_input = st.text_input("Sorunuzu sorun: (örn, yan etkileri nelerdir, haftada kaç gün kullanmalıyım)")

if st.button("Sor") and user_input.strip() and medicine_name_input.strip():
    with st.spinner("İlgileniyorum..."):
        resp = requests.post(BACKEND_URL, json={"medicine_name_input": medicine_name_input,
                   "question": user_input})
        if resp.status_code == 200:
            data = resp.json()
            answer = data["answer"]
            sources = data["sources"]

            st.session_state["history"].append({
                "medicine_name_input": medicine_name_input,
                "question": user_input,
                "answer": answer,
                "sources": sources,
            })
        else:
            st.error(f"Error from backend: {resp.status_code}")

# Show chat history
for turn in reversed(st.session_state["history"]):
    st.markdown(f"**İlaç:** {turn['medicine_name_input']}")
    st.markdown(f"**Siz:** {turn['question']}")
    st.markdown(f"**Asistan:** {turn['answer']}")
    if turn["sources"]:
        st.markdown(f"_Kaynaklar: {', '.join(turn['sources'])}_")
    st.markdown("---")
    st.markdown("⚠️ **Sorumluluk reddi:** Bu sayfa yalnızca ilacın prospektüsünde yer alan bilgileri özetler ve **ASLA** tıbbi bilgi ve tavsiye niteliği taşımaz.")

