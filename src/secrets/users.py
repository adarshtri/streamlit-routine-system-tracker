import json
import streamlit as st

def user_allowed(username: str, password: str):
    user_creds = json.loads(st.secrets["supported_users"])
    return username in user_creds and user_creds[username] == password