import plotly.graph_objects as go
import streamlit as st
import polars as pl

def plot_volume_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Volume'],
        name='Volume'
    ))

    fig.update_layout(
        title="Trading Volume",
        xaxis_title="Date",
        yaxis_title="Shares",
        hovermode="x unified"
    )

    return fig
