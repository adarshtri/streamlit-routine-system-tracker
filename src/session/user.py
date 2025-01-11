import streamlit as st

class UserSession:
    def __init__(self, username):
        self.username = username
        self.habit_session_state_key = f"{self.username}__habits_list"
        self.habit_session_synced_from_server_for_update_key = f"{self.username}_synced_from_server_for_update"
        self.__initialize_user_session_habits_if_not_present()
        self.__initialize_synced_from_server_for_update_status()

    def __initialize_user_session_habits_if_not_present(self):
        if self.habit_session_state_key not in st.session_state:
            st.session_state[self.habit_session_state_key] =[]

    def __initialize_synced_from_server_for_update_status(self, status = False):
        if self.habit_session_synced_from_server_for_update_key not in st.session_state:
            st.session_state[self.habit_session_synced_from_server_for_update_key] = status

    def initialize_user_session_habit(self, habits=None):
        if habits is None:
            habits = []
        st.session_state[self.habit_session_state_key] = habits

    def add_new_habit(self, new_habit: str):
        if new_habit not in st.session_state[self.habit_session_state_key]:
            st.session_state[self.habit_session_state_key].append(new_habit)
            st.success(f"Added habit: {new_habit}")
        else:
            st.warning(f"Habit '{new_habit}' is already in the list.")

    def has_habits(self):
        return len(st.session_state[self.habit_session_state_key]) != 0

    def reset_habits(self):
        st.session_state[self.habit_session_state_key] = []

    def get_habits(self):
        return st.session_state[self.habit_session_state_key]

    def remove_habit(self, habit):
        st.session_state[self.habit_session_state_key].remove(habit)

    def set_synced_from_server_for_update(self):
        st.session_state[self.habit_session_synced_from_server_for_update_key] = True

    def reset_synced_from_server_for_update(self):
        st.session_state[self.habit_session_synced_from_server_for_update_key] = False

    def get_synced_from_server_for_update_status(self):
        return st.session_state[self.habit_session_synced_from_server_for_update_key]