import pandas as pd
import os

# ── 1. Load all three CSV files ──────────────────────────────────────────────
data_folder = "data"

files = [
    os.path.join(data_folder, "daily_sales_data_0.csv"),
    os.path.join(data_folder, "daily_sales_data_1.csv"),
    os.path.join(data_folder, "daily_sales_data_2.csv"),
]

# Read and concatenate all three files into one DataFrame
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

print(f"Total rows loaded: {len(df)}")
print(df.head())

# ── 2. Filter: Keep only Pink Morsels ────────────────────────────────────────
df = df[df["product"] == "pink morsel"]

print(f"Rows after filtering for Pink Morsels: {len(df)}")

# ── 3. Compute Sales = quantity × price ──────────────────────────────────────
# Strip the "$" sign from price and convert to float
df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)

df["sales"] = df["quantity"] * df["price"]

# ── 4. Select only the required columns ──────────────────────────────────────
output_df = df[["sales", "date", "region"]]

# ── 5. Write to output CSV ───────────────────────────────────────────────────
output_path = "output.csv"
output_df.to_csv(output_path, index=False)

print(f"\nOutput saved to: {output_path}")
print(f"Output shape: {output_df.shape}")
print(output_df.head(10))