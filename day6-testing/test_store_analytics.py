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

# --- parse_order_row -------------------------------

def test_parse_order_row_insufficient_arguments():
    with pytest.raises(ValueError):
        parse_order_row(["1004", "widget", "2", "3.00"]) 


def test_parse_order_row_reject_empty_order_id():
    with pytest.raises(ValueError):
        parse_order_row(["   ", "widget", "2", "3.00", "x@y.com"])

def test_parse_order_row_reject_empty_product():
    with pytest.raises(ValueError):
        parse_order_row(["1005", "  ", "2", "3.00", "x@y.com"])

def test_parse_order_row_strips_and_lowercases_product():
    row = ["1002", "  Super WIDGET  ", "1", "5.00", "x@y.com"]
    order = parse_order_row(row)
    assert order["product"] == "super widget"

def test_parse_order_row_reject_non_integer_quantity():
    with pytest.raises(ValueError):
        parse_order_row(["1006", "widget", "2.5", "3.00", "x@y.com"])

def test_parse_order_row_rejects_zero_quantity():
    with pytest.raises(ValueError):
        parse_order_row(["1007", "widget", "0", "3.00", "x@y.com"])

def test_parse_order_row_round_unit_price_decimals():
    row = ["1003", "widget", "2", "3.14159", "x@y.com"]
    order = parse_order_row(row)
    assert order["unit_price"] == 3.14

def test_parse_order_row_reject_negative_unit_price():
    with pytest.raises(ValueError):
        parse_order_row(["1008", "widget", "2", "-1.00", "x@y.com"])

def test_parse_order_row_accepts_zero_unit_price():
    order = parse_order_row(["1009", "freebie", "1", "0", "x@y.com"])
    assert order["unit_price"] == 0.0


# --- compute_line_total ----------------------------------------------------

def test_compute_line_total_multiplies_and_rounds():
    order = {"quantity": 7, "unit_price": 3.333}
    assert compute_line_total(order) == 23.33

# --- summarize_by_product --------------------------------------------------

def test_summarize_by_product_aggregates_repeated_products():
    orders = [
        {"product": "widget", "quantity": 2, "unit_price": 10.0},
        {"product": "widget", "quantity": 3, "unit_price": 10.0},
        {"product": "gadget", "quantity": 1, "unit_price": 4.0},
    ]
    summary = summarize_by_product(orders)
    assert summary["widget"] == {
        "total_quantity": 5,
        "total_revenue": 50.0,
        "order_count": 2,
    }
    assert summary["gadget"]["order_count"] == 1


def test_summarize_by_product_empty_input_returns_empty_dict():
    assert summarize_by_product([]) == {}


# --- top_n_products --------------------------------------------------------

def test_top_n_products_ranks_by_revenue_with_alphabetical_tiebreak():
    summary = {
        "zebra": {"total_quantity": 1, "total_revenue": 100.0, "order_count": 1},
        "middle": {"total_quantity": 1, "total_revenue": 250.0, "order_count": 1},
        "apple": {"total_quantity": 1, "total_revenue": 100.0, "order_count": 1},
    }
    result = top_n_products(summary, n=3)
    products = [name for name, _ in result]
    assert products == ["middle", "apple", "zebra"]


def test_top_n_products_n_larger_than_available_returns_all():
    summary = {
        "a": {"total_quantity": 1, "total_revenue": 10.0, "order_count": 1},
        "b": {"total_quantity": 1, "total_revenue": 20.0, "order_count": 1},
    }
    result = top_n_products(summary, n=10)
    assert len(result) == 2


def test_top_n_products_negative_n_raises():
    with pytest.raises(ValueError):
        top_n_products({}, n=-1)


# --- apply_bulk_discount ---------------------------------------------------

def test_apply_bulk_discount_applies_only_at_or_above_threshold():
    orders = [
        {"order_id": "1", "product": "w", "quantity": 5, "unit_price": 10.0},
        {"order_id": "2", "product": "w", "quantity": 4, "unit_price": 10.0},
    ]
    result = apply_bulk_discount(orders, min_quantity=5, discount_rate=0.1)
    assert result[0]["unit_price"] == 9.0   # 5 >= 5 -> 10% off
    assert result[1]["unit_price"] == 10.0  # 4 < 5 -> unchanged


def test_apply_bulk_discount_does_not_mutate_input():
    original = [{"order_id": "1", "product": "w", "quantity": 5, "unit_price": 10.0}]
    apply_bulk_discount(original, min_quantity=1, discount_rate=0.5)
    assert original[0]["unit_price"] == 10.0


# --- loyalty_tier ----------------------------------------------------------

@pytest.mark.parametrize("spend,expected", [
    (0, "none"),         # bottom of the range
    (99.99, "none"),     # just under the first cutoff
    (100, "silver"),     # exactly on the boundary -> the higher tier
    (499.99, "silver"),
    (500, "gold"),       # boundary
    (999.99, "gold"),
    (1000, "platinum"),  # boundary
    (5000, "platinum"),
])
def test_loyalty_tier_boundaries(spend, expected):
    assert loyalty_tier(spend) == expected


def test_loyalty_tier_negative_raises():
    with pytest.raises(ValueError):
        loyalty_tier(-0.01)

