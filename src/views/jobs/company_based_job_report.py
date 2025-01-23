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

def filter_by_creation_time(jobs, year, month = None):

    time = year

    if month:
        time = time + "-" + month

    return list(filter(lambda x: x["creation_time"].startswith(time), jobs))

def created_count(jobs, selected_company, year):

    if selected_company == all_option:
        return len(jobs)

    filtered_by_company = filter_by_company(jobs, selected_company)
    filtered_by_time = filter_by_creation_time(filtered_by_company, year)

    return len(filtered_by_time)

def applied_count(jobs, selected_company, year):

    if selected_company == all_option:
        return len(list(filter(lambda x: x["applied"] == True, jobs)))

    filtered_by_applied = filter_by_applied(jobs, True)
    filtered_by_company = filter_by_company(filtered_by_applied, selected_company)
    filtered_by_time = filter_by_creation_time(filtered_by_company, year)

    return len(list(filter(lambda x: x["company_name"] == selected_company and x["applied"] == True, jobs)))

def create_company_based_job_report(user_doc: UserDoc):

    jobs = list(user_doc.get_user_jobs())

    years_options = [all_option] + get_unique_years(jobs)
    company_options = [all_option] + get_unique_companies(jobs)

    selection_company_option = st.selectbox("Filter by Company", company_options, index=0)
    selection_year = st.selectbox("Filter by Year", years_options, index=0)

    col1, col2 = st.columns(2)

    col1.metric("Tracked", created_count(jobs, selection_company_option, selection_year), border=True)
    col2.metric("Applied", applied_count(jobs, selection_company_option, selection_year), border=True)