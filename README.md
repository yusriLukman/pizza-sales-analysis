# Pizza Sales: End-to-End Data Analysis & Dashboard

## Project Overview
This project focuses on an end-to-end data analysis of a fictional pizza restaurant's sales. The primary goal is to extract raw relational data using **SQL**, uncover key business performance metrics, and translate those findings into an interactive business dashboard using **Python (Streamlit)**.

## Key Insights & Business Recommendations
1. **Peak Operating Hours:** Order volumes show a bimodal distribution with distinct peaks during lunch (12:00 PM - 1:00 PM) and dinner (5:00 PM - 7:00 PM). 
   * *Action:* Optimize staff allocation and kitchen prep-times during these specific windows to improve service speed and avoid bottlenecks.
2. **Size Preferences:** Customers overwhelmingly prefer Large and Medium pizzas, while XL and XXL sizes show minimal movement.
   * *Action:* Consider phasing out XXL sizes or focusing promotional efforts (like bundle deals) on the highly popular Large size.
3. **Product Performance:** *The Thai Chicken Pizza* and *The Barbecue Chicken Pizza* are the top revenue generators across all categories.
   * *Action:* Ensure consistent inventory for Chicken and Classic category ingredients to prevent stockouts of best-sellers.

## Tech Stack & Tools
* **Data Extraction & Aggregation:** MySQL / DBeaver (SQL)
* **Data Visualization & Deployment:** Python (Streamlit, Pandas, Plotly Express)

---

## Part 1: SQL Data Extraction

The analysis begins by extracting and aggregating raw data to answer core business questions.

### 1. Business Performance Overview (KPIs)
Calculates core metrics including total revenue, total pizzas sold, total unique orders, and Average Order Value (AOV).
```sql
SELECT 
    ROUND(SUM(od.quantity * p.price), 2) AS total_revenue,
    SUM(od.quantity) AS total_pizzas_sold,
    COUNT(DISTINCT od.order_id) AS total_orders,
    ROUND(SUM(od.quantity * p.price) / COUNT(DISTINCT od.order_id), 2) AS average_order_value
FROM order_details od
JOIN pizzas p ON od.pizza_id = p.pizza_id;
```

### 2. Peak Hours Analysis
Identifies high-traffic hours based on order volume to help optimize store staffing and kitchen preparation.
```SQL
SELECT 
    HOUR(order_time) AS order_hour,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY HOUR(order_time)
ORDER BY total_orders DESC;
```
### 3. Top 3 Pizzas per Category
Uses Common Table Expressions (CTEs) and DENSE_RANK() window functions to rank top-performing pizzas by revenue within each category.
```SQL
WITH revenue_per_pizza AS (
    SELECT 
        pt.category,
        pt.name AS pizza_name,
        ROUND(SUM(od.quantity * p.price), 2) AS total_sales
    FROM order_details od
    JOIN pizzas p ON od.pizza_id = p.pizza_id
    JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
    GROUP BY pt.category, pt.name
),
ranked_pizza AS (
    SELECT 
        category,
        pizza_name,
        total_sales,
        DENSE_RANK() OVER(PARTITION BY category ORDER BY total_sales DESC) AS ranking
    FROM revenue_per_pizza
)
SELECT * FROM ranked_pizza 
WHERE ranking <= 3;
```
## Part 2: Interactive Dashboard
The aggregated datasets from the SQL queries above were visualized into an interactive business dashboard using Streamlit.
(Note for viewer: The dashboard allows filtering and deeper dive into the specific metrics mentioned above.)

### Repository Structure
```
├── sql_queries/
│   └── pizza_analysis.sql          
├── data/
│   ├── kpi_business_overview.csv
│   ├── hourly_pizza_trends.csv
│   ├── pizza_size_preferences.csv
│   └── top_3_pizzas_by_category.csv
├── app.py                           
├── requirements.txt                 
└── README.md                        
```
## How to Run the Dashboard Locally

### 1. Clone this repository:
#### Bash
```bash
git clone [https://github.com/yusriLukman/pizza-sales-analysis.git](https://github.com/yusriLukman/pizza-sales-analysis.git)
```

### 2. Install the required dependencies:
#### Bash
```python
pip install -r requirements.txt
```

### 3. Run the application:
#### Bash
```python
streamlit run app.py
```
