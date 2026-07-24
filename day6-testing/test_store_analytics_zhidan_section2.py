"""
Tests for store_analytics.py

These tests cover different behaviors from the function docstrings:
valid input, invalid input, boundaries, sorting, immutability, CSV loading,
and report writing.
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


# Example test from the starter file
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


def test_parse_order_row_cleans_and_rounds_values():
    row = [" 1002 ", "  GaDgEt ", "2", "19.999", " bob@example.com "]

    order = parse_order_row(row)

    assert order["order_id"] == "1002"
    assert order["product"] == "gadget"
    assert order["unit_price"] == 20.00
    assert order["customer_email"] == "bob@example.com"


@pytest.mark.parametrize(
    "row",
    [
        ["1001", "Widget", "4", "9.99"],  # wrong number of fields
        ["", "Widget", "4", "9.99", "a@example.com"],  # empty order_id
        ["1001", "Widget", "0", "9.99", "a@example.com"],  # non-positive quantity
        ["1001", "Widget", "abc", "9.99", "a@example.com"],  # invalid quantity
        ["1001", "Widget", "4", "-1.00", "a@example.com"],  # negative price
    ],
)
def test_parse_order_row_rejects_bad_input(row):
    with pytest.raises(ValueError):
        parse_order_row(row)


def test_compute_line_total_rounds_to_two_decimals():
    order = {
        "order_id": "1001",
        "product": "widget",
        "quantity": 3,
        "unit_price": 3.333,
        "customer_email": "a@example.com",
    }

    assert compute_line_total(order) == 10.00


def test_summarize_by_product_combines_matching_products():
    orders = [
        parse_order_row(["1001", "Widget", "2", "10.00", "a@example.com"]),
        parse_order_row(["1002", "widget", "3", "5.50", "b@example.com"]),
        parse_order_row(["1003", "Gadget", "1", "20.00", "c@example.com"]),
    ]

    summary = summarize_by_product(orders)

    assert summary["widget"] == {
        "total_quantity": 5,
        "total_revenue": 36.50,
        "order_count": 2,
    }
    assert summary["gadget"] == {
        "total_quantity": 1,
        "total_revenue": 20.00,
        "order_count": 1,
    }
    assert summarize_by_product([]) == {}


def test_top_n_products_ranks_revenue_and_breaks_ties_alphabetically():
    summary = {
        "orange": {"total_quantity": 1, "total_revenue": 10.0, "order_count": 1},
        "apple": {"total_quantity": 1, "total_revenue": 10.0, "order_count": 1},
        "banana": {"total_quantity": 2, "total_revenue": 20.0, "order_count": 1},
    }

    result = top_n_products(summary, n=3)

    assert [product for product, _ in result] == ["banana", "apple", "orange"]

    with pytest.raises(ValueError):
        top_n_products(summary, n=-1)


def test_apply_bulk_discount_returns_new_data_without_changing_original():
    orders = [
        parse_order_row(["1001", "Widget", "4", "10.00", "a@example.com"]),
        parse_order_row(["1002", "Gadget", "2", "20.00", "b@example.com"]),
    ]
    original_orders = [order.copy() for order in orders]

    discounted = apply_bulk_discount(
        orders,
        min_quantity=4,
        discount_rate=0.10,
    )

    assert discounted[0]["unit_price"] == 9.00
    assert discounted[1]["unit_price"] == 20.00
    assert orders == original_orders
    assert discounted is not orders
    assert discounted[0] is not orders[0]


@pytest.mark.parametrize(
    "total_spent, expected",
    [
        (99.99, "none"),
        (100, "silver"),
        (500, "gold"),
        (1000, "platinum"),
    ],
)
def test_loyalty_tier_boundary_values(total_spent, expected):
    assert loyalty_tier(total_spent) == expected


def test_load_orders_from_sample_csv():
    orders, errors = load_orders_from_csv("sample_orders.csv")

    assert len(orders) == 3
    assert orders[0]["product"] == "widget"
    assert orders[1]["product"] == "gadget"
    assert orders[2]["order_id"] == "1005"

    assert len(errors) == 2
    assert "row 4" in errors[0]
    assert "row 5" in errors[1]


def test_write_top_products_report(tmp_path):
    summary = {
        "widget": {"total_quantity": 5, "total_revenue": 50.0, "order_count": 2},
        "gadget": {"total_quantity": 2, "total_revenue": 40.0, "order_count": 1},
    }
    output_file = tmp_path / "report.txt"

    result = write_top_products_report(summary, output_file, n=2)

    assert result is None
    assert output_file.read_text().splitlines() == [
        "widget: $50.0 (5 units)",
        "gadget: $40.0 (2 units)",
    ]