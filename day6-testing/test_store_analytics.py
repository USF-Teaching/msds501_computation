"""
test_store_analytics.py
"""

import pytest
from store_analytics import (
    parse_order_row,
    compute_line_total,
    summarize_by_product,
    top_n_products,
    apply_bulk_discount,
    loyalty_tier,
    load_orders_from_csv,
    write_top_products_report,
)


# --- Example test (already written for you) -------------------------------

def test_parse_order_row_valid_row():
    row = ["1001", "Widget", "4", "9.99", "alice@example.com"]
    order = parse_order_row(row)
    assert order == {
        "order_id": "1001",
        "product": "widget",
        "quantity": 4,
        "unit_price": 9.99,
        "customer_email": "alice@example.com",
    }


# --- My tests -------------------------------------------------------------

# BOUNDARY + EXCEPTION: quantity of 0 is rejected.
def test_parse_order_row_rejects_zero_quantity():
    row = ["1001", "Widget", "0", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

# THRESHOLD: 500 is exactly the gold cutoff; 499 is still silver.
def test_loyalty_tier_gold_boundary():
    assert loyalty_tier(500) == "gold"
    assert loyalty_tier(499) == "silver"

# INVARIANT: apply_bulk_discount must NOT mutate the original orders.
def test_apply_bulk_discount_does_not_mutate_input():
    orders = [{"order_id": "1", "product": "widget", "quantity": 10,
               "unit_price": 10.00, "customer_email": "a@x.com"}]
    apply_bulk_discount(orders, min_quantity=5, discount_rate=0.1)
    assert orders[0]["unit_price"] == 10.00

# GROUPING: two orders of the same product roll up into one bucket.
def test_summarize_by_product_combines_same_product():
    orders = [
        {"product": "widget", "quantity": 2, "unit_price": 10.0},
        {"product": "widget", "quantity": 3, "unit_price": 10.0},
    ]
    summary = summarize_by_product(orders)
    assert summary["widget"]["total_quantity"] == 5
    assert summary["widget"]["order_count"] == 2

# EMPTY: an empty order list summarizes to an empty dict.
def test_summarize_by_product_empty():
    assert summarize_by_product([]) == {}

# TIE-BREAK: equal revenue -> alphabetical, so "apple" comes before "banana".
def test_top_n_products_breaks_ties_alphabetically():
    summary = {
        "banana": {"total_quantity": 1, "total_revenue": 100.0, "order_count": 1},
        "apple":  {"total_quantity": 1, "total_revenue": 100.0, "order_count": 1},
    }
    result = top_n_products(summary, n=2)
    assert result[0][0] == "apple"

# INTEGRATION: load_orders_from_csv keeps good rows, records bad ones.
def test_load_orders_from_csv_skips_bad_rows(tmp_path):
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(
        "order_id,product,quantity,unit_price,customer_email\n"
        "1001,Widget,4,9.99,alice@example.com\n"
        "1002,Gadget,-1,5.00,bob@example.com\n"
    )
    orders, errors = load_orders_from_csv(str(csv_file))
    assert len(orders) == 1
    assert len(errors) == 1
    assert "row 3" in errors[0]
