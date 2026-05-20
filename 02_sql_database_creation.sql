-- ================================================================
-- AMAZON E-COMMERCE SALES DATABASE
-- MySQL Database Setup Script
-- ================================================================
-- Author: Business Intelligence Analyst
-- Purpose: Create database schema for Amazon Sales Analytics
-- ================================================================

-- ================================================================
-- STEP 1: CREATE DATABASE
-- ================================================================

CREATE DATABASE IF NOT EXISTS amazon_sales_db;
USE amazon_sales_db;

-- ================================================================
-- STEP 2: CREATE TABLE QUERIES
-- ================================================================

-- Main Sales Table
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    order_status VARCHAR(50),
    fulfilment_method VARCHAR(50),
    sales_channel VARCHAR(50),
    ship_service_level VARCHAR(50),
    style VARCHAR(50),
    sku VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    size VARCHAR(20),
    asin VARCHAR(20),
    courier_status VARCHAR(50),
    quantity INT DEFAULT 0,
    currency VARCHAR(10),
    amount DECIMAL(12, 2) DEFAULT 0.00,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code INT,
    country VARCHAR(10),
    promotion_ids TEXT,
    b2b_flag BOOLEAN,
    fulfilled_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id),
    INDEX idx_order_date (order_date),
    INDEX idx_category (category),
    INDEX idx_state (state),
    INDEX idx_order_status (order_status)
);

-- Date Dimension Table
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_name VARCHAR(20),
    day_of_week INT,
    day_of_month INT,
    day_of_year INT,
    week_of_year INT,
    month_name VARCHAR(20),
    month_number INT,
    quarter_number INT,
    year_number INT,
    fiscal_year VARCHAR(10),
    season VARCHAR(20),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    INDEX idx_full_date (full_date)
);

-- Product Dimension Table
CREATE TABLE IF NOT EXISTS dim_product (
    product_key INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    asin VARCHAR(20),
    product_name VARCHAR(200),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    style VARCHAR(50),
    size VARCHAR(20),
    avg_cost DECIMAL(10, 2),
    std_cost DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sku (sku),
    INDEX idx_category (category)
);

-- Customer Dimension Table
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code INT,
    country VARCHAR(10),
    customer_segment VARCHAR(50),
    customer_tier VARCHAR(20),
    first_order_date DATE,
    last_order_date DATE,
    total_orders INT,
    total_revenue DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_customer_id (customer_id),
    INDEX idx_state (state)
);

-- Geography Dimension Table
CREATE TABLE IF NOT EXISTS dim_geography (
    geography_key INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(100),
    region VARCHAR(50),
    postal_code INT,
    country VARCHAR(10),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    INDEX idx_state (state),
    INDEX idx_region (region)
);

-- Fulfilment Fact Table
CREATE TABLE IF NOT EXISTS fact_fulfilment (
    fulfilment_key INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(50),
    fulfilment_method VARCHAR(50),
    ship_service_level VARCHAR(50),
    courier_status VARCHAR(50),
    order_date DATE,
    ship_date DATE,
    delivery_date DATE,
    days_to_ship INT,
    days_to_deliver INT,
    is_delayed BOOLEAN,
    fulfilment_cost DECIMAL(10, 2),
    INDEX idx_order_id (order_id),
    INDEX idx_fulfilment_method (fulfilment_method)
);

-- ================================================================
-- STEP 3: ALTER TABLE QUERIES
-- ================================================================

-- Add new columns to existing table
ALTER TABLE sales 
ADD COLUMN year INT AFTER order_date,
ADD COLUMN month INT AFTER year,
ADD COLUMN month_name VARCHAR(20) AFTER month,
ADD COLUMN quarter INT AFTER month_name,
ADD COLUMN day_of_week VARCHAR(20) AFTER quarter,
ADD COLUMN is_weekend BOOLEAN AFTER day_of_week,
ADD COLUMN is_cancelled BOOLEAN AFTER is_weekend,
ADD COLUMN is_delivered BOOLEAN AFTER is_cancelled,
ADD COLUMN has_promotion BOOLEAN AFTER is_delivered,
ADD COLUMN revenue_tier VARCHAR(20) AFTER has_promotion,
ADD COLUMN season VARCHAR(20) AFTER revenue_tier;

-- Add computed column for profit calculation
ALTER TABLE sales 
ADD COLUMN profit DECIMAL(12, 2) GENERATED ALWAYS AS (amount * 0.25) STORED;

