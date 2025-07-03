# frontend/app.py
import streamlit as st
import requests

st.set_page_config(page_title="Requirement Classifier", layout="wide")
st.title("📄 Requirement Classification")

uploaded_file = st.file_uploader("Upload PDF File", type="pdf")

if uploaded_file:
    with st.spinner("Uploading and classifying..."):
        try:
            files = {"file": uploaded_file.getvalue()}
            response = requests.post("http://localhost:8000/classify-requirements/", files={"file": uploaded_file})
            data = response.json()

            if "results" in data:
                st.success("Classification complete ✅")
                for item in data["results"]:
                    st.markdown(f"""
                        <div style="padding:10px; margin-bottom:5px; border-radius:5px; background-color:#f0f2f6;">
                            <strong>{item['category']}</strong>: {item['text']}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Failed to classify. Check your PDF or backend.")

        except Exception as e:
            st.error(f"Error: {e}")
