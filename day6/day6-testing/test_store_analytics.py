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

def test_compute_line_total_basic():
    order = {"quantity": 4, "unit_price": 9.99}
    assert compute_line_total(order) == 39.96

def test_compute_line_total_zero_quantity():
    order = {"quantity": 0, "unit_price": 3.49}
    assert compute_line_total(order) == 0.00

def test_compute_line_total_negative_quantity_not_validated():
    order = {"quantity": -2, "unit_price": 10.0}
    assert compute_line_total(order) == -20.0

def test_summarize_by_product_basic():
    orders = [
                {"product": "Widget", "quantity": 4, "unit_price": 1.20},
                {"product": "Widget", "quantity": 1, "unit_price": 2.50},
            ]
    assert summarize_by_product(orders) ==  {
                                            "Widget": {
                                                "total_quantity": 5,
                                                "total_revenue": 7.30,
                                                "order_count": 2,
                                                }
                                            }

def test_top_n_products_negative_n_raises():
    summary = { # it can actually just be an empty dict like summary = {}
                "Widget": {"total_quantity": 5, "total_revenue": 7.30, "order_count": 2}
            }
    with pytest.raises(ValueError):
        top_n_products(summary, n=-1)

def test_top_n_products_fewer_products_than_n():
    summary = {
                "Widget": {"total_quantity": 5, "total_revenue": 7.30, "order_count": 2},
                "Gadget": {"total_quantity": 2, "total_revenue": 15.50, "order_count": 1}
            }
    result = top_n_products(summary, n=3)
    assert result == [
        ("Gadget", {"total_quantity": 2, "total_revenue": 15.50, "order_count": 1}),
        ("Widget", {"total_quantity": 5, "total_revenue": 7.30, "order_count": 2}),
    ]

def test_top_n_products_total_rev_tie():
    summary = {
                "Widget": {"total_quantity": 5, "total_revenue": 7.30, "order_count": 2},
                "Gadget": {"total_quantity": 2, "total_revenue": 7.30, "order_count": 1}
            }
    result = top_n_products(summary, n=3)
    assert result == [
        ("Gadget", {"total_quantity": 2, "total_revenue": 7.30, "order_count": 1}),
        ("Widget", {"total_quantity": 5, "total_revenue": 7.30, "order_count": 2}),
    ]

def test_loyalty_tier_boundary_at_100():
    # 100은 문서에 따르면 "silver" 구간에 포함되어야 함 (>=)
    assert loyalty_tier(100) == "silver"

def test_loyalty_tier_negative_raises():
    with pytest.raises(ValueError):
        loyalty_tier(-1)