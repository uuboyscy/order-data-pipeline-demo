"""Function to get data source from CSV files."""
from pathlib import Path

import pandas as pd

RESOURCES_FOLDER = Path("resources/")

def e_orders() -> pd.DataFrame:
    return pd.read_csv(RESOURCES_FOLDER / "orders.csv", parse_dates=["order_date", "shipping_date"])

def e_issue_code_mapping() -> pd.DataFrame:
    return pd.read_csv(RESOURCES_FOLDER / "issue_code_mapping.csv")

def e_inventory_dict() -> dict:
    """
    Get product info mapping.

    ```
    {
        'P001': {'product_name': 'Widget A', 'category': 'Gadgets', 'inventory_count': 100, 'price': 100.00},
        'P002': {'product_name': 'Widget B', 'category': 'Gadgets', 'inventory_count': 50, 'price': 120.00},
        'P003': {'product_name': 'Widget C', 'category': 'Tools', 'inventory_count': 30, 'price': 50.00},
        ...
    }
    ```
    """
    products = pd.read_csv(RESOURCES_FOLDER / "products.csv")
    return products.set_index("product_id").to_dict("index")
