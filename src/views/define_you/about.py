import streamlit as st

from src.firestore.user import UserDoc
from src.session.user import UserSession
from src.views.define_you.show_define_you_definitions import display_user_definitions_in_columns_using_user_doc


def about(user_doc: UserDoc, user_session: UserSession):
    st.title("Define You!")

    st.write(
        '''A personal echo chamber for positive reinforcement. 
        This tracker is about creating a space where the thoughts 
        I want to internalize—like 'I'm a great flyer'—are echoed back to me. 
        Just as social echo chambers reinforces beliefs through repetition, 
        this is a deliberate effort to shape my mindset in a way that supports confidence, 
        growth, and well-being.\n\n**I would like to take control of defining and feeling who I am.**
        '''
    )

    st.divider()

    display_user_definitions_in_columns_using_user_doc(user_doc)