import pandas as pd
import streamlit as st
from src.firestore.user import UserDoc
import altair as alt


def show_weight_journey_graph(user_doc: UserDoc):
    all_weights = user_doc.get_all_weight()

    kg_df = pd.DataFrame(list(all_weights.items()), columns=["Date", "Weight(kg)"])

    pound_df = pd.DataFrame(kg_df)
    pound_df["Weight(lb)"] = pound_df["Weight(kg)"] * 2.20462
    pound_df = pound_df.drop(columns=["Weight(kg)"])


    kg_df = kg_df.sort_values(by='Date').reset_index(drop=True)
    pound_df = pound_df.sort_values(by='Date').reset_index(drop=True)

    st.markdown("## Below is your Weight Journey")

    metric_type = {
        "Kilograms": "kg",
        "Pounds": "lb"
    }

    selected_metric_display = st.selectbox("Select Metric Type", metric_type)
    metric_type = metric_type[selected_metric_display]

    if metric_type == "kg":
        df = kg_df
        weight_column_name = "Weight(kg)"
    else:
        df = pound_df
        weight_column_name = "Weight(lb)"

    lifetime_value = 100000

    # Dropdown options
    options = {
        '10 Entries': 10,
        '20 Entries': 20,
        '40 Entries': 40,
        '100 Entries': 100,
        'Lifetime': lifetime_value
    }

    # Create dropdown
    selected_display = st.selectbox('Select last how many entries to show:', options)
    selected_value = options[selected_display]

    if selected_value == lifetime_value:
        filtered_df = df
    else:
        filtered_df = df.tail(selected_value)

    # Display selected option
    st.write(f'You selected: {options[selected_display]}')

    y_min = df[weight_column_name].min() - 1
    y_max = df[weight_column_name].max() + 1

    chart = alt.Chart(filtered_df).mark_line().encode(
        x = "Date",
        y = alt.Y(weight_column_name, scale=alt.Scale(domain=[y_min, y_max]))
    ).interactive()

    st.altair_chart(chart, use_container_width=True, theme="streamlit")

    st.divider()

    st.markdown("## Weight Journey Log")
    st.dataframe(filtered_df, hide_index=True, use_container_width=True)