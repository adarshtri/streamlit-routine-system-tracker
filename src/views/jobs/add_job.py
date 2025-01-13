import streamlit as st
from src.firestore.user import UserDoc
from src.session.user import UserSession
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        # Check if the scheme and network location (domain) are valid
        return bool(parsed.scheme) and bool(parsed.netloc)
    except Exception:
        return False

def add_job(user_doc: UserDoc, user_sesion: UserSession):
    job_url = st.text_input("Job Url...")
    company = st.text_input("Company Name...")
    role_name = st.text_input("Role Name...")

    if st.button("Submit Job", key="add_job_tracking_submit_button") and job_url and company and role_name:
        if is_valid_url(job_url):
            add_status = user_doc.add_job_tracking(job_url, company, role_name)

            if add_status:
                st.rerun()
            else:
                st.error("Job already tracked.")
        else:
            st.error("Invalid URL")
