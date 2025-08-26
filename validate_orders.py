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
)

# Create destination folder
OUTPUT_FOLDER = Path("output/")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Load source data (orders and product inventory)
orders_df = e_orders()
inventory_dict = e_inventory_dict()

# List to collect validation issues
issues = []

# Validate each order and get issue code
for _, order in orders_df.iterrows():
    if issue_code := check_invalid_product_id(order):
        issues.append({"order_id": order["order_id"], "issue_code": issue_code})
    if issue_code := check_exceeded_inventory(order):
        issues.append({"order_id": order["order_id"], "issue_code": issue_code})
    if issue_code := check_missing_shipping_date(order):
        issues.append({"order_id": order["order_id"], "issue_code": issue_code})
    if issue_code := check_negative_quantity(order):
        issues.append({"order_id": order["order_id"], "issue_code": issue_code})
    if issue_code := check_price_mismatch(order):
        issues.append({"order_id": order["order_id"], "issue_code": issue_code})
    if issue_code := check_quantity_outlier(order):
        issues.append({"order_id": order["order_id"], "issue_code": issue_code})
    if issue_code := check_temporal_inconsistency(order):
        issues.append({"order_id": order["order_id"], "issue_code": issue_code})

# Convert issue list to DataFrame
issues_df = pd.DataFrame(issues)

# Save invalid orders with issues
issues_df.to_csv(OUTPUT_FOLDER / "invalid_orders.csv", index=False)

# Extract valid orders
invalid_ids = set(issues_df["order_id"])
valid_orders_df = orders_df[~orders_df["order_id"].isin(invalid_ids)]

# Save valid orders
valid_orders_df.to_csv(OUTPUT_FOLDER / "valid_orders.csv", index=False)
