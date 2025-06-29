import streamlit as st
from components.header import render_head
from config import DEFAULT_TICKERS, DEFAULT_DATE_RANGE


st.set_page_config(page_title="Stock dash", layout="wide")
render_head()
