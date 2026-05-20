-- ================================================================
-- AMAZON E-COMMERCE BUSINESS ANALYSIS SQL QUERIES
-- Comprehensive Business Intelligence Queries
-- ================================================================
-- Author: Business Intelligence Analyst
-- Purpose: 50% Core Business Analysis Work
-- Database: MySQL (Amazon Sales Analytics)
-- ================================================================

USE amazon_sales_db;

-- ================================================================
-- SECTION 1: SALES ANALYSIS
-- ================================================================

-- 1.1 Total Revenue
SELECT 
    COUNT(*) AS total_orders,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    MIN(amount) AS min_order_value,
    MAX(amount) AS max_order_value
FROM sales
WHERE order_status != 'Cancelled';

-- 1.2 Total Orders by Status
SELECT 
    order_status,
    COUNT(*) AS order_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage
FROM sales
GROUP BY order_status
ORDER BY order_count DESC;

-- 1.3 Monthly Revenue Trend with CTE
WITH monthly_revenue AS (
    SELECT 
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        MONTHNAME(order_date) AS month_name,
        SUM(amount) AS monthly_revenue,
        COUNT(*) AS order_count
    FROM sales
    WHERE order_status != 'Cancelled'
      AND order_date IS NOT NULL
    GROUP BY YEAR(order_date), MONTH(order_date), MONTHNAME(order_date)
)
SELECT 
    year,
    month,
    month_name,
    monthly_revenue,
    order_count,
    LAG(monthly_revenue, 1) OVER (ORDER BY year, month) AS prev_month_revenue,
    monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year, month) AS revenue_difference,
    ROUND((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year, month)) / 
          LAG(monthly_revenue, 1) OVER (ORDER BY year, month) * 100, 2) AS growth_percentage
FROM monthly_revenue
ORDER BY year, month;

-- 1.4 Quarterly Revenue Analysis
SELECT 
    YEAR(order_date) AS year,
    QUARTER(order_date) AS quarter,
    SUM(amount) AS quarterly_revenue,
    COUNT(*) AS order_count,
    AVG(amount) AS avg_order_value
FROM sales
WHERE order_status != 'Cancelled'
  AND order_date IS NOT NULL
GROUP BY YEAR(order_date), QUARTER(order_date)
ORDER BY year, quarter;

-- 1.5 Yearly Revenue Analysis
SELECT 
    YEAR(order_date) AS year,
    SUM(amount) AS yearly_revenue,
    COUNT(*) AS yearly_orders,
    AVG(amount) AS avg_order_value,
    SUM(amount) / COUNT(*) * 100 AS revenue_per_order
FROM sales
WHERE order_status != 'Cancelled'
  AND order_date IS NOT NULL
GROUP BY YEAR(order_date)
ORDER BY year;

-- 1.6 Running Total (Cumulative Revenue)
SELECT 
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date) AS running_total,
    ROW_NUMBER() OVER (ORDER BY order_date) AS order_sequence
FROM sales
WHERE order_status != 'Cancelled'
  AND order_date IS NOT NULL
ORDER BY order_date;

-- 1.7 Moving Average (7-day)
SELECT 
    order_date,
    amount,
    AVG(amount) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7day,
    SUM(amount) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_sum_7day
FROM sales
WHERE order_status != 'Cancelled'
  AND order_date IS NOT NULL
ORDER BY order_date;

-- 1.8 Revenue by Day of Week
SELECT 
    day_of_week,
    COUNT(*) AS order_count,
    SUM(amount) AS daily_revenue,
    AVG(amount) AS avg_order_value
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY day_of_week
ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

-- ================================================================
-- SECTION 2: PROFIT ANALYSIS
-- ================================================================

-- 2.1 Total Profit (25% of revenue assumed margin)
SELECT 
    SUM(amount) AS total_revenue,
    SUM(amount) * 0.25 AS total_profit,
    SUM(amount) * 0.75 AS total_cost,
    25.0 AS profit_margin_percentage
FROM sales
WHERE order_status != 'Cancelled';

