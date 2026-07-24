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
# parse_order_row -----------------------------------------------------------

def test_parse_order_row_wrong_number_of_fields():
    row = ["1001", "Widget", "4", "9.99"]  # only 4 fields
    with pytest.raises(ValueError):
        parse_order_row(row)


def test_parse_order_row_negative_quantity():
    row = ["1002", "Gadget", "-3", "5.00", "bob@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)


def test_parse_order_row_negative_price():
    row = ["1003", "Gadget", "2", "-1.50", "bob@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)


def test_parse_order_row_strips_whitespace_and_lowercases_product():
    row = ["1004", "  Gizmo  ", "1", "3.00", "carol@example.com"]
    order = parse_order_row(row)
    assert order["product"] == "gizmo"


# compute_line_total ---------------------------------------------------------

def test_compute_line_total_basic():
    order = {"quantity": 3, "unit_price": 2.50}
    assert compute_line_total(order) == 7.50


# summarize_by_product --------------------------------------------------------

def test_summarize_by_product_empty_list():
    assert summarize_by_product([]) == {}


def test_summarize_by_product_groups_same_product():
    orders = [
        {"product": "widget", "quantity": 2, "unit_price": 10.0},
        {"product": "widget", "quantity": 1, "unit_price": 10.0},
    ]
    summary = summarize_by_product(orders)
    assert summary["widget"]["total_quantity"] == 3
    assert summary["widget"]["total_revenue"] == 30.0
    assert summary["widget"]["order_count"] == 2


# top_n_products ---------------------------------------------------------------

def test_top_n_products_ranks_by_revenue():
    summary = {
        "widget": {"total_quantity": 5, "total_revenue": 50.0, "order_count": 1},
        "gadget": {"total_quantity": 5, "total_revenue": 100.0, "order_count": 1},
    }
    top = top_n_products(summary, n=1)
    assert top == [("gadget", summary["gadget"])]


def test_top_n_products_negative_n_raises():
    with pytest.raises(ValueError):
        top_n_products({}, n=-1)


# apply_bulk_discount ------------------------------------------------------------

def test_apply_bulk_discount_applies_to_qualifying_order():
    orders = [{"product": "widget", "quantity": 10, "unit_price": 10.0}]
    discounted = apply_bulk_discount(orders, min_quantity=5, discount_rate=0.1)
    assert discounted[0]["unit_price"] == 9.0


def test_apply_bulk_discount_does_not_modify_original_list():
    orders = [{"product": "widget", "quantity": 10, "unit_price": 10.0}]
    apply_bulk_discount(orders, min_quantity=5, discount_rate=0.1)
    assert orders[0]["unit_price"] == 10.0


def test_apply_bulk_discount_invalid_rate_raises():
    orders = [{"product": "widget", "quantity": 10, "unit_price": 10.0}]
    with pytest.raises(ValueError):
        apply_bulk_discount(orders, min_quantity=5, discount_rate=1.5)


# loyalty_tier ---------------------------------------------------------------------

def test_loyalty_tier_boundaries():
    assert loyalty_tier(0) == "none"
    assert loyalty_tier(100) == "silver"
    assert loyalty_tier(500) == "gold"
    assert loyalty_tier(1000) == "platinum"


def test_loyalty_tier_negative_raises():
    with pytest.raises(ValueError):
        loyalty_tier(-50)


# load_orders_from_csv ---------------------------------------------------------------

def test_load_orders_from_csv_skips_bad_rows(tmp_path):
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(
        "order_id,product,quantity,unit_price,customer_email\n"
        "1001,Widget,4,9.99,alice@example.com\n"
        "1002,Gadget,-1,5.00,bob@example.com\n"
    )
    orders, errors = load_orders_from_csv(csv_file)
    assert len(orders) == 1
    assert len(errors) == 1
    assert "row 3" in errors[0]


# write_top_products_report -----------------------------------------------------------

def test_write_top_products_report_creates_file(tmp_path):
    summary = {
        "widget": {"total_quantity": 5, "total_revenue": 50.0, "order_count": 1},
    }
    out_file = tmp_path / "report.txt"
    write_top_products_report(summary, out_file, n=1)
    contents = out_file.read_text()
    assert "widget: $50.0 (5 units)" in contents