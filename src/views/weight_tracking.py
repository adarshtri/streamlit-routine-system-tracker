import streamlit as st
from src.sqlite.credentials import get_current_user
from src.views.weight.log_weight import log_weight
from src.views.weight.weight_journey import show_weight_journey_graph

current_user = get_current_user()

st.header(f"Welcome to your Job Tracker - {current_user}")

user_doc = st.session_state["user_doc"]
user_session = st.session_state["user_session"]

# Define tabs
tabs = st.tabs(["Log Weight", "Weight Journey"])

with tabs[0]:
    log_weight(user_doc)

with tabs[1]:
    show_weight_journey_graph(user_doc)
