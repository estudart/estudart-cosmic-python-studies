import pytest
from datetime import datetime, timedelta

import domain.model as model
import service_layer.services as services



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
    

tomorrow = datetime.today() + timedelta(days=1)

def test_allocate_returns_allocation():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("b1", "COMPLICATED-LAMP", 100, None, repo, session)
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, FakeSession())
    assert result == "b1"

def test_can_deallocate():
    line = model.OrderLine("o4", "TINY-DESK", 10)
    batch = model.Batch("ref1", "TINY-DESK", 100, eta=None)
    repo = FakeRepository([batch])

    services.allocate(line, repo, FakeSession())
    result = services.deallocate(line, repo, FakeSession())
    assert result == "ref1"

def test_allocate_errors_for_invalid_sku():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("b1", "AREALSKU", 100, None, repo, session)

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("o1", "NONEXISTENTSKU", 10, repo, FakeSession())

def test_commits():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("b1", "OMINOUS-MIRROR", 30, None, repo, session)
    services.allocate("o1", "OMINOUS-MIRROR", 10, repo, session)
    assert session.committed is True

def test_add_batch():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("o1", "MAJESTIC-SOFA", 10, None, repo, session)
    assert repo.get("o1") is not None
    assert session.committed
