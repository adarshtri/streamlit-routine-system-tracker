import streamlit as st
from matplotlib.pyplot import title

from src.cookies.user_cookies import get_current_user
from src.firestore.user import UserDoc
from src.session.user import UserSession
from streamlit_cookies_controller import CookieController

cookie_controller = CookieController()

st.session_state["cookie_controller"] = cookie_controller

current_user = get_current_user()

def setup_user(user):
    return UserDoc(user), UserSession(user)

user_doc, user_session = setup_user(current_user)

st.session_state["user_doc"] = user_doc
st.session_state["user_session"] = user_session

if current_user is None:
    cookie_controller.set("user_logged_in", False)
    login_page = st.Page("src/views/login.py", url_path="login", title="Login")
    pg = st.navigation([login_page])
else:
    login_page = st.Page("src/views/login.py", url_path="account", title="Account")
    habits_page = st.Page("src/views/habits.py", url_path="habits", title="Habit Tracker")
    job_tracking = st.Page("src/views/job_tracking.py", url_path="job_tracking", title="Job Tracker")
    weight_tracking = st.Page("src/views/weight_tracking.py", url_path="weight_tracking", title="Weight Tracker")
    personality_builder = st.Page("src/views/define_you.py", url_path="define_you", title="Define You!")
    pg = st.navigation([login_page, habits_page, job_tracking, weight_tracking, personality_builder])

pg.run()