from functools import partial
import streamlit as st
from src.firestore.user import UserDoc
from datetime import date, timedelta


def log_weight_input_date_change_call(user_doc: UserDoc):
    input_date = st.session_state["weight_log_input_date"]
    st.session_state["weight_log_input_date_string"] = input_date.strftime("%Y-%m-%d")
    st.session_state["weight_log_input_date_data"] = user_doc.get_weight_for_date(st.session_state["weight_log_input_date_string"])

def log_weight(user_doc: UserDoc):

    weight_log_date = st.date_input(
        "Enter the date (YYYY-MM-DD)",
        key="weight_log_input_date",
        format="YYYY-MM-DD",
        on_change=partial(log_weight_input_date_change_call, user_doc),
        min_value=date.today() - timedelta(days=2),
        max_value=date.today()
    )

    weight = 0.0

    if "weight_log_input_date_data" in st.session_state:
        weight = st.session_state["weight_log_input_date_data"]

    weight_input_message = "Enter your weight in kilograms..."

    if weight != 0.0:
        weight_input_message = "Update your weight in kilograms..."

    weight_input = st.number_input(
        weight_input_message,
        value=weight,
        min_value=0.0,
        max_value=500.0
    )

    if st.button("Submit", key="weight_log_submit_button"):
        user_doc.track_weight(weight_log_date, weight_input)
        st.success(f"Weight logged successfully for {weight_input}!")
        st.balloons()