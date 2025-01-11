import streamlit as st

login_page = st.Page("src/views/login.py", url_path="login", title="Login")
habits_page = st.Page("src/views/habits.py", url_path="habits", title="Habit Tracker")

pg = st.navigation([login_page, habits_page])
pg.run()