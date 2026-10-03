# ingestion/fetch_olist.py
import os
import zipfile
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Load Environment Variables & DB Connection
load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Explicitly set the Kaggle Token for the API to find
os.environ['KAGGLE_API_TOKEN'] = os.getenv("KAGGLE_API_TOKEN")

# Now import KaggleApi AFTER setting the environment variable
from kaggle.api.kaggle_api_extended import KaggleApi

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# 2. Authenticate and Download Data
print("Authenticating with Kaggle...")
api = KaggleApi()
api.authenticate()

data_dir = "./data/olist"
os.makedirs(data_dir, exist_ok=True)

print("Downloading Olist dataset...")
api.dataset_download_files('olistbr/brazilian-ecommerce', path=data_dir, unzip=True)
print("Download and extraction complete.")

# 3. Load and Process Dimensions
print("Processing dim_customers...")
df_customers = pd.read_csv(f"{data_dir}/olist_customers_dataset.csv")
# Keep only the columns we defined in our schema
df_customers = df_customers[['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']]
df_customers.to_sql('dim_customers', engine, schema='ecom', if_exists='append', index=False)

print("Processing dim_products...")
df_products = pd.read_csv(f"{data_dir}/olist_products_dataset.csv")
df_products = df_products[['product_id', 'product_category_name', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']]
df_products.to_sql('dim_products', engine, schema='ecom', if_exists='append', index=False)

# 4. Load and Process Fact Table (Orders + Order Items)
print("Processing fact_orders...")
df_orders = pd.read_csv(f"{data_dir}/olist_orders_dataset.csv")
df_items = pd.read_csv(f"{data_dir}/olist_order_items_dataset.csv")

# Merge orders with their specific line items
df_fact = pd.merge(df_orders, df_items, on='order_id', how='inner')

# Select and rename columns to match our Postgres schema exactly
df_fact = df_fact[[
    'order_id', 'order_item_id', 'customer_id', 'product_id', 'order_status', 
    'order_purchase_timestamp', 'order_delivered_customer_date', 
    'order_estimated_delivery_date', 'price', 'freight_value'
]]

# Convert timestamp strings to actual datetime objects
time_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in time_cols:
    df_fact[col] = pd.to_datetime(df_fact[col])

df_fact.to_sql('fact_orders', engine, schema='ecom', if_exists='append', index=False)

print("Olist data successfully loaded into the ecom schema!")