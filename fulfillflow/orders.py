from .audit import AuditLog
from .errors import InvalidOrderState
from .inventory import InventoryLedger
from .models import Order, OrderStatus
from .payments import PaymentGateway


class OrderService:
    def __init__(
        self,
        inventory: InventoryLedger,
        payments: PaymentGateway,
        audit: AuditLog,
    ) -> None:
        self.inventory = inventory
        self.payments = payments
        self.audit = audit

    def confirm_order(self, order: Order) -> None:
        if order.status is not OrderStatus.PENDING:
            raise InvalidOrderState("only pending orders can be confirmed")
        self.inventory.reserve(order.id, order.sku, order.quantity)
        order.status = OrderStatus.CONFIRMED
        self.audit.record("order_confirmed", order.id)

    def cancel_order(self, order: Order) -> None:
        if order.status is not OrderStatus.CONFIRMED:
            raise InvalidOrderState("only confirmed orders can be cancelled")

        # Intentional bug: releasing inventory before the external refund means
        # a rejected refund leaves a confirmed order without its reservation.
        self.inventory.release(order.id)
        self.payments.refund(order.payment_id)

        order.status = OrderStatus.CANCELLED
        self.audit.record("order_cancelled", order.id)
