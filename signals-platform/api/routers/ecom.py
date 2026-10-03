# api/routers/ecom.py
from fastapi import APIRouter, HTTPException
import psycopg2.extras
from ingestion.db import get_db_connection

router = APIRouter(prefix="/ecom", tags=["E-Commerce Analytics"])

@router.get("/summary")
def get_ecom_summary():
    """Returns top-level KPIs: Total Revenue, Total Orders, and Average Order Value."""
    query = """
        SELECT 
            COUNT(DISTINCT f.order_id) AS total_orders,
            COUNT(DISTINCT c.customer_unique_id) AS total_customers,
            ROUND(SUM(f.price)::numeric, 2) AS total_revenue,
            ROUND(AVG(f.price)::numeric, 2) AS avg_item_price
        FROM ecom.fact_orders f
        JOIN ecom.dim_customers c ON f.customer_id = c.customer_id
        WHERE f.order_status = 'delivered';
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()
    return result

@router.get("/monthly-sales")
def get_monthly_sales():
    """Aggregates revenue and order volume by month for trend analysis."""
    query = """
        SELECT 
            TO_CHAR(order_purchase_timestamp, 'YYYY-MM') AS sale_month,
            COUNT(DISTINCT order_id) AS order_count,
            ROUND(SUM(price)::numeric, 2) AS monthly_revenue
        FROM ecom.fact_orders
        WHERE order_status = 'delivered'
        GROUP BY sale_month
        ORDER BY sale_month ASC;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
    return results

@router.get("/rfm-summary")
def get_rfm_summary():
    """Computes basic RFM metrics across unique customers using PostgreSQL window functions."""
    query = """
        WITH customer_aggregates AS (
            SELECT 
                c.customer_unique_id,
                MAX(f.order_purchase_timestamp) AS last_purchase_date,
                COUNT(DISTINCT f.order_id) AS frequency,
                SUM(f.price) AS monetary
            FROM ecom.fact_orders f
            JOIN ecom.dim_customers c ON f.customer_id = c.customer_id
            WHERE f.order_status = 'delivered'
            GROUP BY c.customer_unique_id
        ),
        snapshot AS (
            SELECT MAX(last_purchase_date) + INTERVAL '1 day' AS max_date 
            FROM customer_aggregates
        ),
        rfm_raw AS (
            SELECT 
                ca.customer_unique_id,
                DATE_PART('day', s.max_date - ca.last_purchase_date) AS recency_days,
                ca.frequency,
                ca.monetary
            FROM customer_aggregates ca
            CROSS JOIN snapshot s
        )
        SELECT 
            ROUND(AVG(recency_days)::numeric, 1) AS avg_recency_days,
            ROUND(AVG(frequency)::numeric, 2) AS avg_frequency,
            ROUND(AVG(monetary)::numeric, 2) AS avg_monetary_value,
            COUNT(*) AS total_evaluated_customers
        FROM rfm_raw;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()
    return result