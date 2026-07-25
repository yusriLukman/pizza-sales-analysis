USE Portofolio;



-- 📊 1. METRIK UTAMA BISNIS (OVERVIEW)

SELECT 

    ROUND(SUM(od.quantity * p.price), 2) AS total_revenue,

    SUM(od.quantity) AS total_pizzas_sold,

    COUNT(DISTINCT od.order_id) AS total_orders,

    ROUND(SUM(od.quantity * p.price) / COUNT(DISTINCT od.order_id), 2) AS average_order_value

FROM order_details od

JOIN pizzas p ON od.pizza_id = p.pizza_id;





-- ⏰ 2. ANALISIS JAM SIBUK (PEAK HOURS)

-- Perbaikan: Nama kolom disesuaikan dari 'time' menjadi 'order_time' sesuai struktur tabel standard dataset ini

SELECT 

    HOUR(order_time) AS order_hour,

    COUNT(order_id) AS total_orders

FROM orders

GROUP BY HOUR(order_time)

ORDER BY total_orders DESC;





-- 🍕 3. ANALISIS PRODUK TERLARIS PER KATEGORI (TOP 3 PIZZA)

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

ini file yg saya butuhkan 
