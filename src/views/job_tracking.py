import streamlit as st
from src.views.jobs.add_job import add_job
from src.views.jobs.company_based_job_report import create_company_based_job_report
from src.views.jobs.time_based_job_report import create_time_based_job_report
from src.views.jobs.show_jobs import show_jobs

st.header(f"Welcome to your Job Tracker")

user_doc = st.session_state["user_doc"]
user_session = st.session_state["user_session"]

# Define tabs
tabs = st.tabs(["Add Jobs", "Pending Jobs", "Applied Jobs", "Job Report by Time", "Job Report by Company"])

with tabs[0]:
    add_job(user_doc, user_session)

with tabs[1]:
    show_jobs(user_doc, user_session, False, "pending_jobs")

with tabs[2]:
    show_jobs(user_doc, user_session, True, "applied_jobs")

with tabs[3]:
    create_time_based_job_report(user_doc, user_session, "job_report")

with tabs[4]:
    create_company_based_job_report(user_doc)