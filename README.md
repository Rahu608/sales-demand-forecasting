# Sales Demand Forecasting System

End-to-end portfolio project using Python, Pandas, PostgreSQL/SQL, Statistics,
Machine Learning and Streamlit.

## Project flow
CSV/Excel -> Data Cleaning -> PostgreSQL -> EDA -> Daily Sales -> ML Forecast -> Streamlit

## Dataset
`data/sales_demand_dataset.csv`

Columns:
order_id, order_date, product_id, product_name, category, region, city,
quantity, unit_price, discount, sales

## Setup
1. Create a Python virtual environment:
   python -m venv .venv
2. Activate on Windows:
   .venv\Scripts\activate
3. Install:
   pip install -r requirements.txt
4. Run the Python pipeline:
   python src/forecast_model.py
5. Start dashboard:
   python -m streamlit run app.py

## PostgreSQL
Run `sql/01_create_database.sql`, create database `sales_forecasting`,
then run `sql/02_create_table.sql` and `sql/03_analysis_queries.sql`.

Set DB environment variables if needed:
PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
