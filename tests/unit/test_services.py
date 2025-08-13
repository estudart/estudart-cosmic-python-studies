import pytest
from datetime import datetime, timedelta

from domain import model
from service_layer import services, unit_of_work



class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


class FakeRepository:
    def __init__(self, batches: list[model.Batch]):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)
    
    def list(self):
        return list(self._batches)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])  #(1)
        self.committed = False  #(2)

    def commit(self):
        self.committed = True  #(2)

    def rollback(self):
        pass
    

tomorrow = datetime.today() + timedelta(days=1)

def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "COMPLICATED-LAMP", 100, None, uow)
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "b1"

def test_can_deallocate():
    uow = FakeUnitOfWork()
    line = model.OrderLine("o4", "TINY-DESK", 10)
    batch = model.Batch("ref1", "TINY-DESK", 100, eta=None)
    uow.batches.add(batch)
    services.allocate(line, uow)
    result = services.deallocate(line, uow)
    assert result == "ref1"

def test_allocate_errors_for_invalid_sku():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "AREALSKU", 100, None, uow)

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("o1", "NONEXISTENTSKU", 10, uow)

def test_commits():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "OMINOUS-MIRROR", 30, None, uow)
    services.allocate("o1", "OMINOUS-MIRROR", 10, uow)
    assert uow.committed is True

def test_add_batch():
    uow = FakeUnitOfWork()
    services.add_batch("o1", "MAJESTIC-SOFA", 10, None, uow)
    assert uow.batches.get("o1") is not None
    assert uow.committed
