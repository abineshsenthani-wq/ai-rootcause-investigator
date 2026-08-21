import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

def generate_benchmark_dataset(num_rows=100000, output_path="./data/sample/synthetic_business_data_100k.csv"):
    np.random.seed(42)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Generating synthetic business dataset with {num_rows:,} rows...")

    # Date range: Jan 1, 2026 to July 31, 2026
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 7, 31)
    total_days = (end_date - start_date).days

    # Random dates
    random_days = np.random.randint(0, total_days, size=num_rows)
    dates = [start_date + timedelta(days=int(d)) for d in random_days]

    # Categories
    regions = np.random.choice(["West", "East", "North", "South"], size=num_rows, p=[0.3, 0.3, 0.2, 0.2])
    categories = np.random.choice(["Electronics", "Apparel", "Home & Kitchen", "Office Goods"], size=num_rows)
    channels = np.random.choice(["Online", "Retail Store", "Partner"], size=num_rows, p=[0.5, 0.35, 0.15])
    segments = np.random.choice(["Consumer", "Corporate", "Small Business"], size=num_rows, p=[0.6, 0.25, 0.15])

    # Products A to F
    product_ids = np.random.choice(["Prod_A", "Prod_B", "Prod_C", "Prod_D", "Prod_E", "Prod_F"], size=num_rows)

    quantity = np.random.randint(1, 10, size=num_rows)
    unit_price = np.random.uniform(20.0, 500.0, size=num_rows).round(2)
    discount = np.random.uniform(0.0, 0.25, size=num_rows).round(2)

    # Base revenue & profit
    revenue = quantity * unit_price * (1.0 - discount)
    profit = revenue * np.random.uniform(0.15, 0.40, size=num_rows)
    delivery_days = np.random.normal(3.0, 0.8, size=num_rows).round(1)
    delivery_days = np.clip(delivery_days, 1.0, 10.0)
    marketing_spend = np.random.uniform(100.0, 1000.0, size=num_rows).round(2)

    df = pd.DataFrame({
        "order_id": [f"ORD_{i+100000}" for i in range(num_rows)],
        "order_date": [d.strftime("%Y-%m-%d") for d in dates],
        "customer_id": [f"CUST_{np.random.randint(1000, 9999)}" for _ in range(num_rows)],
        "product_id": product_ids,
        "product_category": categories,
        "region": regions,
        "sales_channel": channels,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount": discount,
        "revenue": revenue.round(2),
        "profit": profit.round(2),
        "delivery_days": delivery_days,
        "customer_segment": segments,
        "marketing_spend": marketing_spend
    })

    # INTRODUCE CONTROLLED EVENTS IN JULY (July = Month 7)
    july_mask = (df["order_date"] >= "2026-07-01") & (df["order_date"] <= "2026-07-31")
    west_mask = df["region"] == "West"
    prod_c_mask = df["product_id"] == "Prod_C"

    # Event 1 & 2: Heavy West Region drop in July (-42%)
    df.loc[july_mask & west_mask, "revenue"] *= 0.58
    df.loc[july_mask & west_mask, "profit"] *= 0.50

    # Event 3: Product C drop in July (-36%)
    df.loc[july_mask & prod_c_mask, "revenue"] *= 0.64

    # Event 4: Delivery Days increase in West in July (+31%)
    df.loc[july_mask & west_mask, "delivery_days"] += 1.8

    # Event 5: Inject 20 explicit transaction anomalies
    anomaly_indices = np.random.choice(df.index, size=20, replace=False)
    df.loc[anomaly_indices, "revenue"] = np.random.uniform(25000.0, 95000.0, size=20).round(2)

    df.to_csv(output_path, index=False)
    print(f"Successfully created benchmark dataset at '{output_path}' ({os.path.getsize(output_path)/(1024*1024):.2f} MB)")

if __name__ == "__main__":
    generate_benchmark_dataset()
