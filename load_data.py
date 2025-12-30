import pandas as pd
import sqlite3
import os

# Current file folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # python folder
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "walmart_sales.csv")
DB_PATH = os.path.join(BASE_DIR, "..", "walmart.db")

# Load CSV
df = pd.read_csv(DATA_PATH)

# Save to DB
conn = sqlite3.connect(DB_PATH)
df.to_sql("walmart_sales", conn, if_exists="replace", index=False)
conn.close()

print("✅ Data loaded to database")
