import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Pizza Sales Performance Dashboard",
    layout="wide",
    page_icon="🍕",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    h1 {
        font-size: 42px !important;
        font-weight: 700 !important;
    }
    h3 {
        font-size: 28px !important;
        font-weight: 600 !important;
    }
    p {
        font-size: 20px !important;
    }
    [data-testid="stMetricValue"] {
        color: #ff4b4b !important;
        font-size: 48px !important; 
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: inherit !important;
        font-size: 20px !important; 
        font-weight: 600 !important;
    }
    .stMetric {
        border-radius: 10px;
        padding: 20px;
        border-left: 10px solid #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Pizza Place Sales Performance Dashboard")
st.markdown("<p>Interactive business analytics dashboard showcasing operational efficiency, customer preferences, and revenue metrics.</p>", unsafe_allow_html=True)
st.markdown("---")

def get_file_path(filename_options):
    for path in filename_options:
        if os.path.exists(path):
            return path
    return filename_options[0]

@st.cache_data
def load_data():
    kpi_path = get_file_path(["data/kpi_business_overview.csv", "kpi_business_overview.csv"])
    hourly_path = get_file_path(["data/hourly_pizza_trends.csv", "hourly_pizza_trends.csv"])
    size_path = get_file_path(["data/pizza_size_preferences.csv", "pizza_size_preferences.csv"])
    top3_path = get_file_path(["data/top_3_pizzas_by_category.csv", "top_3_pizzas_by_category.csv"])

    kpi_df = pd.read_csv(kpi_path)
    hourly_df = pd.read_csv(hourly_path)
    size_df = pd.read_csv(size_path)
    top3_df = pd.read_csv(top3_path)
    return kpi_df, hourly_df, size_df, top3_df

try:
    kpi, hourly, size, top3 = load_data()

    st.sidebar.header("Dashboard Filters")
    st.sidebar.markdown("<p>Filter data to dynamically analyze store performance.</p>", unsafe_allow_html=True)

    all_categories = list(top3['category'].unique())
    selected_categories = st.sidebar.multiselect(
        "Select Pizza Categories:",
        options=all_categories,
        default=all_categories
    )

    all_sizes = list(size['ukuran_pizza'].unique())
    selected_sizes = st.sidebar.multiselect(
        "Select Pizza Sizes:",
        options=all_sizes,
        default=all_sizes
    )

    st.sidebar.markdown("---")
    st.sidebar.info("Tip: Use these filters to isolate performance across menu types.")

    filtered_top3 = top3[top3['category'].isin(selected_categories)]
    filtered_size = size[size['ukuran_pizza'].isin(selected_sizes)]

    st.subheader("Business Performance Overview")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"${kpi['total_revenue'][0]:,.2f}")
    col2.metric("Total Pizzas Sold", f"{kpi['total_pizzas_sold'][0]:,}")
    col3.metric("Total Unique Orders", f"{kpi['total_orders'][0]:,}")
    col4.metric("Avg Order Value (AOV)", f"${kpi['average_order_value'][0]:.2f}")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Peak Operating Hours")
        st.markdown("<p>Distribution of orders throughout the operational hours of the day.</p>", unsafe_allow_html=True)
        
        hourly_sorted = hourly.sort_values('order_hour')
        fig_hourly = px.line(
            hourly_sorted, 
            x="order_hour", 
            y="total_orders", 
            markers=True,
            labels={"order_hour": "Hour of Day", "total_orders": "Total Orders"},
            color_discrete_sequence=["#FF4B4B"]
        )
        fig_hourly.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(dtick=1),
            hovermode="x unified",
            margin=dict(l=20, r=20, t=30, b=20),
            font=dict(size=16)
        )
        st.plotly_chart(fig_hourly, use_container_width=True)

    with col_right:
        st.subheader("Customer Size Preferences")
        st.markdown("<p>Proportion of sales volume based on pizza size variant.</p>", unsafe_allow_html=True)
        
        fig_size = px.pie(
            filtered_size, 
            values='total_loyang_terjual', 
            names='ukuran_pizza', 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_size.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont_size=18 
        )
        fig_size.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            font=dict(size=16)
        )
        st.plotly_chart(fig_size, use_container_width=True)

    st.markdown("---")

    st.subheader("Revenue Performance by Category & Variant")
    st.markdown("<p>Top 3 highest-revenue generating pizzas broken down by category.</p>", unsafe_allow_html=True)

    if not filtered_top3.empty:
        fig_top3 = px.bar(
            filtered_top3, 
            x="total_sales", 
            y="pizza_name", 
            color="category", 
            orientation='h', 
            labels={"total_sales": "Total Sales ($)", "pizza_name": "Pizza Variant"},
            text_auto='.2s',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_top3.update_traces(textfont_size=16)
        fig_top3.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=20, r=20, t=30, b=20),
            font=dict(size=16)
        )
        st.plotly_chart(fig_top3, use_container_width=True)
    else:
        st.warning("No categories selected. Please select at least one category from the sidebar filter.")

except Exception as e:
    st.error(f"Can't Load Data. Detail Error: {e}")
