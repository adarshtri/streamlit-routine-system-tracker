import streamlit as st
from src.views.define_you.about import about
from src.views.define_you.celebrate_yourself import celebrate
from src.views.define_you.manage_definitions import manage

user_doc = st.session_state["user_doc"]
user_session = st.session_state["user_session"]

tabs = st.tabs(["About Define You", "Define Yourself", "Celebrate Yourself", "Progress"])

with tabs[0]:
    about(user_doc, user_session)
with tabs[1]:
    manage(user_doc, user_session)
with tabs[2]:
    celebrate(user_doc, user_session)
with tabs[3]:
    pass

