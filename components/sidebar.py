import streamlit as st
from datetime import datetime
from config import DEFAULT_TICKERS, DEFAULT_DATE_RANGE

def render_sidebar(tickers=DEFAULT_TICKERS, default_range=DEFAULT_DATE_RANGE):
    """
    Renders the sidebar with ticker selection and date range inputs.

    Parameters:
    - tickers: List of stock tickers to display in the dropdown.
    - default_range: Tuple containing the default start and end dates.

    Returns:
    - Selected ticker, start date, and end date.
    """
    st.sidebar.header("Filter Options")

    ticker = st.sidebar.selectbox("Select Ticker", tickers)

    start_date = st.sidebar.date_input("Start Date", default_range[0])
    end_date = st.sidebar.date_input("End Date", default_range[1])

    if st.sidebar.button("Go to Analysis Page"):
        st.switch_page("pages/analysis.py")

    # Ensure end_date >= start_date
    if start_date > end_date:
        st.sidebar.error("Start date must be before end date.")
        start_date, end_date = default_range

    return ticker, start_date, end_date

