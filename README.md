# Signals Platform

An end-to-end data engineering and analytics platform designed to ingest, warehouse, and analyze time-series data across distinct domains. The central thesis of this project explores the relationships between open-source developer activity, financial markets, and business intelligence.

By replacing disjointed scripts with a unified architecture, this platform demonstrates production-ready data pipelines, relational warehousing (Star Schema), RESTful API decoupling, and interactive visualization.

## 🏗 Architecture

The platform is built on a decoupled, four-tier architecture running locally via Docker and Python virtual environments:

1. **Ingestion Layer (Python / Pandas):** Automated scripts that fetch, clean, and transform data from external sources (Kaggle API, Yahoo Finance, GitHub REST API) handling rate limits and data unpivoting.
2. **Data Warehouse (PostgreSQL):** A containerized relational database utilizing isolated schemas (`ecom`, `markets`, `github`, `core`) to enforce data integrity and enable cross-domain SQL joins.
3. **API Service (FastAPI):** A high-performance backend that executes complex SQL aggregations (like window functions for RFM analysis) and serves clean JSON to the frontend.
4. **Dashboard (Streamlit):** An interactive UI utilizing Plotly for dual-axis time-series visualizations and executive KPI tracking.

## 📊 Core Modules

* **E-Commerce Analytics (Olist):** Ingests the Brazilian E-Commerce dataset into a Star Schema. The API computes total revenue, monthly sales trends, and dynamic RFM (Recency, Frequency, Monetary) segmentation using PostgreSQL window functions.
* **Developer Momentum vs. Markets:** Fetches weekly GitHub commit activity for major repositories (Ethereum, Solana, VS Code, TensorFlow) and joins it against corresponding market valuations (ETH, SOL, MSFT, GOOGL) to visualize whether open-source velocity leads or lags financial price.
* **Quantified Self (Upcoming):** Integrating personal Spotify listening history and extracted audio signals (Hz, tempo, energy) to map algorithmic track transitions.

## 🛠 Tech Stack

* **Languages:** Python 3.11+, SQL
* **Data Engineering & Processing:** Pandas, SQLAlchemy, yfinance
* **Backend:** FastAPI, Uvicorn, psycopg2
* **Database:** PostgreSQL 15, Docker Compose
* **Frontend / Visualization:** Streamlit, Plotly Express

## 🚀 Quick Start (Windows)

This repository includes a batch script to automate the entire setup process, including virtual environment creation, dependency installation, and container orchestration.

### Prerequisites
* Python 3.11+
* Docker Desktop (must be running)
* Git

### 1. Clone the repository
```powershell
git clone [https://github.com/yourusername/signals-platform.git](https://github.com/yourusername/signals-platform.git)
cd signals-platform
