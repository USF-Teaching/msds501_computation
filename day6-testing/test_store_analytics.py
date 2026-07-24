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

@pytest.mark.parametrize("input_row, pattern_match", [
    (["1001", "Widget", "4", "9.99"], "expected 5 fields"),
    (["1001", "Widget1", "Widget2", "4", "9.99", "alice@example.com"], "expected 5 fields"),
    ([" ", "Widget1", "4", "9.99", "alice@example.com"], "order_id cannot"),
    (["1001", " ", "4", "9.99", "alice@example.com"], "product cannot"),
    (["1001", "Widget", "3.6", "9.99", "alice@example.com"], "must be a whole"),
    (["1001", "Widget", "0", "9.99", "alice@example.com"], "must be positive"),
    (["1001", "Widget", "-2", "9.99", "alice@example.com"], "must be positive"),
    (["1001", "Widget", "4", "hello", "alice@example.com"], "must be a number"),
    (["1001", "Widget", "4", "-9.99", "alice@example.com"], "cannot be negative")
])
def test_parse_order_row_invalid_row_raises_valueError(input_row, pattern_match):
    with pytest.raises(ValueError, match=pattern_match):
        parse_order_row(input_row)


def test_compute_line_total():
    order = {
        "order_id": "1001",
        "product": "widget",
        "quantity": 4,
        "unit_price": 9.99,
        "customer_email": "alice@example.com",
    }
    expected_ret = 39.96
    assert compute_line_total(order) == expected_ret, "Computed total does not match expected"
