## Requirement
There are two CSV files: Orders (transactional data of customer orders) and Products (inventory
levels for the products available for sale).

### Tasks

#### Please use Python to finish below tasks:
    1. Validate and clean the data
    2. Detect and resolve inconsistencies and outliers
    3. Apply business rules and identify potential fraud
    4. Analyze historical patterns of inventory issues and missing order data

#### Hint:
1. Validate the Referential Integrity:
Ensure all product_id in orders exist in product_inventory
2. Check Business Logic for Orders:
Ensure quantity in orders doesn’t exceed available inventory (inventory_count in
product_inventory)
Detect and flag any orders with negative quantities or price discrepancies
3. Temporal Consistency Check:
Flag any orders where the shipping_date is earlier than the order_date
Flag orders where the shipping date is missing (for shipped orders)
4. Identify Potential Fraud:
Identify any orders with quantities that deviate significantly from historical order patterns
for that product (e.g., more than 2 standard deviations above the average quantity ordered
in the last 30 days)
Detect any orders marked as "shipped" but with no corresponding shipping_date.
5. Generate Cleaned and Validated Dataset:
Output the clean dataset and the dataset with all identified issues and their reasons
(Issues: Invalid product IDs, Exceeded inventory, Price mismatches, Temporal
inconsistencies [shipping date issues], Potential fraud [outliers in order quantity])


### Sample Output

#### Orders Table

| order\_id | customer\_id | product\_id | quantity | price  | order\_date | shipping\_date | order\_status |
| --------- | ------------ | ----------- | -------- | ------ | ----------- | -------------- | ------------- |
| 1001      | C001         | P001        | 2        | 100.00 | 2025-05-01  | 2025-05-03     | Shipped       |
| 1002      | C002         | P002        | 5        | 120.00 | 2025-05-02  | 2025-05-06     | Pending       |
| 1003      | C003         | P005        | 1        | 30.00  | 2025-05-03  | 2025-05-04     | Cancelled     |
| 1004      | C004         | P001        | 3        | 100.00 | 2025-05-04  | 2025-05-07     | Shipped       |
| 1005      | C005         | P003        | 10       | 50.00  | 2025-05-04  | NULL           | Pending       |
| 1006      | C006         | P006        | 1        | 200.00 | 2025-05-05  | 2025-05-06     | Shipped       |


#### Product Inventory Table

| product\_id | product\_name | category  | inventory\_count | price  |
| ----------- | ------------- | --------- | ---------------- | ------ |
| P001        | Widget A      | Gadgets   | 100              | 100.00 |
| P002        | Widget B      | Gadgets   | 50               | 120.00 |
| P003        | Widget C      | Tools     | 30               | 50.00  |
| P004        | Widget D      | Tools     | 200              | 80.00  |
| P005        | Widget E      | Furniture | 0                | 30.00  |
| P006        | Widget F      | Furniture | 10               | 200.00 |


## Implementation
> For Details, please refer to [Implementation.md](Implementation.md)

### Flow chart

```mermaid
flowchart TD
    A[Start] --> B[Load orders.csv]
    A --> C[Load products.csv]
    A --> D[Load issue_code_mapping.csv]
    B --> E[Run issue checkers: t_checker]
    C --> E
    D --> F[Join orders + issues + descriptions]
    E --> F
    E --> G[Filter valid orders]
    E --> H[Export invalid_orders.csv]
    G --> I[Export valid_orders.csv]
    F --> J[Export all_orders_with_issue.csv]
```

### Input Files (resources/)
- orders.csv: Raw order data
- products.csv: Product inventory information
- issue_code_mapping.csv: Mapping of issue codes to descriptions

### Output Files (output/)
- valid_orders.csv: Cleaned valid orders
- invalid_orders.csv: Orders with issue codes
- all_orders_with_issue.csv: Orders joined with issue descriptions


## Analyze historical patterns of inventory issues and missing order data

### MART Table Ideas
- mart_inventory_violation_summary
    > Summarizes how often each product was ordered beyond its available inventory.
- mart_missing_shipping_summary
    > Counts and groups all shipped orders missing shipping dates, categorized by customer, product, and time window.
- mart_product_fraud_risk_score
    > Assigns a potential “fraud risk” score to products based on frequency and type of flagged issues.
- mart_issue_distribution_by_status
    > Distribution of issues across different order_status values.
