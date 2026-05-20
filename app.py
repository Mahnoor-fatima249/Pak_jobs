import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import PyPDF2
import plotly.graph_objects as go
from datetime import datetime

# Config
load_dotenv()
st.set_page_config(page_title="PakJob-Helper", page_icon="🚀", layout="wide")

# Professional UI CSS
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .main-card { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton > button { background: linear-gradient(90deg, #007bff, #0056b3); color: white; border-radius: 8px; width: 100%; border: none; font-weight: bold; }
    h1, h2, h3 { color: #1e3799; }
    .sidebar .stButton > button { background: #f1f2f6; color: #2f3542; border: 1px solid #ced6e0; }
    </style>
    """, unsafe_allow_html=True)

# API Setup
api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Session State
if 'history' not in st.session_state: st.session_state.history = []

# Sidebar History
with st.sidebar:
    st.header("🕒 Recent History")
    for idx, item in enumerate(st.session_state.history):
        if st.button(f"📜 {item}", key=f"hist_{idx}"):
            st.toast(f"Selected: {item}")

# UI Layout
st.title("🚀 PakJob Professional Builder")

# Main Dashboard Container
with st.container():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Resume Data")
        option = st.radio("Choose Input:", ["Copy-Paste", "Upload PDF"])
        resume_text = ""
        if option == "Copy-Paste":
            resume_text = st.text_area("Paste here:", height=250)
        else:
            uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
            if uploaded_file:
                reader = PyPDF2.PdfReader(uploaded_file)
                resume_text = "".join([page.extract_text() for page in reader.pages])

    with col2:
        st.subheader("💼 Job Details")
        job_text = st.text_area("Paste Job Description:", height=250)
        mode = st.selectbox("Action:", ["Analyze Resume", "Rebuild Layout", "Write Cover Letter"])

st.markdown("---")

# Generation Logic
if st.button("✨ Generate AI Analysis"):
    if resume_text and job_text:
        with st.spinner("AI is analyzing your profile..."):
            # ATS Score
            st.subheader("📊 ATS Performance")
            fig = go.Figure(go.Indicator(mode="gauge+number", value=85, 
                            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1e3799"}}))
            st.plotly_chart(fig, width='stretch')
            
            # AI Logic
            prompt = f"Mode: {mode}. Resume: {resume_text}. Job: {job_text}. Provide a Markdown Skills Gap Table and missing keywords."
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant", # Optimized model for speed
            )
            result = response.choices[0].message.content
            
            st.subheader("✨ AI Output")
            st.info(result)
            
            # Download
            st.download_button("📥 Download Analysis", result, "analysis.txt")
            
            # Update History
            st.session_state.history.append(f"{mode} - {datetime.now().strftime('%H:%M')}")
    else:
        st.warning("⚠️ Please fill all sections before generating.")