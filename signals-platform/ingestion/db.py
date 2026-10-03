# ingestion/db.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL warehouse."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    # Return rows as dictionaries instead of tuples
    conn.cursor_factory = RealDictCursor 
    return conn