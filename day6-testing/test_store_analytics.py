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
@pytest.mark.parametrize("order, expected", [
    ({"quantity": 4, "unit_price": 9.99}, 39.96),
    ({"quantity": 2, "unit_price": 19.99}, 39.98),
    ({"quantity": 1, "unit_price": 19.99}, 19.99),
])
def test_compute_line_total(order, expected):
    """tests compute_line_total function
    """
    assert compute_line_total(order) == expected


@pytest.mark.parametrize("orders, expected", [
    ([{"order_id": 1001, "product": "Widget", "quantity": 4, "unit_price": 9.99, "customer_email": "alice@example.com"}],
     {'Widget': {'total_quantity': 4, 'total_revenue': 39.96, 'order_count': 1}}
    ),
    ([{"order_id": 1001, "product": "Widget", "quantity": 4, "unit_price": 9.99, "customer_email": "alice@example.com"},
      {"order_id": 1002, "product": "Gadget", "quantity": 2, "unit_price": 19.99, "customer_email": "bob@example.com"}],
     {'Widget': {'total_quantity': 4, 'total_revenue': 39.96, 'order_count': 1},
      'Gadget': {'total_quantity': 2, 'total_revenue': 39.98, 'order_count': 1}}
    ),
    ([{"order_id": 1001, "product": "Widget", "quantity": 4, "unit_price": 9.99, "customer_email": "alice@example.com"},
      {"order_id": 1002, "product": "Gadget", "quantity": 2, "unit_price": 19.99, "customer_email": "bob@example.com"},
      {"order_id": 1005, "product": "gadget", "quantity": 1, "unit_price": 19.99, "customer_email": "eve@example.com"}], 
     {'Widget': {'total_quantity': 4, 'total_revenue': 39.96, 'order_count': 1},
      'Gadget': {'total_quantity': 2, 'total_revenue': 39.98, 'order_count': 1},
      'gadget': {'total_quantity': 1, 'total_revenue': 19.99, 'order_count': 1}}
    ),
])
def test_summarize_by_product(orders, expected):
    """_summary_

    Args:
        orders (list of dictionaries): [
            {
                "order_id": 1001,
                "product": "Widget",
                "quantity": 4,
                "unit_price": 9.99,
                "customer_email": "alice@example.com"
            }
        ]
        expected (nested dictionary): {
            'Widget': {
                'total_quantity': 4,
                'total_revenue': 39.96,
                'order_count': 1
            }
        }
    """
    assert summarize_by_product(orders) == expected


def test_top_n_products():
    summary = {
        'Widget': {'total_quantity': 4, 'total_revenue': 39.96, 'order_count': 1},
        'Gadget': {'total_quantity': 2, 'total_revenue': 39.98, 'order_count': 1},
        'gadget': {'total_quantity': 1, 'total_revenue': 19.99, 'order_count': 1}
    }
    expected = [
        ('Gadget', {'total_quantity': 2, 'total_revenue': 39.98, 'order_count': 1}),
        ('Widget', {'total_quantity': 4, 'total_revenue': 39.96, 'order_count': 1}),
        ('gadget', {'total_quantity': 1, 'total_revenue': 19.99, 'order_count': 1})
    ]
    assert top_n_products(summary) == expected


def test_apply_bulk_discount():
    orders = [
        {"order_id": 1001, "product": "Widget", "quantity": 4, "unit_price": 9.99, "customer_email": "alice@example.com"},
        {"order_id": 1002, "product": "Gadget", "quantity": 2, "unit_price": 19.99, "customer_email": "bob@example.com"},
        {"order_id": 1005, "product": "gadget", "quantity": 1, "unit_price": 19.99, "customer_email": "eve@example.com"}
    ]
    min_quantity_1 = 5
    discount_rate_1 = "abc"
    min_quantity_2 = -1
    discount_rate_2 = 0.1
    min_quantity_3 = 0
    discount_rate_3 = 0.1

    with pytest.raises((TypeError, ValueError)):
        assert apply_bulk_discount(orders, min_quantity_1, discount_rate_1)
        assert apply_bulk_discount(orders, min_quantity_2, discount_rate_2)
        assert apply_bulk_discount(orders, min_quantity_3, discount_rate_3) == \
            [{'order_id': 1001, 'product': 'Widget', 'quantity': 4, 'unit_price': 8.99, 'customer_email': 'alice@example.com'},
             {'order_id': 1002, 'product': 'Gadget', 'quantity': 2, 'unit_price': 17.99, 'customer_email': 'bob@example.com'},
             {'order_id': 1005, 'product': 'gadget', 'quantity': 1, 'unit_price': 17.99, 'customer_email': 'eve@example.com'}]


def test_loyalty_tier():
    total_spent_1 = -1
    total_spent_2 = "abc"
    total_spent_3 = 50
    total_spent_4 = 100
    total_spent_5 = 500
    total_spent_6 = 5000

    with pytest.raises((TypeError, ValueError)):
        assert loyalty_tier(total_spent_1)
        assert loyalty_tier(total_spent_2)
        assert loyalty_tier(total_spent_3) == "none"
        assert loyalty_tier(total_spent_4) == "silver"
        assert loyalty_tier(total_spent_5) == "gold"
        assert loyalty_tier(total_spent_6) == "platinum"