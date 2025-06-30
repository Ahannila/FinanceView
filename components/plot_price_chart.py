import plotly.graph_objs as go

def plot_price_chart(pl_df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=pl_df["date"].to_list(),
        y=pl_df["close"].to_list(),
        mode='lines',
        name='Close Price'
    ))

    fig.update_layout(
        title="Closing Price Over Time",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode="x unified"
    )

    return fig