-- 2.2 Profit by Category
SELECT 
    category,
    SUM(amount) AS total_revenue,
    SUM(amount) * 0.25 AS estimated_profit,
    SUM(amount) * 0.75 AS estimated_cost,
    25.0 AS margin_percentage,
    RANK() OVER (ORDER BY SUM(amount) * 0.25 DESC) AS profit_rank
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category
ORDER BY total_revenue DESC;

-- 2.3 Most Profitable Products (Top 10)
SELECT 
    sku,
    category,
    style,
    SUM(quantity) AS total_units_sold,
    SUM(amount) AS total_revenue,
    SUM(amount) * 0.25 AS estimated_profit,
    RANK() OVER (ORDER BY SUM(amount) * 0.25 DESC) AS profit_rank
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY sku, category, style
ORDER BY estimated_profit DESC
LIMIT 10;

-- 2.4 Loss-Making Products (Negative or Zero Profit Scenarios)
SELECT 
    sku,
    category,
    SUM(amount) AS total_revenue,
    SUM(quantity) AS units_sold,
    SUM(amount) * 0.25 AS estimated_profit,
    CASE 
        WHEN SUM(amount) * 0.25 < 0 THEN 'Loss'
        WHEN SUM(amount) * 0.25 = 0 THEN 'Break Even'
        ELSE 'Profitable'
    END AS profit_status
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY sku, category
HAVING estimated_profit <= 0
ORDER BY estimated_profit;

-- 2.5 High Revenue Low Profit Products
WITH product_analysis AS (
    SELECT 
        sku,
        category,
        SUM(amount) AS total_revenue,
        SUM(amount) * 0.25 AS estimated_profit,
        SUM(quantity) AS units_sold
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY sku, category
)
SELECT 
    *,
    ROUND(estimated_profit / NULLIF(total_revenue, 0) * 100, 2) AS profit_margin
FROM product_analysis
WHERE total_revenue > (SELECT AVG(total_revenue) FROM product_analysis)
  AND estimated_profit < (SELECT AVG(estimated_profit) FROM product_analysis)
ORDER BY profit_margin ASC
LIMIT 20;

-- 2.6 Product Profitability Score
SELECT 
    sku,
    category,
    SUM(amount) AS revenue,
    SUM(quantity) AS units,
    SUM(amount) * 0.25 AS profit,
    CASE 
        WHEN SUM(quantity) >= 100 AND SUM(amount) * 0.25 > 1000 THEN 'High Volume High Profit'
        WHEN SUM(quantity) >= 100 AND SUM(amount) * 0.25 <= 1000 THEN 'High Volume Low Profit'
        WHEN SUM(quantity) < 100 AND SUM(amount) * 0.25 > 1000 THEN 'Low Volume High Profit'
        ELSE 'Low Volume Low Profit'
    END AS profitability_category
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY sku, category
ORDER BY profit DESC;

-- ================================================================
-- SECTION 3: CUSTOMER ANALYSIS
-- ================================================================

-- 3.1 Top Customers by Revenue
SELECT 
    city,
    state,
    COUNT(*) AS order_count,
    SUM(amount) AS customer_revenue,
    AVG(amount) AS avg_order_value,
    SUM(amount) * 0.25 AS customer_profit,
    DENSE_RANK() OVER (ORDER BY SUM(amount) DESC) AS customer_rank
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY city, state
ORDER BY customer_revenue DESC
LIMIT 20;

-- 3.2 Customer Segmentation (RFM Analysis)
WITH rfm_analysis AS (
    SELECT 
        city,
        state,
        MAX(order_date) AS last_order_date,
        COUNT(*) AS frequency,
        SUM(amount) AS monetary_value
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY city, state
)
SELECT 
    city,
    state,
    frequency,
    monetary_value,
    DATEDIFF(CURRENT_DATE, last_order_date) AS recency_days,
    CASE 
        WHEN frequency >= 5 AND monetary_value >= 5000 THEN 'VIP Customer'
        WHEN frequency >= 3 AND monetary_value >= 2000 THEN 'Valuable Customer'
        WHEN frequency >= 2 THEN 'Regular Customer'
        ELSE 'New Customer'
    END AS customer_segment
FROM rfm_analysis
ORDER BY monetary_value DESC;

