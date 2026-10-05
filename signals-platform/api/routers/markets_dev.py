# api/routers/markets_dev.py
from fastapi import APIRouter
from ingestion.db import get_db_connection

router = APIRouter(prefix="/markets-dev", tags=["Markets vs Developer Activity"])

@router.get("/weekly-signals")
def get_weekly_signals():
    """Returns weekly commit activity joined with weekly average stock/crypto prices."""
    query = """
        WITH market_weekly AS (
            SELECT 
                ticker,
                -- Truncate daily trade dates to the start of the week (Monday)
                DATE_TRUNC('week', trade_date)::date AS week_starting,
                ROUND(AVG(close_price)::numeric, 2) AS avg_price
            FROM markets.price_history
            GROUP BY ticker, DATE_TRUNC('week', trade_date)
        ),
        repo_mapping AS (
            SELECT 'ethereum/go-ethereum' AS repo_name, 'ETH-USD' AS ticker UNION ALL
            SELECT 'solana-labs/solana', 'SOL-USD' UNION ALL
            SELECT 'microsoft/vscode', 'MSFT' UNION ALL
            SELECT 'tensorflow/tensorflow', 'GOOGL'
        )
        SELECT 
            g.repo_name,
            m.ticker,
            g.week_starting,
            g.commit_count,
            m.avg_price
        FROM github.commit_activity g
        JOIN repo_mapping rm ON g.repo_name = rm.repo_name
        -- FIX: Add 1 day to GitHub's Sunday timestamp so it matches Postgres's Monday timestamp
        JOIN market_weekly m ON rm.ticker = m.ticker AND (g.week_starting + INTERVAL '1 day')::date = m.week_starting
        ORDER BY g.repo_name, g.week_starting ASC;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
    return results