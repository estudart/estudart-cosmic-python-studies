from datetime import datetime

from model import OrderLine, Batch



def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-CHAIR", 40, datetime.today())
    line = OrderLine("0001", "SMALL-CHAIR", 2)
    batch.allocate(line)
    assert batch.available_qty == 38

def test_cannot_allocate_if_available_smaller_than_required():
    batch = Batch("batch-002", "SMALL-TABLE", 10, datetime.today())
    line = OrderLine("0002", "SMALL-TABLE", 12)
    assert batch.can_allocate(line) is False

def test_can_allocate_if_available_greater_than_required():
    batch = Batch("batch-002", "ELEGANT-LAMP", 20, datetime.today())
    line = OrderLine("0004", "ELEGANT-LAMP", 12)
    assert batch.can_allocate(line)

def test_can_allocate_if_available_equal_to_required():
    batch = Batch("batch-002", "ELEGANT-LAMP", 12, datetime.today())
    line = OrderLine("0004", "ELEGANT-LAMP", 12)
    assert batch.can_allocate(line)