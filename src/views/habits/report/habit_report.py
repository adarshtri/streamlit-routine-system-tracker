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
            "Performance Score": round(float(self.complete_count) / float(self.sample_count), 2) * self.sample_count
        }

def generate_habit_trend_with_fill_and_accumulation(date_wise_data, habit):

    df = pd.DataFrame(date_wise_data)
    df["Tracking Date"] = pd.to_datetime(df["Tracking Date"])

    # Sort by date to ensure correct ordering
    df = df.sort_values('Tracking Date')
    df.sort_index(inplace=True)
    df['total_days'] = range(1, len(df) + 1)


    # Compute cumulative valid percentage
    df['Habit Completion Rate'] = (df['Was Habit Performed?'].cumsum() / df['total_days']) * 100

    del df['total_days']

    # Fill missing dates
    full_range = pd.date_range(start=df['Tracking Date'].min(), end=df['Tracking Date'].max())
    df = df.set_index('Tracking Date').reindex(full_range).reset_index()
    df["Habit Completion Rate"] = df["Habit Completion Rate"].fillna(method='ffill')

    df['was_missing'] = df['Was Habit Performed?'].isna()

    df['Was Habit Performed?'] = df['Was Habit Performed?'].fillna("Not Tracked")
    df.rename(columns={'index': 'Tracking Date'}, inplace=True)

    df['missing_count'] = df['was_missing'].cumsum()

    df['Not Tracked Rate'] = (df['missing_count'] / df['total_days']) * 100
    df.drop(columns=['was_missing', 'missing_count', 'total_days'], inplace=True)

    return df


def generate_trend_for_habit(user_doc: UserDoc, habit: str):

    user_habits_by_date = user_doc.get_habit_tracking_for_all_dates()
    user_tracked_habits = user_doc.get_habits()

    if habit not in user_tracked_habits:
        return None

    today_date = str(pd.Timestamp.today().date())
    today_date_found = False

    habit_datewise_data = []
    for date in user_habits_by_date:
        habit_entry = None
        if habit in user_habits_by_date[date]:
            habit_entry = user_habits_by_date[date][habit]

        if habit_entry is None:
            continue

        if today_date == date:
            today_date_found = True

        habit_datewise_data.append({"Tracking Date": date, "Was Habit Performed?": habit_entry})

    if not today_date_found:
        habit_datewise_data.append({"Tracking Date": today_date, "Was Habit Performed?": True})

    return habit_datewise_data


def render_habit_trend(user_doc: UserDoc):

    st.markdown("### Habit Trend Charts")

    habits = user_doc.get_habits()

    selected_habit = st.selectbox("Select a habit", habits)

    data_for_trend = generate_trend_for_habit(user_doc, selected_habit)
    trend_df = generate_habit_trend_with_fill_and_accumulation(data_for_trend, selected_habit)

    st.dataframe(trend_df)

    st.markdown("##### Habit Completion Trend Chart")
    st.divider()
    st.line_chart(trend_df, x="Tracking Date", y="Habit Completion Rate")

    st.markdown("##### Habit Not Tracked Trend Chart")
    st.divider()
    st.line_chart(trend_df, x="Tracking Date", y="Not Tracked Rate")

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
    df["Normalized Perf Score"] = (df["Performance Score"] / df["Performance Score"].max()).round(3)
    df = df.sort_values(by="Normalized Perf Score").reset_index(drop=True)
    df = df.tail(top_n)
    return df

def worst_performing_habits(habits, bottom_n = 3):
    df = pd.DataFrame(habits)
    df["Normalized Perf Score"] = (df["Performance Score"] / df["Performance Score"].max()).round(3)
    df = df.sort_values(by="Normalized Perf Score").reset_index(drop=True)
    df = df.head(bottom_n)
    return df

def create_habit_reports(user_doc: UserDoc, user_session: UserSession):

    habit_stats = generate_habit_stats(user_doc)

    habit_stats_values = list(map(lambda x: x.to_dict(), list(habit_stats.values())))

    currently_tracked_habit_status = [habit_stat for habit_stat in habit_stats_values if habit_stat["Habit Status"] == "Tracked"]
    previously_tracked_habit_status = [habit_stat for habit_stat in habit_stats_values if habit_stat["Habit Status"] == "Tracked Previously"]

    st.write("### Quick Stats")

    top_performing_habit = top_performing_habits(currently_tracked_habit_status).to_dict(orient='records')[::-1]
    worst_performing_habit = worst_performing_habits(currently_tracked_habit_status).to_dict(orient='records')

    st.write("#### Top Performer Habits")

    col1, col2, col3 = st.columns(3)
    col1.metric(label=top_performing_habit[0]["Habit"], value=f'{top_performing_habit[0]["Habit Completion Rate"]} %',
                delta=f'{top_performing_habit[0]["Normalized Perf Score"]}', border=True)
    col1.write(f'Performance Score: {top_performing_habit[0]["Normalized Perf Score"]}')
    col2.metric(label=top_performing_habit[1]["Habit"], value=f'{top_performing_habit[1]["Habit Completion Rate"]} %',
                delta=f'{top_performing_habit[1]["Normalized Perf Score"]}', border=True)
    col2.write(f'Performance Score: {top_performing_habit[1]["Normalized Perf Score"]}')
    col3.metric(label=top_performing_habit[2]["Habit"], value=f'{top_performing_habit[2]["Habit Completion Rate"]} %',
                delta=f'{top_performing_habit[2]["Normalized Perf Score"]}', border=True)
    col3.write(f'Performance Score: {top_performing_habit[2]["Normalized Perf Score"]}')

    st.divider()

    st.write("#### Worst Performer Habits")

    col1, col2, col3 = st.columns(3)
    col1.metric(label=worst_performing_habit[0]["Habit"],
                value=f'{worst_performing_habit[0]["Habit Completion Rate"]} %', delta=f'{-worst_performing_habit[0]["Normalized Perf Score"]}', border=True)
    col1.write(f'Performance Score: {worst_performing_habit[0]["Normalized Perf Score"]}')
    col2.metric(label=worst_performing_habit[1]["Habit"],
                value=f'{worst_performing_habit[1]["Habit Completion Rate"]} %', delta=f'{-worst_performing_habit[1]["Normalized Perf Score"]}', border=True)
    col2.write(f'Performance Score: {worst_performing_habit[1]["Normalized Perf Score"]}')
    col3.metric(label=worst_performing_habit[2]["Habit"],
                value=f'{worst_performing_habit[2]["Habit Completion Rate"]} %', delta=f'{-worst_performing_habit[2]["Normalized Perf Score"]}', border=True)
    col3.write(f'Performance Score: {worst_performing_habit[2]["Normalized Perf Score"]}')

    st.divider()

    render_habit_trend(user_doc)

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
