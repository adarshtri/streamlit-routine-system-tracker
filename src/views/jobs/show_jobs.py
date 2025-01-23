import pandas as pd
import streamlit as st
from src.firestore.user import UserDoc, create_hash, get_current_datetime_utc
from src.session.user import UserSession


def show_jobs(user_doc: UserDoc, user_session: UserSession, applied: bool, key_prefix: str):
    jobs = list(user_doc.get_user_jobs(applied=applied))

    top_message = "Jobs with Pending Applications"

    if applied:
        top_message = "Jobs with Applications Completed"

    if len(jobs) == 0:
        st.markdown("## No jobs to show.")
        return

    st.markdown(f"## {top_message}")
    st.divider()

    group_by_company = {}

    for job in jobs:
        company_name = job["company_name"]

        if company_name not in group_by_company:
            group_by_company[company_name] = []

        group_by_company[company_name].append(job)

    for company_name in group_by_company:
        key = f"{key_prefix}_{user_doc.username}_{create_hash(company_name)}"

        applied_icon = "❌"
        if applied:
            applied_icon = "✅"

        with st.expander(f"{company_name}: {len(group_by_company[company_name])} {applied_icon}"):
            for job in group_by_company[company_name]:
                internal_key = f"{key_prefix}_{user_doc.username}_{create_hash(job['job_url'])}_1"
                with st.container():
                    st.write(f"Job URL: {job['job_url']}")
                    st.write(f"Company Name: {job['company_name']}")
                    st.write(f"Role Name: {job['role_name']}")

                    if applied:
                        st.write(f"Application Date: {job['applied_at'].split(' ')[0]}")

                    if not applied:
                        if st.button("🗑", key=f"{internal_key}_untrack_job_button"):
                            user_doc.untrack_job(job)
                            st.success("Job successfully removed from tracking.")
                            st.rerun()

                        applied_button_text = "Change to Applied"

                        if job["applied"]:
                            applied_button_text = "Change to Unapply"

                        if st.button(applied_button_text, key=f'{internal_key}_toogle_apply_button'):
                            job["applied"] = not job["applied"]
                            job["applied_at"] = get_current_datetime_utc()
                            user_doc.applied_to_job(job)
                            st.rerun()

                    st.divider()
        st.divider()