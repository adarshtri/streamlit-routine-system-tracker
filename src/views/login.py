import streamlit as st

from src.secrets.users import user_allowed
from src.sqlite.credentials import is_a_user_logged_in, get_current_user, save_user, delete_user

st.title("Login")

if is_a_user_logged_in():
    st.write(f"User {get_current_user()} already logged in!")

    # Submit button
    if st.button("Logout"):
        if is_a_user_logged_in():
            delete_user(get_current_user())
            st.success("You are logged out.")
            st.switch_page("src/views/login.py")

else:
    # Username input
    username = st.text_input("Username", placeholder="Enter your username")

    # Password input
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    # Submit button
    if st.button("Login"):
        # TODO: Add backend authentication logic here
        if username and password:
            if user_allowed(username, password):
                st.success("Login successful.")
                save_user(username)
                st.switch_page("src/views/habits.py")
            else:
                st.error("Invalid user credentials.")
        else:
            st.error("Please enter both username and password.")
