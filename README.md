# FinanceView

Here's a clean and informative **README.md** you can include in your project directory to explain your Streamlit + yfinance + Polars financial dashboard:

---

```markdown
# 📈 FinanceView — Streamlit Financial Dashboard

A fast and interactive financial dashboard built with **Streamlit**, **Polars**, and **yfinance** for viewing historical stock price data.

---

## 🚀 Features

- 📊 Plot dynamic closing price charts for any ticker
- ⚡ Fast performance with Polars for data processing
- 🔍 Search and filter tickers from a pre-defined list
- 🔄 Automatically adjusts column naming (no hardcoding)
- 💾 Caching with `@st.cache_data` to reduce API calls

---

## 🧱 Tech Stack

- **Python 3.10+**
- [Streamlit](https://streamlit.io)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [Polars](https://www.pola.rs/)
- Plotly for interactive charts

---

## 📁 Project Structure

---

## 📦 Installation

### Option 1: Using Conda (recommended)

```bash
conda env create -f environment.yml
conda activate financeview
````

### Option 2: Using pip

bash
pip install -r requirements.txt



## ▶️ Running the App

```bash
streamlit run main.py
```

It will open in your browser at: `http://localhost:8501`

---

## 🧠 Notes

* Ticker must be a valid Yahoo Finance symbol (e.g. `AAPL`, `TSLA`, `MSFT`)
* The app automatically normalizes column names (e.g. `Adj Close` → `adj_close`)
* Uses `auto_adjust=True` to display adjusted closing prices by default
* You can modify the `config.py` to predefine default tickers and date range

---

## 📌 TODO Ideas

* Add moving averages (SMA/EMA)
* Compare multiple tickers in one chart
* Add earnings calendar integration
* Analyze quarterly reports with LLM (Ollama/OpenAI)

---

## 📝 License

--
