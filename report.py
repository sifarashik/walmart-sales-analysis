import os
from fpdf import FPDF
import pandas as pd
import sqlite3

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "walmart.db")
CHARTS_FOLDER = os.path.join(BASE_DIR, "..", "charts")
REPORT_PATH = os.path.join(BASE_DIR, "..", "Walmart_Sales_Report.pdf")

# -------------------------------
# Connect to DB
# -------------------------------
conn = sqlite3.connect(DB_PATH)

# -------------------------------
# Read data for report
# -------------------------------
total_sales = pd.read_sql("SELECT SUM(total) AS total_sales FROM walmart_sales", conn)["total_sales"][0]

df_branch = pd.read_sql("SELECT branch, SUM(total) AS sales FROM walmart_sales GROUP BY branch", conn)
df_product = pd.read_sql("SELECT product_line, SUM(total) AS sales FROM walmart_sales GROUP BY product_line", conn)
df_kpi = pd.read_sql("""
    SELECT COUNT(*) AS total_orders,
           SUM(total) AS total_revenue,
           AVG(total) AS avg_order_value,
           AVG(rating) AS avg_rating
    FROM walmart_sales
""", conn)

conn.close()

# -------------------------------
# Create PDF
# -------------------------------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Walmart Sales Analysis Report", 0, 1, "C")
pdf.ln(10)

# Total Sales
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, f"Total Sales: ${total_sales:.2f}", 0, 1)
pdf.ln(5)

# KPIs
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Key Performance Indicators (KPIs):", 0, 1)
pdf.set_font("Arial", "", 12)
for col in df_kpi.columns:
    pdf.cell(0, 8, f"{col}: {df_kpi[col][0]:.2f}", 0, 1)
pdf.ln(5)

# Charts
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Charts:", 0, 1)
charts = ["product_sales.png", "branch_sales.png", "sales_distribution.png",
          "monthly_sales_trend.png", "rating_vs_sales.png"]

for chart in charts:
    chart_path = os.path.join(CHARTS_FOLDER, chart)
    if os.path.exists(chart_path):
        pdf.image(chart_path, w=180)
        pdf.ln(10)

pdf.output(REPORT_PATH)
print(f"✅ PDF report generated: {REPORT_PATH}")
