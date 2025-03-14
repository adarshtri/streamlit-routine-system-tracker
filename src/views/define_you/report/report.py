import streamlit as st
from src.firestore.user import UserDoc
from src.session.user import UserSession


def generate_celebration_report(user_doc: UserDoc, user_session: UserSession):

    all_reporting_options = st.selectbox(
        "Select a reporting view",
        ("Daily Trends", "Detailed Report"),
    )

    if all_reporting_options == "Daily Trends":
        pass
    elif all_reporting_options == "Detailed Report":
        pass
    else:
        st.error(f"Reporting view \"{all_reporting_options}\" not supported.")

    tracked_definitions = user_doc.define_you.get_tracked_define_you_definitions()
    untracked_definitions = user_doc.define_you.get_historical_define_you_definitions()

