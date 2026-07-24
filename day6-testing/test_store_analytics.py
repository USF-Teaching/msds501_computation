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

@pytest.mark.parametrize(
    "input_val, expected_context, expected_val",
    [
        ([],pytest.raises(ValueError), None),
        (["", "Widget", "4", "9.99","alice@example.com" ], pytest.raises(ValueError), None),
        (["1001", "", "4", "9.99","alice@example.com" ], pytest.raises(ValueError), None),
        (["1001", "Widget", "4.0", "9.99", "alice@example.com"], pytest.raises(ValueError), None),
        (["1001", "Widget", "-4", "9.99", "alice@example.com"], pytest.raises(ValueError), None),
        (["1001", "Widget", "4", "-9.99", "alice@example.com"], pytest.raises(ValueError), None),
        (["1001", "Widget", "1", "0", "alice@example.com"], nullcontext(), {
            "order_id": "1001",
            "product": "widget",
            "quantity": 1,
            "unit_price": 0.0,
            "customer_email": "alice@example.com",
        }),
    ]
)
def test_parse_order_row_invalid_row(input_val,expected_context, expected_val):
    with expected_context:
        assert parse_order_row(input_val) == expected_val

def test_compute_line_total():
    assert compute_line_total({"quantity": 10, "unit_price": 4.50}) == (10*4.5)

def test_top_n_products_invalid_n():
    with pytest.raises(ValueError):
        assert top_n_products({}, -1) is None
def test_top_n_products():
    products = {
        "A": {
            "total_quantity": 5,
            "total_revenue": 50,   # rounded to 2 decimals
            "order_count": 10,
        },
        "B": {
            "total_quantity": 16,
            "total_revenue": 65.5,   # rounded to 2 decimals
            "order_count": 12,
        }
    }
    assert top_n_products(products, 1) == [("B", {
            "total_quantity": 16,
            "total_revenue": 65.5,   # rounded to 2 decimals
            "order_count": 12,
        })]