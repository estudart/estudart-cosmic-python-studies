from datetime import datetime, timedelta

import pytest

from model import Batch, OrderLine, allocate, OutofStock



def test_batch_are_iqual():
    batch_1 = Batch("002", "LONG-TABLE", 4, datetime.today())
    batch_2 = Batch("003", "LONG-TABLE", 4, datetime.today())

    is_equal = batch_1 == batch_2

    assert is_equal is False

def test_preferable_batch_to_allocate():
    in_stock_batch = Batch("002", "LONG-TABLE", 20, eta=datetime.today())
    shipment_batch = Batch("002", "LONG-TABLE", 30, eta=datetime.today() + timedelta(days=100))

    line = OrderLine("ref-id", "LONG-TABLE", 5)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 15
    assert shipment_batch.available_quantity == 30

def test_raises_out_of_stocks_exception_if_cannot_allocate():
    batch = Batch("002", "MAJESTIC-TABLE", 6, datetime.today())
    line_1 = OrderLine("ref-id", "MAJESTIC-TABLE", 6)
    allocate(line_1, [batch])

    with pytest.raises(OutofStock, match=f"Out of stock for sku: MAJESTIC-TABLE"):
        line_2 = OrderLine("ref-id", "MAJESTIC-TABLE", 1)
        allocate(line_2, [batch])
