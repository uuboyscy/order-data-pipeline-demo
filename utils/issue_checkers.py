
import pandas as pd

from utils.datasource import e_inventory_dict, e_orders

INVALID_PRODUCT_ID = 1
EXCEEDED_INVENTORY = 2
NEGATIVE_QUANTITY = 3
PRICE_MISMATCH = 4
TEMPORAL_INCONSISTENCY = 5
MISSING_SHIPPING_DATE = 6
QUANTITY_OUTLIER = 7

ORDERS_DF = e_orders()
INVENTORY_DICT = e_inventory_dict()

def check_invalid_product_id(order):
    if order["product_id"] not in INVENTORY_DICT:
        return INVALID_PRODUCT_ID
    return None

def check_exceeded_inventory(order):
    product = INVENTORY_DICT.get(order["product_id"])
    if product and order["quantity"] > product["inventory_count"]:
        return EXCEEDED_INVENTORY
    return None

def check_negative_quantity(order):
    if order["quantity"] < 0:
        return NEGATIVE_QUANTITY
    return None

def check_price_mismatch(order):
    product = INVENTORY_DICT.get(order["product_id"])
    if product and order["price"] != product["price"]:
        return PRICE_MISMATCH
    return None

def check_temporal_inconsistency(order):
    if pd.notna(order["shipping_date"]) and order["shipping_date"] < order["order_date"]:
        return TEMPORAL_INCONSISTENCY
    return None

def check_missing_shipping_date(order):
    if order["order_status"] == "Shipped" and pd.isna(order["shipping_date"]):
        return MISSING_SHIPPING_DATE
    return None

def check_quantity_outlier(order):
    product_id = order["product_id"]
    historical = ORDERS_DF[
        (ORDERS_DF["product_id"] == product_id) &
        (ORDERS_DF["order_date"] < order["order_date"])
    ]["quantity"]
    if len(historical) >= 2:
        m = historical.mean()
        s = historical.std()
        if s > 0 and order["quantity"] > m + 2 * s:
            return QUANTITY_OUTLIER
    return None

def t_checker(orders_df: pd.DataFrame)-> pd.DataFrame:
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
    return pd.DataFrame(issues)
