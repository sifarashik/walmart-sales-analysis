import pandas as pd
import random
from datetime import datetime, timedelta
import os

os.makedirs("data", exist_ok=True)

ROWS = 2000

branches = ["A", "B", "C"]
cities = ["Yangon", "Mandalay", "Naypyitaw"]
customer_types = ["Member", "Normal"]
genders = ["Male", "Female"]
product_lines = [
    "Health and beauty",
    "Electronic accessories",
    "Home and lifestyle",
    "Sports and travel",
    "Food and beverages",
    "Fashion accessories"
]
payments = ["Cash", "Credit card", "Ewallet"]

data = []
start_date = datetime(2019, 1, 1)

for i in range(ROWS):
    unit_price = round(random.uniform(10, 100), 2)
    quantity = random.randint(1, 10)
    cogs = unit_price * quantity
    tax = round(cogs * 0.05, 2)
    total = round(cogs + tax, 2)

    row = {
        "invoice_id": f"INV-{1000+i}",
        "branch": random.choice(branches),
        "city": random.choice(cities),
        "customer_type": random.choice(customer_types),
        "gender": random.choice(genders),
        "product_line": random.choice(product_lines),
        "unit_price": unit_price,
        "quantity": quantity,
        "tax_5_percent": tax,
        "total": total,
        "date": (start_date + timedelta(days=random.randint(0, 90))).date(),
        "time": f"{random.randint(9,21)}:{random.randint(0,59):02d}",
        "payment": random.choice(payments),
        "cogs": cogs,
        "gross_margin_percentage": 4.76,
        "gross_income": tax,
        "rating": round(random.uniform(4, 10), 1)
    }
    data.append(row)

pd.DataFrame(data).to_csv("data/walmart_sales.csv", index=False)
print("✅ Dataset created")
