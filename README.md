# 🍕 Pizza Sales SQL Data Analysis

## 📌 Project Overview
This project focuses on analyzing pizza sales data using SQL to uncover key business performance metrics, customer behavior patterns, and product popularity. The queries aim to answer critical business questions that can help optimize sales and operational efficiency.

---

## 🛠️ Tech Stack & Tools
* **Database Management System:** MySQL / DBeaver
* **Language:** SQL

---

## 🔍 Key Insights & Business Questions Answered

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
```sql
SELECT 
    HOUR(order_time) AS order_hour,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY HOUR(order_time)
ORDER BY total_orders DESC;
```

### 3. Top 3 Pizzas per Category
Uses Common Table Expressions (CTEs) and `DENSE_RANK()` window functions to rank top-performing pizzas by revenue within each category.
```sql
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

---

## 📂 Repository Structure
```text
├── pizza.sql                  # Complete SQL script containing all analysis queries
└── README.md                  # Project documentation and summary
