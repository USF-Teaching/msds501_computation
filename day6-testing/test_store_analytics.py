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

# Test: Check that a word with space before and after it still parses correctly
# Test: Correct error is raised for quantity with a negative # and string

# --- Your tests go below here ----------------------------------------------

def test_compute_line_total():
    labels = ["order_id", "product", "quantity", "unit_price", "customer_email"]
    row = ["1002","Gadget",2, 19.99,"bob@example.com"]
    order = dict(zip(labels,row))
    assert compute_line_total(order) == 39.98

def test_parse_order_row_quantity_error():
    # Check that 'abc' throws a ValueError
    row = ["1004", "Gizmo", "abc", "3.50", "dave@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)


def test_summarize_by_product_agg():
    # Test that function is aggregating totals correctly
    orders = [{"order_id": "1002",
        "product": "gadget",
        "quantity": 2,
        "unit_price": 19.99,
        "customer_email": "bob@example.com"},
        {"order_id": "1005",
        "product": "gadget",
        "quantity": 1,
        "unit_price": 19.99,
        "customer_email": "eve@example.com"},]
    
    summary = summarize_by_product(orders)
    assert summary['gadget']["total_quantity"] == 3
    assert summary['gadget']["order_count"] == 2


def test_top_n_products_alpha_order():
    # Test that two products with identical summaries will return in alpha order by product
    summary = {
            "gadget": {
                "total_quantity": 2,
                "total_revenue": 19.99,
                "order_count": 1,
            },
            "widget": {
                "total_quantity": 2,
                "total_revenue": 19.99,
                "order_count": 1,
                }
            }
    items = top_n_products(summary, n=3)
    assert items == [('gadget', {'total_quantity': 2, 'total_revenue': 19.99, 'order_count': 1}), 
                     ('widget', {'total_quantity': 2, 'total_revenue': 19.99, 'order_count': 1})]


# Not a unit test...an integration test? Ish
def test_load_orders_from_csv_utf8_accents(tmp_path):
    filepath = tmp_path / "food_orders.csv"
    filepath.write_text(
        "order_id,product,quantity,unit_price,customer_email\n"
        "1006,açai bowl,3,15.00,erin@example.com\n"
        "1007,café latte,2,5.50,domino@example.com\n"
        "1008,jalepeño poppers,1,8.99,joseph@example.com\n",
        encoding='utf-8',
        )

    orders, errors = load_orders_from_csv(str(filepath))

    assert errors == []     # Check that no lines were caught in errors list
    assert len(orders) == 3 # Check that all rows were parsed
    assert orders[0]["product"] == "açai bowl"
    assert orders[1]["product"] == "café latte"
    assert orders[2]["product"] == "jalepeño poppers"

