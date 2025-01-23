import pandas as pd
import streamlit as st
import altair as alt
from src.firestore.user import UserDoc
from src.session.user import UserSession


def calculate_jobs_by_month(jobs):
    jobs_by_month = {}

    for job in jobs:
        date = job["creation_time"].split(" ")[0]
        month = "-".join(date.split("-")[:2])
        if month not in jobs_by_month:
            jobs_by_month[month] = 0

        jobs_by_month[month] += 1

    jobs_by_month_df = pd.DataFrame(list(jobs_by_month.items()), columns=["Month", "Jobs Tracked"])
    jobs_by_month_df = jobs_by_month_df.sort_values(by='Month').reset_index(drop=True)

    return jobs_by_month_df

def calculate_jobs_by_day(jobs):
    jobs_by_day = {}

    for job in jobs:
        date = job["creation_time"].split(" ")[0]
        if date not in jobs_by_day:
            jobs_by_day[date] = 0

        jobs_by_day[date] += 1

    jobs_by_month_df = pd.DataFrame(list(jobs_by_day.items()), columns=["Date", "Jobs Tracked"])
    jobs_by_month_df = jobs_by_month_df.sort_values(by='Date').reset_index(drop=True)

    return jobs_by_month_df


def create_job_report_per_month(jobs):

    jobs_by_month = calculate_jobs_by_month(jobs)

    st.markdown("### Jobs Tracked per Month")

    y_min = jobs_by_month['Jobs Tracked'].min() - 1
    y_max = jobs_by_month['Jobs Tracked'].max() + 1

    chart = alt.Chart(jobs_by_month).mark_line().encode(
        x="Month",
        y=alt.Y('Jobs Tracked', scale=alt.Scale(domain=[y_min, y_max]))
    ).interactive()

    st.altair_chart(chart, use_container_width=True, theme="streamlit")

    st.divider()

    st.dataframe(jobs_by_month, hide_index=True, use_container_width=True)


def create_job_report_per_day(jobs):

    jobs_by_day = calculate_jobs_by_day(jobs)

    st.markdown("### Jobs Tracked per Day")

    y_min = jobs_by_day['Jobs Tracked'].min() - 1
    y_max = jobs_by_day['Jobs Tracked'].max() + 1

    chart = alt.Chart(jobs_by_day).mark_line().encode(
        x="Date",
        y=alt.Y('Jobs Tracked', scale=alt.Scale(domain=[y_min, y_max]))
    ).interactive()

    st.altair_chart(chart, use_container_width=True, theme="streamlit")

    st.divider()

    st.dataframe(jobs_by_day, hide_index=True, use_container_width=True)


def create_job_report(user_doc: UserDoc, user_session: UserSession, applied: bool, key_prefix: str):
    jobs = list(user_doc.get_user_jobs(applied=applied))

    create_job_report_per_month(jobs)
    create_job_report_per_day(jobs)
