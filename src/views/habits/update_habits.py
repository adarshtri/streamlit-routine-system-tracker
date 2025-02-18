from src.firestore.user import UserDoc
from src.session.user import UserSession
import streamlit as st


def update_habits(user_doc: UserDoc, user_session: UserSession):
    st.header("Update Habits")

    if not user_session.get_synced_from_server_for_update_status():
        user_session.initialize_user_session_habit(user_doc.get_habits())
        user_session.set_synced_from_server_for_update()

    habits = user_session.get_habits()

    st.write("### Current habits:")

    # Display existing habits with delete options (not applied yet)
    for habit in habits:
        col1, col2 = st.columns([4, 1])
        col1.write(f"- {habit}")
        if col2.button(f"Delete {habit}", key=f"delete_{habit}"):
            print(f"\nDeleting {habit}.......")
            user_session.remove_habit(habit)
            print(user_session.get_habits())
            st.switch_page("src/views/habits.py")

    # Add new habits (not applied yet)
    new_habit = st.text_input("Enter a new habit to add:")
    if st.button("Add New Habit"):
        if new_habit:
            user_session.add_new_habit(new_habit)
            st.switch_page("src/views/habits.py")
        elif not new_habit:
            st.error("Please enter a habit name.")

    # Submit button for confirmation
    with st.popover("Ready to submit changes?"):
        if st.button("Submit Changes"):
            user_doc.update_habits(user_session.get_habits())
            user_session.reset_synced_from_server_for_update()
            user_session.initialize_user_session_habit(user_doc.get_habits())
            st.balloons()
            st.switch_page("src/views/habits.py")
