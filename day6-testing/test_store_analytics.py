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


# --- Example test (already written for you) -------------------------------
def test_parse_order_invalid_length():
    row = ['1001', 'Widget'] # does not meet the requirement of 5 fields
    with pytest.raises(ValueError):
        parse_order_row(row)
        assert ValueError(f"expected 5 fields, got {len(row)}: {row}")

def test_parse_order_empty_quantity():
    row = ["1001", "Widget", "", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)
        assert ValueError(f"quantity must be a whole number, got {quantity_str!r}")

def test_parse_order_negative_quantity():
    row = ["1001", "Widget", "-100", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)
        assert ValueError(f"quantity must be positive, got {quantity}")

def test_parse_order_empty_order_id():
    row = ["", "Widget", "-100", "9.99", "alice@example.com"]   
    with pytest.raises(ValueError):
        parse_order_row(row)
        assert ValueError("order_id cannot be empty")

def test_parse_order_empty_product():
    row = ["1001", "", "4", "9.99", "alice@example.com"]
    with pytest.raises(ValueError) as error:
        parse_order_row(row)
        assert str(error.value) == "product cannot be empty"

def test_parse_order_quantity_whole_number():
    row = ["1001", "Widget", "4.1111", "9.99", "alice@example.com"]
    with pytest.raises(ValueError) as error:
        parse_order_row(row)
        assert str(error.value) == f"quantity must be a whole number, got {quantity_str!r}"


def test_compute_line_total_multiplies_and_rounds(): # Check if math is mathing
    order = {
        "quantity": 3,
        "unit_price": 4.567,
    }
    result = compute_line_total(order)
    assert result == 13.70

def test_compute_line_total_correct_answer(): # Check if math is mathing
    row = ["1001", "Widget", "4", "9.99", "alice@example.com"]
    order = parse_order_row(row)
    line_total = compute_line_total(order)
    assert line_total == 39.96


def test_compute_line_total_rounds_result(): # Check if math is mathing
    order = {
        "quantity": 7,
        "unit_price": 1.115,
    }

    result = compute_line_total(order)

    assert result == round(7 * 1.115, 2)

def test_summarize_by_product_matches_products(): # Check if product info matches
    orders = [
        {
            "order_id": "1",
            "product": "Widget",
            "quantity": 2,
            "unit_price": 5.00,
            "customer_email": "a@example.com",
        },
        {
            "order_id": "2",
            "product": "Widget",
            "quantity": 3,
            "unit_price": 4.00,
            "customer_email": "b@example.com",
        },
        {
            "order_id": "3",
            "product": "Gadget",
            "quantity": 1,
            "unit_price": 20.00,
            "customer_email": "c@example.com",
        },
    ]

    result = summarize_by_product(orders)

    assert result == {
        "Widget": {
            "total_quantity": 5,
            "total_revenue": 22.00,
            "order_count": 2,
        },
        "Gadget": {
            "total_quantity": 1,
            "total_revenue": 20.00,
            "order_count": 1,
        },
    }

def test_sort_key_prioritizes_revenue_then_product_name(): # Test if _sort_key() works even if it was not imported
    summary = {
        "scooter": {
            "total_revenue": 50.0, 
            "total_quantity": 1, 
            "order_count": 1
        },
        "ipad": {
            "total_revenue": 50.0, 
            "total_quantity": 1, 
            "order_count": 1
        },
        "watch": {
            "total_revenue": 75.0, 
            "total_quantity": 1, 
            "order_count": 1
        },
    }

    result = top_n_products(summary)

    assert [product for product, n in result] == [
        "watch",
        "ipad",
        "scooter",
    ]

def test_apply_bulk_discount_negative_discount_rate():
    with pytest.raises(ValueError):
        apply_bulk_discount(
            orders=[],
            min_quantity=5,
            discount_rate=-1,
        )

def test_loyalty_tier_max_values(): # check if max value
    total_spend = 1500
    tier = loyalty_tier(total_spend)
    assert tier == "platinum"

def test_loyalty_tier_negative_values(): # check if negative value
    total_spend = -10
    with pytest.raises(ValueError):
        loyalty_tier(total_spend)
