from pathlib import Path

import pandas as pd

from utils.datasource import e_inventory_dict, e_issue_code_mapping, e_orders
from utils.issue_checkers import t_checker

# Create destination folder
OUTPUT_FOLDER = Path("output/")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

def t_filter_valid_ids(orders_df: pd.DataFrame, issues_df:pd.DataFrame) -> pd.DataFrame:
    # Extract valid orders
    invalid_ids = set(issues_df["order_id"])
    return orders_df[~orders_df["order_id"].isin(invalid_ids)]

def t_all_orders_with_issue(
        orders_df:pd.DataFrame,
        issues_df:pd.DataFrame,
        issue_code_mapping_df:pd.DataFrame,
    ) -> pd.DataFrame:
    return orders_df.merge(
        issues_df,
        how="left",
        left_on="order_id",
        right_on="order_id",
    ).merge(
        issue_code_mapping_df,
        how="left",
        left_on="issue_code",
        right_on="issue_code"
    ).sort_values(["order_id", "customer_id"])

def l_df_to_file(df: pd.DataFrame ,file_name: str) -> None:
    df.to_csv(OUTPUT_FOLDER / file_name, index=False)


if __name__ == "__main__":
    orders_df = e_orders()
    inventory_dict = e_inventory_dict()
    issue_code_mapping_df = e_issue_code_mapping()

    issues_df = t_checker(orders_df)

    all_orders_with_issue_df = t_all_orders_with_issue(
        orders_df,
        issues_df,
        issue_code_mapping_df,
    )

    valid_orders_df = t_filter_valid_ids(orders_df, issues_df)

    l_df_to_file(issues_df, "invalid_orders.csv")
    l_df_to_file(valid_orders_df, "valid_orders.csv")
    l_df_to_file(all_orders_with_issue_df, "all_orders_with_issue.csv")
