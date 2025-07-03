import plotly.graph_objects as go
import streamlit as st
import polars as pl

def plot_volume_chart(pl_df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=pl_df['date'],
        y=pl_df['volume'],
        name='volume'
    ))

    fig.update_layout(
        title="Trading Volume",
        xaxis_title="Date",
        yaxis_title="Shares",
        hovermode="x unified"
    )

    return fig
