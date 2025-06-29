from datetime import datetime, timedelta

# Default list of tickers shown in the sidebar dropdown
DEFAULT_TICKERS = [
    "AAPL",  # Apple
    "MSFT",  # Microsoft
    "GOOGL", # Alphabet
    "TSLA",  # Tesla
    "AMZN",  # Amazon
    "NVDA",  # NVIDIA
    "META",  # Meta (Facebook)
    "SPY",   # S&P 500 ETF
]

# Default date range: past 6 months
today = datetime.today()
DEFAULT_DATE_RANGE = (
    today - timedelta(days=180),
    today
)

# Optional: Timezone or plotting settings (if needed later)
PLOT_CONFIG = {
    "xaxis_rangeslider_visible": False,
    "template": "plotly_white"
}
