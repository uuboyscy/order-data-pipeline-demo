
## Implementation

This project is implemented in a modular and extensible way using Python.
The solution covers:

- Data validation and cleaning
- Business rule enforcement
- Fraud detection
- Historical anomaly identification
- Structured output generation for clean and invalid datasets

---

### Folder Structure

```
wonderland_demo/
├── validate_orders.py               # Entry point of the program
├── utils/
│   ├── datasource.py                # Data loading layer (currently reads from CSVs)
│   └── issue_checkers.py            # All rule-based issue detection logic
├── resources/
│   ├── orders.csv                   # Input: raw order data
│   ├── products.csv                 # Input: product inventory data
│   └── issue_code_mapping.csv       # Input: mapping of issue codes and descriptions
└── output/
    ├── valid_orders.csv             # Output: clean, validated orders
    ├── invalid_orders.csv           # Output: orders with issue codes
    └── all_orders_with_issue.csv    # Output: merged view with reasons
```

---

### Process Flow

| Step | Description |
|------|-------------|
| 1. `e_orders()` | Load order data from `orders.csv` |
| 2. `e_inventory_dict()` | Load product inventory into dictionary format |
| 3. `e_issue_code_mapping()` | Load issue code mapping with description |
| 4. `t_checker()` | Run all rule-based validations on each order |
| 5. `t_filter_valid_ids()` | Filter valid orders by excluding any order ID with known issues |
| 6. `t_all_orders_with_issue()` | Join orders with issues and descriptions for full audit trail |
| 7. `l_df_to_file()` | Export all three result datasets to `output/` folder |

---

### Output Files

| File Name | Description |
|-----------|-------------|
| `valid_orders.csv` | All orders that passed all validation checks |
| `invalid_orders.csv` | A list of all order_id + issue_code combinations that failed checks |
| `all_orders_with_issue.csv` | Full detail including issue description for every invalid record |

---

### Issue Code Mapping

This project uses numerical codes to represent each issue type. The `issue_code_mapping.csv` provides descriptions.

| Hint No. | Issue Code | Constant Name             | Description from Hint                                                                 |
|----------|------------|---------------------------|----------------------------------------------------------------------------------------|
| Hint 1   | 1          | INVALID_PRODUCT_ID        | Ensure all product_id in orders exist in product_inventory                             |
| Hint 2   | 2          | EXCEEDED_INVENTORY        | Ensure quantity in orders doesn’t exceed available inventory                           |
| Hint 2   | 3          | NEGATIVE_QUANTITY         | Detect and flag any orders with negative quantities                                     |
| Hint 2   | 4          | PRICE_MISMATCH            | Detect and flag any orders with price discrepancies                                     |
| Hint 3   | 5          | TEMPORAL_INCONSISTENCY    | Flag any orders where the shipping_date is earlier than the order_date                 |
| Hint 3   | 6          | MISSING_SHIPPING_DATE     | Flag orders where the shipping date is missing (for shipped orders)                    |
| Hint 4   | 7          | POTENTIAL_FRAUD           | Identify any orders with quantities more than 2 std dev above avg in last 30 days      |

---

### Highlights

- **Extensibility:** All issue-checking logic is modular. To add a new rule, simply define a new function in `issue_checkers.py` and include it in the check loop.
- **Data Source Flexibility:** `datasource.py` supports refactoring to connect to a database instead of CSVs later on.
- **Debug-Friendly:** `all_orders_with_issue.csv` gives full traceability of what went wrong and why.
