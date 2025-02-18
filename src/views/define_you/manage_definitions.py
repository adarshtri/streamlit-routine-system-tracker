import streamlit as st

from src.firestore.user import UserDoc
from src.session.user import UserSession


def show_definitions_with_delete_buttons(user_doc: UserDoc):

    tracked_definitions = user_doc.define_you.get_tracked_define_you_definitions()

    for definition in tracked_definitions:
        cols = st.columns(2)

        cols[0].write(definition)

        if cols[1].button("Remove", key=f"{user_doc.username}_tracked_{definition}_remove_button"):
            user_doc.define_you.remove_definition(definition)
            st.rerun()


def show_historical_definitions_with_add_back_buttons(user_doc: UserDoc):

    tracked_definitions = user_doc.define_you.get_historical_define_you_definitions()

    for definition in tracked_definitions:
        cols = st.columns(2)

        cols[0].write(definition)

        if cols[1].button("Re-track", key=f"{user_doc.username}_re_tracked_{definition}_remove_button"):
            user_doc.define_you.add_definition(definition)
            st.rerun()


def manage(user_doc: UserDoc, user_session: UserSession):

    st.write("## New Definition")

    new_definition = st.text_input("Enter a new definition about yourself", None)

    if st.button("Add Definition"):

        if not new_definition:
            st.warning("Provide a new definition before submitting.")
        else:
            with st.spinner("Adding..."):
                user_doc.define_you.add_definition(new_definition)
                st.success("Definition added.")

    st.divider()

    st.write("## Manage Current Definitions")
    show_definitions_with_delete_buttons(user_doc)

    st.divider()

    st.write("## Manage Previously Tracked Definitions")
    show_historical_definitions_with_add_back_buttons(user_doc)