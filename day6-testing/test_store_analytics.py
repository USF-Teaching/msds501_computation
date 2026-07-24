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


def test_compute_line_total_rounds_to_two_decimals():
    order = {"quantity": 3, "unit_price": 5.555}
    # 3 * 5.555 is 16.665 in exact math, but in floating point it is stored
    # as 16.6649999..., so round(..., 2) rounds DOWN to 16.66, not 16.67.
    assert compute_line_total(order) == 16.66


def test_summarize_by_product_groups_orders_by_product():
    orders = [
        parse_order_row(["1", "Widget", "2", "10.00", "a@example.com"]),
        parse_order_row(["2", "widget", "1", "5.00", "b@example.com"]),
        parse_order_row(["3", "Gadget", "1", "20.00", "c@example.com"]),
    ]

    summary = summarize_by_product(orders)

    assert summary["widget"]["total_quantity"] == 3
    assert summary["widget"]["order_count"] == 2
    assert summary["widget"]["total_revenue"] == 25.0
    assert summary["gadget"]["total_revenue"] == 20.0


def test_top_n_products_breaks_ties_alphabetically():
    summary = {
        "zeta": {"total_quantity": 1, "total_revenue": 50.0, "order_count": 1},
        "alpha": {"total_quantity": 1, "total_revenue": 50.0, "order_count": 1},
    }

    ranked = top_n_products(summary, 2)

    assert [product for product, _ in ranked] == ["alpha", "zeta"]


def test_apply_bulk_discount_returns_new_orders_without_mutating_input():
    orders = [
        parse_order_row(["1", "Widget", "2", "10.00", "a@example.com"]),
        parse_order_row(["2", "Gadget", "1", "15.00", "b@example.com"]),
    ]

    discounted = apply_bulk_discount(orders, 2, 0.1)

    assert discounted is not orders
    assert discounted[0]["unit_price"] == 9.0
    assert discounted[1]["unit_price"] == 15.0
    assert orders[0]["unit_price"] == 10.0
    assert orders[1]["unit_price"] == 15.0


def test_load_orders_from_csv_parses_valid_rows_and_collects_errors():
    orders, errors = load_orders_from_csv("sample_orders.csv")

    assert [order["order_id"] for order in orders] == ["1001", "1002", "1005"]
    # Row numbers count the header as row 1, so the first data row is row 2.
    # The bad rows (1003, 1004) are therefore rows 4 and 5, as a spreadsheet
    # app would show them.
    assert errors == [
        "row 4: quantity must be positive, got -1",
        "row 5: quantity must be a whole number, got 'abc'",
    ]


def test_parse_order_row_rejects_wrong_field_count():
    with pytest.raises(ValueError, match="expected 5 fields"):
        parse_order_row(["1", "Widget", "2", "9.99"])


def test_parse_order_row_rejects_empty_product():
    with pytest.raises(ValueError, match="product cannot be empty"):
        parse_order_row(["1", "   ", "2", "9.99", "a@example.com"])


def test_top_n_products_rejects_negative_n():
    with pytest.raises(ValueError, match="n cannot be negative"):
        top_n_products({"widget": {"total_quantity": 1, "total_revenue": 10.0, "order_count": 1}}, -1)


def test_loyalty_tier_returns_expected_values():
    assert loyalty_tier(0) == "none"
    assert loyalty_tier(99.99) == "none"
    assert loyalty_tier(100) == "silver"
    assert loyalty_tier(499.99) == "silver"
    assert loyalty_tier(500) == "gold"
    assert loyalty_tier(999.99) == "gold"
    assert loyalty_tier(1000) == "platinum"


def test_write_top_products_report_writes_expected_lines(tmp_path):
    summary = {
        "widget": {"total_quantity": 3, "total_revenue": 25.0, "order_count": 2},
        "gadget": {"total_quantity": 1, "total_revenue": 20.0, "order_count": 1},
    }
    output_path = tmp_path / "report.txt"

    write_top_products_report(summary, str(output_path), n=1)

    assert output_path.read_text() == "widget: $25.0 (3 units)\n"


def test_parse_order_row_rejects_negative_unit_price():
    with pytest.raises(ValueError, match="unit_price cannot be negative"):
        parse_order_row(["1", "Widget", "2", "-1.00", "a@example.com"])


def test_parse_order_row_rejects_empty_order_id():
    with pytest.raises(ValueError, match="order_id cannot be empty"):
        parse_order_row(["   ", "Widget", "2", "9.99", "a@example.com"])


def test_apply_bulk_discount_rejects_out_of_range_discount_rate():
    with pytest.raises(ValueError, match="discount_rate must be between 0 and 1"):
        apply_bulk_discount([], 2, 1.5)


def test_summarize_by_product_returns_empty_dict_for_empty_input():
    assert summarize_by_product([]) == {}


def test_top_n_products_defaults_to_three_and_returns_all_when_needed():
    summary = {
        "beta": {"total_quantity": 1, "total_revenue": 30.0, "order_count": 1},
        "alpha": {"total_quantity": 1, "total_revenue": 50.0, "order_count": 1},
        "gamma": {"total_quantity": 1, "total_revenue": 40.0, "order_count": 1},
    }

    ranked = top_n_products(summary)

    assert [product for product, _ in ranked] == ["alpha", "gamma", "beta"]
