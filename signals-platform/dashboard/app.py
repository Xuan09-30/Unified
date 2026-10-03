# dashboard/app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Signals Platform", layout="wide")
st.title("Signals Platform — Multi-Domain Warehouse")

API_BASE = "http://localhost:8000/api/v1"

st.sidebar.title("Navigation")
domain = st.sidebar.radio("Select Domain", ["E-Commerce Analytics", "Markets vs Dev", "Quantified Self"])

if domain == "E-Commerce Analytics":
    st.header("Olist Business Intelligence")
    res_summary = requests.get(f"{API_BASE}/ecom/summary")
    if res_summary.status_code == 200:
        summary = res_summary.json()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Delivered Orders", f"{summary['total_orders']:,}")
        col2.metric("Total Customers", f"{summary['total_customers']:,}")
        col3.metric("Total Revenue", f"R$ {summary['total_revenue']:,.2f}")
        col4.metric("Avg Item Price", f"R$ {summary['avg_item_price']:,.2f}")

    st.markdown("---")
    res_monthly = requests.get(f"{API_BASE}/ecom/monthly-sales")
    if res_monthly.status_code == 200:
        df_monthly = pd.DataFrame(res_monthly.json())
        fig = px.bar(df_monthly, x="sale_month", y="monthly_revenue", title="Monthly Revenue Trend (BRL)")
        st.plotly_chart(fig, use_container_width=True)

elif domain == "Markets vs Dev":
    st.header("Developer Momentum vs Financial Valuation")
    st.markdown("Does open-source commit velocity lead or lag market price? Select an asset pair below to explore.")
    
    res_signals = requests.get(f"{API_BASE}/markets-dev/weekly-signals")
    if res_signals.status_code == 200:
        df_signals = pd.DataFrame(res_signals.json())
        
        # Create a dropdown to select the asset pair
        asset_pairs = df_signals['repo_name'].unique()
        selected_repo = st.selectbox("Select Repository / Asset Pair", asset_pairs)
        
        # Filter dataframe for the selected pair
        df_filtered = df_signals[df_signals['repo_name'] == selected_repo]
        ticker_name = df_filtered['ticker'].iloc[0]
        
        # Create a dual-axis chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add Market Price line
        fig.add_trace(
            go.Scatter(x=df_filtered['week_starting'], y=df_filtered['avg_price'], name=f"{ticker_name} Price", line=dict(color='blue', width=2)),
            secondary_y=False,
        )
        # Add Commit Count bar chart
        fig.add_trace(
            go.Bar(x=df_filtered['week_starting'], y=df_filtered['commit_count'], name="Weekly Commits", marker_color='rgba(255, 165, 0, 0.5)'),
            secondary_y=True,
        )
        
        fig.update_layout(title_text=f"Correlation: {selected_repo} vs {ticker_name}", hovermode="x unified")
        fig.update_yaxes(title_text="<b>Asset Price (USD)</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>Commit Count</b>", secondary_y=True, showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True)