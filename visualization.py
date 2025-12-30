import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Paths setup
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # python folder
DB_PATH = os.path.join(BASE_DIR, "..", "walmart.db")  # project root
CHARTS_FOLDER = os.path.join(BASE_DIR, "..", "charts")
os.makedirs(CHARTS_FOLDER, exist_ok=True)  # create charts folder if not exists

# -------------------------------
# Connect to Database
# -------------------------------
conn = sqlite3.connect(DB_PATH)

# -------------------------------
# 1️⃣ Sales by Product Line (Bar chart)
# -------------------------------
df_product = pd.read_sql("""
    SELECT product_line, SUM(total) AS sales
    FROM walmart_sales
    GROUP BY product_line
""", conn)

plt.figure(figsize=(10,6))
plt.bar(df_product["product_line"], df_product["sales"], color='skyblue')
plt.xticks(rotation=45)
plt.title("Sales by Product Line")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_FOLDER, "product_sales.png"))
plt.close()

# -------------------------------
# 2️⃣ Sales by Branch (Bar chart)
# -------------------------------
df_branch = pd.read_sql("""
    SELECT branch, SUM(total) AS sales
    FROM walmart_sales
    GROUP BY branch
""", conn)

plt.figure(figsize=(6,4))
plt.bar(df_branch["branch"], df_branch["sales"], color='orange')
plt.title("Sales by Branch")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_FOLDER, "branch_sales.png"))
plt.close()

# -------------------------------
# 3️⃣ Sales Distribution by Product Line (Pie chart)
# -------------------------------
plt.figure(figsize=(8,8))
plt.pie(df_product["sales"], labels=df_product["product_line"], autopct="%1.1f%%", startangle=140)
plt.title("Sales Distribution by Product Line")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_FOLDER, "sales_distribution.png"))
plt.close()

# -------------------------------
# 4️⃣ Monthly Sales Trend (Line chart)
# -------------------------------
df_time = pd.read_sql("SELECT date, total FROM walmart_sales", conn)
df_time["date"] = pd.to_datetime(df_time["date"])
df_time["month"] = df_time["date"].dt.to_period("M")
monthly_sales = df_time.groupby("month")["total"].sum()

plt.figure(figsize=(10,6))
plt.plot(monthly_sales.index.astype(str), monthly_sales.values, marker='o', color='green')
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_FOLDER, "monthly_sales_trend.png"))
plt.close()

# -------------------------------
# 5️⃣ Rating vs Sales (Scatter plot)
# -------------------------------
df_rating = pd.read_sql("SELECT rating, total FROM walmart_sales", conn)
plt.figure(figsize=(8,6))
plt.scatter(df_rating["rating"], df_rating["total"], color='red', alpha=0.6)
plt.title("Rating vs Sales")
plt.xlabel("Customer Rating")
plt.ylabel("Sales Amount")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_FOLDER, "rating_vs_sales.png"))
plt.close()

# -------------------------------
# Close DB
# -------------------------------
conn.close()
print("✅ All charts saved successfully in charts folder")
