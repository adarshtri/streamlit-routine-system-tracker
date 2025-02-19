import streamlit as st
from src.firestore.user import UserDoc
from src.session.user import UserSession
import random
import pandas as pd

def to_df_with_accumulated_count_and_missing_days(timestamps):
    # Convert to DataFrame
    df = pd.DataFrame({"timestamp": pd.to_datetime(timestamps)})

    # Count occurrences per day
    df["Date"] = df["timestamp"].dt.date
    count_per_day = df.groupby("Date").size().reset_index(name="Celebration Count")

    # Create full date range
    full_range = pd.date_range(start=count_per_day["Date"].min(),
                               end=count_per_day["Date"].max())

    # Reindex to fill missing dates with 0
    full_df = pd.DataFrame({"Date": full_range.date})
    full_df = full_df.merge(count_per_day, on="Date", how="left").fillna(0)

    # Convert count to integer and compute cumulative sum
    full_df["Celebration Count"] = full_df["Celebration Count"].astype(int).cumsum()

    return full_df

@st.dialog("You Celebration Info", width="large")
def show_celebration_dialog(user_doc: UserDoc, definition: str):
    celebration_data = user_doc.define_you.get_celebration_data(definition)

    if celebration_data:
        st.write(f"\"**{definition}**\" celebration trend...")


        timestamps = []

        for data in celebration_data:
            timestamps.append(data['created_at'])

        df_timestamps = to_df_with_accumulated_count_and_missing_days(timestamps)

        st.line_chart(df_timestamps, x="Date", y="Celebration Count")
    else:
        st.write("No celebration data available.")



def celebrate(user_doc: UserDoc, user_session: UserSession):

    st.write("## Lets Celebrate You!")

    st.divider()

    tracked_definitions = user_doc.define_you.get_tracked_define_you_definitions()

    for definition in tracked_definitions:

        columns = st.columns(3)

        columns[0].markdown(
            f"""
                                            <div style="background-color: #FFA500; padding: 10px; margin: 5px; margin-bottom: 20px; margin-top: 0px; border-radius: 10px; text-align: center;">
                                                {definition}
                                            </div>
                                            """,
            unsafe_allow_html=True,
        )

        if columns[1].button("Celebrate", key=f"{user_doc.username}_celebrate_tracked_{definition}", icon="🔔"):
            user_doc.define_you.celebrate(definition)
            st.toast("Hurray")
            effect = random.choice([st.snow, st.balloons])  # Randomly pick one
            effect()

        if columns[2].button("Show Celebrations", key=f"{user_doc.username}_show_celebrations_{definition}", icon="📈"):
            show_celebration_dialog(user_doc, definition)