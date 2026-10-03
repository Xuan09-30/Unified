# ingestion/fetch_github.py
import os
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

repos = [
    "ethereum/go-ethereum",
    "solana-labs/solana",
    "microsoft/vscode",
    "tensorflow/tensorflow"
]

# GitHub allows 60 requests per hour unauthenticated, which is plenty for 4 repos.
headers = {"Accept": "application/vnd.github.v3+json"}
all_data = []

print("Fetching weekly commit activity from GitHub...")

for repo in repos:
    url = f"https://api.github.com/repos/{repo}/stats/commit_activity"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        for week in data:
            # GitHub returns Unix timestamps for the start of the week
            week_date = datetime.utcfromtimestamp(week['week']).date()
            all_data.append({
                "repo_name": repo,
                "week_starting": week_date,
                "commit_count": week['total']
            })
        print(f"✅ Fetched 52 weeks of data for {repo}")
    elif response.status_code == 202:
        print(f"⏳ GitHub is caching {repo}. Run script again in 1 minute.")
    else:
        print(f"❌ Failed to fetch {repo}: {response.status_code} - {response.text}")

if all_data:
    df = pd.DataFrame(all_data)
    print(f"Loading {len(df)} rows into PostgreSQL...")
    df.to_sql('commit_activity', engine, schema='github', if_exists='append', index=False)
    print("GitHub data successfully loaded!")