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

## 1
## verifying an exception is raised when an incorrect row length is input
def test_parder_order_row_wrong_number_fields():
    row = ["ID99", "phone", "2", "99.00"]

    with pytest.raises(ValueError):
        store_analytics.parse_order_row(row)

## 2
## verifying that user quantity input is non-negative

def test_parse_order_row_negative_quantity():
     row = ["ID99", "phone", "-2", "99.00", "customer@email.com"]

     with pytest.raises(ValueError):
         store_analytics.parse_order_row(row)

## 3
## verifying it returns correct total
##  create sample order in dictionary form and test function

def test_compute_line_total():

    order = {
        "quantity": 4,
        "unit_price": 5.25
    }

    assert store_analytics.compute_line_total(order) == 21.00

## 4
## verify the correctrounding
## create an order that reguires longer than 2 decimals

def test_compute_line_total_rounding():
    order = {
        "quantity": 3,
        "unit_price":0.333
    }

    assert store_analytics.compute_line_total(order) == 1.00

## 5
## verify an empty list returns an empty dictionary

def test_summarize_by_product_empty_list():
    result = store_analytics.summarize_by_product([])
    assert result == {}

## 6
## verify a single-order

def test_summarize_by_product_single_order():
        order = [
             {
             "order_id": "001",
             "product": "tablet",
        "quantity": 5,
        "unit_price": 5.00,
        "customer_email": "customer@email.com"
    }
        ]
        expected_result = {
             "tablet": {
                  "total_quantity": 5,
                  "total_revenue": 25.00,
                  "order_count": 1
             }
        }
        assert store_analytics.summarize_by_product(order) == expected_result

## 7
## verify multiple orders
def test_summarize_by_product_multiple_orders():
        orders = [
             {
             "order_id": "001",
             "product": "tablet",
        "quantity": 5,
        "unit_price": 5.00,
        "customer_email": "customer@email.com"
        },
        {
             "order_id": "002",
             "product": "tablet",
            "quantity": 2,
        "unit_price": 5.00,
        "customer_email": "customer@email.com"
        }
        ]
        expected_result = {
             "tablet": {
                  "total_quantity": 7,
                  "total_revenue": 35.00,
                  "order_count": 2
             }
        }
        assert store_analytics.summarize_by_product(orders) == expected_result

