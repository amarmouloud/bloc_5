import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

### Config
st.set_page_config(
    page_title="Explore the dataset",
    page_icon="🌍",
    layout="wide"
)


### App

st.header("Explore the dataset 🌍")
st.sidebar.header("Explore the dataset")


@st.cache
def load_data():
    return pd.read_csv('data/data.csv')


with st.spinner(text="Data loading in progress...") : 
    data = load_data()
    st.success('Data loaded', icon="✅")


st.subheader('Delay at checkout')
options = st.multiselect(
    'Checkin type',
    ('mobile', 'connect'),
    default=['mobile', 'connect'])

data_filtered = data[data['checkin_type'].isin(options)]

col1, col2, col3 = st.columns(3)

# Average time delta between 2 rentals
avg_time_delta = int(data_filtered['time_delta_with_previous_rental_in_minutes'].mean())
col1.metric("Average time delta between rentals", str(avg_time_delta) + ' min')

late_checkouts = data_filtered[data_filtered['checkout_status'] == 'Late']

# Percentage of late checkouts
perc_late_checkout = int(len(late_checkouts) / len(data_filtered) * 100)
col2.metric("Percentage of late checkouts", str(perc_late_checkout) + ' %')

# Average delay at checkout
avg_delay_checkout = int(late_checkouts['delay_at_checkout_in_minutes'].mean())
col3.metric("Average delay at checkout", str(avg_delay_checkout) + ' min')

# Histogram delay at checkout

fig = px.histogram(
    late_checkouts[late_checkouts['checkin_type'].isin(options)], 
    x="delay_at_checkout_in_minutes", 
    histnorm='percent', 
    color='checkin_type'
    )
fig.update_layout(
    xaxis_title="Delay at checkout (in minutes)",
    yaxis_title="Percentage of rentals",
    legend_title="Checkin type"
)


st.plotly_chart(fig, use_container_width=True)

# Impact on following rentals
st.subheader('Impact of late checkouts on next rentals')
fig = px.histogram(
    data[data['checkout_status_prev'] == 'Late'], 
    x="checkin_status",
    color='state'
    )
fig.update_layout(
    xaxis_title="Checkin status",
    yaxis_title="Number of rentals",
    legend_title="Rental state"
)

st.plotly_chart(fig, use_container_width=True)