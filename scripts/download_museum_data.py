import httpx
import os

url = "https://raw.githubusercontent.com/anvarnarz/praktikum_datasets/main/museum_visitors.csv"
output_path = "data/museum_visitors.csv"

os.makedirs("data", exist_ok=True)

try:
    print(f"Downloading museum_visitors.csv from {url}...")
    res = httpx.get(url, timeout=15.0)
    if res.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(res.content)
        print(f"Successfully saved {output_path} ({len(res.content)} bytes).")
    else:
        print(f"Failed to download: Status {res.status_code}")
except Exception as e:
        print(f"Error downloading: {e}")
