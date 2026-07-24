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

def test_parse_order_row_valid_row1():
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
# Test 1: parse_order_row should raise ValueError for negative quantity
def test_parse_order_row_negative_quantity():
    row = ["1002", "Laptop", "-3", "999.99", "bob@example.com"]

    with pytest.raises(ValueError):
        parse_order_row(row)


# Test 2: compute_line_total should correctly multiply and round
def test_compute_line_total():
    order = {
        "order_id": "1003",
        "product": "mouse",
        "quantity": 3,
        "unit_price": 19.99,
        "customer_email": "test@example.com",
    }

    assert compute_line_total(order) == 59.97


# Test 3: summarize_by_product should combine quantities and revenue
def test_summarize_by_product():
    orders = [
        {
            "order_id": "1",
            "product": "keyboard",
            "quantity": 2,
            "unit_price": 50.00,
            "customer_email": "a@test.com",
        },
        {
            "order_id": "2",
            "product": "keyboard",
            "quantity": 1,
            "unit_price": 50.00,
            "customer_email": "b@test.com",
        },
    ]

    summary = summarize_by_product(orders)

    assert summary == {
        "keyboard": {
            "total_quantity": 3,
            "total_revenue": 150.00,
            "order_count": 2,
        }
    }


# Test 4: loyalty_tier should return gold for spending between 500 and 999.99
def test_loyalty_tier_gold():
    assert loyalty_tier(750) == "gold"


# Test 5: apply_bulk_discount should discount qualifying orders without modifying original
def test_apply_bulk_discount():
    orders = [
        {
            "order_id": "10",
            "product": "monitor",
            "quantity": 5,
            "unit_price": 100.00,
            "customer_email": "c@test.com",
        }
    ]

    discounted = apply_bulk_discount(orders, min_quantity=5, discount_rate=0.10)

    # New list has discounted price
    assert discounted[0]["unit_price"] == 90.00

    # Original list remains unchanged
    assert orders[0]["unit_price"] == 100.00