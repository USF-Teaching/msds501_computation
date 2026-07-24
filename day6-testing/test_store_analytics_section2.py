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


# --- Your tests go below here ---------------------------------------------


def test_parse_order_row_cleans_and_rounds():
    row = [
        " 1002 ",
        "  WiDGeT  ",
        "2",
        "9.999",
        " bob@example.com "
    ]

    order = parse_order_row(row)

    assert order["order_id"] == "1002"
    assert order["product"] == "widget"
    assert order["unit_price"] == 10.00
    assert order["customer_email"] == "bob@example.com"


@pytest.mark.parametrize(
    "row",
    [
        ["1001", "Widget", "4", "9.99"],
        ["", "Widget", "4", "9.99", "a@example.com"],
        ["1001", "   ", "4", "9.99", "a@example.com"],
        ["1001", "Widget", "0", "9.99", "a@example.com"],
        ["1001", "Widget", "4.2", "9.99", "a@example.com"],
        ["1001", "Widget", "4", "-1", "a@example.com"],
    ],
)
def test_parse_order_row_invalid_input(row):
    with pytest.raises(ValueError):
        parse_order_row(row)


def test_compute_line_total_rounds_to_two_decimals():
    order = {
        "quantity": 3,
        "unit_price": 2.345
    }

    assert compute_line_total(order) == 7.04


def test_summarize_by_product_groups_orders():
    orders = [
        parse_order_row(
            ["1001", "Widget", "2", "10.00", "a@example.com"]
        ),
        parse_order_row(
            ["1002", "Widget", "3", "5.00", "b@example.com"]
        ),
        parse_order_row(
            ["1003", "Gadget", "1", "7.50", "c@example.com"]
        ),
    ]

    summary = summarize_by_product(orders)

    assert summary["widget"] == {
        "total_quantity": 5,
        "total_revenue": 35.0,
        "order_count": 2,
    }

    assert summary["gadget"] == {
        "total_quantity": 1,
        "total_revenue": 7.5,
        "order_count": 1,
    }

    assert summarize_by_product([]) == {}


def test_top_n_products_ranking_and_ties():
    summary = {
        "banana": {
            "total_quantity": 1,
            "total_revenue": 10.0,
            "order_count": 1,
        },
        "apple": {
            "total_quantity": 1,
            "total_revenue": 10.0,
            "order_count": 1,
        },
        "orange": {
            "total_quantity": 1,
            "total_revenue": 5.0,
            "order_count": 1,
        },
    }

    result = top_n_products(summary, n=5)

    assert [product for product, _ in result] == [
        "apple",
        "banana",
        "orange",
    ]


def test_top_n_products_negative_n_raises():
    with pytest.raises(ValueError, match="negative"):
        top_n_products({}, n=-1)


def test_apply_bulk_discount_and_does_not_mutate_input():
    orders = [
        parse_order_row(
            ["1001", "Widget", "4", "10.00", "a@example.com"]
        ),
        parse_order_row(
            ["1002", "Gadget", "2", "5.00", "b@example.com"]
        ),
    ]

    original = [order.copy() for order in orders]

    result = apply_bulk_discount(
        orders,
        min_quantity=4,
        discount_rate=0.10,
    )

    assert result[0]["unit_price"] == 9.00
    assert result[1]["unit_price"] == 5.00

    # Original input should not be changed
    assert orders == original

    # Function should return new objects
    assert result is not orders
    assert result[0] is not orders[0]

    with pytest.raises(ValueError, match="between 0 and 1"):
        apply_bulk_discount(
            orders,
            min_quantity=1,
            discount_rate=1.1,
        )


def test_loyalty_tier_boundaries_and_negative():
    assert loyalty_tier(99.99) == "none"
    assert loyalty_tier(100) == "silver"
    assert loyalty_tier(500) == "gold"
    assert loyalty_tier(1000) == "platinum"

    with pytest.raises(ValueError, match="negative"):
        loyalty_tier(-0.01)


def test_load_orders_from_csv_keeps_valid_rows_and_reports_errors(
    tmp_path,
):
    csv_file = tmp_path / "orders.csv"

    csv_file.write_text(
        "order_id,product,quantity,unit_price,customer_email\n"
        "1001,Widget,2,10.00,a@example.com\n"
        "1002,Gadget,-1,5.00,b@example.com\n"
        "1003,Gizmo,1,7.50,c@example.com\n"
    )

    orders, errors = load_orders_from_csv(csv_file)

    assert len(orders) == 2
    assert [order["order_id"] for order in orders] == [
        "1001",
        "1003",
    ]

    assert len(errors) == 1
    assert "row 3" in errors[0]


def test_write_top_products_report(tmp_path):
    summary = {
        "widget": {
            "total_quantity": 5,
            "total_revenue": 35.0,
            "order_count": 2,
        },
        "gadget": {
            "total_quantity": 1,
            "total_revenue": 7.5,
            "order_count": 1,
        },
    }

    output_file = tmp_path / "report.txt"

    result = write_top_products_report(
        summary,
        output_file,
        n=1,
    )

    assert result is None

    assert output_file.read_text() == (
        "widget: $35.0 (5 units)\n"
    )