import pandas as pd
import altair as alt
import streamlit as st
from src.firestore.user import UserDoc


all_option = "All"

def get_unique_years(jobs):

    years = set()

    for job in jobs:
        year = job["creation_time"].split(" ")[0].split("-")[0]
        years.add(year)

    return list(years)


def get_unique_companies(jobs):

    companies = set()

    for job in jobs:
        company_name = job["company_name"]
        companies.add(company_name)

    return list(companies)

def filter_by_applied(jobs, applied):
    return list(filter(lambda x: x["applied"] == applied, jobs))

def filter_by_company(jobs, selected_company):

    if selected_company == all_option:
        return jobs

    return list(filter(lambda x: x["company_name"] == selected_company, jobs))

def filter_by_creation_time(jobs, year):

    if year == all_option:
        return jobs

    time = year

    return list(filter(lambda x: x["creation_time"].startswith(time), jobs))

def created_count(jobs, selected_company, year):

    if selected_company == all_option:
        return len(filter_by_creation_time(jobs, year))

    filtered_by_company = filter_by_company(jobs, selected_company)
    filtered_by_time = filter_by_creation_time(filtered_by_company, year)

    return len(filtered_by_time)

def applied_count(jobs, selected_company, year):

    filtered_by_applied = filter_by_applied(jobs, True)
    filtered_by_time = filter_by_creation_time(filtered_by_applied, year)

    if selected_company == all_option:
        return len(filtered_by_time)

    filtered_by_applied = filter_by_applied(jobs, True)
    filtered_by_time = filter_by_creation_time(filtered_by_applied, year)
    filtered_by_company = filter_by_company(filtered_by_time, selected_company)


    return len(filtered_by_company)

def create_company_wise_applied_report(jobs, year):
    filtered_by_applied = filter_by_applied(jobs, True)
    filtered_by_time = filter_by_creation_time(filtered_by_applied, year)

    company_wise_count = {}

    for job in filtered_by_time:

        company_name = job["company_name"]

        if company_name not in company_wise_count:
            company_wise_count[company_name] = 0

        company_wise_count[company_name] += 1

    df = pd.DataFrame(company_wise_count.items(), columns=("Company Name", "Count"))

    st.markdown(f"### Applied jobs by Company for {year}")

    y_min = df['Count'].min() - 1
    y_max = df['Count'].max() + 1

    chart = alt.Chart(df).mark_line().encode(
        x="Company Name",
        y=alt.Y('Count', scale=alt.Scale(domain=[y_min, y_max]))
    ).interactive()

    st.altair_chart(chart, use_container_width=True, theme="streamlit")

    st.dataframe(df, hide_index=True, use_container_width=True)


def create_company_wise_report(jobs, year):

    # tracked DF

    filtered_by_time_tracked = filter_by_creation_time(jobs, year)

    company_wise_count_tracked = {}

    for job in filtered_by_time_tracked:

        company_name = job["company_name"]

        if company_name not in company_wise_count_tracked:
            company_wise_count_tracked[company_name] = 0

        company_wise_count_tracked[company_name] += 1

    df_tracked = pd.DataFrame(company_wise_count_tracked.items(), columns=("Company Name", "Tracked Count"))

    # applied df

    filtered_by_applied = filter_by_applied(jobs, True)
    filtered_by_time_applied = filter_by_creation_time(filtered_by_applied, year)

    company_wise_count_applied = {}

    for job in filtered_by_time_applied:

        company_name = job["company_name"]

        if company_name not in company_wise_count_applied:
            company_wise_count_applied[company_name] = 0

        company_wise_count_applied[company_name] += 1

    df_applied = pd.DataFrame(company_wise_count_applied.items(), columns=("Company Name", "Applied Count"))

    df_merged = pd.merge(df_tracked, df_applied, on='Company Name', how='outer').fillna(0)



    st.markdown(f"### Tracking by Company for {year}")


    st.line_chart(df_merged, x = "Company Name", y = ["Applied Count", "Tracked Count"], x_label="Company Name", y_label="Tracked vs Applied Count", use_container_width=True)

    st.dataframe(df_merged, hide_index=True, use_container_width=True)

def create_company_based_job_report(user_doc: UserDoc):

    jobs = list(user_doc.get_user_jobs())

    years_options = [all_option] + get_unique_years(jobs)
    company_options = [all_option] + get_unique_companies(jobs)

    selection_company_option = st.selectbox("Filter by Company", company_options, index=0)
    selection_year = st.selectbox("Filter by Year", years_options, index=0)

    col1, col2 = st.columns(2)

    col1.metric("Tracked", created_count(jobs, selection_company_option, selection_year), border=True)
    col2.metric("Applied", applied_count(jobs, selection_company_option, selection_year), border=True)

    st.divider()
    create_company_wise_report(jobs, selection_year)
