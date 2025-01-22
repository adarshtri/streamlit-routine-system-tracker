from streamlit_cookies_controller import CookieController
import streamlit as st
from src.crypto.aes import encrypt, decrypt
from datetime import datetime, timedelta


def get_current_user(cookie_controller: CookieController = None):
    if not cookie_controller:
        cookie_controller = st.session_state["cookie_controller"]
    encrypted_user = cookie_controller.get("logged_in_user")

    if encrypted_user and type(encrypted_user) is str:
        return decrypt(encrypted_user)
    return encrypted_user

def is_a_user_logged_in(cookie_controller: CookieController = None):
    if not cookie_controller:
        cookie_controller = st.session_state["cookie_controller"]
    return not cookie_controller.get("logged_in_user") is None


def delete_user(cookie_controller: CookieController = None):
    if not cookie_controller:
        cookie_controller = st.session_state["cookie_controller"]
    cookie_controller.remove("logged_in_user")

def save_user(username: str, cookie_controller: CookieController = None):
    if not cookie_controller:
        cookie_controller = st.session_state["cookie_controller"]

    encrypted_user_name = encrypt(username)
    cookie_controller.set("logged_in_user", encrypted_user_name, expires=datetime.now() + timedelta(days=3))