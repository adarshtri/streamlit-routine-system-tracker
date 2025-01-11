import streamlit as st

from src.firestore.user import UserDoc

def display_user_habits_in_columns_using_user_doc(user_doc: UserDoc):
    display_user_habits_in_columns(user_doc.get_habits())

def display_user_habits_in_columns(habits):
    cols = st.columns(3)  # Adjust the number of columns as needed
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