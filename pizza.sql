-- ==========================================
-- PIZZA SALES DATA ANALYSIS
-- Database Engine: MySQL / DBeaver
-- Author: Yusril Lukman
-- ==========================================

USE Portofolio;


-- 📊 1. KEY BUSINESS METRICS (OVERVIEW)
-- Calculates Total Revenue, Total Pizzas Sold, Total Orders, and Average Order Value (AOV)
SELECT 
    ROUND(SUM(od.quantity * p.price), 2) AS total_revenue,
    SUM(od.quantity) AS total_pizzas_sold,
    COUNT(DISTINCT od.order_id) AS total_orders,
    ROUND(SUM(od.quantity * p.price) / COUNT(DISTINCT od.order_id), 2) AS average_order_value
FROM order_details od
JOIN pizzas p ON od.pizza_id = p.pizza_id;


-- ⏰ 2. PEAK HOURS ANALYSIS
-- Identifies high-volume ordering hours to optimize operational workflow and staffing
SELECT 
    HOUR(order_time) AS order_hour,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY HOUR(order_time)
ORDER BY total_orders DESC;


-- 🍕 3. TOP 3 PIZZAS PER CATEGORY BY REVENUE
-- Leverages CTEs and DENSE_RANK() window functions to rank top revenue-generating pizzas within each category
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
