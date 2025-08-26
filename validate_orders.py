from pathlib import Path

import pandas as pd

from utils.datasource import e_inventory_dict, e_orders
from utils.issue_checkers import (
    check_exceeded_inventory,
    check_invalid_product_id,
    check_missing_shipping_date,
    check_negative_quantity,
    check_price_mismatch,
    check_quantity_outlier,
    check_temporal_inconsistency,
    checker_task,
)

# Create destination folder
OUTPUT_FOLDER = Path("output/")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Load source data (orders and product inventory)
orders_df = e_orders()
inventory_dict = e_inventory_dict()

# List to collect validation issues
issues_df = checker_task(orders_df)

# Save invalid orders with issues
issues_df.to_csv(OUTPUT_FOLDER / "invalid_orders.csv", index=False)

# Extract valid orders
invalid_ids = set(issues_df["order_id"])
valid_orders_df = orders_df[~orders_df["order_id"].isin(invalid_ids)]

# Save valid orders
valid_orders_df.to_csv(OUTPUT_FOLDER / "valid_orders.csv", index=False)
