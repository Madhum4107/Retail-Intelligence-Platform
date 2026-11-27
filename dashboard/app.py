"""Interactive retail analytics dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st

from dashboard.analytics import add_business_metrics, category_summary, validate_dataset

st.set_page_config(page_title="Retail Intelligence", page_icon="🛍️", layout="wide")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "retail_store_inventory.csv"
REQUIRED_COLUMNS = {
    "Category", "Region", "Seasonality", "Units Sold",
    "Inventory Level", "Demand Forecast", "Price",
}


@st.cache_data(show_spinner="Loading retail dataset…")
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


st.title("🛍️ Retail Intelligence Platform")
st.write("Explore sales activity, inventory levels, and demand signals with interactive filters.")

if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

df = load_data(str(DATA_PATH))
dataset_errors = validate_dataset(df)
if dataset_errors:
    for error in dataset_errors:
        st.error(error)
    st.stop()

df = add_business_metrics(df)

with st.sidebar:
    st.header("Filters")
    category_options = sorted(df["Category"].dropna().unique().tolist())
    region_options = sorted(df["Region"].dropna().unique().tolist())
    season_options = sorted(df["Seasonality"].dropna().unique().tolist())
    category = st.selectbox("Category", ["All"] + category_options)
    region = st.selectbox("Region", ["All"] + region_options)
    season = st.selectbox("Seasonality", ["All"] + season_options)
    low_stock_threshold = st.number_input("Low-stock threshold", min_value=0.0, value=50.0, step=5.0)
    st.divider()
    st.caption(f"Dataset: {len(df):,} rows · {len(df.columns)} columns")

filtered = df.copy()
if category != "All":
    filtered = filtered[filtered["Category"] == category]
if region != "All":
    filtered = filtered[filtered["Region"] == region]
if season != "All":
    filtered = filtered[filtered["Seasonality"] == season]

if filtered.empty:
    st.warning("No rows match the selected filters. Try changing or clearing the filters.")
    st.stop()

# KPI summary
k1, k2, k3, k4 = st.columns(4)
k1.metric("Units sold", f"{filtered['Units Sold'].sum():,.0f}")
k2.metric("Average inventory", f"{filtered['Inventory Level'].mean():,.1f}")
k3.metric("Average demand forecast", f"{filtered['Demand Forecast'].mean():,.2f}")
k4.metric("Average product price", f"{filtered['Price'].mean():,.2f}")

st.divider()

sales_tab, inventory_tab, data_tab = st.tabs(["📈 Sales insights", "📦 Inventory", "🧾 Data explorer"])

with sales_tab:
    left, right = st.columns(2)
    with left:
        st.subheader("Units sold by category")
        category_sales = filtered.groupby("Category")["Units Sold"].sum().sort_values(ascending=False)
        st.bar_chart(category_sales)
    with right:
        st.subheader("Units sold by region")
        region_sales = filtered.groupby("Region")["Units Sold"].sum().sort_values(ascending=False)
        st.bar_chart(region_sales)

    st.subheader("Demand forecast vs. units sold")
    grouped = category_summary(filtered).set_index("Category")[["Units_Sold", "Demand_Forecast"]]
    st.bar_chart(grouped)
    st.caption("Values are aggregated by category. Forecast gaps are descriptive comparisons, not forecast-accuracy measurements.")

    st.subheader("Business summary")
    category_total = filtered.groupby("Category")["Units Sold"].sum()
    region_total = filtered.groupby("Region")["Units Sold"].sum()
    if not category_total.empty and not region_total.empty:
        a, b, c = st.columns(3)
        a.info(f"Top category by units: **{category_total.idxmax()}**")
        b.info(f"Top region by units: **{region_total.idxmax()}**")
        c.info(f"Highest row-level units sold: **{filtered['Units Sold'].max():,.0f}**")

with inventory_tab:
    avg_inventory = filtered["Inventory Level"].mean()
    if avg_inventory < 200:
        st.warning(f"Average inventory is below the demo threshold (200 units): {avg_inventory:,.1f}.")
    else:
        st.success(f"Average inventory is at or above the demo threshold: {avg_inventory:,.1f}.")

    low_stock = filtered[filtered["Inventory Level"] < low_stock_threshold].sort_values("Inventory Level")
    st.subheader(f"Low-inventory records (below {low_stock_threshold:g} units)")
    st.dataframe(low_stock.head(50), use_container_width=True, hide_index=True)
    st.caption("Inventory and forecast comparisons are simplified signals. Thresholds should reflect product-level replenishment policies.")

with data_tab:
    st.subheader("Filtered dataset")
    st.dataframe(filtered.head(500), use_container_width=True, hide_index=True)
    st.caption(f"Showing up to 500 of {len(filtered):,} filtered records.")
    st.subheader("Data quality snapshot")
    quality = pd.DataFrame({
        "Column": filtered.columns,
        "Missing values": filtered.isna().sum().values,
        "Data type": filtered.dtypes.astype(str).values,
    })
    st.dataframe(quality, use_container_width=True, hide_index=True)

st.download_button(
    "⬇️ Download filtered data (CSV)",
    data=filtered.to_csv(index=False),
    file_name="retail_filtered_data.csv",
    mime="text/csv",
)

st.divider()
st.caption("Built with Python · Streamlit · Pandas | Portfolio analytics prototype")
