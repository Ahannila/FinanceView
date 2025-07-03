import streamlit as st
import polars as pl
from components.header import render_head
from components.sidebar import render_sidebar
from components.plot_price_chart import plot_price_chart
from components.plot_volume_chart import plot_volume_chart
from components.plot_vol_price import plot_price_volume_chart
from config import DEFAULT_TICKERS, DEFAULT_DATE_RANGE
from data.yfinance_loader import load_ticker_data
from llm.ollama_agent import ask_ollama



st.set_page_config(page_title="Stock dash", layout="wide")
st.title("Stock Dashboard")
render_head()

ticker, start_date, end_date = render_sidebar(DEFAULT_TICKERS, DEFAULT_DATE_RANGE)

# ----------- Load stock data --------------
df = load_ticker_data(ticker, start_date, end_date)

if df is not None and df.height > 0:
    st.plotly_chart(plot_price_volume_chart(df), use_container_width=True)
else:
    st.warning("No data returned for selected ticker.")




# ------------------------------------------------------------------ #
# Optional Ollama analysis
# ------------------------------------------------------------------ #
use_llm = st.sidebar.checkbox("💡 Use Ollama AI", value=True)



if use_llm:
    st.markdown("## 🧠 Ollama Insight")
    prompt = st.text_area(
        "Ask something about this period (optional):",
        placeholder="E.g. ‘Summarise notable price moves’",
    )

    if st.button("Generate"):
        # Build a default prompt if the user left it blank
        if not prompt.strip():
            prompt = (
                f"Give a short, useful summary of how {ticker} traded "
                f"from {start_date} to {end_date}. Output 3–5 bullets."
            )
        ask_ollama(prompt, stream=True)
