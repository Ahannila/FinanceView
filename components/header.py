import streamlit as st

def render_head():
    st.title("Hello Reader👋")
    st.markdown(
    """ 
    FinanceView is a **Streamlit** app that allows you to
    visualize stock data in a simple and interactive way.

    You can select a stock ticker and a date range to see the stock's
    performance over time. The app uses **yfinance** to fetch stock data
    and **Plotly** to create interactive charts.
    """
)

