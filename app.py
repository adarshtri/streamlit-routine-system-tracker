import streamlit as st

from src.firestore.user import UserDoc
from src.session.user import UserSession
from src.sqlite.credentials import get_current_user

current_user = get_current_user()

def setup_user(user):
    return UserDoc(user), UserSession(user)

user_doc, user_session = setup_user(current_user)

st.session_state["user_doc"] = user_doc
st.session_state["user_session"] = user_session

login_page = st.Page("src/views/login.py", url_path="login", title="Login")
habits_page = st.Page("src/views/habits.py", url_path="habits", title="Habit Tracker")
job_tracking = st.Page("src/views/job_tracking.py", url_path="job_tracking", title="Job Tracking")
weight_tracking = st.Page("src/views/weight_tracking.py", url_path="weight_tracking", title="Weight Tracking")

pg = st.navigation([login_page, habits_page, job_tracking, weight_tracking])
pg.run()