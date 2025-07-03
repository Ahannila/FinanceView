import plotly.graph_objs as go
import polars as pl
import pandas as pd

__all__ = ["plot_price_volume_chart"]

def _to_pandas(df):
    """Ensure *df* is a pandas.DataFrame for Plotly."""
    if isinstance(df, pl.DataFrame):
        return df.to_pandas()
    if isinstance(df, pd.DataFrame):
        return df
    raise TypeError("Expected polars.DataFrame or pandas.DataFrame")

def plot_price_volume_chart(df):
    """Return a single Plotly figure with close‑price line + volume bars.

    Requirements in *df* (after your loader’s cleaning step):
        • "date"   – datetime / str
        • "close"  – numeric (price)
        • "volume" – numeric
    """
    pdf = _to_pandas(df)

    fig = go.Figure()

    # Close price (primary y‑axis)
    fig.add_trace(
        go.Scatter(
            x=pdf["date"],
            y=pdf["close"],
            mode="lines",
            name="Close Price",
            line=dict(width=2),
        )
    )

    # Volume (secondary y‑axis)
    fig.add_trace(
        go.Bar(
            x=pdf["date"],
            y=pdf["volume"],
            name="Volume",
            opacity=0.35,
            yaxis="y2",
        )
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis=dict(title="Price", side="left"),
        yaxis2=dict(
            title="Volume",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig
