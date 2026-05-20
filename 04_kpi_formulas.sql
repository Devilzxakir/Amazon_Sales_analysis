-- ================================================================
-- AMAZON E-COMMERCE KPI FORMULAS
-- Business Intelligence Key Performance Indicators
-- ================================================================
-- Author: Business Intelligence Analyst
-- Purpose: Standardized KPI calculations for Power BI/Tableau
-- ================================================================

USE amazon_sales_db;

-- ================================================================
-- CORE FINANCIAL KPIs
-- ================================================================

-- KPI 1: Total Revenue
SELECT 
    SUM(amount) AS Total_Revenue
FROM sales
WHERE order_status != 'Cancelled';

-- Power BI DAX:
-- Total Revenue = SUM(sales[amount])

-- KPI 2: Total Profit (with margin assumption)
SELECT 
    SUM(amount) * 0.25 AS Total_Profit,
    SUM(amount) AS Total_Revenue,
    (SUM(amount) * 0.25) / SUM(amount) * 100 AS Profit_Margin_Pct
FROM sales
WHERE order_status != 'Cancelled';

-- Power BI DAX:
-- Total Profit = CALCULATE(SUM(sales[amount]) * 0.25)
-- Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0) * 100

-- KPI 3: Average Order Value (AOV)
SELECT 
    AVG(amount) AS Average_Order_Value
FROM sales
WHERE order_status != 'Cancelled';

-- Power BI DAX:
-- Avg Order Value = AVERAGE(sales[amount])
-- OR: Avg Order Value = DIVIDE(SUM(sales[amount]), COUNTROWS(sales[amount]), 0)

-- KPI 4: Total Orders
SELECT 
    COUNT(*) AS Total_Orders
FROM sales
WHERE order_status != 'Cancelled';

-- Power BI DAX:
-- Total Orders = COUNTROWS(sales)
-- Active Orders = CALCULATE(COUNTROWS(sales), sales[order_status] <> "Cancelled")

-- KPI 5: Total Quantity Sold
SELECT 
    SUM(quantity) AS Total_Quantity
FROM sales
WHERE order_status != 'Cancelled';

-- ================================================================
-- GROWTH KPIs
-- ================================================================

-- KPI 6: Revenue Growth % (Month over Month)
WITH monthly_revenue AS (
    SELECT 
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        SUM(amount) AS revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT 
    year,
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY year, month) AS prev_month_revenue,
    (revenue - LAG(revenue, 1) OVER (ORDER BY year, month)) / 
     NULLIF(LAG(revenue, 1) OVER (ORDER BY year, month), 0) * 100 AS MoM_Growth_Pct
FROM monthly_revenue
ORDER BY year, month;

-- Power BI DAX:
-- Revenue Growth % = 
-- VAR CurrentRevenue = SUM(sales[amount])
-- VAR PreviousRevenue = CALCULATE(SUM(sales[amount]), PREVIOUSMONTH(sales[order_date]))
-- RETURN DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue, 0) * 100

-- KPI 7: Revenue Growth % (Year over Year)
WITH yearly_revenue AS (
    SELECT 
        YEAR(order_date) AS year,
        SUM(amount) AS revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY YEAR(order_date)
)
SELECT 
    year,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY year) AS prev_year_revenue,
    (revenue - LAG(revenue, 1) OVER (ORDER BY year)) / 
     NULLIF(LAG(revenue, 1) OVER (ORDER BY year), 0) * 100 AS YoY_Growth_Pct
FROM yearly_revenue
ORDER BY year;

-- Power BI DAX:
-- YoY Growth % = 
-- VAR CurrentRevenue = SUM(sales[amount])
-- VAR PreviousRevenue = CALCULATE(SUM(sales[amount]), SAMEPERIODLASTYEAR(sales[order_date]))
-- RETURN DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue, 0) * 100

-- KPI 8: Quarter over Quarter Growth
WITH quarterly_revenue AS (
    SELECT 
        YEAR(order_date) AS year,
        QUARTER(order_date) AS quarter,
        SUM(amount) AS revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY YEAR(order_date), QUARTER(order_date)
)
SELECT 
    year,
    quarter,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY year, quarter) AS prev_quarter,
    (revenue - LAG(revenue, 1) OVER (ORDER BY year, quarter)) / 
     NULLIF(LAG(revenue, 1) OVER (ORDER BY year, quarter), 0) * 100 AS QoQ_Growth_Pct
FROM quarterly_revenue
ORDER BY year, quarter;

-- ================================================================
-- PROFITABILITY KPIs
-- ================================================================

-- KPI 9: Profit Margin %
SELECT 
    category,
    SUM(amount) AS revenue,
    SUM(amount) * 0.25 AS profit,
    SUM(amount) * 0.25 / SUM(amount) * 100 AS profit_margin_pct
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category;

-- Power BI DAX:
-- Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0) * 100

-- KPI 10: Gross Profit Margin by Category
SELECT 
    category,
    SUM(amount) AS total_revenue,
    SUM(amount) * 0.25 AS gross_profit,
    SUM(amount) * 0.75 AS cost_of_goods_sold,
    SUM(amount) * 0.25 / SUM(amount) * 100 AS gross_margin_pct
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category
ORDER BY gross_margin_pct DESC;

-- KPI 11: Net Profit Margin
SELECT 
    SUM(amount) AS revenue,
    SUM(amount) * 0.25 AS gross_profit,
    SUM(amount) * 0.05 AS operating_expenses,
    SUM(amount) * 0.25 - SUM(amount) * 0.05 AS net_profit,
    (SUM(amount) * 0.25 - SUM(amount) * 0.05) / SUM(amount) * 100 AS net_margin_pct
FROM sales
WHERE order_status != 'Cancelled';

-- ================================================================
-- CUSTOMER KPIs
-- ================================================================

-- KPI 12: Customer Count
SELECT 
    COUNT(DISTINCT city) AS unique_customers
FROM sales
WHERE order_status != 'Cancelled';

-- Power BI DAX:
-- Unique Customers = DISTINCTCOUNT(sales[city])

-- KPI 13: Customer Contribution %
WITH customer_revenue AS (
    SELECT 
        city,
        SUM(amount) AS customer_revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY city
),
total_revenue AS (
    SELECT SUM(amount) AS total FROM sales WHERE order_status != 'Cancelled'
)
SELECT 
    cr.city,
    cr.customer_revenue,
    cr.customer_revenue / tr.total * 100 AS customer_contribution_pct
FROM customer_revenue cr
CROSS JOIN total_revenue tr
ORDER BY customer_contribution_pct DESC;

-- Power BI DAX:
-- Customer Contribution % = 
-- DIVIDE(
--     SUM(sales[amount]),
--     CALCULATE(SUM(sales[amount]), ALL(sales)),
--     0
-- ) * 100

-- KPI 14: Repeat Customer Rate
WITH customer_orders AS (
    SELECT 
        city,
        COUNT(*) AS order_count
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY city
)
SELECT 
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS repeat_customer_rate_pct,
    SUM(CASE WHEN order_count = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS one_time_customer_rate_pct
FROM customer_orders;

-- Power BI DAX:
-- Repeat Customer Rate = 
-- VAR RepeatCustomers = CALCULATE(COUNTROWS(sales), FILTER(sales, sales[order_count] > 1))
-- VAR TotalCustomers = COUNTROWS(sales)
-- RETURN DIVIDE(RepeatCustomers, TotalCustomers, 0) * 100

-- KPI 15: Customer Lifetime Value (CLV)
SELECT 
    city,
    state,
    MIN(order_date) AS first_purchase,
    MAX(order_date) AS last_purchase,
    COUNT(*) AS total_orders,
    SUM(amount) AS lifetime_value,
    SUM(amount) / COUNT(*) AS avg_order_value,
    DATEDIFF(MAX(order_date), MIN(order_date)) AS customer_tenure_days
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY city, state;

-- ================================================================
-- OPERATIONAL KPIs
-- ================================================================

-- KPI 16: Cancellation Rate
SELECT 
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS cancellation_rate_pct
FROM sales;

-- Power BI DAX:
-- Cancellation Rate = 
-- DIVIDE(
--     CALCULATE(COUNTROWS(sales), sales[order_status] = "Cancelled"),
--     COUNTROWS(sales),
--     0
-- ) * 100

-- KPI 17: Delivery Success Rate
SELECT 
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status LIKE '%Delivered%' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN order_status LIKE '%Delivered%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS delivery_success_rate_pct
FROM sales
WHERE order_status != 'Cancelled';

-- Power BI DAX:
-- Delivery Success Rate = 
-- DIVIDE(
--     CALCULATE(COUNTROWS(sales), sales[order_status] CONTAINS "Delivered"),
--     COUNTROWS(sales),
--     0
-- ) * 100

-- KPI 18: Average Delivery Time (in days)
SELECT 
    AVG(DATEDIFF(order_date, order_date)) AS avg_delivery_days
FROM sales
WHERE order_status LIKE '%Delivered%';

-- Note: This requires actual delivery date tracking

-- KPI 19: Order Fulfillment Rate
SELECT 
    fulfilment_method,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status NOT IN ('Cancelled', 'Pending') THEN 1 ELSE 0 END) AS fulfilled_orders,
    SUM(CASE WHEN order_status NOT IN ('Cancelled', 'Pending') THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS fulfillment_rate_pct
FROM sales
GROUP BY fulfilment_method;

-- KPI 20: Late Delivery Rate
SELECT 
    COUNT(*) AS total_shipped,
    SUM(CASE WHEN DATEDIFF(CURRENT_DATE, order_date) > 7 THEN 1 ELSE 0 END) AS late_deliveries,
    SUM(CASE WHEN DATEDIFF(CURRENT_DATE, order_date) > 7 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_delivery_rate_pct
FROM sales
WHERE order_status = 'Shipped';

-- ================================================================
-- REGIONAL KPIs
-- ================================================================

-- KPI 21: Regional Contribution %
WITH regional_revenue AS (
    SELECT 
        state,
        SUM(amount) AS revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY state
),
total_revenue AS (
    SELECT SUM(amount) AS total FROM sales WHERE order_status != 'Cancelled'
)
SELECT 
    rr.state,
    rr.revenue,
    rr.revenue / tr.total * 100 AS regional_contribution_pct
FROM regional_revenue rr
CROSS JOIN total_revenue tr
ORDER BY regional_contribution_pct DESC;

-- Power BI DAX:
-- Regional Contribution % = 
-- DIVIDE(
--     SUM(sales[amount]),
--     CALCULATE(SUM(sales[amount]), ALL(sales)),
--     0
-- ) * 100

-- KPI 22: State Revenue Share
SELECT 
    state,
    SUM(amount) AS state_revenue,
    SUM(SUM(amount)) OVER () AS total_revenue,
    SUM(amount) / SUM(SUM(amount)) OVER () * 100 AS revenue_share_pct
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY state
ORDER BY revenue_share_pct DESC;

-- KPI 23: Top 10 States Contribution
WITH state_revenue AS (
    SELECT 
        state,
        SUM(amount) AS revenue,
        RANK() OVER (ORDER BY SUM(amount) DESC) AS state_rank
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY state
)
SELECT 
    SUM(CASE WHEN state_rank <= 10 THEN revenue ELSE 0 END) AS top_10_revenue,
    SUM(revenue) AS total_revenue,
    SUM(CASE WHEN state_rank <= 10 THEN revenue ELSE 0 END) / SUM(revenue) * 100 AS top_10_contribution_pct
FROM state_revenue;

-- ================================================================
-- PRODUCT KPIs
-- ================================================================

-- KPI 24: Product Count
SELECT 
    COUNT(DISTINCT sku) AS unique_products
FROM sales;

-- Power BI DAX:
-- Unique Products = DISTINCTCOUNT(sales[sku])

-- KPI 25: Category Revenue Share
SELECT 
    category,
    SUM(amount) AS category_revenue,
    SUM(amount) / SUM(SUM(amount)) OVER () * 100 AS category_revenue_share_pct
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category
ORDER BY category_revenue_share_pct DESC;

-- KPI 26: Product Return Rate (if data available)
-- Assuming 'Returned' status exists
SELECT 
    category,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) AS returns,
    SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS return_rate_pct
FROM sales
GROUP BY category;

-- KPI 27: Best Selling Product (by Quantity)
SELECT 
    sku,
    category,
    SUM(quantity) AS total_units_sold,
    SUM(amount) AS total_revenue
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY sku, category
ORDER BY total_units_sold DESC
LIMIT 1;

-- KPI 28: Product Launch Success Rate
SELECT 
    MONTH(order_date) AS launch_month,
    COUNT(DISTINCT sku) AS new_products,
    SUM(amount) AS launch_revenue,
    AVG(amount) AS avg_first_month_revenue
FROM sales
GROUP BY MONTH(order_date);

-- ================================================================
-- EFFICIENCY KPIs
-- ================================================================

-- KPI 29: Revenue per Order
SELECT 
    SUM(amount) / COUNT(*) AS revenue_per_order
FROM sales
WHERE order_status != 'Cancelled';

-- KPI 30: Revenue per Customer
SELECT 
    SUM(amount) / COUNT(DISTINCT city) AS revenue_per_customer
FROM sales
WHERE order_status != 'Cancelled';

-- KPI 31: Revenue per Day
SELECT 
    order_date,
    SUM(amount) AS daily_revenue
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY order_date
ORDER BY daily_revenue DESC
LIMIT 10;

-- KPI 32: Revenue per Category
SELECT 
    category,
    SUM(amount) AS category_revenue,
    SUM(quantity) AS total_units,
    SUM(amount) / SUM(quantity) AS revenue_per_unit
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category;

-- KPI 33: Inventory Turnover Rate
SELECT 
    category,
    SUM(quantity) AS units_sold,
    SUM(amount) AS cost_of_goods,
    AVG(amount) AS avg_inventory_value,
    SUM(quantity) / NULLIF(AVG(quantity), 0) AS turnover_rate
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category;

-- ================================================================
-- COMPOSITE KPIs
-- ================================================================

-- KPI 34: Customer Acquisition Cost (CAC)
-- Assuming marketing_cost is tracked separately
SELECT 
    SUM(amount) / NULLIF(COUNT(DISTINCT city), 0) AS customer_acquisition_cost
FROM sales
WHERE order_status != 'Cancelled';

-- KPI 35: Return on Investment (ROI)
SELECT 
    SUM(amount) AS revenue,
    SUM(amount) * 0.75 AS total_investment,
    SUM(amount) * 0.25 AS profit,
    (SUM(amount) * 0.25) / (SUM(amount) * 0.75) * 100 AS roi_pct
FROM sales
WHERE order_status != 'Cancelled';

-- KPI 36: Customer Retention Rate
WITH monthly_customers AS (
    SELECT 
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        COUNT(DISTINCT city) AS active_customers
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT 
    year,
    month,
    active_customers,
    LAG(active_customers) OVER (ORDER BY year, month) AS prev_month_customers,
    (active_customers - LAG(active_customers) OVER (ORDER BY year, month)) / 
     NULLIF(LAG(active_customers) OVER (ORDER BY year, month), 0) * 100 AS customer_growth_rate
FROM monthly_customers
ORDER BY year, month;

-- KPI 37: Conversion Rate (Pending to Shipped)
SELECT 
    SUM(CASE WHEN order_status = 'Pending' THEN 1 ELSE 0 END) AS pending_orders,
    SUM(CASE WHEN order_status IN ('Shipped', 'Delivered') THEN 1 ELSE 0 END) AS converted_orders,
    SUM(CASE WHEN order_status IN ('Shipped', 'Delivered') THEN 1 ELSE 0 END) * 100.0 / 
     NULLIF(SUM(CASE WHEN order_status = 'Pending' THEN 1 ELSE 0 END), 0) AS conversion_rate
FROM sales;

-- ================================================================
-- TIME-BASED KPIs
-- ================================================================

-- KPI 38: Day-over-Day Growth
WITH daily_revenue AS (
    SELECT 
        order_date,
        SUM(amount) AS daily_revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY order_date
)
SELECT 
    order_date,
    daily_revenue,
    LAG(daily_revenue, 1) OVER (ORDER BY order_date) AS prev_day_revenue,
    (daily_revenue - LAG(daily_revenue, 1) OVER (ORDER BY order_date)) / 
     NULLIF(LAG(daily_revenue, 1) OVER (ORDER BY order_date), 0) * 100 AS DoD_Growth_Pct
FROM daily_revenue
ORDER BY order_date;

-- KPI 39: Week-over-Week Growth
WITH weekly_revenue AS (
    SELECT 
        WEEK(order_date) AS week_num,
        YEAR(order_date) AS year,
        SUM(amount) AS weekly_revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY WEEK(order_date), YEAR(order_date)
)
SELECT 
    year,
    week_num,
    weekly_revenue,
    LAG(weekly_revenue, 1) OVER (ORDER BY year, week_num) AS prev_week_revenue,
    (weekly_revenue - LAG(weekly_revenue, 1) OVER (ORDER BY year, week_num)) / 
     NULLIF(LAG(weekly_revenue, 1) OVER (ORDER BY year, week_num), 0) * 100 AS WoW_Growth_Pct
FROM weekly_revenue
ORDER BY year, week_num;

-- KPI 40: Seasonality Index
WITH monthly_avg AS (
    SELECT 
        MONTH(order_date) AS month,
        AVG(SUM(amount)) AS avg_monthly_revenue
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY MONTH(order_date)
),
total_avg AS (
    SELECT AVG(SUM(amount)) AS overall_avg
    FROM sales
    WHERE order_status != 'Cancelled'
    GROUP BY MONTH(order_date)
)
SELECT 
    ma.month,
    ma.avg_monthly_revenue,
    ta.overall_avg,
    ma.avg_monthly_revenue / ta.overall_avg AS seasonality_index
FROM monthly_avg ma
CROSS JOIN total_avg ta
ORDER BY ma.month;

-- ================================================================
-- DAX MEASURES FOR POWER BI
-- ================================================================

/*
--- CORE MEASURES ---
Total Revenue = SUM(sales[amount])
Total Orders = COUNTROWS(sales)
Total Profit = [Total Revenue] * 0.25
Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0) * 100
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

--- GROWTH MEASURES ---
Revenue Growth % = 
VAR Current = [Total Revenue]
VAR Previous = CALCULATE([Total Revenue], PREVIOUSMONTH(sales[order_date]))
RETURN DIVIDE(Current - Previous, Previous, 0) * 100

YoY Growth % = 
VAR Current = [Total Revenue]
VAR Previous = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(sales[order_date]))
RETURN DIVIDE(Current - Previous, Previous, 0) * 100

--- CUSTOMER MEASURES ---
Unique Customers = DISTINCTCOUNT(sales[city])
Customer Contribution % = DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(sales)), 0) * 100
Repeat Customer Rate = DIVIDE(COUNTROWS(FILTER(sales, sales[order_count] > 1)), [Total Orders], 0) * 100

--- OPERATIONAL MEASURES ---
Cancellation Rate = DIVIDE(CALCULATE(COUNTROWS(sales), sales[order_status] = "Cancelled"), [Total Orders], 0) * 100
Delivery Rate = DIVIDE(CALCULATE(COUNTROWS(sales), CONTAINS(sales, sales[order_status], "Delivered")), [Total Orders], 0) * 100

--- TIME INTELLIGENCE ---
Running Total = TOTALYTD([Total Revenue], sales[order_date])
YTD Revenue = TOTALYTD([Total Revenue], sales[order_date])
MTD Revenue = TOTALMTD([Total Revenue], sales[order_date])
QTD Revenue = TOTALQTD([Total Revenue], sales[order_date])

--- MOVING AVERAGES ---
7-Day Moving Avg = AVERAGEX(DATESINPERIOD(sales[order_date], LASTDATE(sales[order_date]), -7, DAY), [Total Revenue])
30-Day Moving Avg = AVERAGEX(DATESINPERIOD(sales[order_date], LASTDATE(sales[order_date]), -30, DAY), [Total Revenue])
*/