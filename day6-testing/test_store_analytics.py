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

from pathlib import Path

import pytest

from store_analytics import (
    load_orders_from_csv,
    parse_order_row,
    summarize_by_product,
    top_n_products,
)


CSV_FILE = Path(__file__).with_name("sample_orders.csv")

# verifies that a negative quantity raises a ValueError.
def test_parse_order_row_rejects_negative_quantity():
    row = ["1003", "Widget", "-1", "5.00", "carol@example.com"]

    with pytest.raises(ValueError):
        parse_order_row(row)

# test checks that the function loads three orders and records two errors
def test_load_orders_from_csv():
    orders, errors = load_orders_from_csv(CSV_FILE)

    assert len(orders) == 3
    assert len(errors) == 2

# Checks the totals for gadget and widget
def test_summarize_by_product():
    orders, errors = load_orders_from_csv(CSV_FILE)

    summary = summarize_by_product(orders)

    assert summary["gadget"] == {
        "total_quantity": 3,
        "total_revenue": 59.97,
        "order_count": 2,
    }
    assert summary["widget"] == {
        "total_quantity": 4,
        "total_revenue": 39.96,
        "order_count": 1,
    }

# checks that gadget is ranked first because it has more total revenue than widget
def test_top_product():
    orders, errors = load_orders_from_csv(CSV_FILE)
    summary = summarize_by_product(orders)

    top_products = top_n_products(summary, n=1)

    assert top_products[0][0] == "gadget"