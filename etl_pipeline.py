import pandas as pd
import sqlite3
import requests
from datetime import datetime

# Fetch top 10 crypto market data from CoinGecko API
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False
}

response = requests.get(url, params=params)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data)

# Keep only relevant columns
df = df[['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume']]

# Add timestamp
df['timestamp'] = datetime.now()

# Save to SQLite
conn = sqlite3.connect("crypto.db")
df.to_sql("crypto_market", conn, if_exists="replace", index=False)
conn.close()

print("ETL Completed!")

