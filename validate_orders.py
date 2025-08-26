from pathlib import Path

import pandas as pd

from utils.datasource import e_inventory_dict, e_orders
from utils.issue_checkers import t_checker

# Create destination folder
OUTPUT_FOLDER = Path("output/")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

def t_filter_invalid_ids(orders_df: pd.DataFrame, issues_df:pd.DataFrame) -> pd.DataFrame:
    # Extract valid orders
    invalid_ids = set(issues_df["order_id"])
    return orders_df[~orders_df["order_id"].isin(invalid_ids)]

def l_df_to_file(df: pd.DataFrame ,file_name: str) -> None:
    df.to_csv(OUTPUT_FOLDER / file_name, index=False)


if __name__ == "__main__":
    orders_df = e_orders()
    inventory_dict = e_inventory_dict()

    issues_df = t_checker(orders_df)

    valid_orders_df = t_filter_invalid_ids(orders_df, issues_df)

    l_df_to_file(issues_df, "invalid_orders.csv")
    l_df_to_file(valid_orders_df, "valid_orders.csv")
