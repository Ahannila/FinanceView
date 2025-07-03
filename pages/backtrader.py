import streamlit as st
import polars as pl
import plotly.graph_objs as go
import yfinance as yf
import backtrader as bt
from datetime import date

st.title("📊 Strategy Backtest")

# --- Sidebar ---
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", value=date.today())
run_backtest = st.sidebar.button("Run Backtest")

# --- Backtrader Strategy Example ---
class SmaCross(bt.Strategy):
    params = (('p1', 20), ('p2', 50))

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.p1)
        sma2 = bt.ind.SMA(period=self.p.p2)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()

if run_backtest:
    st.subheader(f"Backtest for {ticker.upper()}")

    # Download and convert to Polars
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True, progress=False)
    df.reset_index(inplace=True)
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    pl_df = pl.from_pandas(df)

    # Plot historical price
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pl_df["date"].to_list(),
        y=pl_df["close"].to_list(),
        mode="lines",
        name="Close"
    ))
    fig.update_layout(title=f"{ticker.upper()} Closing Prices", xaxis_title="Date", yaxis_title="Price (USD)")
    st.plotly_chart(fig, use_container_width=True)

    # Backtrader setup
    data = bt.feeds.PandasData(dataname=df)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)
    cerebro.adddata(data)
    cerebro.broker.set_cash(100000)
    cerebro.run()

    # Plot backtest result
    st.subheader("Backtest Result")
    cerebro.plot(style='candlestick')
