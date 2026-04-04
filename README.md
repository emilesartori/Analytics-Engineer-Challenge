Loadsmart Data Challenge - Analytics Engineering

This repository contains the end-to-end solution for the Loadsmart Data Challenge. The goal of this project is to transform raw logistics data into a structured Star Schema to support business decisions regarding profitability (PnL), carrier performance, and lane optimization.
Architecture & Tech Stack

The project was designed following the Medallion Architecture (Bronze, Silver, Gold) principles:

    Ingestion (Bronze): Python script (Google Colab/Local) using Pandas for data auditing and DuckDB for fast OLAP storage.

    Transformation (Silver/Gold): dbt (Data Build Tool) was used to modularize the SQL logic into Dimensions and Facts.

    Storage: DuckDB as the primary analytical database.

    Quality Assurance: dbt-tests to ensure data integrity (uniqueness, non-null values, and referential integrity).

Data Modeling (Star Schema)

To ensure high performance in Power BI, I implemented a dimensional model:

    fct_loads: The central table containing financial metrics (book_price, source_price, pnl) and operational flags (on_time_delivery).

    dim_lanes: Geolocation dimension separating origin and destination (City/State) for route analysis.

    dim_carriers: Partner dimension including performance ratings and VIP status.

    dim_shippers: Client dimension for revenue and volume concentration analysis.

How to Run the Project
1. Requirements

    Python 3.12+

    dbt-core & dbt-duckdb

2. Setup Environment
Bash

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install dbt-duckdb pandas

3. Run Transformations
Bash

# Execute dbt models
dbt run

# Run data quality tests
dbt test

Used decimal types for prices.

    Data Auditing: Implemented a pre-ingestion check to identify PnL discrepancies.

    Performance: All joins are based on MD5 hashes (Surrogate Keys) for faster indexing and clean BI relationships.
