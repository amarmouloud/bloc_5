import pandas as pd
import streamlit as st
import plotly.express as px

### Config
st.set_page_config(
    page_title="Simulate minimum delay threshold",
    page_icon="🕐",
    layout="wide"
)


### App
st.header("Simulate minimum delay threshold 🕐")

@st.cache
def load_data():
    return pd.read_csv('data/data.csv')


with st.spinner(text="Data loading in progress...") : 
    data = load_data()
    st.success('Data loaded', icon="✅")

threshold = st.slider('Select a min delay (in minutes)', 0, 600, 5)

def simulate_checkin_status(delay_at_checkout_in_minutes_prev,threshold ):
    if delay_at_checkout_in_minutes_prev >= threshold :
        return 'Late'
    else :
        return 'In time'

data_simulation = data.copy()
data_simulation['simulated_checkin_status'] = data_simulation['delay_at_checkout_in_minutes_prev'].apply(lambda x : 'Unknown' if pd.isna(x) else simulate_checkin_status(x,threshold))

fig = px.pie(
    data_simulation[data_simulation['simulated_checkin_status'] != 'Unknown'], 
    names='simulated_checkin_status'
    )
    
fig.update_layout(
    legend_title="Simulated checkin status"
)

st.plotly_chart(fig, use_container_width=True)
