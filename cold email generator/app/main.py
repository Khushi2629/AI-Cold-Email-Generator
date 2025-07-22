import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

import streamlit as st

def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(page_title="Cold Email Generator", page_icon="📨", layout="centered")

    # ✅ Inject working CSS with colorful animated background
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

        html, body, .stApp {
            font-family: 'Inter', sans-serif;
            height: 100%;
            margin: 0;
            padding: 0;
        }

        .stApp {
            background: linear-gradient(135deg, #f6d365, #fda085, #84fab0, #8fd3f4, #fccb90);
            background-size: 500% 500%;
            animation: gradientBG 25s ease infinite;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .block-container {
            background: rgba(255, 255, 255, 0.85);
            padding: 2rem 3rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            backdrop-filter: blur(10px);
            margin-top: 50px;
        }

        .stTextInput input {
            padding: 10px;
            border-radius: 12px;
            border: 1px solid #ccc;
        }

        .stButton button {
            background-color: #1f2937;
            color: #fff;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .stButton button:hover {
            background-color: #111827;
        }

        .stCodeBlock {
            border-radius: 12px !important;
            background-color: #f9fafb !important;
            color: #111827;
            font-size: 14px;
        }

        h1, h2, h3, h4 {
            color: #1f2937;
        }

        </style>
    """, unsafe_allow_html=True)

    # UI content
    st.markdown("## 📨 Generate your Cold Email")
    st.markdown("Craft professional cold emails tailored to job listings with a single click.")

    # URL input
    with st.expander("🔗 Paste Job Listing URL", expanded=True):
        url_input = st.text_input("Enter job URL")
        submit_button = st.button("🎯 Generate Email")

    # Email generation logic
    if submit_button:
        with st.status("⏳ Processing job listing...", expanded=True) as status:
            try:
                loader = WebBaseLoader([url_input])
                raw_data = loader.load().pop().page_content
                data = clean_text(raw_data)

                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                if not jobs:
                    st.warning("⚠️ No jobs found at the given URL.")
                    return

                for i, job in enumerate(jobs, 1):
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)

                    with st.container():
                        st.markdown(f"#### ✉️ Email #{i}")
                        st.code(email, language='markdown')

                status.update(label="✅ Done generating!", state="complete")

            except Exception as e:
                status.update(label="❌ Error", state="error")
                st.error(f"An error occurred: {e}")




if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

