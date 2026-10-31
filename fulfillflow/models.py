from dataclasses import dataclass
from enum import StrEnum


class OrderStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Order:
    id: str
    sku: str
    quantity: int
    payment_id: str
    status: OrderStatus = OrderStatus.PENDING
