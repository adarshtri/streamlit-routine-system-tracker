import streamlit as st

from src.views.habits.report.habit_report import create_habit_reports
from src.views.users.create_habit import create_habits
from src.views.users.show_habits import display_user_habits_in_columns_using_user_doc
from src.views.users.track_habits import track_habits
from src.views.users.update_habits import update_habits

st.header(f"Welcome to your Habit Tracker")

user_doc = st.session_state["user_doc"]
user_session = st.session_state["user_session"]

# Define tabs
tabs = st.tabs(["Manage Habits", "Track Habits", "Update Habits", "Habit Reports"])

with tabs[0]:
    if user_doc.has_habits_defined():
        st.write("### Tracking following habits:")
        display_user_habits_in_columns_using_user_doc(user_doc)
    else:
        create_habits(user_doc,user_session)

with tabs[1]:
    track_habits(user_doc, user_session)

with tabs[2]:
    update_habits(user_doc, user_session)

with tabs[3]:
    create_habit_reports(user_doc, user_session)
