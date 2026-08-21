import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_benchmark_dataset(num_rows: int = 500000, output_path: str = "data/sample_sales.csv"):
    print(f"Generating massive enterprise business dataset ({num_rows:,} rows)...")
    np.random.seed(42)

    start_date = datetime(2026, 1, 1)
    date_range_days = 210  # Jan 1 to July 31, 2026

    # Fast vectorized date creation
    random_days = np.random.randint(0, date_range_days, size=num_rows)
    date_offsets = pd.to_timedelta(random_days, unit='D')
    date_series = pd.Timestamp(start_date) + date_offsets
    formatted_dates = date_series.strftime('%Y-%m-%d')

    regions = ["North", "South", "East", "West"]
    region_probs = [0.25, 0.25, 0.25, 0.25]

    categories = ["Electronics", "Office Supplies", "Furniture", "Software", "Hardware"]
    category_probs = [0.3, 0.25, 0.2, 0.15, 0.1]

    channels = ["Direct Sales", "Online Store", "Partner", "Wholesale"]
    segments = ["Enterprise", "SMB", "Consumer", "Government"]

    region_col = np.random.choice(regions, size=num_rows, p=region_probs)
    category_col = np.random.choice(categories, size=num_rows, p=category_probs)
    channel_col = np.random.choice(channels, size=num_rows)
    segment_col = np.random.choice(segments, size=num_rows)

    quantities = np.random.randint(1, 20, size=num_rows)
    unit_prices = np.random.choice([15.0, 45.0, 120.0, 350.0, 890.0, 1500.0], size=num_rows)
    discounts = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], size=num_rows, p=[0.5, 0.2, 0.15, 0.1, 0.05])

    gross_revenue = quantities * unit_prices * (1.0 - discounts)
    profit_margin = np.random.uniform(0.15, 0.40, size=num_rows)
    profits = gross_revenue * profit_margin

    base_delivery_days = (np.random.poisson(lam=4, size=num_rows) + 1).astype(np.int64)
    marketing_spends = np.random.uniform(50, 500, size=num_rows)

    # Fast string ID creation
    order_ids = [f"ORD-{i:07d}" for i in range(1, num_rows + 1)]
    cust_ids = [f"CUST-{i}" for i in np.random.randint(1000, 9999, size=num_rows)]
    prod_ids = [f"PROD-{i}" for i in np.random.randint(100, 999, size=num_rows)]


    df = pd.DataFrame({
        "order_id": order_ids,
        "order_date": formatted_dates,
        "customer_id": cust_ids,
        "product_id": prod_ids,
        "product_category": category_col,
        "region": region_col,
        "sales_channel": channel_col,
        "quantity": quantities,
        "unit_price": unit_prices,
        "discount": discounts,
        "revenue": gross_revenue,
        "profit": profits,
        "delivery_days": base_delivery_days,
        "customer_segment": segment_col,
        "marketing_spend": marketing_spends
    })

    # Controlled Drop & Operational Correlation in July 2026 for West region
    is_july = date_series.month == 7
    is_west = df["region"] == "West"


    # Reduce revenue in July for West region by ~45%
    df.loc[is_july & is_west, "revenue"] *= 0.55
    df.loc[is_july & is_west, "profit"] *= 0.50

    # Spike delivery days in West region during July by +31%
    july_west_delivery = (df.loc[is_july & is_west, "delivery_days"].values * 1.5).astype(np.int64)
    df.loc[is_july & is_west, "delivery_days"] = july_west_delivery

    # Controlled High Severity Anomalies
    anomaly_indices = np.random.choice(df.index, size=25, replace=False)
    df.loc[anomaly_indices, "revenue"] = df.loc[anomaly_indices, "revenue"] * 12.0
    df.loc[anomaly_indices, "profit"] = df.loc[anomaly_indices, "profit"] * -5.0

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully saved to '{output_path}' ({os.path.getsize(output_path) / (1024*1024):.2f} MB).")

if __name__ == "__main__":
    rows = 500000
    if len(sys.argv) > 1:
        try:
            rows = int(sys.argv[1])
        except ValueError:
            pass
    generate_benchmark_dataset(num_rows=rows)
