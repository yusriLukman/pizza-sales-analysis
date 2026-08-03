import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Pizza Sales Performance Dashboard",
    layout="wide"
)

st.title("Pizza Place Sales Performance Dashboard")
st.markdown("Interactive business dashboard analyzing sales performance, operational trends, and product preferences.")
st.markdown("---")

# 1. Load Datasets dari folder 'data/'
@st.cache_data
def load_data():
    kpi_df = pd.read_csv("data/kpi_business_overview.csv")
    hourly_df = pd.read_csv("data/hourly_pizza_trends.csv")
    size_df = pd.read_csv("data/pizza_size_preferences.csv")
    top3_df = pd.read_csv("data/top_3_pizzas_by_category.csv")
    return kpi_df, hourly_df, size_df, top3_df

try:
    kpi, hourly, size, top3 = load_data()

    # 2. Key Performance Indicators (KPI Scorecard)
    st.subheader("Business Overview (KPIs)")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"${kpi['total_revenue'][0]:,.2f}")
    col2.metric("Total Pizzas Sold", f"{kpi['total_pizzas_sold'][0]:,}")
    col3.metric("Total Orders", f"{kpi['total_orders'][0]:,}")
    col4.metric("Avg Order Value (AOV)", f"${kpi['average_order_value'][0]:.2f}")

    st.markdown("---")

    # 3. Baris Visualisasi 1: Peak Operating Hours & Size Preferences
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Order Volume by Hour (Peak Hours)")
        hourly_sorted = hourly.sort_values('order_hour')
        fig_hourly = px.line(
            hourly_sorted, 
            x="order_hour", 
            y="total_orders", 
            markers=True,
            labels={"order_hour": "Hour of Day", "total_orders": "Total Orders"},
            color_discrete_sequence=["#1F497D"]
        )
        fig_hourly.update_layout(xaxis=dict(dtick=1))
        st.plotly_chart(fig_hourly, use_container_width=True)

    with col_right:
        st.subheader("Pizza Sales by Size")
        fig_size = px.pie(
            size, 
            values='total_loyang_terjual', 
            names='ukuran_pizza', 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_size, use_container_width=True)

    st.markdown("---")

    # 4. Baris Visualisasi 2: Top 3 Pizzas per Category
    st.subheader("Top 3 Pizzas by Revenue (per Category)")
    
    # Filter Interaktif per Kategori
    categories = list(top3['category'].unique())
    selected_category = st.multiselect("Filter Kategori:", categories, default=categories)
    filtered_top3 = top3[top3['category'].isin(selected_category)]

    fig_top3 = px.bar(
        filtered_top3, 
        x="total_sales", 
        y="pizza_name", 
        color="category", 
        orientation='h', 
        labels={"total_sales": "Total Sales ($)", "pizza_name": "Pizza Variant"},
        text_auto='.2s'
    )
    fig_top3.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_top3, use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat data. Pastikan semua file CSV sudah berada di folder 'data/'. Error: {e}")
