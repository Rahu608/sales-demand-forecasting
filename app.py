from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# =========================================================
# PROJECT PATH
# =========================================================
ROOT = Path(__file__).resolve().parent

DATA_FILE = ROOT / "data" / "sales_demand_dataset.csv"
DAILY_FILE = ROOT / "outputs" / "daily_sales.csv"
FORECAST_FILE = ROOT / "outputs" / "forecast_30_days.csv"
METRICS_FILE = ROOT / "outputs" / "model_metrics.csv"


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sales Demand Forecasting",
    page_icon="📈",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📈 Sales Demand Forecasting Dashboard")

st.write(
    "Historical sales analysis and 30-day future sales forecasting"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    raw_data = pd.read_csv(DATA_FILE)

    daily_sales = pd.read_csv(DAILY_FILE)

    forecast = pd.read_csv(FORECAST_FILE)

    metrics = pd.read_csv(METRICS_FILE)


    raw_data["order_date"] = pd.to_datetime(
        raw_data["order_date"],
        format="%d-%m-%Y"
    )

    forecast["forecast_date"] = pd.to_datetime(
        forecast["forecast_date"],
        format="%d-%m-%Y"
    )

    return raw_data, daily_sales, forecast, metrics


raw_data, daily_sales, forecast, metrics = load_data()


# =========================================================
# SIDEBAR FILTER
# =========================================================

st.sidebar.header("🔎 Filters")

categories = sorted(
    raw_data["category"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + categories
)


regions = sorted(
    raw_data["region"].dropna().unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + regions
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_data = raw_data.copy()


if selected_category != "All":

    filtered_data = filtered_data[
        filtered_data["category"] == selected_category
    ]


if selected_region != "All":

    filtered_data = filtered_data[
        filtered_data["region"] == selected_region
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_data["sales"].sum()

total_orders = filtered_data["order_id"].nunique()

total_quantity = filtered_data["quantity"].sum()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Sales",
        f"₹{total_sales:,.0f}"
    )


with col2:

    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )


with col3:

    st.metric(
        "Total Quantity",
        f"{total_quantity:,}"
    )


with col4:

    st.metric(
        "Average Order Value",
        f"₹{average_order_value:,.0f}"
    )


# =========================================================
# SALES TREND
# =========================================================

st.subheader("📈 Historical Sales Trend")

daily_filtered = (
    filtered_data
    .groupby("order_date", as_index=False)["sales"]
    .sum()
    .sort_values("order_date")
)

fig1, ax1 = plt.subplots(figsize=(14, 5))

ax1.plot(
    daily_filtered["order_date"],
    daily_filtered["sales"]
)
ax1.set_xlabel("Date")
ax1.set_ylabel("Sales")

ax1.set_title(
    "Daily Historical Sales"
)

plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig1)

# =========================================================
# CATEGORY SALES
# =========================================================

st.subheader("🛍️ Category-wise Sales")

category_sales = (
    filtered_data
    .groupby("category")["sales"]
    .sum()
    .sort_values(ascending=False)
)


fig2, ax2 = plt.subplots(figsize=(10, 5))

category_sales.plot(
    kind="bar",
    ax=ax2
)

ax2.set_xlabel("Category")

ax2.set_ylabel("Sales")

ax2.set_title(
    "Sales by Category"
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig2)


# =========================================================
# REGION SALES
# =========================================================

st.subheader("🌍 Region-wise Sales")

region_sales = (
    filtered_data
    .groupby("region")["sales"]
    .sum()
    .sort_values(ascending=False)
)


fig3, ax3 = plt.subplots(figsize=(10, 5))

region_sales.plot(
    kind="bar",
    ax=ax3
)

ax3.set_xlabel("Region")

ax3.set_ylabel("Sales")

ax3.set_title(
    "Sales by Region"
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig3)


# =========================================================
# 30-DAY FORECAST
# =========================================================

st.subheader("🔮 Next 30 Days Sales Forecast")


fig4, ax4 = plt.subplots(figsize=(14, 5))

ax4.plot(
    forecast["forecast_date"],
    forecast["forecast_sales"]
)

ax4.set_xlabel("Forecast Date")

ax4.set_ylabel("Predicted Sales")

ax4.set_title(
    "30-Day Future Sales Forecast"
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig4)


# =========================================================
# FORECAST TABLE
# =========================================================

st.subheader("📅 Forecast Details")

display_forecast = forecast.copy()

display_forecast["forecast_date"] = (
    display_forecast["forecast_date"]
    .dt.strftime("%Y-%m-%d")
)

display_forecast["forecast_sales"] = (
    display_forecast["forecast_sales"]
    .round(2)
)


st.dataframe(
    display_forecast,
    use_container_width=True
)


# =========================================================
# MODEL PERFORMANCE
# =========================================================

st.subheader("🤖 Model Performance")

st.dataframe(
    metrics,
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.write(
    "Sales Demand Forecasting System | "
    "Python + Pandas + Machine Learning + Streamlit"
)