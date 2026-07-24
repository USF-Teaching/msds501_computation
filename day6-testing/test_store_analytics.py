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
import os

def test_parse_order_row_wrong():
    row = ["123", "Laptop", "2", "999.99"]  # Only 4 fields

    with pytest.raises(ValueError):
        parse_order_row(row)

def test_parse_order_row_wrong():
    row = [123, 123, 123, 123, 123]  # <====== list of ints instead of string

    with pytest.raises(AttributeError): # <==== using wrong type of input
            parse_order_row(row)

def test_load_orders_from_csv_sample_file():

    csv_path = os.path.join(os.path.dirname(__file__), "sample_orders.csv")

    orders, errors = load_orders_from_csv(csv_path)

    assert len(orders) == 3

    order_ids = [order["order_id"] for order in orders]
    assert order_ids == ["1001", "1002", "1005"]           #<----- only ones that did not throw error

    assert orders[0] == { #sample of correct one
        "order_id": "1001",
        "product": "widget",
        "quantity": 4,
        "unit_price": 9.99,
        "customer_email": "alice@example.com",
    }

    assert orders[1]["product"] == "gadget"
    assert orders[2]["product"] == "gadget"
    assert errors[0].startswith("row 4:")
    assert "quantity must be positive" in errors[0]
    assert "-1" in errors[0]

    assert errors[1].startswith("row 5:")
    assert "quantity must be a whole number" in errors[1]

def test_top_n_products_default_n_returns_top_three():
    summary = {
        "widget":  {"total_quantity": 10, "total_revenue": 500.0, "order_count": 5},
        "gadget":  {"total_quantity": 8,  "total_revenue": 800.0, "order_count": 4},
        "gizmo":   {"total_quantity": 6,  "total_revenue": 300.0, "order_count": 3},
        "doohickey": {"total_quantity": 4, "total_revenue": 200.0, "order_count": 2},
        "thingamajig": {"total_quantity": 2, "total_revenue": 9000000000000000.0, "order_count": 1},
    }

    result = top_n_products(summary)  # <--- n not passed, so length should be 3

    assert len(result) == 3
    assert [product for product, _ in result] == ["thingamajig", "gadget", "widget"]

def test_load_orders_from_csv_large_list_errors(tmp_path):
    csv_path = tmp_path / "large_orders.csv"

    header = "order_id,product,quantity,unit_price,customer_email\n"
    rows = []
    expected_errors = []
    expected_valid_count = 0

    for i in range(1, 201):  # 200 data rows
        row_num = i + 1  # +1 because header is row 1
        if i % 4 == 0:
            # invalid: bad quantity
            rows.append(f"{i},Widget,-1,9.99,user{i}@example.com")
            expected_errors.append((row_num, "quantity must be positive"))
        else:
            rows.append(f"{i},Widget,2,9.99,user{i}@example.com")
            expected_valid_count += 1

    csv_path.write_text(header + "\n".join(rows) + "\n")

    orders, errors = load_orders_from_csv(str(csv_path))

    # nothing dropped or duplicated
    assert len(orders) == expected_valid_count
    assert len(errors) == len(expected_errors)

    # every error has the correct row number, in order
    for error_str, (expected_row, expected_msg) in zip(errors, expected_errors):
        assert error_str.startswith(f"row {expected_row}:")
        assert expected_msg in error_str