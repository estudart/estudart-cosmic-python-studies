from datetime import datetime, timedelta

from model import Batch, OrderLine, allocate



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

    assert in_stock_batch.available_quantity == 16
    assert shipment_batch == 30