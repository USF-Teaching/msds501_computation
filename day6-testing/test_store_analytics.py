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

def test_compute_line_total():
    order = {
        "order_id": "1002",
        "product": "Gadget",
        "quantity": 2,
        "unit_price": 19.99,
        "customer_email": "bob@example.com",
    }
    assert compute_line_total(order) == 39.98

# test 2
def test_loyalty_tier(): # boundary check
    assert loyalty_tier(0) == "none"
    assert loyalty_tier(99.99) == "none"
    assert loyalty_tier(100.00) == "silver"
    assert loyalty_tier(499.99) == "silver"
    assert loyalty_tier(500) == "gold"
    assert loyalty_tier(999.99) == "gold"
    assert loyalty_tier(1000) == "platinum"

# Test 3
def test_summarize_by_product():
    assert summarize_by_product([]) == {}

# Test 4
def test_apply_bulk_discount_rate():
    with pytest.raises(ValueError):
        apply_bulk_discount([], 1, 1.1) # otu of range of discount rate

# Test 5
def test_top_n_products(): # val error negative num products
    with pytest.raises(ValueError):
        top_n_products({}, -5)