-- 3.3 Repeat Customers Analysis
WITH order_counts AS (
    SELECT 
        city,
        state,
        COUNT(*) AS order_count,
        SUM(amount) AS total_revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY city, state
)
SELECT 
    customer_type,
    COUNT(*) AS customer_count,
    SUM(total_revenue) AS total_revenue,
    AVG(avg_order_value) AS avg_order_value
FROM (
    SELECT 
        city,
        state,
        order_count,
        total_revenue,
        total_revenue / order_count AS avg_order_value,
        CASE 
            WHEN order_count > 1 THEN 'Repeat Customer'
            ELSE 'One-time Customer'
        END AS customer_type
    FROM order_counts
) customer_analysis
GROUP BY customer_type;

-- 3.4 High Value Customers (> INR 2000 average order)
SELECT 
    city,
    state,
    COUNT(*) AS order_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    SUM(amount) * 0.25 AS customer_profit,
    PERCENT_RANK() OVER (ORDER BY AVG(amount)) AS percentile
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY city, state
HAVING avg_order_value > 2000
ORDER BY avg_order_value DESC;

-- 3.5 Customer Revenue Contribution
WITH customer_revenue AS (
    SELECT 
        city,
        state,
        SUM(amount) AS revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY city, state
),
total_revenue AS (
    SELECT SUM(amount) AS total FROM sales WHERE order_status != 'Cancelled'
)
SELECT 
    cr.city,
    cr.state,
    cr.revenue,
    ROUND(cr.revenue / tr.total * 100, 2) AS revenue_contribution_pct,
    ROUND(SUM(cr.revenue) OVER (ORDER BY cr.revenue DESC) / tr.total * 100, 2) AS cumulative_contribution,
    DENSE_RANK() OVER (ORDER BY cr.revenue DESC) AS revenue_rank
FROM customer_revenue cr
CROSS JOIN total_revenue tr
ORDER BY cr.revenue DESC;

