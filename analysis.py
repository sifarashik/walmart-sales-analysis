import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("walmart.db")

# -----------------------------
# 1️⃣ TOTAL SALES
# -----------------------------
print("🔹 Total Sales")
print(pd.read_sql("""
    SELECT ROUND(SUM(total),2) AS total_sales
    FROM walmart_sales
""", conn))


# -----------------------------
# 2️⃣ SALES BY BRANCH
# -----------------------------
print("\n🔹 Sales by Branch")
print(pd.read_sql("""
    SELECT branch,
           ROUND(SUM(total),2) AS sales
    FROM walmart_sales
    GROUP BY branch
    ORDER BY sales DESC
""", conn))


# -----------------------------
# 3️⃣ TOP SELLING PRODUCTS
# -----------------------------
print("\n🔹 Top Products (by Quantity)")
print(pd.read_sql("""
    SELECT product_line,
           SUM(quantity) AS total_quantity
    FROM walmart_sales
    GROUP BY product_line
    ORDER BY total_quantity DESC
""", conn))


# -----------------------------
# 4️⃣ KEY BUSINESS KPIs
# -----------------------------
print("\n🔹 Key Performance Indicators (KPIs)")
print(pd.read_sql("""
    SELECT 
        COUNT(invoice_id) AS total_orders,
        ROUND(SUM(total),2) AS total_revenue,
        ROUND(AVG(total),2) AS avg_order_value,
        ROUND(AVG(rating),2) AS avg_rating
    FROM walmart_sales
""", conn))


# -----------------------------
# 5️⃣ SALES BY CITY
# -----------------------------
print("\n🔹 Sales by City")
print(pd.read_sql("""
    SELECT city,
           ROUND(SUM(total),2) AS city_sales
    FROM walmart_sales
    GROUP BY city
    ORDER BY city_sales DESC
""", conn))


# -----------------------------
# 6️⃣ PROFIT ESTIMATION
# (Assume 70% cost)
# -----------------------------
print("\n🔹 Estimated Profit")
print(pd.read_sql("""
    SELECT ROUND(SUM(total - (unit_price * quantity * 0.7)),2) AS profit
    FROM walmart_sales
""", conn))


# -----------------------------
# 7️⃣ RATING vs SALES CORRELATION
# -----------------------------
print("\n🔹 Rating vs Sales Correlation")
df_corr = pd.read_sql("""
    SELECT rating, total
    FROM walmart_sales
""", conn)
print(df_corr.corr())


# Close DB
conn.close()
