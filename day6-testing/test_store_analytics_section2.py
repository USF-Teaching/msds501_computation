"""
test_store_analytics.py

Starter file for the "write your own tests" exercise.

pytest and the module under test are already imported below, and there's
one fully-worked example test to show you the pattern. Everything after
that is up to you: add your own test functions (name them test_something)
that check store_analytics.py against its docstrings.

Run your tests from this folder with:
    pytest -v
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


# --- Your tests go below here ----------------------------------------------

# make sure valid output for compute_line_total
def test_compute_line_total():
    order = {
        "order_id": "1001",
        "product": "widget",
        "quantity": 4,
        "unit_price": 9.99,
        "customer_email": "alice@example.com",
    } 
    output = compute_line_total(order)
    assert output == 39.96


# loyalty_tier returns the right tier for a given spend
def test_loyalty_tier():
    assert loyalty_tier(50) == "none"
    assert loyalty_tier(1500) == "platinum"


# top_n_products ranks by revenue, highest first
def test_top_n_products():
    summary = {
        "widget": {"total_quantity": 5, "total_revenue": 50.0, "order_count": 2},
        "gadget": {"total_quantity": 1, "total_revenue": 200.0, "order_count": 1},
    }
    top = top_n_products(summary, n=1)
    assert top[0][0] == "gadget"


# apply_bulk_discount lowers the price of a qualifying order
def test_apply_bulk_discount():
    orders = [{"quantity": 10, "unit_price": 10.0}]
    discounted = apply_bulk_discount(orders, min_quantity=5, discount_rate=0.1)
    assert discounted[0]["unit_price"] == 9.0


# summarize_by_product returns empty dict for empty input
def test_summarize_by_product_empty():
    assert summarize_by_product([]) == {}


# parse_order_row raises ValueError when the row isn't 5 fields
def test_parse_order_row_wrong_field_count():
    with pytest.raises(ValueError):
        parse_order_row(["1001", "Widget", "4"])