import streamlit as st

from src.firestore.user import UserDoc
from src.session.user import UserSession


def show_track_habit_popover(user_doc: UserDoc, user_session: UserSession, input_date):
    with st.popover("Submit Tracking"):
        existing_habit_tracking_for_date = user_doc.get_tracking_for_a_date(input_date)
        if existing_habit_tracking_for_date:

