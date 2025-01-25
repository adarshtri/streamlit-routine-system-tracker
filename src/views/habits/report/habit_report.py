from src.firestore.user import UserDoc
from src.session.user import UserSession
import streamlit as st


class HabitStats:
    def __init__(self, habit, habit_currently_tracked):
        self.habit = habit
        self.habit_currently_tracked = habit_currently_tracked
        self.complete_count = 0
        self.incomplete_count = 0
        self.sample_count = 0

    def increment_complete_count(self, increment_sample_count = False):
        self.complete_count += 1

        if increment_sample_count:
            self.sample_count += 1

    def increment_incomplete_count(self, increment_sample_count = False):
        self.incomplete_count += 1

        if increment_sample_count:
            self.sample_count += 1

    def to_dict(self):
        return {
            "Habit": self.habit,
            "Habit Status": "Tracked" if self.habit_currently_tracked else "Tracked Previously",
            "Habit Completion Rate": round(float(self.complete_count) / float(self.sample_count)*100, 2),
            "Days Tracked": self.sample_count
        }


def generate_habit_stats(user_doc: UserDoc):
    user_habits_by_date = user_doc.get_habit_tracking_for_all_dates()
    user_tracked_habits = user_doc.get_habits()

    habit_stats = {}

    for date in user_habits_by_date:
        for habit in user_habits_by_date[date]:

            if habit not in habit_stats:
                habit_stats[habit] = HabitStats(habit, habit in user_tracked_habits)

            habit_status = habit_stats[habit]

            if user_habits_by_date[date][habit]:
                habit_status.increment_complete_count(True)
            else:
                habit_status.increment_incomplete_count(True)

    return habit_stats


def create_habit_reports(user_doc: UserDoc, user_session: UserSession):

    habit_stats = generate_habit_stats(user_doc)

    habit_stats_values = list(map(lambda x: x.to_dict(), list(habit_stats.values())))

    currently_tracked_habit_status = [habit_stat for habit_stat in habit_stats_values if habit_stat["Habit Status"] == "Tracked"]
    previously_tracked_habit_status = [habit_stat for habit_stat in habit_stats_values if habit_stat["Habit Status"] == "Tracked Previously"]

    st.write("### Currently Tracked Habit Stats")
    st.dataframe(currently_tracked_habit_status)

    st.divider()

    st.write("### Previously Tracked Habit Stats")
    st.dataframe(previously_tracked_habit_status)

    st.divider()