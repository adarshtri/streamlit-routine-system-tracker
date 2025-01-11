import streamlit as st
from src.firestore.user import UserDoc
from src.session.user import UserSession
from functools import partial


def tracking_habit_input_date_change_callback(user_doc: UserDoc):
    input_date = st.session_state["tracking_habit_date_input"]
    st.session_state["tracking_habit_date_input_string"] = input_date.strftime("%Y-%m-%d")
    input_date_tracking_data = user_doc.get_tracking_for_a_date(st.session_state["tracking_habit_date_input_string"])

    user_habits = user_doc.get_habits()
    habit_dict = {}
    if input_date_tracking_data:
        for habit in user_habits:
            if habit in input_date_tracking_data:
                habit_dict[habit] = input_date_tracking_data[habit]
            else:
                habit_dict[habit] = False

        st.session_state["tracking_habit_input_date_data"] = habit_dict
    else:
        habits = user_doc.get_habits()
        habits_dict = {}
        for habit in habits:
            habits_dict[habit] = False
        st.session_state["tracking_habit_input_date_data"] = habits_dict


def track_habits(user_doc: UserDoc, user_session: UserSession):
    # Check if the document exists and habits are available
    if user_doc.has_habits_defined():
        st.write("### Track your habits")

        # Input for the date
        input_date = st.date_input("Enter the date (YYYY-MM-DD)", key="tracking_habit_date_input", format="YYYY-MM-DD", on_change=partial(tracking_habit_input_date_change_callback, user_doc))

        # Dictionary to maintain checkbox values
        checkbox_dict = {}

        # Create checkboxes for each habit
        st.write("### Select the habits you completed:")
        for habit in st.session_state["tracking_habit_input_date_data"]:
            checkbox_dict[habit] = st.checkbox(habit, value=st.session_state["tracking_habit_input_date_data"][habit])

        st.session_state["tracking_habit_input_date_data"] = checkbox_dict

        # Submit button
        if st.button("Submit"):
            user_doc.update_tracking_for_a_date(input_date, checkbox_dict)
            st.success(f"Habit tracking for {input_date} updated successfully!")
            st.balloons()

    else:
        st.warning("No habits available to track. Please add habits first.")
