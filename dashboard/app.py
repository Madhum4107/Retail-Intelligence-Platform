import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Retail AI Intelligence Platform",
    layout="wide"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/retail_store_inventory.csv")
    return df

df = load_data()

# ---------------------------------
# TITLE
# ---------------------------------
st.title("🛒 Retail AI Intelligence Platform")
st.write("Smart Demand Prediction + Business Insights Dashboard")

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
st.sidebar.header("🔍 Filters")

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["Region"].unique().tolist())
)

season = st.sidebar.selectbox(
    "Seasonality",
    ["All"] + sorted(df["Seasonality"].unique().tolist())
)

filtered_df = df.copy()

if category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

if region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == region
    ]

if season != "All":
    filtered_df = filtered_df[
        filtered_df["Seasonality"] == season
    ]

# ---------------------------------
# KPI CARDS
# ---------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Sales",
        f"{filtered_df['Units Sold'].sum():,.0f}"
    )

with col2:
    st.metric(
        "📦 Avg Inventory",
        f"{filtered_df['Inventory Level'].mean():.0f}"
    )

with col3:
    st.metric(
        "📈 Avg Forecast",
        f"{filtered_df['Demand Forecast'].mean():.2f}"
    )

with col4:
    st.metric(
        "💲 Avg Price",
        f"{filtered_df['Price'].mean():.2f}"
    )

# ---------------------------------
# CATEGORY SALES
# ---------------------------------
st.subheader("📊 Category Wise Sales")

category_sales = (
    filtered_df.groupby("Category")["Units Sold"]
    .sum()
)

st.bar_chart(category_sales)

# ---------------------------------
# REGION SALES
# ---------------------------------
st.subheader("🌍 Region Wise Sales")

region_sales = (
    filtered_df.groupby("Region")["Units Sold"]
    .sum()
)

st.bar_chart(region_sales)

# ---------------------------------
# DEMAND VS SALES
# ---------------------------------
st.subheader("📈 Demand Forecast vs Units Sold")

chart_df = filtered_df[
    ["Demand Forecast", "Units Sold"]
].head(100)

st.line_chart(chart_df)

# ---------------------------------
# INVENTORY STATUS
# ---------------------------------
st.subheader("🚨 Inventory Status")

avg_inventory = filtered_df["Inventory Level"].mean()

if avg_inventory < 200:
    st.error("Low Inventory Alert 🚨")
else:
    st.success("Inventory Level Healthy ✅")

# ---------------------------------
# LOW STOCK PRODUCTS
# ---------------------------------
st.subheader("⚠️ Low Inventory Records")

low_stock = filtered_df[
    filtered_df["Inventory Level"] < 50
]

st.dataframe(low_stock.head(20))

# ---------------------------------
# BUSINESS INSIGHTS
# ---------------------------------
st.subheader("📈 Business Insights")

best_category = (
    filtered_df.groupby("Category")["Units Sold"]
    .sum()
    .idxmax()
)

best_region = (
    filtered_df.groupby("Region")["Units Sold"]
    .sum()
    .idxmax()
)

st.write(f"🏆 Best Category: {best_category}")
st.write(f"🌍 Best Region: {best_region}")

st.write(
    f"💰 Highest Sale: {filtered_df['Units Sold'].max()}"
)

st.write(
    f"📉 Lowest Sale: {filtered_df['Units Sold'].min()}"
)

# ---------------------------------
# DATA PREVIEW
# ---------------------------------
st.subheader("📋 Dataset Preview")

st.dataframe(filtered_df.head(20))

# ---------------------------------
# DOWNLOAD REPORT
# ---------------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Report",
    data=csv,
    file_name="retail_report.csv",
    mime="text/csv"
)

# ---------------------------------
# FOOTER
# ---------------------------------
st.markdown("---")
st.caption("🚀 AI Retail Intelligence Platform | Streamlit Dashboard")