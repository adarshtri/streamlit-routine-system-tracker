import streamlit as st
from src.firestore.user import UserDoc
from src.session.user import UserSession


def report_all(user_doc: UserDoc, user_session: UserSession, definitions):
    st.write(definitions)