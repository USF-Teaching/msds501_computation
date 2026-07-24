"""
Tests for store_analytics.py.

Run from the day6-testing folder with:
    python3 -m pytest -v
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


# Example supplied in the starter file.
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


@pytest.mark.parametrize(
    "bad_row",
    [
        ["1001", "Widget", "4", "9.99"],
        ["1001", "Widget", "0", "9.99", "alice@example.com"],
        ["1001", "Widget", "four", "9.99", "alice@example.com"],
        ["1001", "Widget", "4", "-1.00", "alice@example.com"],
    ],
)
def test_parse_order_row_rejects_invalid_data(bad_row):
    """Malformed rows, bad quantities, and negative prices must be rejected."""
    with pytest.raises(ValueError):
        parse_order_row(bad_row)


def test_compute_line_total_multiplies_and_rounds():
    order = {"quantity": 3, "unit_price": 2.335}

    assert compute_line_total(order) == 7.0


def test_summarize_by_product_groups_multiple_orders():
    orders = [
        {"product": "widget", "quantity": 2, "unit_price": 10.00},
        {"product": "widget", "quantity": 3, "unit_price": 5.50},
        {"product": "gadget", "quantity": 1, "unit_price": 7.25},
    ]

    summary = summarize_by_product(orders)

    assert summary["widget"] == {
        "total_quantity": 5,
        "total_revenue": 36.50,
        "order_count": 2,
    }
    assert summary["gadget"] == {
        "total_quantity": 1,
        "total_revenue": 7.25,
        "order_count": 1,
    }
    assert summarize_by_product([]) == {}


def test_top_n_products_ranks_revenue_and_breaks_ties_alphabetically():
    summary = {
        "zebra": {"total_revenue": 50.0},
        "apple": {"total_revenue": 50.0},
        "middle": {"total_revenue": 75.0},
    }

    result = top_n_products(summary, n=2)

    assert [product for product, _ in result] == ["middle", "apple"]


def test_top_n_products_rejects_negative_n():
    with pytest.raises(ValueError, match="n cannot be negative"):
        top_n_products({}, n=-1)


def test_apply_bulk_discount_uses_threshold_without_mutating_input():
    orders = [
        {"product": "widget", "quantity": 5, "unit_price": 20.00},
        {"product": "gadget", "quantity": 4, "unit_price": 10.00},
    ]

    discounted = apply_bulk_discount(
        orders, min_quantity=5, discount_rate=0.10
    )

    assert discounted[0]["unit_price"] == 18.00
    assert discounted[1]["unit_price"] == 10.00
    assert orders[0]["unit_price"] == 20.00
    assert discounted is not orders
    assert discounted[0] is not orders[0]


def test_loyalty_tier_handles_boundaries_and_negative_values():
    assert loyalty_tier(99.99) == "none"
    assert loyalty_tier(100) == "silver"
    assert loyalty_tier(500) == "gold"
    assert loyalty_tier(1000) == "platinum"

    with pytest.raises(ValueError):
        loyalty_tier(-0.01)


def test_load_orders_from_csv_keeps_valid_rows_and_reports_errors(tmp_path):
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(
        "order_id,product,quantity,unit_price,customer_email\n"
        "1001,Widget,2,9.99,alice@example.com\n"
        "1002,Gadget,0,5.00,bob@example.com\n"
        "1003,Gizmo,1,3.50,carol@example.com\n"
    )

    orders, errors = load_orders_from_csv(csv_file)

    assert [order["order_id"] for order in orders] == ["1001", "1003"]
    assert errors == ["row 3: quantity must be positive, got 0"]


def test_write_top_products_report_writes_ranked_text(tmp_path):
    summary = {
        "widget": {
            "total_quantity": 3,
            "total_revenue": 30.5,
            "order_count": 2,
        },
        "gadget": {
            "total_quantity": 2,
            "total_revenue": 20.0,
            "order_count": 1,
        },
    }
    report_file = tmp_path / "report.txt"

    result = write_top_products_report(summary, report_file, n=1)

    assert result is None
    assert report_file.read_text() == "widget: $30.5 (3 units)\n"
