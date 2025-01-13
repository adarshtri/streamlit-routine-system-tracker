import streamlit as st
from src.sqlite.credentials import get_current_user
from src.views.jobs.add_job import add_job
from src.views.jobs.show_jobs import show_jobs

current_user = get_current_user()

st.header(f"Welcome to your Job Tracker - {current_user}")

user_doc = st.session_state["user_doc"]
user_session = st.session_state["user_session"]

# Define tabs
tabs = st.tabs(["Add Jobs", "Pending Jobs", "Applied Jobs", "Job Report"])

with tabs[0]:
    add_job(user_doc, user_session)

with tabs[1]:
    show_jobs(user_doc, user_session, False, "pending_jobs")

with tabs[2]:
    show_jobs(user_doc, user_session, True, "applied_jobs")

with tabs[3]:
    show_jobs(user_doc, user_session, True, "job_report")
