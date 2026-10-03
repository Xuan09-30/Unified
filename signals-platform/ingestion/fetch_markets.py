# ingestion/fetch_markets.py
import os
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Database Connection setup
load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# 2. Define our target assets
# ETH & SOL for crypto tooling analysis, MSFT & GOOGL for corporate open-source analysis
tickers = ["ETH-USD", "SOL-USD", "MSFT", "GOOGL"]

print(f"Fetching 3 years of historical data for: {', '.join(tickers)}")

# 3. Download data
# yfinance returns a MultiIndex DataFrame if you pass multiple tickers
data = yf.download(tickers, period="3y", interval="1d")

# 4. Transform data to match our schema
# We need to unpivot the data so 'ticker' is a column, not part of a MultiIndex
df_melted = data.stack(level=1).reset_index()

# Rename columns to match PostgreSQL
df_melted.rename(columns={
    'Date': 'trade_date',
    'Ticker': 'ticker',
    'Open': 'open_price',
    'High': 'high_price',
    'Low': 'low_price',
    'Close': 'close_price',
    'Volume': 'volume'
}, inplace=True)

# Ensure date format is correct
df_melted['trade_date'] = pd.to_datetime(df_melted['trade_date']).dt.date

# Drop any rows where we don't have a closing price (e.g., market holidays)
df_clean = df_melted.dropna(subset=['close_price'])

# We only need these specific columns
final_cols = ['ticker', 'trade_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']
df_clean = df_clean[final_cols]

print(f"Transform complete. Loading {len(df_clean)} rows into PostgreSQL...")

# 5. Load into the database
# We use if_exists='append' to add to the table. In a production system, 
# you'd use a more complex upsert (INSERT ON CONFLICT DO UPDATE) to avoid duplicates.
df_clean.to_sql('price_history', engine, schema='markets', if_exists='append', index=False)

print("Markets data successfully loaded!")