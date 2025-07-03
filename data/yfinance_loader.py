import yfinance as yf
import streamlit as st
import polars as pl

@st.cache_data(ttl=3600)
def load_ticker_data(ticker: str, start_date, end_date) -> pl.DataFrame | None:

    """Load stock data from Yahoo Finance using yfinance.
    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
    Returns:
        pl.DataFrame | None: Polars DataFrame with stock data or None if an error occurs.
    """

    try:
        ticker = str(ticker)
        df = yf.download(ticker, start=start_date, end=end_date)
        if df is None or df.empty:
            return None

        df.reset_index(inplace=True)

        # Flatten MultiIndex columns (like ('Close', 'AAPL')) to 'close_aapl'
        df.columns = [
            col[0].lower() if isinstance(col, tuple) else str(col).lower().replace(" ", "_")
            for col in df.columns
        ]
        #st.write("✅ Cleaned pandas columns:", df.columns)
        pl_df = pl.from_pandas(df)


        #print(f"📈 Data for {ticker} loaded successfully with {pl_df.height} rows.")
        #print(df.head())
        #st.write(pl_df.columns)
        #st.write(pl_df.head())

        return pl_df

    except Exception as e:
        st.error(f"❌ Error fetching data for {ticker}: {e}")
        return None

