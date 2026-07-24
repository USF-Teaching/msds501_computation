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

"""
1. parse_order_row(row)
2. compute_line_total(order)
3. summarize_by_product(orders)
4. _sort_key(item)
5. top_n_products(summary, n=3)
6. apply_bulk_discount(orders, min_quantity, discount_rate)
7. loyalty_tier(total_spent)
8. load_orders_from_csv(filepath)
9. write_top_products_report(summary, filepath, n=3)
"""


@pytest.mark.parametrize("i_row, e_order, e_prod, e_quant, e_price, e_email", [
    (["1001", "WIDGET", "4", "9.99", "alice@example.com"], "1001", "widget", 4, 9.99, "alice@example.com"), # prod: caps
    (["1002", " widget  ", "4", "9.99", "alice@example.com"], "1002", "widget", 4, 9.99, "alice@example.com"), # prod: whitespace

    (["1003", "Widget", "4", "0", "alice@example.com"], "1003", "widget", 4, 0.00, "alice@example.com"), # price: zero
    (["1004", "Widget", "4", "9.999", "alice@example.com"], "1004", "widget", 4, 10.00, "alice@example.com") # price: 2dp
])
def test_parse_order_row(i_row, e_order, e_prod, e_quant, e_price, e_email):
    assert parse_order_row(i_row) == {"order_id": e_order,
                                      "product": e_prod,       # stripped of whitespace and lowercased
                                      "quantity": e_quant,      # must be a positive whole number
                                      "unit_price": e_price,  # must be zero or positive, rounded to 2 decimals
                                      "customer_email": e_email
                                      }

@pytest.mark.parametrize("i_row, e_error", [
    (["1001", "Widget", "4", "9.99", "alice@example.com", "foo"], pytest.raises(ValueError)), # len(row) > 5
    (["1001", "Widget", "4", "9.99"], pytest.raises(ValueError)), # len(row) < 5

    (["   ", "Widget", "4", "9.99", "alice@example.com"], pytest.raises(ValueError)), # order empty
    (["1001", " ", "4", "9.99", "alice@example.com"], pytest.raises(ValueError)), # prod empty

    (["1001", "Widget", "4.0", "9.99", "alice@example.com"], pytest.raises(ValueError)), # float quant
    (["1001", "Widget", "foo", "9.99", "alice@example.com"], pytest.raises(ValueError)), # non int quant
    (["1001", "Widget", "-4", "9.99", "alice@example.com"], pytest.raises(ValueError)), # neg quant
    (["1001", "Widget", "0", "9.99", "alice@example.com"], pytest.raises(ValueError)), # quant == 0

    (["1001", "Widget", "4", "foo", "alice@example.com"], pytest.raises(ValueError)), # non num price
    (["1001", "Widget", "4", "-9.99", "alice@example.com"], pytest.raises(ValueError)) # neg price
])
def test_parse_order_row_error(i_row, e_error):
    with e_error:
        parse_order_row(i_row)