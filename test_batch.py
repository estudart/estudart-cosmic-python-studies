from datetime import datetime

from model import Batch



def test_batch_are_iqual():
    batch_1 = Batch("002", "LONG-TABLE", 4, datetime.today())
    batch_2 = Batch("003", "LONG-TABLE", 4, datetime.today())

    is_equal = batch_1 == batch_2

    assert is_equal is False