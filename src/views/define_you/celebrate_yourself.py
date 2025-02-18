import streamlit as st
from src.firestore.user import UserDoc
from src.session.user import UserSession
import random

@st.dialog("You Celebration Info", width="large")
def show_celebration_dialog(user_doc: UserDoc, definition: str):
    st.write(f"\"{definition}\" celebration data...")

    celebration_data = user_doc.define_you.get_celebration_data(definition)

    if celebration_data:
        for data in celebration_data:
            st.write(data)
            st.write("\n")
    else:
        st.write("No celebration data available.")



def celebrate(user_doc: UserDoc, user_session: UserSession):

    st.write("## Lets Celebrate You!")

    st.divider()

    tracked_definitions = user_doc.define_you.get_tracked_define_you_definitions()

    for definition in tracked_definitions:

        columns = st.columns(3)

        columns[0].markdown(
            f"""
                                            <div style="background-color: #FFA500; padding: 10px; margin: 5px; margin-bottom: 20px; margin-top: 0px; border-radius: 10px; text-align: center;">
                                                {definition}
                                            </div>
                                            """,
            unsafe_allow_html=True,
        )

        if columns[1].button("Celebrate", key=f"{user_doc.username}_celebrate_tracked_{definition}"):
            user_doc.define_you.celebrate(definition)
            st.toast("Hurray")
            effect = random.choice([st.snow, st.balloons])  # Randomly pick one
            effect()

        if columns[2].button("Show Celebrations", key=f"{user_doc.username}_show_celebrations_{definition}"):
            show_celebration_dialog(user_doc, definition)