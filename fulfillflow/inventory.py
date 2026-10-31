from dataclasses import dataclass, field

from .errors import InsufficientStock


@dataclass
class InventoryLedger:
    available: dict[str, int]
    reservations: dict[str, tuple[str, int]] = field(default_factory=dict)

    def reserve(self, order_id: str, sku: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if self.available.get(sku, 0) < quantity:
            raise InsufficientStock(f"not enough stock for {sku}")
        self.available[sku] -= quantity
        self.reservations[order_id] = (sku, quantity)

    def release(self, order_id: str) -> None:
        reservation = self.reservations.pop(order_id, None)
        if reservation is None:
            return
        sku, quantity = reservation
        self.available[sku] = self.available.get(sku, 0) + quantity

    def is_reserved(self, order_id: str) -> bool:
        return order_id in self.reservations
