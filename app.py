from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent
EXCEL_PATH = BASE_DIR / "active forcast.xlsx"

# Set up page config
st.set_page_config(
    page_title="Active Forecast Dashboard",
    page_icon="📊",
    layout="wide"
)

if not EXCEL_PATH.exists():
    st.error(f"Excel file not found: {EXCEL_PATH}")
    st.stop()

df = pd.read_excel(EXCEL_PATH, sheet_name="Sales")

# Calculate yearly value (Yearly_used * Price)
df["Yearly_Value"] = df["Yearly_used"] * df["Price"]

# Keep the dashboard aligned with the real workbook columns
# (Item Name, Monthly_used, Yearly_used, forecast(six))

# App Title
st.title("📊 Active Forecast Dashboard")
st.markdown("---")

# Key Metrics Rows
total_monthly = df["Monthly_used"].sum()
total_yearly = df["Yearly_used"].sum()
total_forecast = df["forecast(six)"].sum()
Yearly_value= df["Yearly_Value"].sum() 

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Monthly Usage", value=f"{total_monthly:,.1f}")
with col2:
    st.metric(label="Total Yearly Usage", value=f"{total_yearly:,.1f}")
with col3:
    st.metric(label="Total 6-Month Forecast", value=f"{total_forecast:,.1f}")
with col4:
    st.metric(label="Total Value", value=f"${Yearly_value:,.2f}")

st.markdown("---")

# Layout columns for data profile and charts
left_col, right_col = st.columns([1, 1.2])

with left_col:
    st.subheader("📋 Item Usage Data Profile")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Filter capability
    st.subheader("🔍 Filter Item Details")
    selected_item = st.selectbox("Select an item to view specific metrics:", df["Item Name"].unique())
    item_row = df[df["Item Name"] == selected_item].iloc[0]
    
    sub_c1, sub_c2, sub_c3 = st.columns(3)
    sub_c1.metric("Monthly", f"{item_row['Monthly_used']:,.1f}")
    sub_c2.metric("Yearly", f"{item_row['Yearly_used']:,.1f}")
    sub_c3.metric("Forecast (6M)", f"{item_row['forecast(six)']:,.1f}")

with right_col:
    st.subheader("📈 Usage Comparison Chart")
    usage_chart_df = df.sort_values("Yearly_used", ascending=False)
    fig = px.pie(
        usage_chart_df,
        names="Item Name",
        values="Yearly_used",
        title="Yearly Used Quantity by Item",
        labels={"Yearly_used": "Quantity / Volume", "Item Name": "Product Item"},
        hole=0.35,
        height=500,
    )
    fig.update_traces(textposition="inside", textinfo="label+percent")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Price visualization section
price_col1, price_col2 = st.columns([1, 1.2])

with price_col1:
    st.subheader("💰 Price Information")
    price_df = df[["Item Name", "Price"]].sort_values("Price", ascending=False)
    st.dataframe(price_df, use_container_width=True, hide_index=True)

with price_col2:
    st.subheader("💵 Price by Item")
    fig_price = px.bar(
        df.sort_values("Price", ascending=False),
        x="Item Name",
        y="Price",
        title="Price per Item",
        labels={"Price": "Price ($)", "Item Name": "Product Item"},
        height=500,
        color="Price",
        color_continuous_scale="Viridis"
    )
    fig_price.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_price, use_container_width=True)

st.markdown("---")

# Yearly Usage by Value section
yearly_col1, yearly_col2 = st.columns([1, 1.2])

with yearly_col1:
    st.subheader("📊 Yearly Usage by Item")
    yearly_df = df[["Item Name", "Yearly_Value"]].sort_values("Yearly_Value", ascending=False)
    st.dataframe(yearly_df, use_container_width=True, hide_index=True)

with yearly_col2:
    st.subheader("💎 Yearly Value by Item")
    fig_yearly_value = px.bar(
        df.sort_values("Yearly_Value", ascending=False),
        x="Item Name",
        y="Yearly_Value",
        title="Annual Usage Value by Item (Quantity × Price)",
        labels={"Yearly_Value": "Annual Value ($)", "Item Name": "Product Item"},
        height=500,
        color="Yearly_Value",
        color_continuous_scale="Reds"
    )
    fig_yearly_value.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_yearly_value, use_container_width=True)

st.markdown("---")
st.caption("Dashboard compiled automatically based on active forecast records.")
