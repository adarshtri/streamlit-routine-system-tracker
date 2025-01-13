import streamlit as st
from src.firestore.user import UserDoc
from src.session.user import UserSession
from src.sqlite.credentials import get_current_user
from src.views.users.create_habit import create_habits
from src.views.users.show_habits import display_user_habits_in_columns_using_user_doc
from src.views.users.track_habits import track_habits
from src.views.users.update_habits import update_habits

current_user = get_current_user()

st.header(f"Welcome to your Habit Tracker - {current_user}")

user_doc = st.session_state["user_doc"]
user_session = st.session_state["user_session"]

# Define tabs
tabs = st.tabs(["Manage Habits", "Track Habits", "Update Habits"])

with tabs[0]:
    if user_doc.has_habits_defined():
        st.write("### Tracking following habits:")
        display_user_habits_in_columns_using_user_doc(user_doc)
    else:
        create_habits(user_doc,user_session)

with tabs[1]:
    track_habits(user_doc, user_session)

with tabs[2]:
    #user_session.reset_habits()
    update_habits(user_doc, user_session)