-- 3.6 Customer Purchase Frequency
SELECT 
    month_name,
    year,
    COUNT(DISTINCT city) AS unique_customers,
    COUNT(*) AS total_orders,
    COUNT(*) * 1.0 / COUNT(DISTINCT city) AS orders_per_customer
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY month_name, year
ORDER BY year, FIELD(month_name, 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December');

-- ================================================================
-- SECTION 4: PRODUCT ANALYSIS
-- ================================================================

-- 4.1 Top Selling Products (by Quantity)
SELECT 
    sku,
    category,
    style,
    SUM(quantity) AS total_units_sold,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_unit_price,
    RANK() OVER (ORDER BY SUM(quantity) DESC) AS quantity_rank
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY sku, category, style
ORDER BY total_units_sold DESC
LIMIT 10;

-- 4.2 Bottom Selling Products
SELECT 
    sku,
    category,
    style,
    SUM(quantity) AS total_units_sold,
    SUM(amount) AS total_revenue,
    RANK() OVER (ORDER BY SUM(quantity) ASC) AS quantity_rank
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY sku, category, style
HAVING SUM(quantity) > 0
ORDER BY total_units_sold ASC
LIMIT 10;

-- 4.3 Category-wise Sales
SELECT 
    category,
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_units,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    SUM(amount) * 0.25 AS estimated_profit,
    RANK() OVER (ORDER BY SUM(amount) DESC) AS revenue_rank,
    DENSE_RANK() OVER (ORDER BY SUM(quantity) DESC) AS volume_rank
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category
ORDER BY total_revenue DESC;

-- 4.4 Sub-category (Style) Performance
SELECT 
    category,
    style,
    COUNT(*) AS order_count,
    SUM(quantity) AS units_sold,
    SUM(amount) AS revenue,
    AVG(amount) AS avg_price,
    SUM(amount) * 0.25 AS profit,
    RANK() OVER (PARTITION BY category ORDER BY SUM(amount) DESC) AS category_rank
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category, style
ORDER BY category, revenue DESC;

-- 4.5 Product Revenue Ranking (Dense Rank)
SELECT 
    sku,
    category,
    SUM(amount) AS revenue,
    DENSE_RANK() OVER (ORDER BY SUM(amount) DESC) AS dense_rank,
    RANK() OVER (ORDER BY SUM(amount) DESC) AS rank,
    ROW_NUMBER() OVER (ORDER BY SUM(amount) DESC) AS row_num,
    PERCENT_RANK() OVER (ORDER BY SUM(amount)) AS percentile
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY sku, category
ORDER BY revenue DESC
LIMIT 50;

-- 4.6 Size-wise Product Performance
SELECT 
    category,
    size,
    COUNT(*) AS order_count,
    SUM(amount) AS revenue,
    AVG(amount) AS avg_price
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category, size
ORDER BY category, revenue DESC;

-- 4.7 Product Life Cycle Analysis
SELECT 
    sku,
    category,
    MIN(order_date) AS first_sale_date,
    MAX(order_date) AS last_sale_date,
    COUNT(*) AS total_transactions,
    SUM(quantity) AS units_sold,
    SUM(amount) AS revenue,
    DATEDIFF(MAX(order_date), MIN(order_date)) AS product_lifespan_days
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY sku, category
HAVING COUNT(*) > 1
ORDER BY product_lifespan_days DESC;

-- ================================================================
-- SECTION 5: REGIONAL ANALYSIS
-- ================================================================

-- 5.1 State-wise Revenue
SELECT 
    state,
    COUNT(*) AS order_count,
    SUM(quantity) AS units_sold,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    SUM(amount) * 0.25 AS estimated_profit,
    ROUND(SUM(amount) / SUM(SUM(amount)) OVER () * 100, 2) AS revenue_share_pct,
    DENSE_RANK() OVER (ORDER BY SUM(amount) DESC) AS state_rank
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY state
ORDER BY total_revenue DESC;

-- 5.2 City-wise Profit Analysis
SELECT 
    city,
    state,
    COUNT(*) AS order_count,
    SUM(amount) AS total_revenue,
    SUM(amount) * 0.25 AS estimated_profit,
    SUM(amount) * 0.75 AS estimated_cost,
    25.0 AS profit_margin,
    RANK() OVER (PARTITION BY state ORDER BY SUM(amount) DESC) AS city_rank_in_state
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY city, state
ORDER BY total_revenue DESC;

-- 5.3 Lowest Performing States
SELECT 
    state,
    COUNT(*) AS order_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    SUM(amount) * 0.25 AS profit,
    DENSE_RANK() OVER (ORDER BY SUM(amount) ASC) AS low_performer_rank
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY state
ORDER BY total_revenue ASC
LIMIT 10;

-- 5.4 Regional Contribution Percentage
WITH regional_revenue AS (
    SELECT 
        state,
        SUM(amount) AS revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY state
),
total AS (
    SELECT SUM(amount) AS total_revenue FROM sales WHERE order_status != 'Cancelled'
)
SELECT 
    rr.state,
    rr.revenue,
    ROUND(rr.revenue / total.total_revenue * 100, 2) AS contribution_pct,
    ROUND(SUM(rr.revenue) OVER (ORDER BY rr.revenue DESC) / total.total_revenue * 100, 2) AS cumulative_pct
FROM regional_revenue rr
CROSS JOIN total
ORDER BY rr.revenue DESC;

-- 5.5 State Performance by Quarter
SELECT 
    YEAR(order_date) AS year,
    QUARTER(order_date) AS quarter,
    state,
    SUM(amount) AS quarterly_revenue,
    COUNT(*) AS order_count
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY YEAR(order_date), QUARTER(order_date), state
ORDER BY year, quarter, quarterly_revenue DESC;

-- 5.6 Regional Growth Analysis
WITH monthly_state AS (
    SELECT 
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        state,
        SUM(amount) AS revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY YEAR(order_date), MONTH(order_date), state
)
SELECT 
    state,
    year,
    month,
    revenue,
    LAG(revenue, 1) OVER (PARTITION BY state ORDER BY year, month) AS prev_month,
    ROUND((revenue - LAG(revenue, 1) OVER (PARTITION BY state ORDER BY year, month)) / 
          NULLIF(LAG(revenue, 1) OVER (PARTITION BY state ORDER BY year, month), 0) * 100, 2) AS month_growth_pct
FROM monthly_state
ORDER BY state, year, month;

-- ================================================================
-- SECTION 6: OPERATIONAL ANALYSIS
-- ================================================================

-- 6.1 Cancellation Rate Analysis
SELECT 
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS cancellation_rate_pct,
    SUM(CASE WHEN order_status != 'Cancelled' THEN 1 ELSE 0 END) AS successful_orders
FROM sales
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year, month;

-- 6.2 Cancellation by Category
SELECT 
    category,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS cancellation_rate
FROM sales
GROUP BY category
ORDER BY cancellation_rate DESC;

-- 6.3 Delivery Delay Analysis
SELECT 
    fulfilment_method,
    courier_status,
    COUNT(*) AS order_count,
    SUM(CASE WHEN courier_status = 'Shipped' THEN 1 ELSE 0 END) AS shipped,
    SUM(CASE WHEN courier_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
    SUM(CASE WHEN order_status LIKE '%Delivered%' THEN 1 ELSE 0 END) AS delivered,
    SUM(CASE WHEN order_status LIKE '%Delivered%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS delivery_rate
FROM sales
GROUP BY fulfilment_method, courier_status
ORDER BY order_count DESC;

-- 6.4 Payment Mode Analysis
SELECT 
    promotion_ids,
    COUNT(*) AS order_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value
FROM sales
WHERE order_status != 'Cancelled'
  AND promotion_ids != 'No Promotion'
GROUP BY promotion_ids
ORDER BY order_count DESC
LIMIT 10;

-- 6.5 Order Status Funnel
SELECT 
    order_status,
    COUNT(*) AS order_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage,
    SUM(COUNT(*)) OVER (ORDER BY COUNT(*) DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_count
FROM sales
GROUP BY order_status
ORDER BY order_count DESC;

-- 6.6 Shipment Performance Dashboard
SELECT 
    fulfilment_method,
    ship_service_level,
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN order_status LIKE '%Delivered%' THEN 1 ELSE 0 END) AS delivered,
    SUM(CASE WHEN order_status = 'Shipped' THEN 1 ELSE 0 END) AS in_transit,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
    SUM(CASE WHEN order_status LIKE '%Delivered%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS delivery_success_rate
FROM sales
GROUP BY fulfilment_method, ship_service_level
ORDER BY delivery_success_rate DESC;

-- 6.7 B2B vs B2C Analysis
SELECT 
    b2b_flag,
    COUNT(*) AS order_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY b2b_flag;

-- ================================================================
-- SECTION 7: ADVANCED SQL - WINDOW FUNCTIONS
-- ================================================================

-- 7.1 Lead and Lag Analysis
SELECT 
    order_date,
    amount,
    LAG(amount, 1) OVER (ORDER BY order_date) AS prev_day_amount,
    LEAD(amount, 1) OVER (ORDER BY order_date) AS next_day_amount,
    amount - LAG(amount, 1) OVER (ORDER BY order_date) AS daily_difference
FROM sales
WHERE order_status != 'Cancelled'
ORDER BY order_date
LIMIT 30;

-- 7.2 Percentile Analysis
SELECT 
    category,
    amount,
    PERCENT_RANK() OVER (PARTITION BY category ORDER BY amount) AS percentile,
    CUME_DIST() OVER (PARTITION BY category ORDER BY amount) AS cumulative_distribution
FROM sales
WHERE order_status != 'Cancelled'
ORDER BY category, amount DESC;

-- 7.3 Running Total by Category
SELECT 
    order_date,
    category,
    amount,
    SUM(amount) OVER (PARTITION BY category ORDER BY order_date) AS running_total_by_category
FROM sales
WHERE order_status != 'Cancelled'
ORDER BY category, order_date;

-- 7.4 First and Last Order Analysis
SELECT 
    city,
    state,
    MIN(order_date) AS first_order,
    MAX(order_date) AS last_order,
    COUNT(*) AS total_orders,
    FIRST_VALUE(amount) OVER (PARTITION BY city, state ORDER BY order_date) AS first_order_amount,
    LAST_VALUE(amount) OVER (PARTITION BY city, state ORDER BY order_date) AS last_order_amount
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY city, state, order_date, amount;

-- 7.5 Moving Average by Week
SELECT 
    week,
    year,
    SUM(amount) AS weekly_revenue,
    AVG(SUM(amount)) OVER (ORDER BY year, week ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS moving_avg_4weeks
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY week, year
ORDER BY year, week;

-- 7.6 Case When with Window Functions
SELECT 
    category,
    sku,
    amount,
    CASE 
        WHEN PERCENT_RANK() OVER (PARTITION BY category ORDER BY amount) >= 0.9 THEN 'Top 10%'
        WHEN PERCENT_RANK() OVER (PARTITION BY category ORDER BY amount) >= 0.7 THEN 'Top 30%'
        WHEN PERCENT_RANK() OVER (PARTITION BY category ORDER BY amount) >= 0.5 THEN 'Above Median'
        ELSE 'Below Median'
    END AS revenue_tier
FROM sales
WHERE order_status != 'Cancelled';

-- ================================================================
-- SECTION 8: CTE ADVANCED QUERIES
-- ================================================================

-- 8.1 Complex CTE Analysis
WITH monthly_metrics AS (
    SELECT 
        order_date,
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        SUM(amount) AS monthly_revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY order_date, YEAR(order_date), MONTH(order_date)
),
growth_metrics AS (
    SELECT 
        year,
        month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (ORDER BY year, month) AS prev_month,
        ROUND((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY year, month)) / 
              NULLIF(LAG(monthly_revenue) OVER (ORDER BY year, month), 0) * 100, 2) AS growth_rate
    FROM monthly_metrics
)
SELECT 
    year,
    month,
    monthly_revenue,
    prev_month,
    growth_rate,
    AVG(growth_rate) OVER (ORDER BY year, month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avg_growth_3months
FROM growth_metrics
ORDER BY year, month;

-- 8.2 Customer Lifetime Value
WITH customer_orders AS (
    SELECT 
        city,
        state,
        MIN(order_date) AS first_purchase,
        MAX(order_date) AS last_purchase,
        COUNT(*) AS total_orders,
        SUM(amount) AS lifetime_value
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY city, state
)
SELECT 
    city,
    state,
    total_orders,
    lifetime_value,
    DATEDIFF(last_purchase, first_purchase) AS customer_tenure_days,
    lifetime_value / NULLIF(DATEDIFF(last_purchase, first_purchase), 0) AS daily_value,
    CASE 
        WHEN lifetime_value >= 5000 THEN 'Premium'
        WHEN lifetime_value >= 2000 THEN 'Gold'
        WHEN lifetime_value >= 1000 THEN 'Silver'
        ELSE 'Bronze'
    END AS customer_tier
FROM customer_orders
ORDER BY lifetime_value DESC;

-- 8.3 Product Seasonality Analysis
WITH product_monthly AS (
    SELECT 
        sku,
        category,
        month,
        SUM(amount) AS monthly_revenue,
        SUM(quantity) AS monthly_units
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY sku, category, month
),
seasonality_index AS (
    SELECT 
        sku,
        category,
        monthly_revenue,
        AVG(monthly_revenue) OVER (PARTITION BY sku) AS avg_revenue,
        monthly_revenue / NULLIF(AVG(monthly_revenue) OVER (PARTITION BY sku), 0) AS seasonality_index
    FROM product_monthly
)
SELECT 
    sku,
    category,
    ROUND(AVG(seasonality_index), 2) AS avg_seasonality_index,
    MIN(seasonality_index) AS low_season,
    MAX(seasonality_index) AS peak_season
FROM seasonality_index
GROUP BY sku, category
ORDER BY avg_seasonality_index DESC;

-- ================================================================
-- SECTION 9: JOINS AND SUBQUERIES
-- ================================================================

-- 9.1 Join with Date Dimension
SELECT 
    s.order_date,
    d.month_name,
    d.quarter_number,
    d.season,
    s.category,
    s.amount
FROM sales s
LEFT JOIN dim_date d ON DATE_FORMAT(s.order_date, '%Y%m%d') = d.date_key
WHERE s.order_status != 'Cancelled'
ORDER BY s.order_date;

-- 9.2 Correlated Subquery - Find High Value Orders per State
SELECT 
    state,
    order_id,
    amount,
    (SELECT AVG(amount) FROM sales s2 WHERE s2.state = s.state AND s2.order_status != 'Cancelled') AS state_avg,
    amount - (SELECT AVG(amount) FROM sales s2 WHERE s2.state = s.state AND s2.order_status != 'Cancelled') AS vs_avg_difference
FROM sales s
WHERE order_status != 'Cancelled'
  AND amount > (SELECT AVG(amount) * 2 FROM sales WHERE state = s.state)
ORDER BY state, amount DESC;

-- 9.3 Non-Correlated Subquery
SELECT 
    category,
    SUM(amount) AS category_revenue,
    SUM(amount) * 100.0 / (SELECT SUM(amount) FROM sales WHERE order_status != 'Cancelled') AS revenue_share
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category
HAVING SUM(amount) > (SELECT AVG(SUM(amount)) FROM sales WHERE order_status != 'Cancelled' GROUP BY category);

-- 9.4 Self Join for Product Comparison
SELECT 
    s1.sku AS product_1,
    s2.sku AS product_2,
    s1.category,
    s1.amount AS price_1,
    s2.amount AS price_2,
    s1.amount - s2.amount AS price_difference
FROM sales s1
JOIN sales s2 ON s1.category = s2.category 
             AND s1.order_date = s2.order_date
             AND s1.sku != s2.sku
WHERE s1.order_status != 'Cancelled'
  AND s2.order_status != 'Cancelled'
LIMIT 20;

-- ================================================================
-- SECTION 10: COALESCE, NULLIF, CASE
-- ================================================================

-- 10.1 Handle Division by Zero
SELECT 
    category,
    SUM(amount) AS revenue,
    SUM(quantity) AS units,
    SUM(quantity) AS total_units,
    SUM(amount) / NULLIF(SUM(quantity), 0) AS avg_price_per_unit
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category;

-- 10.2 Case When with Multiple Conditions
SELECT 
    order_id,
    amount,
    quantity,
    CASE 
        WHEN amount > 2000 THEN 'Premium Order'
        WHEN amount > 1000 THEN 'High Value Order'
        WHEN amount > 500 THEN 'Medium Order'
        WHEN amount > 0 THEN 'Standard Order'
        ELSE 'Cancelled/No Value'
    END AS order_category,
    CASE 
        WHEN quantity >= 5 THEN 'Bulk Order'
        WHEN quantity >= 2 THEN 'Multi-unit'
        WHEN quantity = 1 THEN 'Single Item'
        ELSE 'Zero Qty'
    END AS quantity_category
FROM sales;

-- 10.3 Coalesce for Missing Values
SELECT 
    order_id,
    COALESCE(order_status, 'Unknown') AS status,
    COALESCE(courier_status, 'Pending') AS courier_status,
    COALESCE(amount, 0) AS amount,
    COALESCE(quantity, 0) AS quantity
FROM sales;

-- 10.4 NullIf for Safe Division
SELECT 
    category,
    SUM(amount) AS total_revenue,
    COUNT(*) AS order_count,
    SUM(amount) / NULLIF(COUNT(*), 0) AS avg_order_value,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0) AS cancellation_rate
FROM sales
GROUP BY category;

-- ================================================================
-- EXECUTIVE SUMMARY QUERIES
-- ================================================================

-- Summary Dashboard Query
WITH summary AS (
    SELECT 
        'Total Revenue' AS metric,
        CAST(SUM(amount) AS CHAR) AS value
    FROM sales WHERE order_status != 'Cancelled'
    UNION ALL
    SELECT 'Total Orders', CAST(COUNT(*) AS CHAR) FROM sales WHERE order_status != 'Cancelled'
    UNION ALL
    SELECT 'Average Order Value', CAST(ROUND(AVG(amount), 2) AS CHAR) FROM sales WHERE order_status != 'Cancelled'
    UNION ALL
    SELECT 'Cancellation Rate', CAST(ROUND(SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS CHAR) FROM sales
    UNION ALL
    SELECT 'Total States', CAST(COUNT(DISTINCT state) AS CHAR) FROM sales
    UNION ALL
    SELECT 'Total Categories', CAST(COUNT(DISTINCT category) AS CHAR) FROM sales
)
SELECT * FROM summary;