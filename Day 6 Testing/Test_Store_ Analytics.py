"""
Tests for store_analytics.py. Run with: pytest test_store_analytics.py -v
"""
 
import pytest
 
from store_analytics import (
    apply_bulk_discount,
    load_orders_from_csv,
    loyalty_tier,
    parse_order_row,
    summarize_by_product,
    top_n_products,
)
 
 
def make_order(product, quantity, unit_price, order_id="X-1"):
    """Build a parsed-order dict without going through parse_order_row."""
    return {
        "order_id": order_id,
        "product": product,
        "quantity": quantity,
        "unit_price": unit_price,
        "customer_email": "buyer@example.com",
    }
 
 
# 1. parse_order_row: the happy path, including all the cleanup it promises
 
def test_parse_order_row_cleans_and_converts_fields():
    row = ["  A-100 ", "  Blue WIDGET ", " 3 ", "4.567", " sam@example.com "]
 
    assert parse_order_row(row) == {
        "order_id": "A-100",        # whitespace stripped
        "product": "blue widget",   # stripped AND lowercased
        "quantity": 3,              # str -> int
        "unit_price": 4.57,         # str -> float, rounded to 2 decimals
        "customer_email": "sam@example.com",
    }
 
 
# 2. parse_order_row: every documented way a row can be rejected
 
@pytest.mark.parametrize("bad_row, reason", [
    (["A-1", "mug", "2", "9.99"],                     "only 4 fields"),
    (["A-1", "mug", "2", "9.99", "a@x.com", "extra"], "6 fields"),
    (["   ", "mug", "2", "9.99", "a@x.com"],          "blank order_id"),
    (["A-1", "   ", "2", "9.99", "a@x.com"],          "blank product"),
    (["A-1", "mug", "two", "9.99", "a@x.com"],        "quantity not a number"),
    (["A-1", "mug", "2.5", "9.99", "a@x.com"],        "quantity not a whole number"),
    (["A-1", "mug", "0", "9.99", "a@x.com"],          "quantity not positive"),
    (["A-1", "mug", "-2", "9.99", "a@x.com"],         "quantity negative"),
    (["A-1", "mug", "2", "free", "a@x.com"],          "price not a number"),
    (["A-1", "mug", "2", "-9.99", "a@x.com"],         "price negative"),
])
def test_parse_order_row_rejects_bad_rows(bad_row, reason):
    with pytest.raises(ValueError):
        parse_order_row(bad_row)


# 3. summarize_by_product: grouping, accumulating, and the empty case
 
def test_summarize_by_product_groups_and_totals():
    orders = [
        make_order("mug", 2, 10.00),   # 20.00
        make_order("pen", 1, 2.50),    #  2.50
        make_order("mug", 3, 10.00),   # 30.00
    ]
 
    summary = summarize_by_product(orders)
 
    assert set(summary) == {"mug", "pen"}
    assert summary["mug"] == {
        "total_quantity": 5,
        "total_revenue": pytest.approx(50.00),
        "order_count": 2,
    }
    assert summary["pen"]["order_count"] == 1
    assert summarize_by_product([]) == {}
 

# 4. top_n_products: ranking, tie-breaking, and the boundaries of n
 
def test_top_n_products_ranks_by_revenue_then_alphabetically():
    summary = {
        "pen": {"total_quantity": 1, "total_revenue": 50.00, "order_count": 1},
        "hat": {"total_quantity": 3, "total_revenue": 75.00, "order_count": 1},
        "mug": {"total_quantity": 5, "total_revenue": 50.00, "order_count": 2},
    }
 
    # hat wins on revenue; mug and pen tie, so they fall back to alphabetical
    assert [name for name, _ in top_n_products(summary, 3)] == ["hat", "mug", "pen"]
    assert [name for name, _ in top_n_products(summary, 2)] == ["hat", "mug"]
 
    assert len(top_n_products(summary, 99)) == 3   # n bigger than the data
    assert top_n_products(summary, 0) == []
    assert top_n_products({}, 3) == []
 
    with pytest.raises(ValueError):
        top_n_products(summary, -1)
 
 
# 5. apply_bulk_discount: discounts the right orders, mutates nothing
 
def test_apply_bulk_discount_returns_new_data_and_leaves_input_alone():
    bulk = make_order("mug", 10, 5.00)
    small = make_order("pen", 2, 3.00)
    orders = [bulk, small]
 
    result = apply_bulk_discount(orders, min_quantity=5, discount_rate=0.2)
 
    assert result[0]["unit_price"] == pytest.approx(4.00)  # 10 units -> 20% off
    assert result[1]["unit_price"] == pytest.approx(3.00)  # 2 units  -> untouched
 
    # the originals must be completely undisturbed
    assert bulk["unit_price"] == pytest.approx(5.00)
    assert small["unit_price"] == pytest.approx(3.00)
    assert result[0] is not bulk
 
    with pytest.raises(ValueError):
        apply_bulk_discount(orders, min_quantity=5, discount_rate=1.5)

# 6. loyalty_tier: the value on each side of every cutoff
 
@pytest.mark.parametrize("spent, expected", [
    (0,       "none"),
    (99.99,   "none"),
    (100,     "silver"),    
    (499.99,  "silver"),
    (500,     "gold"),
    (999.99,  "gold"),
    (1000,    "platinum"),
    (25000,   "platinum"),
])
def test_loyalty_tier_boundaries(spent, expected):
    assert loyalty_tier(spent) == expected
 
 
def test_loyalty_tier_rejects_negative_spend():
    with pytest.raises(ValueError):
        loyalty_tier(-0.01)
 
 
# 7. load_orders_from_csv: bad rows are skipped, not fatal, and numbered the way a spreadsheet would number them
 
def test_load_orders_from_csv_skips_bad_rows_and_reports_row_numbers(tmp_path):
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(
        "order_id,product,quantity,unit_price,customer_email\n"  
        "A1,Mug,2,10.00,a@example.com\n"                         
        "A2,Pen,-1,3.00,b@example.com\n"                         
        "A3,Hat,1,25.00,c@example.com\n"                         
    )
 
    orders, errors = load_orders_from_csv(str(csv_file))
 
    assert [o["product"] for o in orders] == ["mug", "hat"]
    assert len(errors) == 1
    assert errors[0].startswith("row 3:")                    
    assert "positive" in errors[0]
 
