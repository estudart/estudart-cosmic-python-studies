from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass
from typing import List



def allocate(line: OrderLine, batch_list: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batch_list) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration as err:
        raise OuOfStock(f"Out of stock for sku: {line.sku}")

class OuOfStock(Exception):
    pass

@dataclass(frozen=True)
class OrderLine:
    ref: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: datetime):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_qty = qty
        self._allocations = set()

    def __repr__(self):
        return f"<Batch {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __gt__(self, other):
        if not self.eta:
            return False
        if not other.eta:
            return True
        return self.eta > other.eta
    
    def __hash__(self):
        return hash(self.reference)

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)
    
    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)
    
    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_qty - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
