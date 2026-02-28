import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("🚀 Crypto Dashboard")

# Load data from SQLite
conn = sqlite3.connect("crypto.db")
df = pd.read_sql("SELECT * FROM crypto_market", conn)
conn.close()

if df.empty:
    st.warning("No data available. Run ETL first!")
else:
    # Show metrics
    st.subheader("Market Summary")
    total_market_cap = df['market_cap'].sum()
    total_volume = df['total_volume'].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Market Cap (USD)", f"${total_market_cap:,.0f}")
    col2.metric("Total Volume (USD)", f"${total_volume:,.0f}")

    # Show table
    st.subheader("Top 10 Cryptos")
    st.dataframe(df)

    # Market Cap Bar Chart
    st.subheader("Market Cap Chart")
    st.bar_chart(df.set_index("name")['market_cap'])
    # 2️⃣ Price Metrics
st.subheader("Price Summary")
avg_price = df['current_price'].mean()
max_price = df['current_price'].max()
min_price = df['current_price'].min()

st.metric("Average Price (USD)", f"${avg_price:,.2f}")
st.metric("Highest Price (USD)", f"${max_price:,.2f}")
st.metric("Lowest Price (USD)", f"${min_price:,.2f}")
st.subheader("Market Cap Chart")
st.bar_chart(df.set_index('name')['market_cap'])
# 3️⃣ Price Bar Chart
st.subheader("Current Price Chart")
st.bar_chart(df.set_index('name')['current_price'])
# 4️⃣ Volume Metrics and Chart
st.subheader("Volume Summary")
total_volume = df['total_volume'].sum()
avg_volume = df['total_volume'].mean()

st.metric("Total Volume (USD)", f"${total_volume:,.0f}")
st.metric("Average Volume (USD)", f"${avg_volume:,.0f}")

st.subheader("Volume Chart")
st.bar_chart(df.set_index('name')['total_volume'])

# 5️⃣ Historical Price Trend (for Top Crypto)
st.subheader("Top Crypto Price Trend")

# Pick the crypto with highest market cap
top_crypto = df.sort_values(by='market_cap', ascending=False).iloc[0]['id']

# Fetch historical data from CoinGecko API
import requests
import pandas as pd

url = f"https://api.coingecko.com/api/v3/coins/{top_crypto}/market_chart?vs_currency=usd&days=30"
data = requests.get(url).json()

prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
prices['timestamp'] = pd.to_datetime(prices['timestamp'], unit='ms')
prices.set_index('timestamp', inplace=True)

st.line_chart(prices['price'])
