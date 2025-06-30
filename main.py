import streamlit as st
import polars as pl
from components.header import render_head
from components.sidebar import render_sidebar
from components.plot_price_chart import plot_price_chart
from components.plot_volume_chart import plot_volume_chart
from config import DEFAULT_TICKERS, DEFAULT_DATE_RANGE
from data.yfinance_loader import load_ticker_data



st.set_page_config(page_title="Stock dash", layout="wide")
st.title("Stock Dashboard")

ticker, start_date, end_date = render_sidebar(DEFAULT_TICKERS, DEFAULT_DATE_RANGE)

# Load stock data
df = load_ticker_data(ticker, start_date, end_date)

if df is not None and df.height > 0:
    st.plotly_chart(plot_price_chart(df), use_container_width=True)
else:
    st.warning("No data returned for selected ticker.")



render_head()
