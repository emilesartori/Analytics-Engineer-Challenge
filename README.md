## Loadsmart Data Challenge - Analytics Engineering

This repository contains the end-to-end solution for the Loadsmart Data Challenge. The goal of this project is to transform raw logistics data into a structured Star Schema to support business decisions.

Architecture & Tech Stack

# The project was designed following the Medallion Architecture (Bronze, Silver, Gold) principles:

    01. Ingestion (Bronze): scripts/01_loadsmart_extract_load.py.
    Python script using Pandas for data auditing and DuckDB for fast OLAP storage.

    02. Transformation (Silver/Gold): /models/silver/stg_load.sql 
                                  /models/gold/01_dim_carriers.sql    
                                  /models/gold/02_dim_lanes.sql
                                  /models/gold/03_dim_shippers.sql
                                  /models/gold/04_fct_loads.sql
                                  /models/gold/05_export_dw.sql
                                  
    Dbt (Data Build Tool) was used to modularize the SQL logic into Dimensions and Facts.

    Storage: DuckDB as the primary analytical database.

    Quality Assurance: dbt-tests to ensure data integrity (uniqueness, non-null values, and referential integrity).



The core functional requirements for data distribution are implemented in the **`/scripts/02_loadsmart_export_last_month.py`** notebook. This module centralizes the following tasks:

- **Email Automation:** A  Python function that attaches the generated CSV report, handles subject/body parameters, and ensures secure delivery.
- **sFTP Integration:** A  Python function that attaches the generated CSV report to remote servers for downstream consumption.
- **Last Month Export Logic:** A  query that identifies the latest month available in the dataset and exports all corresponding `loadsmart_id` records, ensuring the report is always up-to-date.


- **`03_loadsmart_export_complete.py`**: A script designed to **export the complete database**, ensuring data backup and full-scale availability.
- **`04_loadsmart_export_csv.py`**: A script to **generate the processed CSVs** used as the primary data source for the Power BI dashboard.
    

# Data Modeling (Star Schema)

To ensure high performance in Power BI:

    fct_loads: The central table containing financial metrics (book_price, source_price, pnl).

    dim_lanes: Geolocation dimension separating origin and destination (City/State) for route analysis.

    dim_carriers: Partner dimension.

    dim_shippers: Customer dimension.


## Key Business Metrics (DAX)

To measure the success of Loadsmart's operation, the following measures were developed:

1. **Total Gross Profit (PnL):** - `Total_Gross_Profit = SUM(gold_fct_loads[pnl_amount])`
   - *Direct visibility into the actual margin of each load.*
2. **Profit Margin %:** - `Profit_Margin_% = DIVIDE([Total_Gross_Profit], SUM(gold_fct_loads[total_price]), 0)`
   - *Normalizes performance across different Shipper sizes.*


## Technical Highlights

### 1. Data Integrity & Calendar Fixes
- **Granularity Sync:** Resolved a critical "Blank" issue in the Year filter by converting the `delivery_at` field from *DateTime* to *Date*, ensuring a perfect 1:N relationship with the Dimension Table.
- **Dynamic Calendar:** Implemented a DAX-based `d_calendario` that automatically covers the data range, ensuring the dashboard remains scalable for future data.

---
## Analytical Note: Timeframe Scope
Please note that the **Power BI dashboard focuses exclusively on 2024 data**. Although the dataset includes entries for early 2025, the volume appeared incomplete for a full-year comparison. To maintain data integrity and provide a reliable baseline for seasonality and performance KPIs, the 2025 records were excluded from the primary visuals.


## Repository Structure
- `/models`: Segmented into `silver` (cleaning) and `gold` (final dimensional model).
- `/data`: Central repository for all datasets, including:
    - Raw Data: Original files received for the challenge.
    - Processed Data: Cleaned CSVs generated during the ETL pipeline for Power BI consumption.
- `/scripts`: Houses the standalone `.py` scripts for database exports and CSV generation.
- `/power_bi`: The `.pbix` dashboard;

