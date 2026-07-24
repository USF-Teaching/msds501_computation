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


"""
TEST PARSE_ORDER_ROW
"""

## Happy Paths

# Valid row returns expected value
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

# Surrounding whitespace is stripped from the fields.
def test_parse_order_row_strips_whitespace():
    row = ["  1001  ", " widget", "4 ", "9.99", "  alice@example.com  "]
    order = parse_order_row(row)
    assert order["order_id"] == "1001"
    assert order["product"] == "widget"
    assert order["quantity"] == 4
    assert order["customer_email"] == "alice@example.com"

# Product is lowercased.
def test_parse_order_row_lowercases_product():
    row = ["1001", "WIDGET", "4", "9.99", "alice@example.com"]
    order = parse_order_row(row)
    assert order["product"] == "widget"

# Unit price is rounded to 2 decimals. Both collapse to 2.0.
@pytest.mark.parametrize("price_str", ["1.999", "2.001"])
def test_parse_order_row_rounds_unit_price(price_str):
    row = ["1001", "Widget", "4", price_str, "alice@example.com"]
    order = parse_order_row(row)
    assert order["unit_price"] == 2.0

## Unhappy Paths

# Raise error if row does not have five str fields (try edges like 3 or 4)
def test_parse_order_row_does_not_have_five_fields():
    row = ["1001", "Widget", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

# Raise an error if order_id is empty
@pytest.mark.parametrize("order_id", ["", "   "])
def test_parse_order_row_empty_order_id_raises(order_id):
    row = [order_id, "widget", "4", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

# Raise an error if product is empty
@pytest.mark.parametrize("product", ["", "   "])
def test_parse_order_row_empty_product_raises(product):
    row = ["1001", product, "4", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

# Raise an error if quantity is not a valid str value
def test_parse_order_row_invalid_str_value_quantity_raises():
    row = ["1001", "Widget", "twenty", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

# Raise an error if quantity is less than or equal to 0 (one with 0 and another
# with a negative number)
@pytest.mark.parametrize("quantity", ["0", "-0.00001", "-1"])
def test_parse_order_row_not_positive_quantity_raises(quantity):
    row = ["1001", "Widget", quantity, "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

# Raise an error if unit_price is not a valid str value
def test_parse_order_row_invalid_str_value_unit_price_raises():
    row = ["1001", "Widget", "4", "nine", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

# Raise an error if unit_price is less than 0
@pytest.mark.parametrize("unit_price", ["-0.00001", "-1"])
def test_parse_order_row_less_than_zero_unit_price_raises(unit_price):
    row = ["1001", "Widget", "4", unit_price, "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

"""
TESTING COMPUTE_LINE_TOTAL
"""
# Check if rounding works
@pytest.mark.parametrize("unit_price, expected", [(0.0001, 0), (0.9999, 2)])
def test_compute_line_total_rounds_to_two_decimal_places(unit_price, expected):
    assert compute_line_total({'quantity': 2, 'unit_price': unit_price}) == expected

"""
TESTING SUMMARIZE_BY_PRODUCT 
"""
def make_order(product, quantity=1, unit_price=10.0):
    """Build an order dict; override only the fields a test cares about."""
    return {
        "product": product,
        "quantity": quantity,
        "unit_price": unit_price
    }

test_orders = [make_order("macbook", 2, 1000), make_order("ipad", 1, 500), 
               make_order("macbook", 1, 1000), make_order("iphone", 1, 250)]

# Return a dictionary with the correct values
def test_summarize_by_product_returns_a_dictionary():
    assert summarize_by_product(test_orders) == {
        "macbook": {"total_quantity": 3, "total_revenue": 3000, "order_count": 2},
        "ipad": {"total_quantity": 1, "total_revenue": 500, "order_count": 1},
        "iphone": {"total_quantity": 1, "total_revenue": 250, "order_count": 1},
    }

# Return an empty dictionary if orders is empty
def test_summarize_by_product_returns_an_empty_dictionary():
    assert summarize_by_product([]) == {}


"""
TESTING TOP_N_PRODUCTS
"""
# Raise error if n is negative
def test_top_n_products_negative_n_raises():
    summary_result = {
            "macbook": {"total_quantity": 3, "total_revenue": 3000, "order_count": 2},
            "ipad": {"total_quantity": 1, "total_revenue": 500, "order_count": 1},
            "iphone": {"total_quantity": 1, "total_revenue": 250, "order_count": 1},
        }
    with pytest.raises(ValueError):
        top_n_products(summary_result, -1)

# Check if tie is broken by alphabetical order
def test_top_n_products_alphabetical_tie_breaker():
    summary_result = {
            "macbook": {"total_quantity": 3, "total_revenue": 3000, "order_count": 2},
            "ipad": {"total_quantity": 1, "total_revenue": 3000, "order_count": 1},
            "iphone": {"total_quantity": 1, "total_revenue": 3000, "order_count": 1},
        }
    assert top_n_products(summary_result, 2) == [
        ("ipad", {"total_quantity": 1, "total_revenue": 3000, "order_count": 1}),
        ("iphone", {"total_quantity": 1, "total_revenue": 3000, "order_count": 1}),
    ]


# N larger than product count returns all of them
def test_top_n_products_n_larger_than_products_returns_all():
    summary_result = {
        "macbook": {"total_quantity": 3, "total_revenue": 3000, "order_count": 2},
        "ipad": {"total_quantity": 1, "total_revenue": 500, "order_count": 1},
    }
    assert len(top_n_products(summary_result, 3)) == 2


# Empty summary returns an empty list
def test_top_n_products_empty_returns_empty_list():
    assert top_n_products({}, 3) == []


"""
TESTING LOYALTY_TIER
"""

# Each cutoff tested from both sides: just below (previous tier) and exactly at
# the boundary (new tier). This is where a > vs >= mistake would show up.
@pytest.mark.parametrize("total_spent, expected", [
    (0, "none"),
    (99.99, "none"),
    (100, "silver"),
    (499.99, "silver"),
    (500, "gold"),
    (999.99, "gold"),
    (1000, "platinum"),
    (5000, "platinum"),
])
def test_loyalty_tier_boundaries(total_spent, expected):
    assert loyalty_tier(total_spent) == expected


# Negative spend raises.
def test_loyalty_tier_negative_raises():
    with pytest.raises(ValueError):
        loyalty_tier(-1)
