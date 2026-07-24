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
# Test that compute_line_total correctly multiplies quantity * price
# and rounds the final answer to 2 decimal places.
def test_compute_line_total_rounding():

    # Create a sample order
    order = {
        "order_id": "1002",
        "product": "widget",
        "quantity": 3,
        "unit_price": 2.555,
        "customer_email": "bob@example.com",
    }

    # 3 * 2.555 = 7.665
    # Rounded to 2 decimal places should be 7.67
    assert compute_line_total(order) == 7.67


# Test that summarize_by_product correctly handles an empty list.
# The function should return an empty dictionary when there are no orders.
def test_summarize_by_product_empty_list():

    # Empty list should produce an empty summary.
    assert summarize_by_product([]) == {}


# Test that top_n_products raises a ValueError
# when a negative value is passed for n.
def test_top_n_products_negative_n():

    # pytest expects a ValueError to be raised.
    # If no error occurs, the test will fail.
    with pytest.raises(ValueError):
        top_n_products({}, -1)


# Test that apply_bulk_discount returns a NEW list
# and does not modify the original orders list.
def test_apply_bulk_discount_does_not_modify_original():

    # Create one sample order.
    orders = [
        {
            "order_id": "1003",
            "product": "book",
            "quantity": 10,
            "unit_price": 20.00,
            "customer_email": "test@example.com",
        }
    ]

    # Apply a 10% discount to any order with quantity >= 5.
    discounted = apply_bulk_discount(orders, 5, 0.10)

    # Check that the ORIGINAL order was not changed.
    assert orders[0]["unit_price"] == 20.00

    # Check that the returned copy has the discounted price.
    # $20.00 with a 10% discount becomes $18.00.
    assert discounted[0]["unit_price"] == 18.00


# Test that spending exactly $500 places a customer
# into the "gold" loyalty tier.
def test_loyalty_tier_gold_boundary():

    # $500 is the minimum value for the gold tier.
    assert loyalty_tier(500) == "gold"
