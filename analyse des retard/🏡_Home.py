import streamlit as st

st.set_page_config(
    page_title="Getaround Delay Analysis",
    page_icon="🚗",
)

st.write("# Welcome to Getaround Delay Analysis! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This application was build for the obtention of the Fullstack Data Science certification by Jedha

    ### What is it about?
    GetAround is the Airbnb for cars. You can rent cars from any person for a few hours to a few days! Founded in 2009, this company has known rapid growth. In 2019, they count over 5 million users and about 20K available cars worldwide.
    
    When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

    The goal of this analysis is to help the Product Manager to decide how long the minimum delay between rentals should be.

 
"""
)