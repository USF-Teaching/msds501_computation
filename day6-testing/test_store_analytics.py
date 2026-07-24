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


<<<<<<< HEAD
# --- Your tests go below here ----------------------------------------------
def test_parse_order_row_invalid(): 
    with pytest.raises(ValueError, match="expected 5 fields"):
        parse_order_row(["101", "Coffee Mug", "2", "12.50"])
    with pytest.raises(ValueError, match="quantity must be positive"):
        parse_order_row(["101", "Mug", "0", "12.50", "siva@example.com"])


# ine total calculation with decimal rounding
def test_compute_line_total():
    order = {"quantity": 3, "unit_price": 10.333} #checking for rounding
    assert compute_line_total(order) == 31.00


#grouping the orders by product and calculating total revenue/quantities
def test_summarize_by_product():
    orders = [
        {"product": "mug", "quantity": 2, "unit_price": 69.00},
        {"product": "mug", "quantity": 1, "unit_price": 67.00},
        {"product": "notebook", "quantity": 5, "unit_price": 4.00},
    ]
    summary = summarize_by_product(orders)
    assert summary == {
        "mug": {"total_quantity": 3, "total_revenue": 205.00, "order_count": 2},
        "notebook": {"total_quantity": 5, "total_revenue": 20.00, "order_count": 1},
    }


#ranking top products by revenue with alphabetical tie-breaking
def test_top_n_products_ranking_and_tiebreak():
    summary = {
        "apple": {"total_revenue": 50.0},
        "banana": {"total_revenue": 100.0},
        "cherry": {"total_revenue": 50.0},
    }
    top_2 = top_n_products(summary, n=2)
    # Highest revenue first; tie between apple and cherry broken alphabetically
    expected = [
        ("banana", {"total_revenue": 100.0}),
        ("apple", {"total_revenue": 50.0}),
    ]
    assert top_2 == expected


#bulk discount application without modifying original order dicts (immutability)
def test_apply_bulk_discount_immutability():
    original_orders = [
        {"product": "mug", "quantity": 10, "unit_price": 10.00},
        {"product": "pen", "quantity": 2, "unit_price": 2.00},
    ]
    discounted = apply_bulk_discount(original_orders, min_quantity=5, discount_rate=0.10)
    assert discounted[0]["unit_price"] == 9.00
    assert discounted[1]["unit_price"] == 2.00



#customer loyalty tiers across threshold boundaries
@pytest.mark.parametrize("spend, expected_tier",[
        (0, "none"),
        (100, "silver"),
        (500, "gold"),
        (1000, "platinum"),
    ],
)
def test_loyalty_tier_boundaries(spend, expected_tier):
    assert loyalty_tier(spend) == expected_tier


# SV loading parsing header skipping and error capturing for invalid rows
def test_load_orders_from_csv(tmp_path):
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(
        "order_id,product,quantity,unit_price,customer_email\n"
        "101,Mug,2,10.00,siva@example.com\n"
        "102,Pen,-1,2.00,bad@example.com\n"
    )

    orders, errors = load_orders_from_csv(csv_file)
    assert len(orders) == 1
    assert orders[0]["order_id"] == "101"
    assert len(errors) == 1
    assert "row 3: quantity must be positive" in errors[0]


# Test 9: Verify report file creation and formatted text output
def test_write_top_products_report(tmp_path):
    summary = {
        "coffee mug": {"total_quantity": 5, "total_revenue": 50.0},
        "notebook": {"total_quantity": 2, "total_revenue": 20.0},
    }
    report_file = tmp_path / "report.txt"

    write_top_products_report(summary, report_file, n=1)
    content = report_file.read_text()
    assert content == "coffee mug: $50.0 (5 units)\n"
=======
def test_parse_order_row_missing_order_id():
    row = ["", "Widget", "4", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

def test_parse_order_row_wrong_number_of_fields():
    row = ["Widget", "4", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

def test_compute_line_total():
    order = {
        "order_id": "1001",
        "product": "widget",
        "quantity": 3,
        "unit_price": 9.99,
        "customer_email": "alice@example.com",
    }
    assert compute_line_total(order) == 29.97


def test_loyalty_tier_platinum():
    total_spent = 10001
    assert loyalty_tier(total_spent) == "platinum"

def test_loyalty_tier_silver():
    total_spent = 150
    assert loyalty_tier(total_spent) == "silver"
>>>>>>> upstream/main
