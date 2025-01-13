import streamlit as st
from src.firestore.user import UserDoc, create_hash
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

    for job in jobs:
        key = f"{key_prefix}_{user_doc.username}_{create_hash(job['job_url'])}"
        applied_icon = "❌"
        if job["applied"]:
            applied_icon = "✅"
        with st.expander(f"{job['role_name']}: {applied_icon}"):
            st.write(f"Job URL: {job['job_url']}")
            st.write(f"Company Name: {job['company_name']}")
            st.write(f"Role Name: {job['role_name']}")

            if not applied:
                if st.button("🗑", key=f"{key}_untrack_job_button"):
                    user_doc.untrack_job(job)
                    st.success("Job successfully removed from tracking.")
                    st.rerun()

                applied_button_text = "Change to Applied"

                if job["applied"]:
                    applied_button_text = "Change to Unapply"

                if st.button(applied_button_text, key=f'{key}_toogle_apply_button'):
                    job["applied"] = not job["applied"]
                    user_doc.toggle_apply_job(job)
                    st.rerun()

        st.divider()