-- Add index for performance optimization
ALTER TABLE sales 
ADD INDEX idx_year_month (year, month),
ADD INDEX idx_state_category (state, category),
ADD INDEX idx_date_status (order_date, order_status);

-- Rename columns
ALTER TABLE sales 
CHANGE COLUMN ship_service_level ship_service_level VARCHAR(50),
CHANGE COLUMN sales_channel sales_channel VARCHAR(50);

-- Modify data types
ALTER TABLE sales 
MODIFY COLUMN order_status ENUM('Shipped', 'Shipped - Delivered to Buyer', 'Cancelled', 'Pending', 'Refunded');

-- ================================================================
-- STEP 4: INSERT QUERIES
-- ================================================================

-- Insert sample data (for testing)
INSERT INTO sales (
    order_id, order_date, order_status, fulfilment_method, sales_channel,
    ship_service_level, style, sku, category, size, asin, courier_status,
    quantity, currency, amount, city, state, postal_code, country,
    promotion_ids, b2b_flag, fulfilled_by
) VALUES 
('405-8078784-5731545', '2022-04-30', 'Cancelled', 'Merchant', 'Amazon.in',
 'Standard', 'SET389', 'SET389-KR-NP-S', 'Set', 'S', 'B09KXVBD7Z', '',
 0, 'INR', 647.62, 'MUMBAI', 'MAHARASHTRA', 400081, 'IN',
 '', FALSE, 'Easy Ship'),

('171-9198151-1101146', '2022-04-30', 'Shipped - Delivered to Buyer', 'Merchant', 'Amazon.in',
 'Standard', 'JNE3781', 'JNE3781-KR-XXXL', 'kurta', '3XL', 'B09K3WFS32', 'Shipped',
 1, 'INR', 406.00, 'BENGALURU', 'KARNATAKA', 560085, 'IN',
 'Amazon PLCC Free-Financing', FALSE, 'Easy Ship'),

('404-0687676-7273146', '2022-04-30', 'Shipped', 'Amazon', 'Amazon.in',
 'Expedited', 'JNE3371', 'JNE3371-KR-XL', 'kurta', 'XL', 'B07WV4JV4D', 'Shipped',
 1, 'INR', 329.00, 'NAVI MUMBAI', 'MAHARASHTRA', 410210, 'IN',
 'IN Core Free Shipping', FALSE, '');

-- ================================================================
-- STEP 5: IMPORT DATA FROM CSV
-- ================================================================

-- Option 1: Using LOAD DATA INFILE (MySQL Server)
LOAD DATA INFILE '/path/to/cleaned_data/amazon_sales_cleaned.csv'
INTO TABLE sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, order_date, order_status, fulfilment_method, sales_channel,
 ship_service_level, style, sku, category, size, asin, courier_status,
 quantity, currency, amount, city, state, postal_code, country,
 promotion_ids, b2b_flag, fulfilled_by, @var1, @var2, @var3, @var4, @var5,
 @var6, @var7, @var8, @var9, @var10, @var11)
SET 
    year = @var1,
    month = @var2,
    month_name = @var3,
    quarter = @var4,
    day_of_week = @var5,
    is_weekend = @var6,
    is_cancelled = @var7,
    is_delivered = @var8,
    has_promotion = @var9,
    revenue_tier = @var10,
    season = @var11;

-- Option 2: Using MySQL Workbench Import Wizard
-- Right-click on database -> Table Data Import Wizard -> Select CSV file

-- Option 3: Using mysqlimport
-- mysqlimport --local --ignore-lines=1 --fields-terminated-by=',' amazon_sales_db sales /path/to/amazon_sales_cleaned.csv

-- ================================================================
-- STEP 6: STORED PROCEDURES
-- ================================================================

DELIMITER //

-- Procedure to refresh date dimension
CREATE PROCEDURE refresh_dim_date()
BEGIN
    DECLARE start_date DATE DEFAULT '2022-01-01';
    DECLARE end_date DATE DEFAULT '2023-12-31';
    DECLARE current_date DATE;
    
    TRUNCATE TABLE dim_date;
    SET current_date = start_date;
    
    WHILE current_date <= end_date DO
        INSERT INTO dim_date (
            date_key, full_date, day_name, day_of_week, day_of_month,
            day_of_year, week_of_year, month_name, month_number, quarter_number,
            year_number, season, is_weekend
        ) VALUES (
            DATE_FORMAT(current_date, '%Y%m%d'),
            current_date,
            DAYNAME(current_date),
            DAYOFWEEK(current_date),
            DAYOFMONTH(current_date),
            DAYOFYEAR(current_date),
            WEEKOFYEAR(current_date),
            MONTHNAME(current_date),
            MONTH(current_date),
            QUARTER(current_date),
            YEAR(current_date),
            CASE 
                WHEN MONTH(current_date) IN (3, 4, 5) THEN 'Spring'
                WHEN MONTH(current_date) IN (6, 7, 8) THEN 'Summer'
                WHEN MONTH(current_date) IN (9, 10, 11) THEN 'Autumn'
                ELSE 'Winter'
            END,
            IF(DAYNAME(current_date) IN ('Saturday', 'Sunday'), TRUE, FALSE)
        );
        
        SET current_date = DATE_ADD(current_date, INTERVAL 1 DAY);
    END WHILE;
