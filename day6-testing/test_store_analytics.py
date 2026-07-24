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

# parse_order_row

def test_parse_order_row():
    row = ["  1001  ", "  Widget  ", " 4 ", " 9.999 ", " alice@example.com "]
    order = parse_order_row(row)
    assert order["order_id"] == "1001"
    assert order["product"] == "widget"
    assert order["customer_email"] == "alice@example.com"
    assert order["unit_price"] == 10.0

def test_parse_order_row_wrong_number_of_fields():
    with pytest.raises(ValueError):
        parse_order_row(["1001", "Widget", "4", "9.99"]) # only 4 fields


def test_parse_order_row_empty_order_id():
    with pytest.raises(ValueError):
        parse_order_row(["", "Widget", "4", "9.99", "alice@example.com"])


def test_parse_order_row_empty_product():
    with pytest.raises(ValueError):
        parse_order_row(["1001", "", "4", "9.99", "alice@example.com"])


def test_parse_order_row_non_int_quantity():
    with pytest.raises(ValueError):
        parse_order_row(["1004", "Gizmo", "abc", "3.50", "dave@example.com"])


def test_parse_order_row_zero_quantity():
    with pytest.raises(ValueError):
        parse_order_row(["1001", "Widget", "0", "9.99", "alice@example.com"])


def test_parse_order_row_neg_quantity():
    with pytest.raises(ValueError):
        parse_order_row(["1003", "Widget", "-1", "5.00", "carol@example.com"])


def test_parse_order_row_non_numeric_unit_price():
    with pytest.raises(ValueError):
        parse_order_row(["1001", "Widget", "4", "cheap", "alice@example.com"])


def test_parse_order_row_neg_unit_price():
    with pytest.raises(ValueError):
        parse_order_row(["1001", "Widget", "4", "-9.99", "alice@example.com"])


def test_parse_order_row_zero_unit_price_allowed():
    order = parse_order_row(["1006", "Freebie", "1", "0", "frank@example.com"])
    assert order["unit_price"] == 0.0


# compute_line_total

def test_compute_line_total():
    order = {"quantity": 3, "unit_price": 2.5}
    assert compute_line_total(order) == 7.5


# summarize_by_product

def test_summarize_by_product_empty_list():
    assert summarize_by_product([]) == {}


def test_summarize_by_product_aggregates_same_product():
    orders = [
        {"order_id": "1", "product": "widget", "quantity": 2, "unit_price": 10.0, "customer_email": "a@x.com"},
        {"order_id": "2", "product": "widget", "quantity": 3, "unit_price": 10.0, "customer_email": "b@x.com"},
    ]
    summary = summarize_by_product(orders)
    assert summary == {"widget": {"total_quantity": 5, "total_revenue": 50.0, "order_count": 2}}


def test_summarize_by_product_separates_diff_products():
    orders = [
        {"order_id": "1", "product": "widget", "quantity": 2, "unit_price": 10.0, "customer_email": "a@x.com"},
        {"order_id": "2", "product": "gadget", "quantity": 1, "unit_price": 20.0, "customer_email": "b@x.com"},
    ]
    summary = summarize_by_product(orders)
    assert set(summary.keys()) == {"widget", "gadget"}
    assert summary["gadget"]["order_count"] == 1


# top_n_products

def test_top_n_products_ranks_by_revenue_desc():
    summary = {
        "widget": {"total_quantity": 1, "total_revenue": 50.0, "order_count": 1},
        "gadget": {"total_quantity": 1, "total_revenue": 100.0, "order_count": 1},
        "gizmo": {"total_quantity": 1, "total_revenue": 10.0, "order_count": 1},
    }
    result = top_n_products(summary, n=2)
    assert result == [("gadget", summary["gadget"]), ("widget", summary["widget"])]


def test_top_n_products_breaks_ties_alphabetically():
    summary = {
        "alpha": {"total_quantity": 1, "total_revenue": 50.0, "order_count": 1},
        "zeta": {"total_quantity": 1, "total_revenue": 50.0, "order_count": 1},
    }
    result = top_n_products(summary, n=2)
    assert [product for product, _ in result] == ["alpha", "zeta"]


def test_top_n_products_n_larger_than_available_returns():
    summary = {
        "widget": {"total_quantity": 1, "total_revenue": 50.0, "order_count": 1},
    }
    result = top_n_products(summary, n=5)
    assert len(result) == 1


def test_top_n_products_empty():
    assert top_n_products({}, n=3) == []


def test_top_n_products_neg_n_raises():
    with pytest.raises(ValueError):
        top_n_products({"widget": {"total_quantity": 1, "total_revenue": 50.0, "order_count": 1}}, n=-1)


# apply_bulk_discount

def test_apply_bulk_discount_below_threshold_unchanged():
    orders = [{"order_id": "1", "product": "widget", "quantity": 2, "unit_price": 10.0, "customer_email": "a@x.com"}]
    result = apply_bulk_discount(orders, min_quantity=5, discount_rate=0.1)
    assert result[0]["unit_price"] == 10.0


def test_apply_bulk_discount_at_threshold_discounted():
    orders = [{"order_id": "1", "product": "widget", "quantity": 5, "unit_price": 10.0, "customer_email": "a@x.com"}]
    result = apply_bulk_discount(orders, min_quantity=5, discount_rate=0.1)
    assert result[0]["unit_price"] == 9.0


def test_apply_bulk_discount_invalid_rate_raises():
    orders = [{"order_id": "1", "product": "widget", "quantity": 5, "unit_price": 10.0, "customer_email": "a@x.com"}]
    with pytest.raises(ValueError):
        apply_bulk_discount(orders, min_quantity=5, discount_rate=1.5)


# loyalty_tier

@pytest.mark.parametrize("total_spent, expected_tier", [
    (0, "none"),
    (99.99, "none"),
    (100, "silver"),
    (499.99, "silver"),
    (500, "gold"),
    (999.99, "gold"),
    (1000, "platinum"),
])
def test_loyalty_tier_boundaries(total_spent, expected_tier):
    assert loyalty_tier(total_spent) == expected_tier


def test_loyalty_tier_negative_raises():
    with pytest.raises(ValueError):
        loyalty_tier(-1)