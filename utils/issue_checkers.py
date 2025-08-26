
import pandas as pd

from utils.datasource import e_inventory_dict, e_orders

ORDERS_DF = e_orders()
INVENTORY_DICT = e_inventory_dict()

def check_invalid_product_id(order):
    if order["product_id"] not in INVENTORY_DICT:
        return 1  # INVALID_PRODUCT_ID
    return None

def check_exceeded_inventory(order):
    product = INVENTORY_DICT.get(order["product_id"])
    if product and order["quantity"] > product["inventory_count"]:
        return 2  # EXCEEDED_INVENTORY
    return None

def check_negative_quantity(order):
    if order["quantity"] < 0:
        return 3  # NEGATIVE_QUANTITY
    return None

def check_price_mismatch(order):
    product = INVENTORY_DICT.get(order["product_id"])
    if product and order["price"] != product["price"]:
        return 4  # PRICE_MISMATCH
    return None

def check_temporal_inconsistency(order):
    if pd.notna(order["shipping_date"]) and order["shipping_date"] < order["order_date"]:
        return 5  # TEMPORAL_INCONSISTENCY
    return None

def check_missing_shipping_date(order):
    if order["order_status"] == "Shipped" and pd.isna(order["shipping_date"]):
        return 6  # MISSING_SHIPPING_DATE
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
            return 7  # QUANTITY_OUTLIER
    return None
