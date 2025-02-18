import streamlit as st

from src.firestore.user import UserDoc
from src.session.user import UserSession
from src.views.habits.show_habits import display_user_habits_in_columns


def create_habits(user_doc: UserDoc, user_session: UserSession):

    st.write("Add your habits to track:")

    # Input for a new habit
    new_habit = st.text_input("Enter a habit", key="habit_input")

    # Button to add the habit to the list
    if st.button("Add Habit"):
        if new_habit:
            user_session.add_new_habit(new_habit)
        else:
            st.warning("Please enter a habit.")

    # Display current list of habits using a better UI element
    if user_session.has_habits():
        st.write("### Current habits to track:")
        display_user_habits_in_columns(st.session_state[user_session.habit_session_state_key])
    else:
        st.info("No habits added yet.")

    # Submit button to save habits to Firestore
    if st.button("Submit Habits"):
        if user_session.has_habits():
            # Update the 'habits' field in Firestore
            user_doc.update_habits(user_session.get_habits())
            # Clear user session tracking habits
            user_session.reset_habits()

            st.switch_page("src/views/habits.py")
        else:
            st.warning("No habits to submit.")
