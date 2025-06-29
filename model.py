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
        self.qty = qty
        self.eta = eta
        self.available_qty = qty

    def can_allocate(self, line: OrderLine) -> bool:
        return (
            line.sku == self.sku
            and
            line.qty <= self.available_qty
        )

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self.available_qty -= line.qty