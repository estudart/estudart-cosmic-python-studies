from datetime import datetime

from model import OrderLine, Batch



def make_batch_and_line(sku: str, batch_qty: int, line_qty: int):
    return (
        Batch("batch-001", sku, batch_qty, eta=datetime.today()),
        OrderLine("ref-id", sku, line_qty)
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line("SMALL-CHAIR", 40, 2)
    batch.allocate(line)
    assert batch.available_quantity == 38

def test_cannot_allocate_if_available_smaller_than_required():
    batch, line = make_batch_and_line("SMALL-CHAIR", 10, 12)
    assert batch.can_allocate(line) is False

def test_can_allocate_if_available_greater_than_required():
    batch, line = make_batch_and_line("SMALL-CHAIR", 20, 12)
    assert batch.can_allocate(line)

def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("SMALL-CHAIR", 2, 2)
    assert batch.can_allocate(line)

def test_cannot_allocate_if_skus_not_the_same():
    batch = Batch("batch-002", "WOODEN-DOOR", 12, datetime.today())
    different_sku_line = OrderLine("0004", "ELEGANT-LAMP", 12)
    assert batch.can_allocate(different_sku_line) is False