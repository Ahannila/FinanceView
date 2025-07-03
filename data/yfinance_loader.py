import yfinance as yf
import streamlit as st
import polars as pl
import textwrap

__all__ = [
    "load_ticker_data",
    "snapshot_df",
]

# ---------------------------------------------------------------------------
# Helper ― create an LLM‑friendly snapshot of a Polars frame
# ---------------------------------------------------------------------------

def snapshot_df(pl_df: pl.DataFrame, head_rows: int = 5) -> str:  # noqa: D401
    """Return a compact markdown snapshot suitable for LLM context.

    The snapshot includes:
    • first *head_rows* rows
    • last  *head_rows* rows (if long enough)
    • simple stats for *close* & *volume*
    """

    if pl_df.height == 0:
        return "<empty data frame>"

    head_md = pl_df.head(head_rows).to_pandas().to_markdown(index=False)
    tail_md = pl_df.tail(head_rows).to_pandas().to_markdown(index=False)

    # basic quick stats (add/remove as you like)
    try:
        stats_md = (
            pl_df.select(
                [
                    pl.col("close").mean().alias("mean_close"),
                    pl.col("close").std().alias("std_close"),
                    pl.col("volume").mean().alias("mean_volume"),
                ]
            )
            .to_pandas()
            .to_markdown(index=False)
        )
    except pl.ComputeError:
        stats_md = "<stats unavailable>"

    return textwrap.dedent(
        f"""
        **Head ({head_rows} rows)**  
        {head_md}

        **Tail ({head_rows} rows)**  
        {tail_md}

        **Quick stats**  
        {stats_md}
        """
    )


# ---------------------------------------------------------------------------
# Cached loader
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600)
def load_ticker_data(
    ticker: str,
    start_date,
    end_date,
    *,
    return_snapshot: bool = False,
    head_rows: int = 5,
) -> pl.DataFrame | tuple[pl.DataFrame, str] | None:  # noqa: D401
    """Fetch Yahoo Finance data and optionally return an LLM snapshot.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol.
    start_date, end_date : str | datetime
        Date range.
    return_snapshot : bool, default False
        If *True*, the function returns a tuple ``(pl_df, snapshot_str)``.
    head_rows : int, default 5
        Number of rows to include in head/tail sections of the snapshot.

    Returns
    -------
    pl.DataFrame | (pl.DataFrame, str) | None
    """

    try:
        df = yf.download(
            str(ticker),
            start=start_date,
            end=end_date,
            group_by="column",
            auto_adjust=True,
            progress=False,
        )
        if df is None or df.empty:
            return None

        df.reset_index(inplace=True)
        df.columns = [
            col[0].lower() if isinstance(col, tuple) else str(col).lower().replace(" ", "_")
            for col in df.columns
        ]

        pl_df = pl.from_pandas(df)

        if return_snapshot:
            return pl_df, snapshot_df(pl_df, head_rows=head_rows)
        return pl_df

    except Exception as err:  # pragma: no cover
        st.error(f"❌ Error fetching data for {ticker}: {err}")
        return None
