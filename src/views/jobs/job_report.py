import pandas as pd
import streamlit as st
import altair as alt
from src.firestore.user import UserDoc
from src.session.user import UserSession

lifetime_value = 100000

def calculate_jobs_by_month(jobs):
    jobs_by_month = {}

    for job in jobs:
        date = job["creation_time"].split(" ")[0]
        month = "-".join(date.split("-")[:2])
        if month not in jobs_by_month:
            jobs_by_month[month] = 0

        jobs_by_month[month] += 1

    jobs_by_month_df = pd.DataFrame(list(jobs_by_month.items()), columns=["Month", "Count"])
    jobs_by_month_df = jobs_by_month_df.sort_values(by='Month').reset_index(drop=True)

    return jobs_by_month_df

def calculate_jobs_by_day(jobs):
    jobs_by_day = {}

    for job in jobs:
        date = job["creation_time"].split(" ")[0]
        if date not in jobs_by_day:
            jobs_by_day[date] = 0

        jobs_by_day[date] += 1

    jobs_by_month_df = pd.DataFrame(list(jobs_by_day.items()), columns=["Date", "Count"])
    jobs_by_month_df = jobs_by_month_df.sort_values(by='Date').reset_index(drop=True)

    return jobs_by_month_df


def create_job_report_per_month(jobs, report_for):

    jobs_by_month = calculate_jobs_by_month(jobs)

    st.markdown(f"### Jobs {report_for} per Month")

    y_min = jobs_by_month['Count'].min() - 1
    y_max = jobs_by_month['Count'].max() + 1

    chart = alt.Chart(jobs_by_month).mark_line().encode(
        x="Month",
        y=alt.Y('Count', scale=alt.Scale(domain=[y_min, y_max]))
    ).interactive()

    st.altair_chart(chart, use_container_width=True, theme="streamlit")

    st.divider()

    st.dataframe(jobs_by_month, hide_index=True, use_container_width=True)


def create_job_report_per_day(jobs, report_for):

    jobs_by_day = calculate_jobs_by_day(jobs)

    st.markdown(f"### Jobs {report_for} per Day")

    y_min = jobs_by_day['Count'].min() - 1
    y_max = jobs_by_day['Count'].max() + 1

    chart = alt.Chart(jobs_by_day).mark_line().encode(
        x="Date",
        y=alt.Y('Count', scale=alt.Scale(domain=[y_min, y_max]))
    ).interactive()

    st.altair_chart(chart, use_container_width=True, theme="streamlit")

    st.divider()

    st.dataframe(jobs_by_day, hide_index=True, use_container_width=True)


def create_job_report(user_doc: UserDoc, user_session: UserSession, key_prefix: str):

    jobs = list(user_doc.get_user_jobs())
    jobs_applied = list(user_doc.get_user_jobs(applied=True))

    time_frame_options = {
        "By Month": "m",
        "By Date": "d",
    }

    selection_time_frame_option = st.selectbox('Timeframe', time_frame_options)
    selected_time_frame_value = time_frame_options[selection_time_frame_option]


    if selected_time_frame_value == 'm':
        create_job_report_per_month(jobs, "Tracked")
        create_job_report_per_month(jobs_applied, "Applied")
    elif selected_time_frame_value == 'd':
        create_job_report_per_day(jobs, "Tracked")
        create_job_report_per_day(jobs_applied, "Applied")
    else:
        st.markdown("#### You have selected invalid time frame for job report.")