END //

DELIMITER ;

-- ================================================================
-- STEP 7: VIEWS FOR COMMON ANALYSIS
-- ================================================================

-- Monthly Sales Summary View
CREATE OR REPLACE VIEW v_monthly_sales AS
SELECT 
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    MONTHNAME(order_date) AS month_name,
    COUNT(*) AS total_orders,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    SUM(CASE WHEN is_cancelled THEN 1 ELSE 0 END) AS cancelled_orders,
    SUM(CASE WHEN is_delivered THEN 1 ELSE 0 END) AS delivered_orders
FROM sales
WHERE order_date IS NOT NULL
GROUP BY YEAR(order_date), MONTH(order_date), MONTHNAME(order_date)
ORDER BY year, month;

-- Category Performance View
CREATE OR REPLACE VIEW v_category_performance AS
SELECT 
    category,
    COUNT(*) AS total_orders,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    SUM(profit) AS total_profit,
    RANK() OVER (ORDER BY SUM(amount) DESC) AS revenue_rank
FROM sales
WHERE order_status != 'Cancelled'
GROUP BY category;

-- State Performance View
CREATE OR REPLACE VIEW v_state_performance AS
SELECT 
    state,
    COUNT(*) AS total_orders,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    SUM(CASE WHEN is_delivered THEN 1 ELSE 0 END) / COUNT(*) * 100 AS delivery_rate
FROM sales
GROUP BY state
ORDER BY total_revenue DESC;

-- ================================================================
-- STEP 8: INDEX OPTIMIZATION
-- ================================================================

-- Composite indexes for common queries
CREATE INDEX idx_composite_1 ON sales (order_date, category, amount);
CREATE INDEX idx_composite_2 ON sales (state, category, order_status);
CREATE INDEX idx_composite_3 ON sales (year, month, order_status);

-- Full-text index for promotion search
ALTER TABLE sales ADD FULLTEXT INDEX ft_promotion (promotion_ids);

-- ================================================================
-- STEP 9: TRIGGERS
-- ================================================================

DELIMITER //

-- Trigger to update customer metrics on new order
CREATE TRIGGER tr_after_order_insert
AFTER INSERT ON sales
FOR EACH ROW
BEGIN
    DECLARE cust_exists INT;
    
    SELECT COUNT(*) INTO cust_exists FROM dim_customer WHERE customer_id = NEW.order_id;
    
    IF cust_exists = 0 THEN
        INSERT INTO dim_customer (customer_id, total_orders, total_revenue)
        VALUES (NEW.order_id, 1, NEW.amount);
    ELSE
        UPDATE dim_customer 
        SET total_orders = total_orders + 1,
            total_revenue = total_revenue + NEW.amount
        WHERE customer_id = NEW.order_id;
    END IF;
END //

DELIMITER ;

-- ================================================================
-- STEP 10: DATABASE DOCUMENTATION
-- ================================================================

COMMENT ON TABLE sales IS 'Main fact table containing all sales transactions';
COMMENT ON TABLE dim_date IS 'Date dimension table for time-based analysis';
COMMENT ON TABLE dim_product IS 'Product dimension table for product analytics';
COMMENT ON TABLE dim_customer IS 'Customer dimension table for customer insights';
COMMENT ON TABLE dim_geography IS 'Geography dimension table for regional analysis';
COMMENT ON TABLE fact_fulfilment IS 'Fulfilment fact table for operational analytics';

COMMENT ON COLUMN sales.order_id IS 'Unique order identifier';
COMMENT ON COLUMN sales.amount IS 'Order total amount in INR';
COMMENT ON COLUMN sales.profit IS 'Calculated profit (25% of amount)';
COMMENT ON COLUMN sales.b2b_flag IS 'Business to business order indicator';