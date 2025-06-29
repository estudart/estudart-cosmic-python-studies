from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    ref: str
    sku: str
    qty: int


class Batch:
    def __init__(self, batch_id: str, sku: str, qty: int, eta: datetime):
        self.batch_id = batch_id
        self.sku = sku
        self.eta = eta
        self._purchased_qty = qty
        self._allocations = set()

    def can_allocate(self, line: OrderLine) -> bool:
        return (
            self.sku == line.sku
            and
            self.available_quantity >= line.qty
        )

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
