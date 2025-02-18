import streamlit as st
from src.firestore.user import UserDoc


def display_user_definitions_in_columns_using_user_doc(user_doc: UserDoc):
    st.markdown("## Currently Tracked")
    display_user_definitions_in_columns(user_doc.define_you.get_tracked_define_you_definitions())
    st.divider()
    st.markdown("## Historical")
    display_user_definitions_in_columns(user_doc.define_you.get_historical_define_you_definitions())

def display_user_definitions_in_columns(habits):
    cols = st.columns(1)
    for i, habit in enumerate(habits):
        col = cols[i % len(cols)]
        col.markdown(
            f"""
                                    <div style="background-color: #FFA500; padding: 10px; margin: 5px; margin-bottom: 20px; margin-top: 20px; border-radius: 10px; text-align: center;">
                                        {habit}
                                    </div>
                                    """,
            unsafe_allow_html=True,
        )