import pytest

import model
import services



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


def test_returns_allocation():
    line = model.OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = model.Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = FakeRepository([batch])  #(1)

    result = services.allocate(line, repo, FakeSession())  #(2) (3)
    assert result == "b1"

def test_can_deallocate():
    line = model.OrderLine("o4", "TINY-DESK", 10)
    batch = model.Batch("ref1", "TINY-DESK", 100, eta=None)
    repo = FakeRepository([batch])

    services.allocate(line, repo, FakeSession())
    result = services.deallocate(line, repo, FakeSession())
    assert result == "ref1"

def test_error_for_invalid_sku():
    line = model.OrderLine("o1", "NONEXISTENTSKU", 10)
    batch = model.Batch("b1", "AREALSKU", 100, eta=None)
    repo = FakeRepository([batch])  #(1)

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate(line, repo, FakeSession())  #(2) (3)

def test_commits():
    line = model.OrderLine("o1", "OMINOUS-MIRROR", 10)
    batch = model.Batch("b1", "OMINOUS-MIRROR", 30, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()

    services.allocate(line, repo, session)
    assert session.committed is True
