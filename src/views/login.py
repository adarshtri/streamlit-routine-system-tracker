import streamlit as st
from streamlit_cookies_controller import CookieController

from src.cookies.user_cookies import get_current_user, is_a_user_logged_in, delete_user, save_user
from src.firestore.user import UserDoc
from src.secrets.users import user_allowed
from src.session.user import UserSession
from datetime import datetime, timedelta


if is_a_user_logged_in():
    st.title("Account")
    st.write(f"User {get_current_user()} logged in!")

    # Submit button
    if st.button("Logout"):
        delete_user()
        st.success("You are logged out.")
        st.rerun()
else:
    st.title("Login")
    # Username input
    username = st.text_input("Username", placeholder="Enter your username")

    # Password input
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    st.write("Are you a guest? Use these credentials to test out this app. Username: **guest** Password: **guest**")

    # Submit button
    if st.button("Login"):
        # TODO: Add backend authentication logic here
        if username and password:
            if user_allowed(username, password):
                cookie_controller = CookieController()
                expiry_date = datetime.now() + timedelta(seconds=30)

                save_user(username)

                st.success("Login successful.")
                save_user(username)
                user_doc = UserDoc(username)
                user_session = UserSession(username)
                st.session_state["user_doc"] = user_doc
                st.session_state["user_session"] = user_session
                st.rerun()
            else:
                st.error("Invalid user credentials.")
        else:
            st.error("Please enter both username and password.")
