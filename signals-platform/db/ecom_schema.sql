-- Dimension: Customers
CREATE TABLE IF NOT EXISTS ecom.dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50) NOT NULL,
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(5)
);

-- Dimension: Products
CREATE TABLE IF NOT EXISTS ecom.dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_weight_g NUMERIC,
    product_length_cm NUMERIC,
    product_height_cm NUMERIC,
    product_width_cm NUMERIC
);

-- Fact: Orders & Order Items
CREATE TABLE IF NOT EXISTS ecom.fact_orders (
    order_id VARCHAR(50),
    order_item_id INT,
    customer_id VARCHAR(50) REFERENCES ecom.dim_customers(customer_id),
    product_id VARCHAR(50) REFERENCES ecom.dim_products(product_id),
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    price NUMERIC(10, 2),
    freight_value NUMERIC(10, 2),
    PRIMARY KEY (order_id, order_item_id)
);

-- Index critical time-series & foreign keys
CREATE INDEX IF NOT EXISTS idx_fact_orders_timestamp ON ecom.fact_orders(order_purchase_timestamp);
CREATE INDEX IF NOT EXISTS idx_fact_orders_customer ON ecom.fact_orders(customer_id);