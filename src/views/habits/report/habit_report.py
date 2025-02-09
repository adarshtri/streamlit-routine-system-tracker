import pandas as pd

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
            "Days Tracked": self.sample_count,
            "Performance Score": round(float(self.complete_count) / float(self.sample_count)*100, 2) * self.sample_count
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


def top_performing_habits(habits, top_n = 3):

    df = pd.DataFrame(habits)
    df = df.sort_values(by="Performance Score").reset_index(drop=True)
    df = df.tail(top_n)
    return df

def worst_performing_habits(habits, bottom_n = 3):
    df = pd.DataFrame(habits)
    df = df.sort_values(by="Performance Score").reset_index(drop=True)
    df = df.head(bottom_n)
    return df

def create_habit_reports(user_doc: UserDoc, user_session: UserSession):

    habit_stats = generate_habit_stats(user_doc)

    habit_stats_values = list(map(lambda x: x.to_dict(), list(habit_stats.values())))

    currently_tracked_habit_status = [habit_stat for habit_stat in habit_stats_values if habit_stat["Habit Status"] == "Tracked"]
    previously_tracked_habit_status = [habit_stat for habit_stat in habit_stats_values if habit_stat["Habit Status"] == "Tracked Previously"]

    st.write("### Quick Stats")

    top_performing_habit = top_performing_habits(currently_tracked_habit_status).to_dict(orient='records')
    worst_performing_habit = worst_performing_habits(currently_tracked_habit_status).to_dict(orient='records')

    st.write("#### Top Performer Habits")

    col1, col2, col3 = st.columns(3)
    col1.metric(label=top_performing_habit[0]["Habit"], value=f'{top_performing_habit[0]["Habit Completion Rate"]} %',
                delta=" ", border=True)
    col1.write(f'Performance Score: {top_performing_habit[0]["Performance Score"]}')
    col2.metric(label=top_performing_habit[1]["Habit"], value=f'{top_performing_habit[1]["Habit Completion Rate"]} %',
                delta=" ", border=True)
    col2.write(f'Performance Score: {top_performing_habit[1]["Performance Score"]}')
    col3.metric(label=top_performing_habit[2]["Habit"], value=f'{top_performing_habit[2]["Habit Completion Rate"]} %',
                delta=" ", border=True)
    col3.write(f'Performance Score: {top_performing_habit[2]["Performance Score"]}')

    st.divider()

    st.write("#### Worst Performer Habits")

    col1, col2, col3 = st.columns(3)
    col1.metric(label=worst_performing_habit[0]["Habit"],
                value=f'{worst_performing_habit[0]["Habit Completion Rate"]} %', delta=" ", border=True)
    col1.write(f'Performance Score: {worst_performing_habit[0]["Performance Score"]}')
    col2.metric(label=worst_performing_habit[1]["Habit"],
                value=f'{worst_performing_habit[1]["Habit Completion Rate"]} %', delta=" ", border=True)
    col2.write(f'Performance Score: {worst_performing_habit[1]["Performance Score"]}')
    col3.metric(label=worst_performing_habit[2]["Habit"],
                value=f'{worst_performing_habit[2]["Habit Completion Rate"]} %', delta=" ", border=True)
    col3.write(f'Performance Score: {worst_performing_habit[2]["Performance Score"]}')

    st.divider()

    st.write("### Currently Tracked Habit Stats")

    st.dataframe(currently_tracked_habit_status)

    st.divider()

    st.write("### Previously Tracked Habit Stats")
    if previously_tracked_habit_status:
        st.dataframe(previously_tracked_habit_status)
    else:
        st.write("You don't have a historical value that was tracked previously.")

    st.divider()